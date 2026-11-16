from fastapi import APIRouter, HTTPException, Response, status
from pydantic import BaseModel
from ulid import ULID

from app.exceptions import MissingValueException
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.repositories import utils
from app.services import cart as service

router = APIRouter()

# nts: have no wired up the user account system at all yet!!


# nts: does the thing below work for using the given user (which in turn is passed by something else)
# or are we relying on a session variable that holds the current active user?


@router.get(
    "/carts/",
    summary="Returns the current active cart for the curent user",
    response_model=Cart,
)
def get_active_cart(user_id: ULID) -> Cart:
    """
    Retrieve what from who.

    Args:
        arg1: what it does

    Returns:
        what?
    """
    pass


@router.patch(
    "/carts/",
    summary="Updates current active cart for the current user",
    response_model=Cart,
)
def update_current_cart(user_id: ULID):
    """
    Retrieve what from who.

    Args:
        arg1: what it does

    Returns:
        what?
    """
    pass


@router.delete(
    "/carts/",
    summary="Clears the current active cart for the current restaurant",
    response_model=Cart,
)
def clear_active_cart(user_id: ULID) -> Cart:
    """
    Retrieve what from who.

    Args:
        arg1: what it does

    Returns:
        what?
    """
    pass


@router.get(
    "/carts/{restaurant_id}",
    summary="Returns the cart items for the given restaurant",
    response_model=Cart,
)
def get_cart(restaurant_id: ULID, user_id: ULID):
    """
    Retrieve what from who.

    Args:
        arg1: what it does

    Returns:
        what?
    """
    pass


# nts: how many carts can be *active* at a time?
# current assumption -> nuke all other is_active for the carts to false to activate just one
@router.post(
    "/carts/{restaurant_id}/activate",
    summary="Activates a cart for the given restaurant",
    response_model=Cart,
)
def activate_cart(user_id: ULID, restaurant_id: str):
    """
    Activate a cart while deactivating all other ones.

    Args:
        TBD.
    Returns:
        TBD.
    """
    pass


@router.patch(
    "/carts/{restaurant_id}",
    summary="Updates the cart items for the given restaurant",
    response_model=Cart,
)
def update_cart(restaurant_id: str, menu_item_id: str, quantity: int, user_id: ULID):
    """
    Retrieve what from who.

    Args:
        arg1: what it does

    Returns:
        what?
    """

    # try
    # service.add_item_to_cart
    # except MissingValue

    pass


@router.delete(
    "/carts/{restaurant_id}",
    summary="Deletes the cart for the given restaurant",
    response_model=Cart,
)
def clear_cart(restaurant_id: str, user_id: ULID) -> Cart:
    """
    Retrieve what from who.

    Args:
        arg1: what it does

    Returns:
        what?
    """
    # return service.clear_cart(user_id,restaurant_id)
    pass
