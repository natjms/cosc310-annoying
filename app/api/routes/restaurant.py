from fastapi import APIRouter, HTTPException

from app.repositories.repo import UniqueError
from app.models.restaurant import Restaurant
from app.services.restaurant import list_all_restaurants, find_restaurant_by_id, create_restaurant
from app.models.menu import Menu
from app.services.menu import list_restaurant_menus, create_menu

restaurant_router = APIRouter()

@restaurant_router.get(
    "/restaurant",
    summary="Returns a list of all restaurants",
)
def get_restaurants() -> list[Restaurant]:
    return list_all_restaurants()

@restaurant_router.get(
    "/restaurant/{restaurant_id}",
    summary="Returns the restaurant with the given ID",
)
def get_restaurant_id(restaurant_id: str) -> Restaurant:
    try:
        return find_restaurant_by_id(restaurant_id)
    except UniqueError:
        raise HTTPException(status_code=404)

@restaurant_router.get(
    "/restaurant/{restaurant_id}/menus",
    summary="Returns the menus for the given restaurant",
)
def get_restaurant_menus(restaurant_id: str) -> list[Menu]:
    try:
        restaurant = find_restaurant_by_id(restaurant_id) # assert restaurant exists
        return list_restaurant_menus(restaurant.id) # then return the menus
        # possibly also check if the restaurant is active?
    except UniqueError:
        raise HTTPException(status_code=404)

@restaurant_router.post(
    "/restaurant",
    summary="Creates a new restaurant",
)
def post_restaurant(owner_id: str, name: str) -> Restaurant:
    # TODO: check owner, implement owner, etc.
    return create_restaurant(owner_id, name)

@restaurant_router.post(
    "/restaurant/{restaurant_id}/menu",
    summary="Creates a new menu for the given restaurant",
)
def post_restaurant_menu(restaurant_id: str, name: str) -> Menu:
    try:
        restaurant = find_restaurant_by_id(restaurant_id) # assert restaurant exists
        return create_menu(restaurant.id, name)
    except UniqueError:
        raise HTTPException(status_code=404)
