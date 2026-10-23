from fastapi import APIRouter

from .health import health_router
from .user import user_router
from .restaurant import restaurant_router
from .menu_item import menu_item_router


PREFIX = "/api"


api_router = APIRouter(prefix=PREFIX)

api_router.include_router(user_router)
api_router.include_router(restaurant_router)
api_router.include_router(menu_item_router)
