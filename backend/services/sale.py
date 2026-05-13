# services/sale.py
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from models.models import Product, Sale, SaleItem, Stock
from schemas.sale import SaleCreate


async def get_sales_by_branch(db: AsyncSession, branch_id: uuid.UUID) -> list[Sale]:
    """Devuelve todas las ventas de una sucursal con sus items y productos."""
    result = await db.execute(
        select(Sale)
        .where(Sale.branch_id == branch_id)
        .options(
            selectinload(Sale.items).selectinload(SaleItem.product)
        )
        .order_by(Sale.created_at.desc())
    )
    return list(result.scalars().all())


async def get_sale_by_id(db: AsyncSession, sale_id: uuid.UUID) -> Sale | None:
    """Devuelve una venta por ID con sus items y productos."""
    result = await db.execute(
        select(Sale)
        .where(Sale.id == sale_id)
        .options(
            selectinload(Sale.items).selectinload(SaleItem.product)
        )
    )
    return result.scalar_one_or_none()


async def create_sale(
    db: AsyncSession,
    data: SaleCreate,
    branch_id: uuid.UUID,
    user_id: uuid.UUID,
) -> Sale | dict:
    """
    Registra una venta nueva.
    1. Verifica que haya stock suficiente para todos los items
    2. Si alguno falla devuelve el error sin tocar nada
    3. Si todo ok crea la venta, descuenta el stock y calcula el total
    """

    # ── Paso 1: verificar stock y traer productos ──
    items_data = []

    for item in data.items:

        # traer el stock de ese producto en esa sucursal
        stock_result = await db.execute(
            select(Stock).where(
                Stock.branch_id == branch_id,
                Stock.product_id == item.product_id,
            )
        )
        stock = stock_result.scalar_one_or_none()

        if not stock:
            return {
                "error": f"Producto {item.product_id} no existe en esta sucursal"
            }

        if stock.quantity < item.quantity:
            return {
                "error": f"Stock insuficiente para el producto {item.product_id}. "
                         f"Disponible: {stock.quantity}, solicitado: {item.quantity}"
            }

        # traer el precio actual del producto
        product_result = await db.execute(
            select(Product).where(Product.id == item.product_id)
        )
        product = product_result.scalar_one_or_none()

        items_data.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": product.price,
            "stock": stock,
        })

    # ── Paso 2: crear la venta ──
    total = sum(i["quantity"] * i["unit_price"] for i in items_data)

    sale = Sale(
        branch_id=branch_id,
        user_id=user_id,
        total=total,
    )
    db.add(sale)
    await db.flush()  # para obtener el sale.id antes del commit

    # ── Paso 3: crear los items y descontar stock ──
    for item_data in items_data:
        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=item_data["product_id"],
            quantity=item_data["quantity"],
            unit_price=item_data["unit_price"],
        )
        db.add(sale_item)

        # descontar del stock
        item_data["stock"].quantity -= item_data["quantity"]

    await db.commit()

    # recargar la venta con todos sus items y productos
    result = await db.execute(
        select(Sale)
        .where(Sale.id == sale.id)
        .options(
            selectinload(Sale.items).selectinload(SaleItem.product)
        )
    )
    return result.scalar_one()