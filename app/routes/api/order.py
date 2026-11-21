from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from ulid import ULID

from app.auth import guard_authorization
from app.exceptions import MissingValueException
from app.models.order import Order
from app.models.session import Session
from app.models.user import User
from app.services import order as service
from app.services.utils import maybe_ulid

router = APIRouter()


def get_current_user(x_token: Annotated[str, Header()]) -> User:
    # ugly hack
    auth = guard_authorization(x_token, {"customer", "restaurateur", "admin"})
    return auth[0]


@router.get(
    "/orders/",
    summary="Returns the current active orders for the current user",
    response_model=list[Order],
)
def get_all_orders(user: User = Depends(get_current_user)) -> list[Order]:
    """
    Retrieve what from who.

    Args:
        arg1: what it does

    Returns:
        what?
    """
    try:
        return service.get_all_orders(user.id)
    except MissingValueException:
        raise HTTPException(status_code=404, detail="missing value")


@router.post(
    "/orders/",
    summary="Creates order for the current user",
    response_model=Order,
)
def create_order(restaurant_id: str, user: User = Depends(get_current_user)):
    try:
        return service.create_order_from_cart(user.id, maybe_ulid(restaurant_id))
    except MissingValueException:
        raise HTTPException(status_code=400, detail="bad request")


@router.get(
    "/orders/{order_id}",
    summary="Returns a single order by id for the current user",
    response_model=Order,
)
def get_order_by_id(order_id: str, user: User = Depends(get_current_user)):
    try:
        return service.get_order_by_id(user.id, maybe_ulid(order_id))
    except MissingValueException:
        raise HTTPException(status_code=404, detail="bad request")


# STUB STUB STUB
@router.patch(
    "/orders/{order_id}",
    summary="Updates a single order by id for the current user",
    response_model=Order,
)
def update_order_by_id(order_id: str, user: User = Depends(get_current_user)):
    try:
        return service.update_order(user.id, maybe_ulid(order_id), status="preparing")
    except MissingValueException:
        raise HTTPException(status_code=404, detail="missing value")


@router.post(
    "/orders/{order_id}/cancel",
    summary="Cancels a single order by id for the current user",
    response_model=Order,
)
def cancel_order_by_id(order_id: str, user: User = Depends(get_current_user)):
    try:
        return service.cancel_order(user.id, maybe_ulid(order_id))
    except MissingValueException:
        raise HTTPException(status_code=404, detail="missing value")
