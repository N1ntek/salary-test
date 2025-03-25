import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.taxes.schemas import TaxRateType
from src.core.models import TaxRate, TaxExemption

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
            name="Social Fund (Private Sector, Higher Education, Medical Institutions)",
            type=TaxRateType.social_fund,
            code="social_fund",
            rate=0.24,
            description="Social fund contribution (24%) for private sector, higher education, and medical institutions",
        ),
        TaxRate(
            name="Social Fund (Public Institutions)",
            type=TaxRateType.social_fund,
            code="social_fund_29",
            rate=0.29,
            description="Social fund contribution (29%) for budgetary/public institutions",
        ),
        TaxRate(
            name="Special Conditions (Private Sector, Higher Education, Medical Institutions)",
            type=TaxRateType.social_fund,
            code="social_fund_32",
            rate=0.32,
            description="Social fund contribution (32%) for special conditions in private sector, higher education, and medical institutions",
        ),
        TaxRate(
            name="Special Conditions (Public Institutions)",
            type=TaxRateType.social_fund,
            code="social_fund_39",
            rate=0.39,
            description="Social fund contribution (39%) for special conditions in budgetary/public institutions",
        ),
        TaxRate(
            name="Medical Insurance",
            type=TaxRateType.medical_insurance,
            code="medical_insurance",
            rate=0.09,
            description="Medical insurance contribution (9%)",
        ),
        TaxRate(
            name="Income Tax",
            type=TaxRateType.income_tax,
            code="income_tax",
            rate=0.12,
            description="Income tax (12%)",
        ),
    ]

    session.add_all(tax_rates)
    await session.commit()

    logger.info("Default tax rates initialized.")


async def init_tax_exemptions(session: AsyncSession) -> None:
    """
    Initialize tax exemptions in the database if they don't exist.
    """
    existing_exemptions = (await session.scalars(select(TaxExemption))).all()
    if existing_exemptions:
        return

    tax_exemptions = [
        TaxExemption(
            name="Scutirea personala",
            code="personal",
            annual_amount=29700,
            monthly_amount=2475,
            description="Personal exemption",
        ),
        TaxExemption(
            name="Scutirea personala majorata",
            code="personal_increased",
            annual_amount=34620,
            monthly_amount=2885,
            description="Increased personal exemption",
        ),
        TaxExemption(
            name="Scutirea acordata sotiei (sotului) majorata",
            code="spouse_increased",
            annual_amount=21780,
            monthly_amount=1815,
            description="Increased spouse exemption",
        ),
        TaxExemption(
            name="Scutirea pentru pers. intretinute cu except. pers. cu dizabilitati",
            code="dependent",
            annual_amount=9900,
            monthly_amount=825,
            description="Exemption for dependents except those with disabilities",
        ),
        TaxExemption(
            name="Scutirea pentru pers. intretinute cu dizabilitati",
            code="dependent_disabled",
            annual_amount=21780,
            monthly_amount=1815,
            description="Exemption for dependents with disabilities from birth or childhood",
        ),
    ]

    session.add_all(tax_exemptions)
    await session.commit()

    logger.info("Default tax exemptions initialized.")


async def init_db(db: AsyncSession):
    """
    Initialize the database with default data.
    """
    await init_tax_rates(db)
    await init_tax_exemptions(db)
