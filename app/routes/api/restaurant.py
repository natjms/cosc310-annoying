from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel

from app.repositories.repo import UniqueError
from app.exceptions import MissingValueException
from app.schemas import User
from app.services.user import find_user_by_id
from app.schemas.restaurant import PatchRestaurantRequest, PostRestaurantRequest, RestaurantResponse
from app.services.restaurant import get_all_restaurants, find_restaurant_by_id, create_restaurant, search_restaurants, update_restaurant
from app.services.menu import list_restaurant_menus, create_menu


router = APIRouter()


@router.get(
    "/restaurant",
    summary="Returns a list of all restaurants",
    response_model=list[RestaurantResponse],
)
def get_all_restaurants() -> list[RestaurantResponse]:
    """
    Retrieve all restaurants.

    Returns:
        A list of all restaurants.
    """
    restaurants = get_all_restaurants()

    return [RestaurantResponse(restaurant) for restaurant in restaurants]


@router.get(
    "/restaurant/search",
    summary="Search restaurants by name",
    response_model=list[RestaurantResponse],
)
def search_restaurants(query: str) -> list[RestaurantResponse]:
    """
    Filter for restaurants by name.

    Args:
        query: The name of the restaurant you are looking for.

    Returns:
        A list of matching restaurants.
    """
    restaurants = search_restaurants(query)

    return [RestaurantResponse(restaurant) for restaurant in restaurants]


@router.get(
    "/restaurant/{restaurant_id}",
    summary="Returns the restaurant with the given ID",
    response_model=RestaurantResponse,
)
def get_restaurant_by_id(restaurant_id: str) -> RestaurantResponse:
    """
    Retrieve a restaurant by ID.

    Args:
        restaurant_id: The ID of the restaurant.

    Returns:
        A single restaurant.
    """
    try:
        restaurant = find_restaurant_by_id(restaurant_id)
        return RestaurantResponse(restaurant)
    except MissingValueException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.patch(
    "/restaurant/{restaurant_id}",
    summary="Updates a restaurant",
    response_model=RestaurantResponse,
)
def patch_restaurant(restaurant_id: str, request: PatchRestaurantRequest)-> RestaurantResponse:
    try:
        restaurant = update_restaurant(restaurant_id, request.model_dump())
        return RestaurantResponse(restaurant)
    except UniqueError:
        raise HTTPException(status_code=404, detail="Restaurant does not exist")
    except MissingValueException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.post(
    "/restaurant",
    summary="Creates a new restaurant",
    response_model=RestaurantResponse,
)
def post_restaurant(request: PostRestaurantRequest, response: Response) -> RestaurantResponse:
    """
    Post a restaurant.

    Args:
        request: The restaurant data needed for the post request.

    Returns:
        The created restaurant.
    """
    try:
        restaurant = create_restaurant(request.owner_id, request.name)
        response.status_code = status.HTTP_201_CREATED
        return RestaurantResponse(restaurant)
    except MissingValueException as e:
        raise HTTPException(status_code=404, detail=e.message)
