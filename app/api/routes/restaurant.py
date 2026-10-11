from fastapi import APIRouter
from app.schemas.restaurant import Restaurant
from app.repositories.restaurant import load_restaurants

restaurant_router = APIRouter()

@restaurant_router.get(
    "/restaurants",
    summary="Get a list of all restaurants.",
    response_model=list[Restaurant]
)
def get_restaurants() -> list[Restaurant]:
    return load_restaurants()
