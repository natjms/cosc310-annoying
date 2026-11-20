from fastapi import HTTPException, Request
from ulid import ULID

from app.repositories.repo import UniqueError
from app.exceptions import MissingValueException
from app.models import Role, RoleName
from app.repositories import roles
from app.services import session as session_service, user as user_service

def assign_role(user_id: ULID, role: RoleName) -> None:
    """
    Grants a user a role if they don't already have it; otherwise, does nothing.
    Raises MissingValueException if the user doesn't exist
    """

    if user_has_role(user_id, role):
        return

    roles.create(user_id=user_id, role=role)

def revoke_role(user_id: ULID, role: RoleName) -> None:
    """
    Revokes a user's role if they have it; otherwise, does nothing. Raises
    MissingValueException if the user doesn't exist
    """

    if not user_has_role(user_id, role):
        return

    role_record = roles.unique(user_id=user_id, role=role)
    roles.delete(id=role_record.id)

def find_user_roles(user_id: ULID) -> set[RoleName]:
    """
    Returns a set of roles possessed by a user. Raises MissingValueException if
    the user doesn't exist
    """

    user = user_service.find_user_by_id(user_id)
    user_roles = roles.select(user_id=user_id)
    return set(r.role for r in user_roles)

def user_has_role(user_id: ULID, role: RoleName) -> bool:
    """
    Returns true if the given role is possessed by the given user. Raises
    MissingValueException if the user doesn't exist
    """

    return role in find_user_roles(user_id)

def user_has_any_roles_of(user_id: ULID, roles: set[RoleName]) -> bool:
    """
    Returns true if the user has at least one of the roles in the given set of
    role requirements.

    - Raises MissingValueException if the user doesn't exist
    - Raises ValueError if the role requirement set is empty
    """

    if len(roles) == 0:
        raise ValueError('At least one role must be provided for authorization')

    return len(roles.intersection(find_user_roles(user_id))) >= 1

def user_has_all_roles_of(user_id: ULID, roles: set[RoleName]) -> bool:
    """
    Returns true if the user has at least one of the roles in the given set of
    role requirements.

    - Raises MissingValueException if the user doesn't exist
    - Raises ValueError if the role requirement set is empty
    """

    if len(roles) == 0:
        raise ValueError('At least one role must be provided for authorization')

    return len(roles.intersection(find_user_roles(user_id))) == len(roles)

def guard_authorization(request: Request, required_roles: set[RoleName]) -> list[RoleName]:
    """
    Function invoked at the start of a route function to ensure only
    authenticated users with one of a set of roles can access it

    - Raises an HTTPException with status code 403 if the user lacks any of the
      expected roles
    - Raises an HTTPException if the user is unauthenticated (see
      `app.services.session.guard_authentication` for more information)
    """
    (user, session) = session_service.guard_authentication(request)

    if not user_has_any_roles_of(user.id, required_roles):
        raise HTTPException(
            status_code=403,
            detail=f"Only the following kinds of users can do this: {', '.join(required_roles)}"
        )

    return (user, find_user_roles(user.id), session)
