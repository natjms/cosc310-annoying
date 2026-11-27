from typing import Annotated

from fastapi import Header, HTTPException

import app.services.role as role_service
import app.services.session as session_service
import app.services.user as user_service
from app.exceptions import MissingValueException
from app.models.role import RoleName


def guard_authentication(x_token: str):
    try:
        session = session_service.find_session(x_token)
    except MissingValueException:
        raise HTTPException(
            status_code=401, detail="Session not found. Please try logging in again"
        )

    if not session_service.session_is_valid(session.token):
        session_service.log_out(session.token)
        raise HTTPException(
            status_code=401,
            detail="Your session has expired. Please try logging in again",
        )

    user = user_service.find_user_by_id(session.user_id)

    return (user, session)


def guard_authorization(x_token: str, required_roles: set[RoleName]) -> list[RoleName]:
    """
    Function invoked at the start of a route function to ensure only
    authenticated users with one of a set of roles can access it

    - Raises an HTTPException with status code 403 if the user lacks any of the
      expected roles
    - Raises an HTTPException if the user is unauthenticated (see
      `app.services.session.guard_authentication` for more information)
    """
    (user, session) = guard_authentication(x_token)

    if not role_service.user_has_any_roles_of(user.id, required_roles):
        allowed_roles = ", ".join(required_roles)
        raise HTTPException(
            status_code=403,
            detail=f"Only the following kinds of users can do this: {', '.join(required_roles)}",
        )

    return (user, role_service.find_user_roles(user.id), session)
