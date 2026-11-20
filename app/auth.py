from fastapi import HTTPException, Request
from app.exceptions import MissingValueException
import app.services.session as session_service
import app.services.role as role_service
import app.services.user as user_service
from app.models.role import RoleName

def guard_authentication(request: Request):
    if "authorization" not in request.headers:
        raise HTTPException(status_code=401, detail="Session token not provided")

    # e.g. Authorization: Bearer 056b322f90557e6796d4d76de5227d90...
    try:
        auth_scheme, session_token = request.headers["authorization"].split(" ")
    except ValueError:
        # Will occur if the header looks like "Authorization: 056b322f90557e6796d4d76de5227d90..."
        # which is an incorrect use of the Authorization header
        raise HTTPException(status_code=422, detail="Invalid Authorization header")

    if auth_scheme != "Bearer":
        raise HTTPException(status_code=422, detail="Only the Bearer authentication scheme is supported")

    try:
        session = session_service.find_session(session_token)
    except MissingValueException:
        raise HTTPException(status_code=401, detail="Session not found. Please try logging in again")

    if not session_service.session_is_valid(session.token):
        session.log_out(session.token)
        raise HTTPException(status_code=401, detail="Your session has expired. Please try logging in again")

    user = user_service.find_user_by_id(session.user_id)

    return (user, session)

def guard_authorization(request: Request, required_roles: set[RoleName]) -> list[RoleName]:
    """
    Function invoked at the start of a route function to ensure only
    authenticated users with one of a set of roles can access it

    - Raises an HTTPException with status code 403 if the user lacks any of the
      expected roles
    - Raises an HTTPException if the user is unauthenticated (see
      `app.services.session.guard_authentication` for more information)
    """
    (user, session) = guard_authentication(request)

    if not role_service.user_has_any_roles_of(user.id, required_roles):
        raise HTTPException(
            status_code=403,
            detail=f"Only the following kinds of users can do this: {', '.join(required_roles)}"
        )

    return (user, role_service.find_user_roles(user.id), session)
