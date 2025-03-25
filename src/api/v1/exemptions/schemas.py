from enum import StrEnum
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class TaxExemptionType(StrEnum):
    personal = "personal"
    personal_increased = "personal_increased"
    spouse = "spouse"
    spouse_increased = "spouse_increased"
    dependent = "dependent"
    dependent_disabled = "dependent_disabled"


class TaxExemptionCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=100)
    annual_amount: float = Field(..., ge=0)
    monthly_amount: float = Field(..., ge=0)
    description: str | None = Field(None, max_length=255)


class TaxExemptionUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    code: str | None = Field(None, min_length=1, max_length=100)
    annual_amount: float | None = Field(None, ge=0)
    monthly_amount: float | None = Field(None, ge=0)
    description: str | None = Field(None, max_length=255)


class TaxExemptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(..., min_length=1, max_length=100)
    code: str = Field(..., min_length=1, max_length=100)
    annual_amount: float = Field(..., ge=0)
    monthly_amount: float = Field(..., ge=0)
    description: str | None = Field(None, max_length=255)
    created_at: datetime
    updated_at: datetime