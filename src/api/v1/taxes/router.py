from fastapi import APIRouter, HTTPException, status

from src.api.v1.taxes import crud
from src.api.v1.taxes.dependencies import TaxByIdDep
from src.api.v1.taxes.schemas import (
    TaxRateCreate,
    TaxRateUpdate,
    TaxRateResponse,
    TaxRateType,
)
from src.core.database import DbSessionDep

router = APIRouter(prefix="/taxes", tags=["taxes"])


@router.post("/", response_model=TaxRateResponse, status_code=status.HTTP_201_CREATED)
async def create_tax_rate(
    tax_rate: TaxRateCreate,
    session: DbSessionDep,
):
    """
    Create a new tax rate.
    
    - **name**: Tax rate name (required)
    - **code**: Unique tax rate code (required) ("social_fund", "medical_insurance", "income_tax")
    - **rate**: Tax rate value between 0 and 1 (required)
    - **description**: Optional description
    
    Returns the created tax rate.
    """
    # Check if tax rate with the same code already exists
    existing_tax_rate = await crud.get_tax_rate_by_code(session, tax_rate.code)
    if existing_tax_rate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tax rate with code '{tax_rate.code}' already exists",
        )
    
    return await crud.create_tax_rate(session, tax_rate)


@router.get("/", response_model=list[TaxRateResponse])
async def get_tax_rates(
    session: DbSessionDep,
    tax_type: TaxRateType | None = None,
):
    """
    Get all tax rates.
    
    Returns a list of tax rates.
    """
    return await crud.get_tax_rates(session, tax_type)


@router.get("/{tax_rate_id}", response_model=TaxRateResponse)
async def get_tax_rate(
    tax_rate: TaxByIdDep,
):
    """
    Get a tax rate by ID.
    
    - **tax_rate_id**: Tax rate ID (required)
    
    Returns the tax rate if found.
    """
    return tax_rate


@router.get("/code/{code}", response_model=TaxRateResponse)
async def get_tax_rate_by_code(
    code: str,
    session: DbSessionDep,
):
    """
    Get a tax rate by code.
    
    - **code**: Tax rate code (required)
    
    Returns the tax rate if found.
    """
    tax_rate = await crud.get_tax_rate_by_code(session, code)
    if not tax_rate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tax rate with code '{code}' not found",
        )
    
    return tax_rate


@router.put("/{tax_rate_id}", response_model=TaxRateResponse)
async def update_tax_rate(
    tax_rate_update: TaxRateUpdate,
    session: DbSessionDep,
    tax_rate: TaxByIdDep,
):
    """
    Update a tax rate.
    
    - **tax_rate_id**: Tax rate ID (required)
    - **name**: New tax rate name (optional)
    - **rate**: New tax rate value between 0 and 1 (optional)
    - **description**: New description (optional)
    
    Returns the updated tax rate if found.
    """
    updated_tax_rate = await crud.update_tax_rate(session, tax_rate, tax_rate_update)
    return updated_tax_rate


@router.delete("/{tax_rate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tax_rate(
    session: DbSessionDep,
    tax_rate: TaxByIdDep,
):
    """
    Delete a tax rate.
    
    - **tax_rate_id**: Tax rate ID (required)
    
    Returns no content if successful.
    """
    await crud.delete_tax_rate(session, tax_rate)