from fastapi import APIRouter, HTTPException

from app.repositories.repo import UniqueError
from app.models.user import User
from app.services.user import find_user_by_id, create_user


user_router = APIRouter()


@user_router.get(
    "/user/{user_id}",
    summary="Returns a user by ID",
)
def get_user_by_id(user_id: str) -> User:
    """
    Retrieve a specific user by ID.

    Args:
        user_id: The ID of the user.

    Returns:
        A single user.
    """
    try:
        return find_user_by_id(user_id)
    except UniqueError:
        raise HTTPException(status_code=400)


@user_router.post(
    "/user",
    summary="Creates a new user",
)
def post_user() -> User:
    """
    Create a user.

    Returns:
        A single user.
    """
    return create_user()
