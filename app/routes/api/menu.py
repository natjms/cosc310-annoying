from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Response, status
from pydantic import BaseModel

import app.services.menu as service
from app.auth import guard_authorization
from app.exceptions import MissingValueException
from app.models.menu import Menu, PatchMenuRequest, PostMenuRequest
from app.models.menu_item import PatchMenuItemRequest
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
    request: PostMenuRequest, response: Response, x_token: Annotated[str, Header()]
) -> Menu:
    """
    Post a menu given.

    Args:
        request: The menu data needed for the post request. See PostMenuRequest model

    Returns:
        The created menu.
    """
    guard_authorization(x_token, {"restaurateur"})

    try:
        restaurant = find_restaurant_by_id(request.restaurant_id)
        response.status_code = status.HTTP_201_CREATED
        return create_menu(restaurant.id, request.name)
    except UniqueError:
        raise HTTPException(status_code=404, detail="Restaurant not found.")


@router.get("/{menu_id}", summary="get a menu by id")
def get_menu_by_id(menu_id: str) -> Menu:
    try:
        return service.get_menu_by_id(menu_id)
    except MissingValueError:
        raise HTTPException(status_code=404, detail="menu not found")


@router.patch("/{menu_id}", summary="update a menu by id")
def patch_menu(
    menu_id: str, request: PatchMenuRequest, x_token: Annotated[str, Header()]
) -> Menu:
    guard_authorization(x_token, {"restaurateur"})
    try:
        return service.update_menu(menu_id, request.model_dump(exclude_unset=True))
    except MissingValueError:
        raise HTTPException(status_code=404, detail="menu not found")


@router.delete("/{menu_id}", summary="delete a menu by id")
def delete_menu(menu_id: str, x_token: Annotated[str, Header()]) -> None:
    guard_authorization(x_token, {"restaurateur"})
    try:
        service.delete_menu(None, menu_id)
    except MissingValueException:
        raise HTTPException(status_code=404, detail="menu not found")
