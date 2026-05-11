# services/branch.py
import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Branch
from schemas.branch import BranchCreate, BranchUpdate


async def get_all_branches(db: AsyncSession) -> list[Branch]:
    """Devuelve todas las sucursales."""
    result = await db.execute(select(Branch))
    return list(result.scalars().all())


async def get_branch_by_id(db: AsyncSession, branch_id: uuid.UUID) -> Branch | None:
    """Busca una sucursal por ID."""
    result = await db.execute(select(Branch).where(Branch.id == branch_id))
    return result.scalar_one_or_none()


async def create_branch(db: AsyncSession, data: BranchCreate) -> Branch:
    """Crea una sucursal nueva."""
    branch = Branch(
        name=data.name,
        address=data.address,
    )
    db.add(branch)
    await db.commit()
    await db.refresh(branch)
    return branch


async def update_branch(
    db: AsyncSession, branch_id: uuid.UUID, data: BranchUpdate
) -> Branch | None:
    """
    Actualiza solo los campos que se manden.
    Si la sucursal no existe devuelve None.
    """
    branch = await get_branch_by_id(db, branch_id)
    if not branch:
        return None

    # model_dump(exclude_unset=True) devuelve solo los campos que el cliente mandó
    # así no pisamos campos con None sin querer
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(branch, field, value)

    await db.commit()
    await db.refresh(branch)
    return branch


async def delete_branch(db: AsyncSession, branch_id: uuid.UUID) -> bool:
    """
    Elimina una sucursal.
    Devuelve True si se eliminó, False si no existía.
    """
    branch = await get_branch_by_id(db, branch_id)
    if not branch:
        return False

    await db.delete(branch)
    await db.commit()
    return True