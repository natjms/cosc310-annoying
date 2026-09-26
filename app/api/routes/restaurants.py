from json import load
from fastapi import APIRouter
from app.schemas.restaurant import Restaurant


RESTAURANTS_FILEPATH = "data/restaurants.json"


restaurant_router = APIRouter()

@restaurant_router.get(
    "/restaurants",
    summary="Get a list of all restaurants.",
    response_model=list[Restaurant]
)
def get_restaurants() -> list[Restaurant]:
    with open(RESTAURANTS_FILEPATH) as file:
        data = load(file)

    return [Restaurant(**restaurant) for restaurant in data]
