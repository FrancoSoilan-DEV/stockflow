# schemas/stock.py
import uuid

from pydantic import BaseModel

from schemas.product import ProductResponse


class StockUpdate(BaseModel):
    """Para actualizar la cantidad de stock."""
    quantity: int


class StockResponse(BaseModel):
    """Stock de un producto en una sucursal."""
    id: uuid.UUID
    branch_id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    product: ProductResponse

    model_config = {"from_attributes": True}


class StockByProductResponse(BaseModel):
    """Para ver en qué sucursales hay stock de un producto."""
    branch_id: uuid.UUID
    branch_name: str
    quantity: int