from fastapi import APIRouter, HTTPException, status

from app.exceptions import BadRequestException, ForbiddenException, MissingRecordException, MissingValueException
from app.schemas.restaurant import PatchRestaurantRequest, PostRestaurantRequest, RestaurantResponse
from app.services.restaurant import RestaurantService


PREFIX = "/restaurants"


router = APIRouter(prefix=PREFIX)
service = RestaurantService()  # Need to find a way to inject this dependency. RestaurantRouter object? Passing a service as an argument to route functions is bad because FastAPI expects all parameters to be parameters found in the request.

user_id = "NOT A REAL USER ID"  # TODO WARNING This is temporary. We need some kind of session middleware to get the user ID from something like session.user_id. In the meantime, use this temporary value.


@router.get("", summary="Returns a list of all restaurants")
def get_all_restaurants() -> list[RestaurantResponse]:
    """
    Retrieve all restaurants.

    Returns:
        A list of all restaurants.
    """
    restaurants = service.get_all_restaurants()

    return [RestaurantResponse(restaurant) for restaurant in restaurants]


@router.get("/search", summary="Search restaurants by name")
def search_restaurants(query: str) -> list[RestaurantResponse]:
    """
    Filter for restaurants by name.

    Args:
        query: The name of the restaurant you are looking for.

    Returns:
        A list of matching restaurants.
    """
    restaurants = service.search_restaurants(query)

    return [RestaurantResponse(restaurant) for restaurant in restaurants]


@router.get("/{restaurant_id}", summary="Returns the restaurant with the given ID")
def get_restaurant_by_id(restaurant_id: str) -> RestaurantResponse:
    """
    Retrieve a restaurant by ID.

    Args:
        restaurant_id: The ID of the restaurant.

    Returns:
        A single restaurant.
    """
    try:
        restaurant = service.get_restaurant_by_id(restaurant_id)
    except MissingRecordException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

    return RestaurantResponse(restaurant)


@router.post(
    "",
    summary="Creates a new restaurant",
    status_code=status.HTTP_201_CREATED,
)
def post_restaurant(request: PostRestaurantRequest) -> RestaurantResponse:
    """
    Post a restaurant.

    Args:
        request: The restaurant data needed for the post request.

    Returns:
        The created restaurant.
    """
    keyword_arguments = request.model_dump()

    try:
        restaurant = service.create_restaurant(user_id=user_id, **keyword_arguments)
    except MissingRecordException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message)

    return RestaurantResponse(restaurant)


@router.patch("/{restaurant_id}", summary="Updates a restaurant")
def patch_restaurant(restaurant_id: str, request: PatchRestaurantRequest)-> RestaurantResponse:
    keyword_arguments = request.model_dump(exclude_unset=True)

    try:
        restaurant = service.update_restaurant(
            id=restaurant_id,
            user_id=user_id,
            **keyword_arguments,
        )
    except MissingRecordException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except BadRequestException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.message) 
    except ForbiddenException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)

    return RestaurantResponse(restaurant)


@router.delete("/{restaurant_id}", summary="Deletes a restaurant")
def delete_restaurant(restaurant_id: str)-> RestaurantResponse:
    try:
        restaurant = service.delete_restaurant_by_id(id=restaurant_id, user_id=user_id)
    except MissingRecordException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except ForbiddenException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)

    return RestaurantResponse(restaurant)
