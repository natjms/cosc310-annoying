from fastapi import APIRouter, HTTPException, Request, Response, Header, status
from typing import Annotated
from ulid import ULID

from app.exceptions import MissingValueException, AuthenticationException
from app.models.session import SessionResponse, PostSessionRequest
from app.models.user import UserResponse
from app.services.user import find_user_by_id
from app.services.session import log_in, log_out
from app.services.role import find_user_roles
from app.auth import guard_authentication

router = APIRouter(prefix="/auth")

@router.post(
    "/login",
    summary="Log in, creating a session token"
)
def post_login(payload: PostSessionRequest, response: Response) -> SessionResponse:
    try:
        session = log_in(payload.username_or_email, payload.password_plaintext)
        response.status_code = status.HTTP_200_OK
        return SessionResponse(
            **session.model_dump(),
            user=UserResponse(**find_user_by_id(session.user_id).model_dump()),
            roles=find_user_roles(session.user_id)
        )
    except AuthenticationException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)

@router.post(
    "/logout",
    summary="Log out, removing the session"
)
def post_logout(
    response: Response, 
    x_token: Annotated[str, Header()]
) -> None:
    (_, session) = guard_authentication(x_token)
    try:
        log_out(session.token)
    except MissingValueException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.message)
