from pydantic import BaseModel, ConfigDict

class SalaryCalculationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    social_fund: float
    medical_insurance: float
    income_tax: float

    gross_salary: float
    net_salary: float
    total_salary: float
