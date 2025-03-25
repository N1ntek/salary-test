from fastapi import Depends, HTTPException, Path
from typing_extensions import Annotated

from src.api.v1.taxes import crud
from src.core.database import DbSessionDep
from src.core.models import TaxRate


async def get_tax_by_id(session: DbSessionDep, tax_rate_id: Annotated[int, Path]) -> TaxRate:
    tax_rate =  await crud.get_tax_rate_by_id(session, tax_rate_id)

    if tax_rate is None:
        raise HTTPException(status_code=404, detail="Tax rate not found")
    return tax_rate


TaxByIdDep = Annotated[TaxRate, Depends(get_tax_by_id)]