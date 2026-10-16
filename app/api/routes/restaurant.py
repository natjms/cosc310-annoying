from fastapi import APIRouter, HTTPException

from app.schemas.restaurant import Restaurant
from app.services.restaurant import get_all_restaurants, get_restaurant_by_id

restaurant_router = APIRouter()


@restaurant_router.get(
    "/restaurants",
    summary="Get a list of all restaurants.",
    response_model=list[Restaurant],
)
def get_restaurants() -> list[Restaurant]:
    return get_all_restaurants()


@restaurant_router.get(
    "/restaurants/{restaurant_id}",
    summary="Get a specific restaurant using its ID.",
    response_model=Restaurant,
)
def get_restaurant(restaurant_id: str) -> Restaurant:
    try:
        return get_restaurant_by_id(restaurant_id)
    except ValueError as e:
        raise HTTPException(status_code=404)
