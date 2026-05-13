# schemas/stock_request.py
import uuid
from datetime import datetime

from pydantic import BaseModel

from models.models import RequestStatus
from schemas.product import ProductResponse


class StockRequestCreate(BaseModel):
    """Lo que el staff manda para solicitar stock de otra sucursal."""
    to_branch_id: uuid.UUID
    product_id: uuid.UUID
    quantity: int


class StockRequestStatusUpdate(BaseModel):
    """Lo que el admin manda para aprobar o rechazar un pedido."""
    status: RequestStatus


class StockRequestResponse(BaseModel):
    id: uuid.UUID
    from_branch_id: uuid.UUID
    to_branch_id: uuid.UUID
    product_id: uuid.UUID
    quantity: int
    status: RequestStatus
    created_at: datetime
    product: ProductResponse

    model_config = {"from_attributes": True}