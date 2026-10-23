from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel

from app.repositories.repo import UniqueError
from app.exceptions import MissingValueException
from app.models.user import User
from app.services.user import find_user_by_id
from app.models.restaurant import PatchRestaurantRequest, PostRestaurantRequest, Restaurant
from app.services.restaurant import list_all_restaurants, find_restaurant_by_id, create_restaurant, search_restaurants, update_restaurant
from app.models.menu import Menu, PostMenuRequest
from app.services.menu import list_restaurant_menus, create_menu


router = APIRouter()


@router.get(
    "/restaurant/{restaurant_id}/menu",
    summary="Returns the menus for the given restaurant",
    response_model=list[Menu],
)
def get_all_menus_by_restaurant_id(restaurant_id: str) -> list[Menu]:
    """
    Retrieve all menus from a given restaurant.

    Args:
        restaurant_id: The ID of the restaurant.

    Returns:
        A list of restaurant menus.
    """
    try:
        restaurant = find_restaurant_by_id(restaurant_id) # assert restaurant exists
        return list_restaurant_menus(restaurant.id) # then return the menus
        # possibly also check if the restaurant is active?
    except UniqueError:
        raise HTTPException(status_code=404, detail="Restaurant is nonexistent")


@router.post(
    "/restaurant/{restaurant_id}/menu",
    summary="Creates a new menu for the given restaurant",
    response_model=Menu,
)
def post_menu(restaurant_id: str, request: PostMenuRequest) -> Menu:
    """
    Post a menu given.

    Args:
        restaurant_id: The restaurant ID that the menu is being posted t/o.
        request: The menu data needed for the post request.

    Returns:
        The created menu.
    """
    
    try:
        restaurant = find_restaurant_by_id(restaurant_id) # assert restaurant exists
        return create_menu(restaurant.id, request.name)
    except UniqueError:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
