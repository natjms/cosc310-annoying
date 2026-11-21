from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel

from app.auth import get_current_user
from app.exceptions import AuthenticationError, MissingValueError
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

router = APIRouter(prefix="/restaurants")


@router.get(
    "/",
    summary="Returns a list of all restaurants",
)
def get_all_restaurants() -> list[Restaurant]:
    """Retrieve all restaurants.

    Returns:
        A list of all restaurants.

    """
    return list_all_restaurants()


@router.get(
    "/search",
    summary="Search restaurants by name",
)
def search_restaurants(query: str) -> list[Restaurant]:
    """Filter for restaurants by name.

    Args:
        query: The name of the restaurant you are looking for.

    Returns:
        A list of matching restaurants.

    """
    return search_restaurants(query)


@router.get(
    "/{restaurant_id}",
    summary="Returns the restaurant with the given ID",
)
def get_restaurant_by_id(restaurant_id: str) -> Restaurant:
    """Retrieve a restaurant by ID.

    Args:
        restaurant_id: The ID of the restaurant.

    Returns:
        A single restaurant.

    """
    try:
        return find_restaurant_by_id(restaurant_id)
    except MissingValueError:
        raise HTTPException(status_code=404, detail="restaurant not found")


@router.patch(
    "/{restaurant_id}",
    summary="Updates a restaurant",
)
def patch_restaurant(
    restaurant_id: str,
    request: PatchRestaurantRequest,
    user: Annotated[User, Depends(get_current_user)],
) -> Restaurant:
    try:
        return update_restaurant(restaurant_id, request.model_dump())
    except (UniqueError, MissingValueError):
        raise HTTPException(status_code=404, detail="restaurant does not exist")


@router.post(
    "/",
    summary="Creates a new restaurant",
)
def post_restaurant(
    request: PostRestaurantRequest,
    response: Response,
    user: Annotated[User, Depends(get_current_user)],
) -> Restaurant:
    """Post a restaurant.

    Args:
        request: The restaurant data needed for the post request.

    Returns:
        The created restaurant.

    """
    try:
        new_restaurant = create_restaurant(request.owner_id, request.name)
        response.status_code = status.HTTP_201_CREATED
        return new_restaurant
    except AuthenticationError:
        raise HTTPException(status_code=401, detail="authentication failed")
    except MissingValueError:
        raise HTTPException(status_code=404, detail="value missing")


#### ADD DELETE ENDPOINT HERE
