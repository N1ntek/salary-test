from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.taxes.schemas import TaxRateCreate, TaxRateUpdate
from src.core.models.tax_rate import TaxRate


async def create_tax_rate(session: AsyncSession, tax_rate: TaxRateCreate) -> TaxRate:
    """
    Create a new tax rate.
    
    Args:
        session: Database session
        tax_rate: Tax rate data
        
    Returns:
        Created tax rate
    """
    db_tax_rate = TaxRate(**tax_rate.model_dump())
    session.add(db_tax_rate)
    await session.commit()
    await session.refresh(db_tax_rate)
    return db_tax_rate


async def get_tax_rates(session: AsyncSession) -> List[TaxRate]:
    """
    Get all tax rates.
    
    Args:
        session: Database session
        
    Returns:
        List of tax rates
    """
    result = await session.execute(select(TaxRate))
    return list(result.scalars().all())


async def get_tax_rate_by_id(session: AsyncSession, tax_rate_id: int) -> TaxRate | None:
    """
    Get a tax rate by ID.
    
    Args:
        session: Database session
        tax_rate_id: Tax rate ID
        
    Returns:
        Tax rate if found, None otherwise
    """
    result = await session.execute(select(TaxRate).where(TaxRate.id == tax_rate_id))
    return result.scalar_one_or_none()


async def get_tax_rate_by_code(session: AsyncSession, code: str) -> TaxRate | None:
    """
    Get a tax rate by code.
    
    Args:
        session: Database session
        code: Tax rate code
        
    Returns:
        Tax rate if found, None otherwise
    """
    result = await session.execute(select(TaxRate).where(TaxRate.code == code))
    return result.scalar_one_or_none()


async def update_tax_rate(
    session: AsyncSession, tax_rate: TaxRate, tax_rate_update: TaxRateUpdate
) -> TaxRate | None:
    """
    Update a tax rate.
    
    Args:
        session: Database session
        tax_rate: Tax rate object
        tax_rate_update: Tax rate update data
        
    Returns:
        Updated tax rate if found, None otherwise
    """
    update_data = tax_rate_update.model_dump(
        exclude_unset=True, exclude_none=True,
    )
    
    if not update_data:
        return tax_rate

    for key, value in update_data.items():
        setattr(tax_rate, key, value)
    await session.commit()
    await session.refresh(tax_rate)

    return tax_rate


async def delete_tax_rate(session: AsyncSession, tax_rate: TaxRate) -> None:
    """
    Delete a tax rate.
    
    Args:
        session: Database session
        tax_rate: Tax rate object
        
    Returns:
        True if deleted, False if not found
    """
    await session.delete(tax_rate)
    await session.commit()
