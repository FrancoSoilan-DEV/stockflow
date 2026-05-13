# routers/sales.py
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user
from db.session import get_db
from models.models import User
from schemas.sale import SaleCreate, SaleResponse
from services.sale import create_sale, get_sale_by_id, get_sales_by_branch

router = APIRouter(prefix="/sales", tags=["sales"])


@router.get("/branch/{branch_id}", response_model=list[SaleResponse])
async def list_sales_by_branch(
    branch_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Devuelve todas las ventas de una sucursal.
    Acceso: admin y staff.
    """
    return await get_sales_by_branch(db, branch_id)


@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(
    sale_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Devuelve una venta por ID con todos sus items.
    Acceso: admin y staff.
    """
    sale = await get_sale_by_id(db, sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venta no encontrada",
        )
    return sale


@router.post("/branch/{branch_id}", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
async def create_sale_endpoint(
    branch_id: uuid.UUID,
    data: SaleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Registra una venta nueva en una sucursal.
    - Valida stock antes de confirmar
    - Descuenta stock automáticamente
    - Calcula el total automáticamente
    Acceso: admin y staff.
    """
    result = await create_sale(db, data, branch_id, current_user.id)

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"],
        )

    return result