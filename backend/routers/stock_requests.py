# routers/stock_requests.py
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user, require_admin
from db.session import get_db
from models.models import User
from schemas.stock_request import StockRequestCreate, StockRequestResponse, StockRequestStatusUpdate
from services.stock_request import (
    create_stock_request,
    get_all_requests,
    get_request_by_id,
    get_requests_by_branch,
    update_request_status,
)

router = APIRouter(prefix="/stock-requests", tags=["stock-requests"])


@router.get("/", response_model=list[StockRequestResponse])
async def list_all_requests(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Devuelve todos los pedidos de todas las sucursales. Solo admin."""
    return await get_all_requests(db)


@router.get("/branch/{branch_id}", response_model=list[StockRequestResponse])
async def list_requests_by_branch(
    branch_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Devuelve los pedidos enviados y recibidos de una sucursal. Admin y staff."""
    return await get_requests_by_branch(db, branch_id)


@router.get("/{request_id}", response_model=StockRequestResponse)
async def get_request(
    request_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Devuelve un pedido por ID. Admin y staff."""
    request = await get_request_by_id(db, request_id)
    if not request:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado",
        )
    return request


@router.post("/", response_model=StockRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_request(
    data: StockRequestCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Crea un pedido de stock a otra sucursal.
    Admin y staff — la sucursal origen es la del usuario autenticado.
    """
    result = await create_stock_request(db, data, current_user.branch_id)

    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"],
        )
    return result


@router.patch("/{request_id}/status", response_model=StockRequestResponse)
async def update_status(
    request_id: uuid.UUID,
    data: StockRequestStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """
    Aprueba o rechaza un pedido.
    Si aprueba transfiere el stock automáticamente.
    Solo admin.
    """
    result = await update_request_status(db, request_id, data)

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido no encontrado",
        )
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=result["error"],
        )
    return result