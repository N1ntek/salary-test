from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.api.v1.exemptions import crud
from src.core.database import DbSessionDep
from src.core.models.tax_exemption import TaxExemption


async def get_tax_exemption_by_id(
    tax_exemption_id: int,
    session: DbSessionDep,
) -> TaxExemption:
    """
    Get a tax exemption by ID.

    Args:
        tax_exemption_id: Tax exemption ID
        session: Database session

    Returns:
        Tax exemption if found

    Raises:
        HTTPException: If tax exemption not found
    """
    tax_exemption = await crud.get_tax_exemption_by_id(session, tax_exemption_id)
    if not tax_exemption:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tax exemption with ID {tax_exemption_id} not found",
        )

    return tax_exemption


TaxExemptionByIdDep = Annotated[TaxExemption, Depends(get_tax_exemption_by_id)]
