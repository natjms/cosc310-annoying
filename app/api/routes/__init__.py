from fastapi import APIRouter

from .health import health_router
from .restaurant import router as restaurant_router
from .menu_item import router as menu_item_router


PREFIX = "/api"


api_router = APIRouter(prefix=PREFIX)

api_router.include_router(health_router)
api_router.include_router(restaurant_router)
api_router.include_router(menu_item_router)
