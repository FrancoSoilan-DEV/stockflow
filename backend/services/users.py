# services/users.py
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import hash_password
from models.models import User
from schemas.user import UserCreate, UserUpdate


async def get_all_users(db: AsyncSession) -> list[User]:
    """Devuelve todos los usuarios."""
    result = await db.execute(select(User))
    return list(result.scalars().all())


async def get_user_by_id_service(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    """Busca un usuario por ID."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user_service(db: AsyncSession, data: UserCreate) -> User | None:
    """
    Crea un usuario nuevo.
    Devuelve None si el email o username ya existen.
    """
    existing = await db.execute(
        select(User).where(
            (User.email == data.email) | (User.username == data.username)
        )
    )
    if existing.scalar_one_or_none():
        return None

    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
        role=data.role,
        branch_id=data.branch_id,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def update_user_service(
    db: AsyncSession, user_id: uuid.UUID, data: UserUpdate
) -> User | None:
    """
    Actualiza solo los campos que se manden.
    Si mandan password la hashea antes de guardarla.
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return None

    update_data = data.model_dump(exclude_unset=True)

    # si mandan password la hasheamos antes de guardar
    if "password" in update_data:
        update_data["hashed_password"] = hash_password(update_data.pop("password"))

    for field, value in update_data.items():
        setattr(user, field, value)

    await db.commit()
    await db.refresh(user)
    return user


async def delete_user_service(db: AsyncSession, user_id: uuid.UUID) -> bool:
    """
    Elimina un usuario.
    Devuelve True si se eliminó, False si no existía.
    """
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return False

    await db.delete(user)
    await db.commit()
    return True