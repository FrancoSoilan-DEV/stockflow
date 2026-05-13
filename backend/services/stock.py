# services/stock.py
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.models import Branch, Stock
from schemas.stock import StockByProductResponse, StockUpdate


async def get_stock_by_branch(db: AsyncSession, branch_id: uuid.UUID) -> list[Stock]:
    """Devuelve todo el stock de una sucursal con los datos del producto."""
    result = await db.execute(
        select(Stock)
        .where(Stock.branch_id == branch_id)
        .options(selectinload(Stock.product))
    )
    return list(result.scalars().all())


async def get_stock_by_product_all_branches(
    db: AsyncSession, product_id: uuid.UUID
) -> list[StockByProductResponse]:
    """
    Devuelve el stock de un producto en todas las sucursales.
    Útil para saber dónde hay disponibilidad cuando una sucursal no tiene.
    """
    result = await db.execute(
        select(Stock, Branch)
        .join(Branch, Stock.branch_id == Branch.id)
        .where(Stock.product_id == product_id)
    )
    rows = result.all()

    return [
        StockByProductResponse(
            branch_id=stock.branch_id,
            branch_name=branch.name,
            quantity=stock.quantity,
        )
        for stock, branch in rows
    ]


async def get_stock_entry(
    db: AsyncSession, branch_id: uuid.UUID, product_id: uuid.UUID
) -> Stock | None:
    """Busca un registro de stock específico por sucursal y producto."""
    result = await db.execute(
        select(Stock)
        .where(Stock.branch_id == branch_id, Stock.product_id == product_id)
        .options(selectinload(Stock.product))
    )
    return result.scalar_one_or_none()


async def update_stock(
    db: AsyncSession,
    branch_id: uuid.UUID,
    product_id: uuid.UUID,
    data: StockUpdate,
) -> Stock | None:
    """
    Actualiza la cantidad de stock de un producto en una sucursal.
    Si no existe el registro devuelve None.
    """
    stock = await get_stock_entry(db, branch_id, product_id)
    if not stock:
        return None

    stock.quantity = data.quantity
    await db.commit()
    await db.refresh(stock)
    return stock