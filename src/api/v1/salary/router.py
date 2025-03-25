import asyncio
from typing import Annotated

from fastapi import APIRouter, Query

from src.api.v1.salary.schemas import SalaryCalculationResponse
from src.api.v1.taxes.crud import get_tax_rate_by_code
from src.api.v1.taxes.schemas import TaxRateType
from src.core.database import DbSessionDep

router = APIRouter(prefix="/salary", tags=["salary"])

@router.post("/calculate", response_model=SalaryCalculationResponse)
async def calculate_salary(
    session: DbSessionDep,
    gross_salary: Annotated[float, Query(gt=0)],
):
    """
    Calculate taxes and net salary based on gross salary.

    - **gross_salary**: Gross salary amount (required)

    Returns calculated taxes and net salary.
    """
    tax_rates = await asyncio.gather(
        get_tax_rate_by_code(session, TaxRateType.social_fund),
        get_tax_rate_by_code(session, TaxRateType.medical_insurance),
        get_tax_rate_by_code(session, TaxRateType.income_tax),
    )

    social_fund_rate, medical_insurance_rate, income_tax_rate = (
        rate.rate if rate is not None else 0 for rate in tax_rates
    )

    social_fund = gross_salary * social_fund_rate
    medical_insurance = gross_salary * medical_insurance_rate

    # Taxable income after deductions
    taxable_income = gross_salary - medical_insurance

    # Calculate income tax
    income_tax = taxable_income * income_tax_rate

    # Calculate net salary
    net_salary = gross_salary - medical_insurance - income_tax

    # Calculate total salary
    total_salary = gross_salary + social_fund

    return {
        "gross_salary": gross_salary,
        "social_fund": social_fund,
        "medical_insurance": medical_insurance,
        "income_tax": income_tax,
        "net_salary": net_salary,
        "total_salary": total_salary,
    }