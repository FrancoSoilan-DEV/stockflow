# routers/branches.py
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user, require_admin
from db.session import get_db
from models.models import User
from schemas.branch import BranchCreate, BranchResponse, BranchUpdate
from services.branch import (
    create_branch,
    delete_branch,
    get_all_branches,
    get_branch_by_id,
    update_branch,
)

router = APIRouter(prefix="/branches", tags=["branches"])


@router.get("/", response_model=list[BranchResponse])
async def list_branches(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Devuelve todas las sucursales. Acceso: admin y staff."""
    return await get_all_branches(db)


@router.get("/{branch_id}", response_model=BranchResponse)
async def get_branch(
    branch_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Devuelve una sucursal por ID. Acceso: admin y staff."""
    branch = await get_branch_by_id(db, branch_id)
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sucursal no encontrada",
        )
    return branch


@router.post("/", response_model=BranchResponse, status_code=status.HTTP_201_CREATED)
async def create_branch_endpoint(
    data: BranchCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Crea una sucursal nueva. Acceso: solo admin."""
    return await create_branch(db, data)


@router.patch("/{branch_id}", response_model=BranchResponse)
async def update_branch_endpoint(
    branch_id: uuid.UUID,
    data: BranchUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Actualiza una sucursal. Acceso: solo admin."""
    branch = await update_branch(db, branch_id, data)
    if not branch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sucursal no encontrada",
        )
    return branch


@router.delete("/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_branch_endpoint(
    branch_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Elimina una sucursal. Acceso: solo admin."""
    deleted = await delete_branch(db, branch_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sucursal no encontrada",
        )