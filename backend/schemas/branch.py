# schemas/branch.py
import uuid

from pydantic import BaseModel


# ──────────────────────────── Request schemas (entrada) ────────────────────────────

class BranchCreate(BaseModel):
    """Lo que el admin manda para crear una sucursal."""
    name: str
    address: str | None = None


class BranchUpdate(BaseModel):
    """Todos los campos opcionales — solo se actualizan los que se manden."""
    name: str | None = None
    address: str | None = None


# ──────────────────────────── Response schemas (salida) ────────────────────────────

class BranchResponse(BaseModel):
    """Lo que devuelve la API cuando retorna una sucursal."""
    id: uuid.UUID
    name: str
    address: str | None = None

    model_config = {"from_attributes": True}