from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel

from app.exceptions import MissingValueError
from app.models.menu import Menu, PostMenuRequest
from app.models.restaurant import (
    PatchRestaurantRequest,
    PostRestaurantRequest,
    Restaurant,
)
from app.models.user import User
from app.repositories.repo import UniqueError
from app.services.menu import create_menu, list_restaurant_menus
from app.services.restaurant import (
    create_restaurant,
    find_restaurant_by_id,
    list_all_restaurants,
    search_restaurants,
    update_restaurant,
)
from app.services.user import find_user_by_id

router = APIRouter(prefix="/menus")


@router.get(
    "/",
    summary="Returns the menus for the given restaurant",
)
def get_all_menus_by_restaurant_id(restaurant: str) -> list[Menu]:
    """Retrieve all menus from a given restaurant.

    Args:
        restaurant: The ID of the restaurant.

    Returns:
        A list of restaurant menus.

    """
    try:
        restaurant_record = find_restaurant_by_id(restaurant)
        return list_restaurant_menus(restaurant_record.id)
        # TODO: possibly also check if the restaurant is active?
    except UniqueError:
        raise HTTPException(status_code=404, detail="Restaurant is nonexistent")


@router.post(
    "/",
    summary="Creates a new menu for the given restaurant",
)
def post_menu(restaurant_id: str, request: PostMenuRequest) -> Menu:
    """Post a menu given.

    Args:
        request: The menu data needed for the post request. See PostMenuRequest model

    Returns:
        The created menu.

    """
    try:
        restaurant = find_restaurant_by_id(request.restaurant_id)
        return create_menu(restaurant.id, request.name)
    except UniqueError:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
