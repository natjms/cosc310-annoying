from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel, AfterValidator
from typing import Annotated

from app.exceptions import MissingValueException
from app.models import MenuItem
from app.models.menu_item import PatchMenuItemRequest, PostMenuItemRequest
from app.services import menu_item as service
import app.validators as v


NOT_FOUND_STATUS = 404


router = APIRouter()


@router.get(
    "/restaurants/{restaurant_id}/menus/{menu_id}/items/",
    summary="Get all menu item by restaurant ID and menu ID.",
    response_model=list[MenuItem],
)
def get_all_menu_items(restaurant_id: str, menu_id: str) -> list[MenuItem]:
    """Retrieve all menu items from a given restaurant menu.

    Args:
        restaurant_id: The ID of the restaurant.
        menu_id: The ID of the menu.

    Returns:
        A list of menu items.

    """
    try:
        return service.get_all_menu_items(restaurant_id, menu_id)
    except MissingValueException:
        raise HTTPException(status_code=NOT_FOUND_STATUS)


@router.get(
    "/restaurants/{restaurant_id}/menus/{menu_id}/items/{menu_item_id}",
    summary="Get a menu item by restaurant ID, menu ID and menu item ID.",
    response_model=MenuItem,
)
def get_menu_item_by_id(
    restaurant_id: str,
    menu_id: str,
    menu_item_id: str,
) -> MenuItem:
    """Retrieve a specific menu item by ID.

    Args:
        restaurant_id: The ID of the restaurant.
        menu_id: The ID of the menu.
        menu_item_id: The ID of the menu item.

    Returns:
        A single menu item.

    """
    try:
        return service.get_menu_item_by_id(
            restaurant_id,
            menu_id,
            menu_item_id,
        )
    except MissingValueException as e:
        raise HTTPException(status_code=NOT_FOUND_STATUS, detail=e.message)


@router.patch(
    "/restaurants/{restaurant_id}/menus/{menu_id}/items/{menu_item_id}",
    summary="Update a menu item by restaurant ID, menu ID and menu item ID.",
    response_model=MenuItem,
)
def patch_menu_item(
    restaurant_id: str,
    menu_id: str,
    menu_item_id: str,
    request: PatchMenuItemRequest
) -> MenuItem:
    """Update an existing menu ID

    Path arguments:
        restaurant_id: The ID of the restaurant.
        menu_id: The ID of the menu.
        menu_item_id: The ID of the menu item.

    Body arguments:
        name: New name for the menu item. Optional
        price: New cost of the menu item. Optional

    Returns:
        A single menu item.

    """
    try:
        return service.update_menu_item_by_id(
            restaurant_id,
            menu_id,
            menu_item_id,
            request.model_dump()
        )
    except MissingValueException as e:
        raise HTTPException(status_code=NOT_FOUND_STATUS, detail=e.message)


@router.post(
    "/restaurants/{restaurant_id}/menus/{menu_id}/items/",
    summary="Create a new menu item given the restaurant and menu ID",
    response_model=MenuItem,
)
def post_menu_item(
    restaurant_id: str,
    menu_id: str,
    request: PostMenuItemRequest,
    response: Response
) -> MenuItem:
    """Create a new menu item

    Path arguments:
        restaurant_id: The ID of the restaurant.
        menu_id: The ID of the menu.

    Body arguments:
        name: New name for the menu item. Optional
        price: New cost of the menu item. Optional

    Returns:
        A single menu item.

    """
    try:
        new_menu_item = service.create_menu_item(
            restaurant_id,
            menu_id,
            request.name,
            request.price
        )
        response.status_code = status.HTTP_201_CREATED
        return new_menu_item
    except MissingValueException:
        raise HTTPException(status_code=NOT_FOUND_STATUS)
