from fastapi import APIRouter, HTTPException, status

from app.exceptions import MissingValueException
from app.repositories.repo import UniqueError
from app.schemas import UserResponse
from app.services import UserService


router = APIRouter()
service = UserService()


@router.get(
    "/user/{user_id}",
    summary="Returns a user by ID",
    response_model=UserResponse
)
def get_user_by_id(user_id: str) -> UserResponse:
    """
    Retrieve a specific user by ID.

    Args:
        user_id: The ID of the user.

    Returns:
        A single user.
    """
    try:
        return service.get_user_by_id(user_id)
    except MissingValueException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.post(
    "/user",
    summary="Creates a new user",
    response_model=UserResponse
)
def post_user() -> UserResponse:
    """
    Create a user.

    Returns:
        A single user.
    """
    return service.create_user()
