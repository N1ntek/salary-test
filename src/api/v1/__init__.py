from fastapi import APIRouter

from .salary.router import router as salary_router
from .taxes.router import router as taxes_router
from .exemptions.router import router as exemptions_router

router = APIRouter(prefix="/v1")

router.include_router(salary_router)
router.include_router(taxes_router)
router.include_router(exemptions_router)
