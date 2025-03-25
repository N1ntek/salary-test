from fastapi import APIRouter, HTTPException, status

from src.api.v1.exemptions import crud
from src.api.v1.exemptions.dependencies import TaxExemptionByIdDep
from src.api.v1.exemptions.schemas import (
    TaxExemptionCreate,
    TaxExemptionUpdate,
    TaxExemptionResponse,
)
from src.core.database import DbSessionDep

router = APIRouter(prefix="/exemptions", tags=["exemptions"])


@router.post("/", response_model=TaxExemptionResponse, status_code=status.HTTP_201_CREATED)
async def create_tax_exemption(
    tax_exemption: TaxExemptionCreate,
    session: DbSessionDep,
):
    """
    Create a new tax exemption.
    
    - **name**: Tax exemption name (required)
    - **code**: Unique tax exemption code (required)
    - **annual_amount**: Annual exemption amount (required)
    - **monthly_amount**: Monthly exemption amount (required)
    - **description**: Optional description
    
    Returns the created tax exemption.
    """
    # Check if tax exemption with the same code already exists
    existing_tax_exemption = await crud.get_tax_exemption_by_code(session, tax_exemption.code)
    if existing_tax_exemption:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tax exemption with code '{tax_exemption.code}' already exists",
        )
    
    return await crud.create_tax_exemption(session, tax_exemption)


@router.get("/", response_model=list[TaxExemptionResponse])
async def get_tax_exemptions(
    session: DbSessionDep,
):
    """
    Get all tax exemptions.
    
    Returns a list of tax exemptions.
    """
    return await crud.get_tax_exemptions(session)


@router.get("/{tax_exemption_id}", response_model=TaxExemptionResponse)
async def get_tax_exemption(
    tax_exemption: TaxExemptionByIdDep,
):
    """
    Get a tax exemption by ID.
    
    - **tax_exemption_id**: Tax exemption ID (required)
    
    Returns the tax exemption if found.
    """
    return tax_exemption


@router.get("/code/{code}", response_model=TaxExemptionResponse)
async def get_tax_exemption_by_code(
    code: str,
    session: DbSessionDep,
):
    """
    Get a tax exemption by code.
    
    - **code**: Tax exemption code (required)
    
    Returns the tax exemption if found.
    """
    tax_exemption = await crud.get_tax_exemption_by_code(session, code)
    if not tax_exemption:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tax exemption with code '{code}' not found",
        )
    
    return tax_exemption


@router.put("/{tax_exemption_id}", response_model=TaxExemptionResponse)
async def update_tax_exemption(
    tax_exemption_update: TaxExemptionUpdate,
    session: DbSessionDep,
    tax_exemption: TaxExemptionByIdDep,
):
    """
    Update a tax exemption.
    
    - **tax_exemption_id**: Tax exemption ID (required)
    - **name**: New tax exemption name (optional)
    - **code**: New tax exemption code (optional)
    - **annual_amount**: New annual exemption amount (optional)
    - **monthly_amount**: New monthly exemption amount (optional)
    - **description**: New description (optional)
    
    Returns the updated tax exemption if found.
    """
    updated_tax_exemption = await crud.update_tax_exemption(session, tax_exemption, tax_exemption_update)
    return updated_tax_exemption


@router.delete("/{tax_exemption_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tax_exemption(
    session: DbSessionDep,
    tax_exemption: TaxExemptionByIdDep,
):
    """
    Delete a tax exemption.
    
    - **tax_exemption_id**: Tax exemption ID (required)
    
    Returns no content if successful.
    """
    await crud.delete_tax_exemption(session, tax_exemption)