# routers/users.py
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.dependencies import get_current_user, require_admin
from db.session import get_db
from models.models import User
from schemas.user import UserCreate, UserResponse, UserUpdate
from services.users import (
    create_user_service,
    delete_user_service,
    get_all_users,
    get_user_by_id_service,
    update_user_service,
)

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[UserResponse])
async def list_users(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Devuelve todos los usuarios. Acceso: admin y staff."""
    return await get_all_users(db)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Devuelve un usuario por ID. Acceso: admin y staff."""
    user = await get_user_by_id_service(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Crea un usuario nuevo. Acceso: solo admin."""
    user = await create_user_service(db, data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El email o username ya están en uso",
        )
    return user


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: uuid.UUID,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Actualiza un usuario. Acceso: solo admin."""
    user = await update_user_service(db, user_id, data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Elimina un usuario. Acceso: solo admin."""
    deleted = await delete_user_service(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado",
        )