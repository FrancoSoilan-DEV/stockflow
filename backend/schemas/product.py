# schemas/product.py
import uuid

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    category: str | None = None
    price: float


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    category: str | None = None
    price: float | None = None


class ProductResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None = None
    category: str | None = None
    price: float

    model_config = {"from_attributes": True}