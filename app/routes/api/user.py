from typing import Annotated

from fastapi import APIRouter, Header, HTTPException, Request, Response, status
from ulid import ULID
from app.exceptions import MissingValueException, ResourceConflictException
from app.models.user import User, UserResponse, PostUserRequest, PatchUserRequest
from app.models.role import RoleName
from app.services.user import find_user_by_id, register_user, update_user, deactivate_user
from app.auth import guard_authorization, guard_authentication

from app.auth import guard_authentication, guard_authorization
from app.exceptions import MissingValueError, ResourceConflictError
from app.models.user import PatchUserRequest, PostUserRequest, User, UserResponse
from app.services.user import (
    deactivate_user,
    find_user_by_id,
    register_user,
    update_user,
)

router = APIRouter(prefix="/users")


@router.get(
    "/{user_id}",
    summary="Returns a user by ID",
)
def get_user_by_id(user_id: ULID, x_token: Annotated[str, Header()]) -> UserResponse:
    """Retrieve a specific user by ID.

    Args:
        user_id: The ID of the user.

    Returns:
        A single user.

    """
    (user, _) = guard_authentication(x_token)
    if user.id != user_id:
        guard_authorization(x_token, {"admin"})

    try:
        return UserResponse(**find_user_by_id(user_id).model_dump())
    except MissingValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

@router.post(
    "/",
    summary="Register a user"
)
def create_user(payload: PostUserRequest, response: Response, role: RoleName | None = None) -> UserResponse:
    try:
        new_user = register_user(**payload.model_dump(), role=role)
        response.status_code = status.HTTP_201_CREATED
        return UserResponse(**new_user.model_dump())
    except ResourceConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)


@router.patch("/{user_id}", summary="Update a user")
def patch_user(
    payload: PatchUserRequest,
    user_id: ULID,
    response: Response,
    x_token: Annotated[str, Header()],
) -> UserResponse:
    (user, _) = guard_authentication(x_token)
    if user.id != user_id:
        guard_authorization(x_token, {"admin"})

    try:
        updated_user = update_user(user_id, change_set=payload.model_dump())
        response.status_code = status.HTTP_200_OK
        return UserResponse(**updated_user.model_dump())
    except ResourceConflictError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.message)
    except MissingValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)


@router.delete(
    "/{user_id}",
    summary="Deactivate a user, such that you can no longer log in as them",
)
def deactivate_user_request(
    user_id: ULID, response: Response, x_token: Annotated[str, Header()]
) -> None:
    (user, _) = guard_authentication(x_token)
    if user.id != user_id:
        guard_authorization(x_token, {"admin"})

    try:
        deactivate_user(user_id)
        response.status_code = status.HTTP_204_NO_CONTENT
    except MissingValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
