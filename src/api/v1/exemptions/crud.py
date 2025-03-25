from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.exemptions.schemas import TaxExemptionCreate, TaxExemptionUpdate
from src.core.models.tax_exemption import TaxExemption


async def create_tax_exemption(
    session: AsyncSession, tax_exemption: TaxExemptionCreate
) -> TaxExemption:
    """
    Create a new tax exemption.

    Args:
        session: Database session
        tax_exemption: Tax exemption data

    Returns:
        Created tax exemption
    """
    db_tax_exemption = TaxExemption(**tax_exemption.model_dump())
    session.add(db_tax_exemption)
    await session.commit()
    return db_tax_exemption


async def get_tax_exemptions(session: AsyncSession) -> list[TaxExemption]:
    """
    Get all tax exemptions.

    Args:
        session: Database session

    Returns:
        list of tax exemptions
    """
    result = await session.execute(select(TaxExemption))
    return list(result.scalars().all())


async def get_tax_exemption_by_id(
    session: AsyncSession, tax_exemption_id: int
) -> TaxExemption | None:
    """
    Get a tax exemption by ID.

    Args:
        session: Database session
        tax_exemption_id: Tax exemption ID

    Returns:
        Tax exemption if found, None otherwise
    """
    result = await session.execute(
        select(TaxExemption).where(TaxExemption.id == tax_exemption_id)
    )
    return result.scalar_one_or_none()


async def get_tax_exemption_by_code(
    session: AsyncSession, code: str
) -> TaxExemption | None:
    """
    Get a tax exemption by code.

    Args:
        session: Database session
        code: Tax exemption code

    Returns:
        Tax exemption if found, None otherwise
    """
    result = await session.execute(
        select(TaxExemption).where(TaxExemption.code == code)
    )
    return result.scalar_one_or_none()


async def update_tax_exemption(
    session: AsyncSession,
    tax_exemption: TaxExemption,
    tax_exemption_update: TaxExemptionUpdate,
) -> TaxExemption | None:
    """
    Update a tax exemption.

    Args:
        session: Database session
        tax_exemption: Tax exemption object
        tax_exemption_update: Tax exemption update data

    Returns:
        Updated tax exemption if found, None otherwise
    """
    update_data = tax_exemption_update.model_dump(
        exclude_unset=True,
        exclude_none=True,
    )

    if not update_data:
        return tax_exemption

    for key, value in update_data.items():
        setattr(tax_exemption, key, value)
    await session.commit()
    await session.refresh(tax_exemption)

    return tax_exemption


async def delete_tax_exemption(
    session: AsyncSession, tax_exemption: TaxExemption
) -> None:
    """
    Delete a tax exemption.

    Args:
        session: Database session
        tax_exemption: Tax exemption object

    Returns:
        True if deleted, False if not found
    """
    await session.delete(tax_exemption)
    await session.commit()
