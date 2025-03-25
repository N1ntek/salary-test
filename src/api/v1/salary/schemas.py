from pydantic import BaseModel, ConfigDict

class SalaryCalculationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    social_fund: float
    medical_insurance: float
    income_tax: float
    tax_exemptions: float = 0

    gross_salary: float
    net_salary: float
    total_salary: float
