from fastapi import APIRouter, HTTPException

from app.repositories.repo import UniqueError
from app.models.user import User
from app.services.user import find_user_by_id, create_user

user_router = APIRouter()

@user_router.get(
    "/user/{user_id}",
    summary="Returns a user by ID",
)
def get_user(user_id: str) -> User:
    try:
        return find_user_by_id(user_id)
    except UniqueError:
        raise HTTPException(status_code=400)

@user_router.post(
    "/user",
    summary="Creates a new user",
)
def post_user() -> User:
    return create_user()
