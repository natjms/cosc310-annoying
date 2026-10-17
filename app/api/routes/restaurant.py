from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.repositories.repo import UniqueError
from app.models.user import User
from app.services.user import find_user_by_id
from app.models.restaurant import Restaurant
from app.services.restaurant import list_all_restaurants, find_restaurant_by_id, create_restaurant, search_restaurants, update_restaurant
from app.models.menu import Menu
from app.services.menu import list_restaurant_menus, create_menu

restaurant_router = APIRouter()

@restaurant_router.get(
    "/restaurant",
    summary="Returns a list of all restaurants",
    response_model=list[Restaurant],
)
def get_restaurant() -> list[Restaurant]:
    return list_all_restaurants()
    
@restaurant_router_get(
    "/restaurant/search",
    summary="Search restaurants by name",
    response_model=list[Restaurant],
)
def search_restaurant_endpoint(query: str) -> list[Restaurant]:
    return search_restaurants(query)

@restaurant_router.get(
    "/restaurant/{restaurant_id}",
    summary="Returns the restaurant with the given ID",
    response_model=Restaurant,
)
def get_restaurant_id(restaurant_id: str) -> Restaurant:
    try:
        return find_restaurant_by_id(restaurant_id)
    except UniqueError:
        raise HTTPException(status_code=404, detail="Restaurant not found")

class RestaurantUpdateRequest(BaseModel):
    name: str | None = None 
    description: str | None = None
    phone_number: str | None = None

@restaurant_router.put(
    f"/restaurant/{restaurant_id}",
    summary="Updates a restaurant",
    response_model=Restaurant,
)

def put_restaurant(restaurant_id: str, request: RestaurantUpdateRequest)-> Restaurant:
    update_data = {k: v for k, v in request.model_dump().items() if v is not None}
    try:
        return update_restaurant(restaurant_id,update_data)
    except UniqueError:
        raise HTTPException(status_code=404,detail="Restaurant does not exist")

    }
@restaurant_router.get(
    "/restaurant/{restaurant_id}/menu",
    summary="Returns the menus for the given restaurant",
    response_model=list[Menu],
)
def get_restaurant_id_menu(restaurant_id: str) -> list[Menu]:
    try:
        restaurant = find_restaurant_by_id(restaurant_id) # assert restaurant exists
        return list_restaurant_menus(restaurant.id) # then return the menus
        # possibly also check if the restaurant is active?
    except UniqueError:
        raise HTTPException(status_code=404, detail="Restaurant is nonexistent")

class RestaurantCreateRequest(BaseModel):
    owner_id: str
    name: str

@restaurant_router.post(
    "/restaurant",
    summary="Creates a new restaurant",
    response_model=Restaurant,
)
def post_restaurant(request: RestaurantCreateRequest) -> Restaurant:
    try:
        owner = find_user_by_id(request.owner_id)
    except UniqueError:
        raise HTTPException(status_code=400, detail="Owner is nonexistent")
    return create_restaurant(owner.id, request.name)

class MenuCreateRequest(BaseModel):
    name: str

@restaurant_router.post(
    "/restaurant/{restaurant_id}/menu",
    summary="Creates a new menu for the given restaurant",
    response_model=Menu,
)
def post_restaurant_id_menu(restaurant_id: str, request: MenuCreateRequest) -> Menu:
    try:
        restaurant = find_restaurant_by_id(restaurant_id) # assert restaurant exists
        return create_menu(restaurant.id, request.name)
    except UniqueError:
        raise HTTPException(status_code=404, detail="Restaurant not found.")
