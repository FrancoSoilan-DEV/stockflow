# schemas/user.py
import uuid

from pydantic import BaseModel, EmailStr

from models.models import UserRole


# ──────────────────────────── Request schemas (entrada) ────────────────────────────

class UserCreate(BaseModel):
    """Lo que el admin manda para crear un usuario."""
    username: str
    email: EmailStr
    password: str
    role: UserRole = UserRole.staff
    branch_id: uuid.UUID


class UserLogin(BaseModel):
    """Lo que manda cualquier usuario para hacer login."""
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    """Todos los campos opcionales — solo se actualizan los que se manden."""
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    role: UserRole | None = None
    branch_id: uuid.UUID | None = None
    
# ──────────────────────────── Response schemas (salida) ────────────────────────────

class UserResponse(BaseModel):
    """Lo que devuelve la API cuando retorna un usuario — nunca expone la contraseña."""
    id: uuid.UUID
    username: str
    email: EmailStr
    role: UserRole
    branch_id: uuid.UUID

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    """Lo que devuelve la API después de un login exitoso."""
    access_token: str
    token_type: str = "bearer"