from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status

from app.exceptions import MissingRecordException, NotOwnerException
from app.schemas import PatchRestaurantRequest, PostRestaurantRequest, RestaurantResponse
from app.services import RestaurantService


PREFIX = "/restaurants"


def get_restaurant_service() -> RestaurantService:
    return RestaurantService()


def get_session_service() -> SessionService:
    return SessionService()


restaurant_service_dependency = Depends(get_restaurant_service)
RestaurantServiceDependency = Annotated[RestaurantService, restaurant_service_dependency]

session_service_dependency = Depends(get_session_service)
SessionServiceDependency = Annotated[SessionService, session_service_dependency]

router = APIRouter(prefix=PREFIX)


@router.post(
    "",
    summary="Creates a new restaurant",
    status_code=status.HTTP_201_CREATED,
)
def post_restaurant(
        request: Request,
        payload: PostRestaurantRequest,
        restaurant_service: RestaurantServiceDependency,
        session_service: SessionServiceDependency,
    ) -> RestaurantResponse:
    user_id = session_service.get_requester_id(request)

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")
    
    keyword_arguments = payload.model_dump()

    restaurant = restaurant_service.create_restaurant(user_id=user_id, **keyword_arguments)

    return RestaurantResponse(restaurant)


@router.get("", summary="Returns a list of all restaurants")
def get_all_restaurants(service: RestaurantServiceDependency) -> list[RestaurantResponse]:
    restaurants = service.get_all_restaurants()

    return [RestaurantResponse(restaurant) for restaurant in restaurants]


@router.get("/search", summary="Search restaurants by name")
def search_restaurants(query: str, service: RestaurantServiceDependency) -> list[RestaurantResponse]:  # This is declared before /{restaurant_id} because otherwise the router would attempt to process /search as an ID.
    restaurants = service.search_restaurants(query)

    return [RestaurantResponse(restaurant) for restaurant in restaurants]


@router.get("/{restaurant_id}", summary="Returns the restaurant with the given ID")
def get_restaurant_by_id(restaurant_id: str, service: RestaurantServiceDependency) -> RestaurantResponse:
    try:
        restaurant = service.get_restaurant_by_id(restaurant_id)
    except MissingRecordException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

    return RestaurantResponse(restaurant)


@router.patch("/{restaurant_id}", summary="Updates a restaurant")
def patch_restaurant(
        restaurant_id: str,
        request: Request,
        payload: PatchRestaurantRequest,
        session_service: SessionServiceDependency,
        restaurant_service: RestaurantServiceDependency,
    )-> RestaurantResponse:
    user_id = session_service.get_requester_id(request)

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")

    keyword_arguments = payload.model_dump(exclude_unset=True)

    try:
        restaurant = restaurant_service.update_restaurant(
            id=restaurant_id,
            user_id=user_id,
            **keyword_arguments,
        )
    except MissingRecordException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except NotOwnerException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)

    return RestaurantResponse(restaurant)


@router.delete("/{restaurant_id}", summary="Deletes a restaurant")
def delete_restaurant(
        restaurant_id: str,
        request: Request,
        session_service: SessionServiceDependency,
        restaurant_service: RestaurantServiceDependency,
    ) -> RestaurantResponse:
    user_id = session_service.get_requester_id(request)

    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated.")

    try:
        restaurant = restaurant_service.delete_restaurant_by_id(id=restaurant_id, user_id=user_id)
    except MissingRecordException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    except NotOwnerException as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=e.message)

    return RestaurantResponse(restaurant)
