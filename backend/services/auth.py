# services/auth.py
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import create_access_token, hash_password, verify_password
from models.models import User
from schemas.user import UserCreate


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Busca un usuario por email en la DB."""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    """Busca un usuario por ID en la DB."""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, data: UserCreate) -> User:
    """
    Crea un usuario nuevo.
    - Recibe la contraseña en texto plano
    - La hashea antes de guardarla
    """
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


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    """
    Verifica credenciales.
    - Busca el usuario por email
    - Compara la contraseña con el hash guardado
    - Si todo ok devuelve el usuario, si no devuelve None
    """
    user = await get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def login_user(db: AsyncSession, email: str, password: str) -> dict | None:
    """
    Flujo completo de login.
    - Autentica al usuario
    - Si es válido genera y devuelve el token
    """
    user = await authenticate_user(db, email, password)
    if not user:
        return None

    token = create_access_token(data={
        "sub": str(user.id),
        "role": user.role.value,
        "branch_id": str(user.branch_id),
    })

    return {"access_token": token, "token_type": "bearer"}