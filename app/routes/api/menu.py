from fastapi import APIRouter, HTTPException, Response, status, Header
from pydantic import BaseModel
from typing import Annotated

from app.repositories.repo import UniqueError
from app.exceptions import MissingValueException
from app.models.user import User
from app.services.user import find_user_by_id
from app.models.restaurant import PatchRestaurantRequest, PostRestaurantRequest, Restaurant
from app.services.restaurant import list_all_restaurants, find_restaurant_by_id, create_restaurant, search_restaurants, update_restaurant
from app.models.menu import Menu, PostMenuRequest
from app.services.menu import list_restaurant_menus, create_menu
from app.auth import guard_authorization


router = APIRouter(prefix="/menus")


@router.get(
    "/",
    summary="Returns the menus for the given restaurant",
    response_model=list[Menu],
)
def get_all_menus_by_restaurant_id(restaurant: str) -> list[Menu]:
    """
    Retrieve all menus from a given restaurant.

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
    response_model=Menu,
)
def post_menu(
    request: PostMenuRequest,
    response: Response,
    x_token: Annotated[str, Header()]
) -> Menu:
    """
    Post a menu given.

    Args:
        request: The menu data needed for the post request. See PostMenuRequest model

    Returns:
        The created menu.
    """
    guard_authorization(x_token, {'restaurateur'})

    try:
        restaurant = find_restaurant_by_id(request.restaurant_id)
        response.status_code = status.HTTP_201_CREATED
        return create_menu(restaurant.id, request.name)
    except UniqueError:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
