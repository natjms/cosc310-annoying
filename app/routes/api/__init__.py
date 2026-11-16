from fastapi import APIRouter

from .user import router as user_router
from .auth import router as auth_router
from .restaurant import router as restaurant_router
from .menu import router as menu_router
from .menu_item import router as menu_item_router
from .cart import router as cart_router
from .menu import router as menu_router
# why was the menu router not here before?
from .order import router as order_router

PREFIX = "/api"


api_router = APIRouter(prefix=PREFIX)

api_router.include_router(user_router)
api_router.include_router(auth_router)
api_router.include_router(restaurant_router)
api_router.include_router(menu_router)
api_router.include_router(menu_item_router)
api_router.include_router(cart_router)
api_router.include_router(menu_router)
api_router.include_router(order_router)
