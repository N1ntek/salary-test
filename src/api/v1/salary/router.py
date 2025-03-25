from typing import Annotated
from fastapi import APIRouter, Query

from src.api.v1.salary.schemas import SalaryCalculationResponse
from src.api.v1.taxes.crud import get_tax_rate_by_code, get_tax_rate_by_id
from src.api.v1.exemptions.crud import get_tax_exemption_by_code
from src.api.v1.taxes.schemas import TaxRateType
from src.core.database import DbSessionDep

router = APIRouter(prefix="/salary", tags=["salary"])


@router.post("/calculate", response_model=SalaryCalculationResponse)
async def calculate_salary(
    session: DbSessionDep,
    gross_salary: Annotated[float, Query(gt=0)],
    social_rate_id: int | None = None,
    custom_medical_insurance_rate: int | None = Query(
        None, description="Asigurare medicală Angajat(% manual, optional):"
    ),
    use_personal_exemption: bool = Query(False, description="Apply personal exemption"),
    use_increased_personal_exemption: bool = Query(
        False, description="Apply increased personal exemption"
    ),
    use_increased_spouse_exemption: bool = Query(
        False, description="Apply increased spouse exemption"
    ),
    dependent_count: int = Query(
        0, ge=0, description="Number of dependents without disabilities"
    ),
    disabled_dependent_count: int = Query(
        0, ge=0, description="Number of dependents with disabilities"
    ),
):
    """
    Calculate taxes and net salary based on gross salary.

    - **gross_salary**: Gross salary amount (required)
    - **social_rate_id**: Optional ID of a specific social rate to use (if not provided, default social rate will be used)
    - **custom_medical_insurance_rate**: Optional custom medical insurance rate (percentage)
    - **use_personal_exemption**: Whether to apply personal exemption
    - **use_increased_personal_exemption**: Whether to apply increased personal exemption
    - **use_increased_spouse_exemption**: Whether to apply increased spouse exemption
    - **dependent_count**: Number of dependents without disabilities
    - **disabled_dependent_count**: Number of dependents with disabilities

    Returns calculated taxes and net salary.
    """
    # Get medical insurance and income tax rates
    income_tax_rate_obj = await get_tax_rate_by_code(session, TaxRateType.income_tax)

    # Get social fund rate - either by ID if provided, or default
    if social_rate_id is not None:
        social_fund_rate_obj = await get_tax_rate_by_id(session, social_rate_id)
        if (
            social_fund_rate_obj is None
            or social_fund_rate_obj.type != TaxRateType.social_fund
        ):
            # Fallback to default if specified ID is not found or not a social fund rate
            social_fund_rate_obj = await get_tax_rate_by_code(
                session, TaxRateType.social_fund
            )
    else:
        social_fund_rate_obj = await get_tax_rate_by_code(
            session, TaxRateType.social_fund
        )

    # Extract rates from objects
    social_fund_rate = (
        social_fund_rate_obj.rate if social_fund_rate_obj is not None else 0
    )

    # Extract default rate
    if custom_medical_insurance_rate is None:
        medical_insurance_rate_obj = await get_tax_rate_by_code(
            session, TaxRateType.medical_insurance
        )
        medical_insurance_rate = (
            medical_insurance_rate_obj.rate
            if medical_insurance_rate_obj is not None
            else 0
        )
    else:
        medical_insurance_rate = custom_medical_insurance_rate / 100
        print(medical_insurance_rate)

    income_tax_rate = income_tax_rate_obj.rate if income_tax_rate_obj is not None else 0

    social_fund = gross_salary * social_fund_rate
    medical_insurance = gross_salary * medical_insurance_rate

    # Get tax exemptions
    total_exemption_amount = 0.0

    # Personal exemption (only one of personal or increased personal can be applied)
    if use_increased_personal_exemption:
        personal_exemption = await get_tax_exemption_by_code(
            session, "personal_increased"
        )
        if personal_exemption:
            total_exemption_amount += personal_exemption.monthly_amount
    elif use_personal_exemption:
        personal_exemption = await get_tax_exemption_by_code(session, "personal")
        if personal_exemption:
            total_exemption_amount += personal_exemption.monthly_amount

    # Spouse exemption
    if use_increased_spouse_exemption:
        spouse_exemption = await get_tax_exemption_by_code(session, "spouse_increased")
        if spouse_exemption:
            total_exemption_amount += spouse_exemption.monthly_amount

    # Dependent exemptions
    if dependent_count > 0:
        dependent_exemption = await get_tax_exemption_by_code(session, "dependent")
        if dependent_exemption:
            total_exemption_amount += (
                dependent_exemption.monthly_amount * dependent_count
            )

    if disabled_dependent_count > 0:
        disabled_dependent_exemption = await get_tax_exemption_by_code(
            session, "dependent_disabled"
        )
        if disabled_dependent_exemption:
            total_exemption_amount += (
                disabled_dependent_exemption.monthly_amount * disabled_dependent_count
            )

    # Taxable income after deductions and exemptions
    taxable_income = max(0.0, gross_salary - medical_insurance - total_exemption_amount)

    # Calculate income tax
    income_tax = taxable_income * income_tax_rate

    # Calculate net salary
    net_salary = gross_salary - medical_insurance - income_tax

    # Calculate total salary
    total_salary = gross_salary + social_fund

    return {
        "gross_salary": round(gross_salary, 2),
        "social_fund": round(social_fund, 2),
        "medical_insurance": round(medical_insurance, 2),
        "income_tax": round(income_tax, 2),
        "tax_exemptions": round(total_exemption_amount, 2),
        "net_salary": round(net_salary, 2),
        "total_salary": round(total_salary, 2),
    }
