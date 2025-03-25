import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.models import TaxRate

logger = logging.getLogger(__name__)

async def init_tax_rates(session: AsyncSession) -> None:
    """
    Initialize tax rates in the database if they don't exist.
    """
    existing_rates = (await session.scalars(select(TaxRate))).all()
    if existing_rates:
        return
    
    tax_rates = [
        TaxRate(
            name="Social Fund",
            code="social_fund",
            rate=0.24,
            description="Social fund contribution (24%)"
        ),
        TaxRate(
            name="Medical Insurance",
            code="medical_insurance",
            rate=0.09,
            description="Medical insurance contribution (9%)"
        ),
        TaxRate(
            name="Income Tax",
            code="income_tax",
            rate=0.12,
            description="Income tax (12%)"
        )
    ]

    session.add_all(tax_rates)
    await session.commit()
    
    logger.info("Default tax rates initialized.")


async def init_db(db: AsyncSession):
    """
    Initialize the database with default data.
    """
    await init_tax_rates(db)