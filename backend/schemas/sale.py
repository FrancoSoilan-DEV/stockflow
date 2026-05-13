# schemas/sale.py
import uuid
from datetime import datetime

from pydantic import BaseModel

from schemas.product import ProductResponse


# ──────────────────────────── Request schemas (entrada) ────────────────────────────

class SaleItemCreate(BaseModel):
    """Un item dentro de una venta — qué producto y cuántos."""
    product_id: uuid.UUID
    quantity: int


class SaleCreate(BaseModel):
    """Lo que el staff manda para registrar una venta."""
    items: list[SaleItemCreate]


# ──────────────────────────── Response schemas (salida) ────────────────────────────

class SaleItemResponse(BaseModel):
    """Un item de venta con los datos del producto."""
    id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    unit_price: float
    product: ProductResponse

    model_config = {"from_attributes": True}


class SaleResponse(BaseModel):
    """Una venta completa con todos sus items."""
    id: uuid.UUID
    branch_id: uuid.UUID
    user_id: uuid.UUID
    total: float
    created_at: datetime
    items: list[SaleItemResponse]

    model_config = {"from_attributes": True}