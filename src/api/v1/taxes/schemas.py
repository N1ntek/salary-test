from enum import StrEnum
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TaxRateType(StrEnum):
    social_fund = "social_fund"
    medical_insurance = "medical_insurance"
    income_tax = "income_tax"


class TaxRateCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    type: TaxRateType
    code: str = Field(..., min_length=1, max_length=100)
    rate: float = Field(..., gt=0, lt=1)
    description: str | None = Field(None, max_length=255)


class TaxRateUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    type: TaxRateType | None = None
    code: str | None = Field(None, min_length=1, max_length=100)
    rate: float | None = Field(None, gt=0, lt=1)
    description: str | None = Field(None, max_length=255)


class TaxRateResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(..., min_length=1, max_length=100)
    type: TaxRateType
    code: str = Field(..., min_length=1, max_length=100)
    rate: float = Field(..., gt=0, lt=1)
    description: str | None = Field(None, max_length=255)
    created_at: datetime
    updated_at: datetime