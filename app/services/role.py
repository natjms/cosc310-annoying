from fastapi import HTTPException, Request
from ulid import ULID

from app.exceptions import MissingValueException
from app.models import Role, RoleName
from app.repositories import roles
from app.repositories.repo import UniqueError
from app.services import user as user_service


def assign_role(user_id: ULID, role: RoleName) -> None:
    """Grants a user a role if they don't already have it; otherwise, does nothing.
    Raises MissingValueException if the user doesn't exist.
    """
    if user_has_role(user_id, role):
        return

    roles.create(user_id=user_id, role=role)


def revoke_role(user_id: ULID, role: RoleName) -> None:
    """Revokes a user's role if they have it; otherwise, does nothing. Raises
    MissingValueException if the user doesn't exist.
    """
    if not user_has_role(user_id, role):
        return

    role_record = roles.unique(user_id=user_id, role=role)
    roles.delete(id=role_record.id)


def find_user_roles(user_id: ULID) -> set[RoleName]:
    """Returns a set of roles possessed by a user. Raises MissingValueException if
    the user doesn't exist.
    """
    user = user_service.find_user_by_id(user_id)
    user_roles = roles.select(user_id=user_id)
    return set(r.role for r in user_roles)


def user_has_role(user_id: ULID, role: RoleName) -> bool:
    """Returns true if the given role is possessed by the given user. Raises
    MissingValueException if the user doesn't exist.
    """
    return role in find_user_roles(user_id)


def user_has_any_roles_of(user_id: ULID, roles: set[RoleName]) -> bool:
    """Returns true if the user has at least one of the roles in the given set of
    role requirements.

    - Raises MissingValueException if the user doesn't exist
    - Raises ValueError if the role requirement set is empty
    """
    if len(roles) == 0:
        raise ValueError("At least one role must be provided for authorization")

    return len(roles.intersection(find_user_roles(user_id))) >= 1


def user_has_all_roles_of(user_id: ULID, roles: set[RoleName]) -> bool:
    """Returns true if the user has at least one of the roles in the given set of
    role requirements.

    - Raises MissingValueException if the user doesn't exist
    - Raises ValueError if the role requirement set is empty
    """
    if len(roles) == 0:
        raise ValueError("At least one role must be provided for authorization")

    return len(roles.intersection(find_user_roles(user_id))) == len(roles)
