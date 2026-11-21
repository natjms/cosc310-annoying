from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
from ulid import ULID

from app.exceptions import MissingValueException
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.session import Session
from app.models.user import User
from app.repositories import utils
from app.services import cart as service
from app.services.session import guard_authentication
from app.services.utils import maybe_ulid

router = APIRouter()


def get_current_user(
    auth: tuple[User, Session] = Depends(guard_authentication),
) -> User:
    return auth[0]


# nts: does the thing below work for using the given user (which in turn is passed by something else)
# or are we relying on a session variable that holds the current active user?


@router.get(
    "/carts/",
    summary="Returns the current active cart for the curent user",
    response_model=Cart,
)
def get_active_cart(user: User = Depends(get_current_user)) -> Cart:
    """
    Retrieve what from who.

    Args:
        arg1: what it does

    Returns:
        what?
    """
    try:
        return service.get_active_cart(user.id)
    except MissingValueException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch(
    "/carts/",
    summary="Updates current active cart for the current user",
    response_model=Cart,
)
def update_current_cart(
    menu_item_id: str, quantity: int, user: User = Depends(get_current_user)
) -> Cart:
    """
    Retrieve what from who.

    Args:
        arg1: what it does

    Returns:
        what?
    """
    try:
        active_cart = service.get_active_cart(user.id)
        return service.update_cart_item(
            user.id, active_cart.restaurant_id, maybe_ulid(menu_item_id), quantity
        )
    except MissingValueException:
        raise HTTPException(status_code=404, detail="missing value")


@router.delete(
    "/carts/",
    summary="Clears the current active cart for the current restaurant",
    response_model=Cart,
)
def clear_active_cart(user: User = Depends(get_current_user)) -> Cart:
    """
    Retrieve what from who.

    Args:
        arg1: what it does

    Returns:
        what?
    """
    try:
        active_cart = service.get_active_cart(user.id)
        return service.clear_cart(user.id, active_cart.restaurant_id)
    except MissingValueException:
        raise HTTPException(status_code=404, detail="missing value")


@router.get(
    "/carts/{restaurant_id}",
    summary="Returns the cart items for the given restaurant",
    response_model=Cart,
)
def get_cart(restaurant_id: ULID, user: User = Depends(get_current_user)) -> Cart:
    """
    Retrieve what from who.

    Args:
        arg1: what it does

    Returns:
        what?
    """
    return service.get_or_create_cart(user.id, maybe_ulid(restaurant_id))


# nts: how many carts can be *active* at a time?
# current assumption -> nuke all other is_active for the carts to false to activate just one
@router.post(
    "/carts/{restaurant_id}/activate",
    summary="Activates a cart for the given restaurant",
    response_model=Cart,
)
def activate_cart(restaurant_id: str, user: User = Depends(get_current_user)) -> Cart:
    """
    Activate a cart while deactivating all other ones.

    Args:
        TBD.
    Returns:
        TBD.
    """
    return service.activate_cart(
        user.id, maybe_ulid(restaurant_id)
    )  # nts: this is not in the service layer yet


@router.patch(
    "/carts/{restaurant_id}",
    summary="Updates the cart items for the given restaurant",
    response_model=Cart,
)
def update_cart(
    restaurant_id: str,
    menu_item_id: str,
    quantity: int,
    user: User = Depends(get_current_user),
) -> Cart:
    """
    Retrieve what from who.

    Args:
        arg1: what it does

    Returns:
        what?
    """

    try:
        return service.update_cart_item(
            user.id, maybe_ulid(restaurant_id), maybe_ulid(menu_item_id), quantity
        )
    except MissingValueException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete(
    "/carts/{restaurant_id}",
    summary="Deletes the cart for the given restaurant",
    response_model=Cart,
)
def clear_cart(restaurant_id: str, user: User = Depends(get_current_user)) -> Cart:
    """
    Retrieve what from who.

    Args:
        arg1: what it does

    Returns:
        what?
    """
    return service.clear_cart(user.id, maybe_ulid(restaurant_id))
