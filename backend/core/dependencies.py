# core/dependencies.py
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from core.security import decode_access_token
from db.session import get_db
from models.models import User, UserRole
from services.auth import get_user_by_id

# Le dice a FastAPI dónde está el endpoint de login para pedir el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Extrae y valida el token de cada request.
    - Si el token es inválido o venció → 401
    - Si el usuario no existe en la DB → 401
    - Si todo ok → devuelve el objeto User completo
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if not payload:
        raise credentials_exception

    user_id: str | None = payload.get("sub")
    if not user_id:
        raise credentials_exception

    user = await get_user_by_id(db, uuid.UUID(user_id))
    if not user:
        raise credentials_exception

    return user


async def require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Extiende get_current_user — además verifica que sea admin.
    - Si no es admin → 403
    """
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren permisos de administrador",
        )
    return current_user