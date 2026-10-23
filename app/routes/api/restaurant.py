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
    "/restaurant",
    summary="Returns a list of all restaurants",
    response_model=list[Restaurant],
)
def get_all_restaurants() -> list[Restaurant]:
    """
    Retrieve all restaurants.

    Returns:
        A list of all restaurants.
    """
    return list_all_restaurants()


@router.get(
    "/restaurant/search",
    summary="Search restaurants by name",
    response_model=list[Restaurant],
)
def search_restaurants(query: str) -> list[Restaurant]:
    """
    Filter for restaurants by name.

    Args:
        query: The name of the restaurant you are looking for.

    Returns:
        A list of matching restaurants.
    """
    return search_restaurants(query)


@router.get(
    "/restaurant/{restaurant_id}",
    summary="Returns the restaurant with the given ID",
    response_model=Restaurant,
)
def get_restaurant_by_id(restaurant_id: str) -> Restaurant:
    """
    Retrieve a restaurant by ID.

    Args:
        restaurant_id: The ID of the restaurant.

    Returns:
        A single restaurant.
    """
    try:
        return find_restaurant_by_id(restaurant_id)
    except MissingValueException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.patch(
    "/restaurant/{restaurant_id}",
    summary="Updates a restaurant",
    response_model=Restaurant,
)
def patch_restaurant(restaurant_id: str, request: PatchRestaurantRequest)-> Restaurant:
    try:
        return update_restaurant(restaurant_id, request.model_dump())
    except UniqueError:
        raise HTTPException(status_code=404, detail="Restaurant does not exist")
    except MissingValueException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post(
    "/restaurant",
    summary="Creates a new restaurant",
    response_model=Restaurant,
)
def post_restaurant(request: PostRestaurantRequest, response: Response) -> Restaurant:
    """
    Post a restaurant.

    Args:
        request: The restaurant data needed for the post request.

    Returns:
        The created restaurant.
    """
    try:
        new_restaurant = create_restaurant(request.owner_id, request.name)
        response.status_code = status.HTTP_201_CREATED
        return new_restaurant
    except MissingValueException as e:
        raise HTTPException(status_code=404, detail=e.message)
