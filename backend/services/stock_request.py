# services/stock_request.py
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.models import RequestStatus, Stock, StockRequest, UserRole, User
from schemas.stock_request import StockRequestCreate, StockRequestStatusUpdate


async def get_all_requests(db: AsyncSession) -> list[StockRequest]:
    """Devuelve todos los pedidos. Solo para admin."""
    result = await db.execute(
        select(StockRequest)
        .options(selectinload(StockRequest.product))
        .order_by(StockRequest.created_at.desc())
    )
    return list(result.scalars().all())


async def get_requests_by_branch(
    db: AsyncSession, branch_id: uuid.UUID
) -> list[StockRequest]:
    """Devuelve los pedidos de una sucursal — enviados y recibidos."""
    result = await db.execute(
        select(StockRequest)
        .where(
            (StockRequest.from_branch_id == branch_id) |
            (StockRequest.to_branch_id == branch_id)
        )
        .options(selectinload(StockRequest.product))
        .order_by(StockRequest.created_at.desc())
    )
    return list(result.scalars().all())


async def get_request_by_id(
    db: AsyncSession, request_id: uuid.UUID
) -> StockRequest | None:
    result = await db.execute(
        select(StockRequest)
        .where(StockRequest.id == request_id)
        .options(selectinload(StockRequest.product))
    )
    return result.scalar_one_or_none()


async def create_stock_request(
    db: AsyncSession,
    data: StockRequestCreate,
    from_branch_id: uuid.UUID,
) -> StockRequest | dict:
    """
    Crea un pedido de stock.
    Valida que la sucursal destino tenga suficiente stock disponible.
    """
    stock_result = await db.execute(
        select(Stock).where(
            Stock.branch_id == data.to_branch_id,
            Stock.product_id == data.product_id,
        )
    )
    stock = stock_result.scalar_one_or_none()

    if not stock:
        return {"error": "El producto no existe en la sucursal destino"}

    if stock.quantity < data.quantity:
        return {
            "error": f"Stock insuficiente en la sucursal destino. "
                     f"Disponible: {stock.quantity}, solicitado: {data.quantity}"
        }

    request = StockRequest(
        from_branch_id=from_branch_id,
        to_branch_id=data.to_branch_id,
        product_id=data.product_id,
        quantity=data.quantity,
        status=RequestStatus.pending,
    )
    db.add(request)
    await db.commit()
    await db.refresh(request)

    result = await db.execute(
        select(StockRequest)
        .where(StockRequest.id == request.id)
        .options(selectinload(StockRequest.product))
    )
    return result.scalar_one()


async def update_request_status(
    db: AsyncSession,
    request_id: uuid.UUID,
    data: StockRequestStatusUpdate,
) -> StockRequest | dict | None:
    """
    Admin aprueba o rechaza un pedido.
    Si aprueba transfiere el stock automáticamente.
    Solo se pueden actualizar pedidos en estado pending.
    """
    request = await get_request_by_id(db, request_id)
    if not request:
        return None

    if request.status != RequestStatus.pending:
        return {"error": "Solo se pueden actualizar pedidos en estado pending"}

    if data.status == RequestStatus.approved:
        # verificar stock disponible en sucursal origen
        stock_from_result = await db.execute(
            select(Stock).where(
                Stock.branch_id == request.to_branch_id,
                Stock.product_id == request.product_id,
            )
        )
        stock_from = stock_from_result.scalar_one_or_none()

        if not stock_from or stock_from.quantity < request.quantity:
            return {"error": "Ya no hay stock suficiente para aprobar este pedido"}

        # verificar si existe el stock en la sucursal destino
        stock_to_result = await db.execute(
            select(Stock).where(
                Stock.branch_id == request.from_branch_id,
                Stock.product_id == request.product_id,
            )
        )
        stock_to = stock_to_result.scalar_one_or_none()

        if stock_to:
            stock_to.quantity += request.quantity
        else:
            # si no existe el registro de stock lo creamos
            new_stock = Stock(
                branch_id=request.from_branch_id,
                product_id=request.product_id,
                quantity=request.quantity,
            )
            db.add(new_stock)

        # descontar de la sucursal origen
        stock_from.quantity -= request.quantity

    request.status = data.status
    await db.commit()

    result = await db.execute(
        select(StockRequest)
        .where(StockRequest.id == request_id)
        .options(selectinload(StockRequest.product))
    )
    return result.scalar_one()