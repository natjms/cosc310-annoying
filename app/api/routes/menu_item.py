from fastapi import APIRouter, HTTPException

from app.exceptions import MissingValueException
from app.models import MenuItem
from app.services import menu_item as service


NOT_FOUND_STATUS = 404


menu_item_router = APIRouter()


@menu_item_router.get(
    "/restaurants/{restaurant_id}/menus/{menu_id}/items/",
    summary="Get all menu item by restaurant ID and menu ID.",
    response_model=list[MenuItem],
)
def get_all_menu_items(restaurant_id: str, menu_id: str) -> list[MenuItem]:
    try:
        return service.get_all_menu_items(restaurant_id, menu_id)
    except MissingValueException:
        raise HTTPException(status_code=NOT_FOUND_STATUS)


@menu_item_router.get(
    "/restaurants/{restaurant_id}/menus/{menu_id}/items/{menu_item_id}",
    summary="Get a menu item by restaurant ID, menu ID and menu item ID.",
    response_model=MenuItem,
)
def get_menu_item_by_id(
    restaurant_id: str,
    menu_id: str,
    menu_item_id: str,
) -> MenuItem:
    try:
        return service.get_menu_item_by_id(
            restaurant_id,
            menu_id,
            menu_item_id,
        )
    except MissingValueException:
        raise HTTPException(status_code=NOT_FOUND_STATUS)
