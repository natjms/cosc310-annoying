from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import BaseModel
from ulid import ULID

from app.exceptions import MissingValueException
from app.models.order import Order
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


@router.get(
    "/orders/",
    summary="Returns the current active order for the current user",
    response_model=Order,
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
        return service.get_active_order(user.id)
    except MissingValueException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post(
    "/orders/",
    summary="Creates order for the current user",
    response_model=Order,
)
def order():
    pass


@router.get(
    "/orders/{id}",
    summary="Returns a single order by id for the current user",
    response_model=Order,
)
def order():
    pass


@router.patch(
    "/orders/{id}",
    summary="Updates a single order by id for the current user",
    response_model=Order,
)
def order():
    pass


@router.post(
    "/orders/{id}/cancel",
    summary="Deletes a single order by id for the current user",
    response_model=Order,
)
def order():
    pass
