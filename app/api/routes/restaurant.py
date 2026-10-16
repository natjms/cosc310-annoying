from fastapi import APIRouter, HTTPException

from app.exceptions import MissingValueException
from app.models import Restaurant
from app.services import restaurant as service


NOT_FOUND_STATUS = 404


router = APIRouter()


@router.get(
    "/restaurants",
    summary="Get a list of all restaurants.",
    response_model=list[Restaurant],
)
def get_all_restaurants() -> list[Restaurant]:
    return service.get_all_restaurants()


@router.get(
    "/restaurants/{restaurant_id}",
    summary="Get a specific restaurant using its ID.",
    response_model=Restaurant,
)
def get_restaurant_by_id(restaurant_id: str) -> Restaurant:
    try:
        return service.get_restaurant_by_id(restaurant_id)
    except MissingValueException:
        raise HTTPException(status_code=NOT_FOUND_STATUS)
