from fastapi import APIRouter

from .api import api_router
from .health import router as health_router


router = APIRouter()

router.include_router(api_router)
router.include_router(health_router)
