from fastapi import APIRouter
from pydantic import BaseModel

import app.services.menu as service
from app.schemas.menu import Menu

menu_router = APIRouter(prefix='/menu')

@menu_router.get('/{restaurant_id}', summary='Return a list of menus associated with a given restaurant')
def get_menus_for_restaurant(restaurant_id: str) -> list[Menu]:
	return service.get_restaurant_menus(restaurant_id)
