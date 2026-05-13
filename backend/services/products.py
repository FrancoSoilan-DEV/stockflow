# services/products.py
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Product
from schemas.product import ProductCreate, ProductUpdate


async def get_all_products(db: AsyncSession) -> list[Product]:
    result = await db.execute(select(Product))
    return list(result.scalars().all())


async def get_product_by_id(db: AsyncSession, product_id: uuid.UUID) -> Product | None:
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar_one_or_none()


async def create_product(db: AsyncSession, data: ProductCreate) -> Product:
    product = Product(
        name=data.name,
        description=data.description,
        category=data.category,
        price=data.price,
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def update_product(
    db: AsyncSession, product_id: uuid.UUID, data: ProductUpdate
) -> Product | None:
    product = await get_product_by_id(db, product_id)
    if not product:
        return None

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)
    return product


async def delete_product(db: AsyncSession, product_id: uuid.UUID) -> bool:
    product = await get_product_by_id(db, product_id)
    if not product:
        return False

    await db.delete(product)
    await db.commit()
    return True