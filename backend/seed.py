# seed.py
import asyncio
from decimal import Decimal

from db.session import AsyncSessionLocal
from models.models import Branch, Message, Product, RequestStatus, Sale, SaleItem, Stock, StockRequest, User, UserRole
from core.security import hash_password


async def seed():
    async with AsyncSessionLocal() as db:

        # ── Sucursales ──
        branch1 = Branch(name="Sucursal Centro", address="Av. Principal 123")
        branch2 = Branch(name="Sucursal Norte", address="Calle Norte 456")
        branch3 = Branch(name="Sucursal Sur", address="Av. Sur 789")

        db.add_all([branch1, branch2, branch3])
        await db.flush()

        # ── Usuarios ──
        admin = User(
            username="admin",
            email="admin@stockflow.com",
            hashed_password=hash_password("admin123"),
            role=UserRole.admin,
            branch_id=branch1.id,
        )
        juan = User(
            username="juan",
            email="juan@stockflow.com",
            hashed_password=hash_password("juan123"),
            role=UserRole.staff,
            branch_id=branch1.id,
        )
        maria = User(
            username="maria",
            email="maria@stockflow.com",
            hashed_password=hash_password("maria123"),
            role=UserRole.staff,
            branch_id=branch2.id,
        )
        carlos = User(
            username="carlos",
            email="carlos@stockflow.com",
            hashed_password=hash_password("carlos123"),
            role=UserRole.staff,
            branch_id=branch3.id,
        )

        db.add_all([admin, juan, maria, carlos])
        await db.flush()

        # ── Productos ──
        teclado = Product(
            name="Teclado Mecánico RGB",
            description="Teclado mecánico con switches blue y retroiluminación RGB",
            category="Periféricos",
            price=85.00,
        )
        mouse = Product(
            name="Mouse Inalámbrico",
            description="Mouse inalámbrico 2.4GHz 1600 DPI",
            category="Periféricos",
            price=45.00,
        )
        monitor = Product(
            name="Monitor 24\" Full HD",
            description="Monitor IPS 24 pulgadas 1920x1080 75Hz",
            category="Monitores",
            price=220.00,
        )
        ssd = Product(
            name="SSD 500GB",
            description="SSD SATA III 500GB lectura 550MB/s",
            category="Almacenamiento",
            price=65.00,
        )
        ram = Product(
            name="RAM 16GB DDR4",
            description="Memoria RAM DDR4 3200MHz 16GB",
            category="Memoria",
            price=55.00,
        )
        auriculares = Product(
            name="Auriculares Gamer",
            description="Auriculares con micrófono y sonido 7.1 virtual",
            category="Audio",
            price=75.00,
        )

        db.add_all([teclado, mouse, monitor, ssd, ram, auriculares])
        await db.flush()

        # ── Stock por sucursal ──
        stocks = [
            # Centro
            Stock(branch_id=branch1.id, product_id=teclado.id, quantity=10),
            Stock(branch_id=branch1.id, product_id=mouse.id, quantity=15),
            Stock(branch_id=branch1.id, product_id=monitor.id, quantity=5),
            Stock(branch_id=branch1.id, product_id=ssd.id, quantity=8),
            Stock(branch_id=branch1.id, product_id=ram.id, quantity=12),
            Stock(branch_id=branch1.id, product_id=auriculares.id, quantity=0),  # sin stock
            # Norte
            Stock(branch_id=branch2.id, product_id=teclado.id, quantity=3),
            Stock(branch_id=branch2.id, product_id=mouse.id, quantity=7),
            Stock(branch_id=branch2.id, product_id=monitor.id, quantity=0),  # sin stock
            Stock(branch_id=branch2.id, product_id=ssd.id, quantity=4),
            Stock(branch_id=branch2.id, product_id=ram.id, quantity=6),
            Stock(branch_id=branch2.id, product_id=auriculares.id, quantity=9),
            # Sur
            Stock(branch_id=branch3.id, product_id=teclado.id, quantity=0),  # sin stock
            Stock(branch_id=branch3.id, product_id=mouse.id, quantity=11),
            Stock(branch_id=branch3.id, product_id=monitor.id, quantity=3),
            Stock(branch_id=branch3.id, product_id=ssd.id, quantity=0),  # sin stock
            Stock(branch_id=branch3.id, product_id=ram.id, quantity=2),
            Stock(branch_id=branch3.id, product_id=auriculares.id, quantity=5),
        ]

        db.add_all(stocks)
        await db.flush()

        # ── Ventas ──
        venta1 = Sale(
            branch_id=branch1.id,
            user_id=juan.id,
            total=175.00,
        )
        venta2 = Sale(
            branch_id=branch1.id,
            user_id=juan.id,
            total=220.00,
        )
        venta3 = Sale(
            branch_id=branch2.id,
            user_id=maria.id,
            total=120.00,
        )

        db.add_all([venta1, venta2, venta3])
        await db.flush()

        # ── Items de ventas ──
        items = [
            # venta1: 1 teclado + 1 mouse
            SaleItem(sale_id=venta1.id, product_id=teclado.id, quantity=1, unit_price=85.00),
            SaleItem(sale_id=venta1.id, product_id=mouse.id, quantity=2, unit_price=45.00),
            # venta2: 1 monitor
            SaleItem(sale_id=venta2.id, product_id=monitor.id, quantity=1, unit_price=220.00),
            # venta3: 1 ram + 1 ssd
            SaleItem(sale_id=venta3.id, product_id=ram.id, quantity=1, unit_price=55.00),
            SaleItem(sale_id=venta3.id, product_id=ssd.id, quantity=1, unit_price=65.00),
        ]

        db.add_all(items)
        await db.flush()

        # ── Pedidos de stock entre sucursales ──
        requests = [
            # Sur le pide teclados a Centro
            StockRequest(
                from_branch_id=branch3.id,
                to_branch_id=branch1.id,
                product_id=teclado.id,
                quantity=3,
                status=RequestStatus.pending,
            ),
            # Norte le pide monitores a Sur
            StockRequest(
                from_branch_id=branch2.id,
                to_branch_id=branch3.id,
                product_id=monitor.id,
                quantity=2,
                status=RequestStatus.approved,
            ),
            # Centro le pide auriculares a Norte
            StockRequest(
                from_branch_id=branch1.id,
                to_branch_id=branch2.id,
                product_id=auriculares.id,
                quantity=4,
                status=RequestStatus.rejected,
            ),
        ]

        db.add_all(requests)
        await db.flush()

        # ── Mensajes de chat ──
        messages = [
            Message(
                sender_id=juan.id,
                receiver_id=maria.id,
                content="Hola Maria, ¿tienen teclados disponibles en Norte?",
            ),
            Message(
                sender_id=maria.id,
                receiver_id=juan.id,
                content="Sí, tenemos 3 unidades. ¿Cuántos necesitás?",
            ),
            Message(
                sender_id=juan.id,
                receiver_id=maria.id,
                content="Necesitamos 3, ya hice el pedido formal.",
            ),
            Message(
                sender_id=carlos.id,
                receiver_id=admin.id,
                content="Admin, necesitamos reponer stock de SSD en Sur.",
            ),
            Message(
                sender_id=admin.id,
                receiver_id=carlos.id,
                content="Entendido Carlos, lo gestiono esta semana.",
            ),
        ]

        db.add_all(messages)
        await db.commit()

        print("✓ Sucursales creadas:  Centro, Norte, Sur")
        print("✓ Usuarios creados:")
        print("  admin@stockflow.com  / admin123  (admin  - Centro)")
        print("  juan@stockflow.com   / juan123   (staff  - Centro)")
        print("  maria@stockflow.com  / maria123  (staff  - Norte)")
        print("  carlos@stockflow.com / carlos123 (staff  - Sur)")
        print("✓ Productos creados:   6 productos")
        print("✓ Stock cargado:       18 registros (3 sucursales x 6 productos)")
        print("✓ Ventas creadas:      3 ventas con sus items")
        print("✓ Pedidos creados:     3 pedidos entre sucursales")
        print("✓ Mensajes creados:    5 mensajes de chat")


if __name__ == "__main__":
    asyncio.run(seed())