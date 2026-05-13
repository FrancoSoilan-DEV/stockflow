# routers/stock.py
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from core.ws_manager import manager
from services.branch import get_branch_by_id
from core.dependencies import get_current_user
from db.session import get_db
from models.models import User
from schemas.stock import StockByProductResponse, StockResponse, StockUpdate
from services.stock import (
    get_stock_by_branch,
    get_stock_by_product_all_branches,
    get_stock_entry,
    update_stock,
)

router = APIRouter(prefix="/stock", tags=["stock"])


@router.get("/branch/{branch_id}", response_model=list[StockResponse])
async def list_stock_by_branch(
    branch_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Devuelve todo el stock de una sucursal.
    Acceso: admin y staff.
    """
    return await get_stock_by_branch(db, branch_id)


@router.get("/product/{product_id}", response_model=list[StockByProductResponse])
async def list_stock_by_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Devuelve el stock de un producto en todas las sucursales.
    Útil para saber dónde hay disponibilidad.
    Acceso: admin y staff.
    """
    return await get_stock_by_product_all_branches(db, product_id)


# actualizar el endpoint
@router.patch("/branch/{branch_id}/product/{product_id}", response_model=StockResponse)
async def update_stock_endpoint(
    branch_id: uuid.UUID,
    product_id: uuid.UUID,
    data: StockUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    stock = await update_stock(db, branch_id, product_id, data)
    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontró stock para ese producto en esa sucursal",
        )

    # notificar a todos los conectados en tiempo real
    branch = await get_branch_by_id(db, branch_id)
    await manager.broadcast_stock_update(
        product_id=str(stock.product_id),
        product_name=stock.product.name,
        branch_id=str(branch_id),
        branch_name=branch.name,
        quantity=stock.quantity,
    )

    return stock