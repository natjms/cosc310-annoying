from ulid import ULID
import bcrypt

from app.models.user import User
from app.models.role import RoleName
from app.repositories.user import users
from app.repositories.repo import UniqueError
from app.services import role as role_service
from app.exceptions import MissingValueException, ResourceConflictException, AuthorizationException

def find_user_by_id(user_id: ULID | str) -> User:
    try:
        return users.unique(id=user_id)
    except UniqueError:
        raise MissingValueException("Given user does not exist")

def find_user_by_username(username: str) -> User:
    try:
        return users.unique(username=username)
    except UniqueError:
        raise MissingValueException("Given username does not match any user")

def find_user_by_email(email: str) -> User:
    try:
        return users.unique(email=email)
    except UniqueError:
        raise MissingValueException("Given email does not match any user")

def find_user_by_credential(username_or_email: str) -> User:
    try:
        return find_user_by_username(username_or_email)
    except MissingValueException:
        try:
            return find_user_by_email(username_or_email)
        except MissingValueException:
            raise MissingValueException("Given username or email does not match any user")

def _check_for_conflicts(username: str | None = None, email: str | None = None) -> None:
    user = None
    try:
        if username is not None:
            user = find_user_by_username(username)
    except MissingValueException:
        pass

    try:
        if email is not None:
            user = find_user_by_email(email)
    except MissingValueException:
        pass

    if user is not None:
        raise ResourceConflictException("The given username or email is already in use")


def register_user(
    username: str,
    email: str,
    password_plaintext: str,
    role = None,
    dangerously_set_password_hash: str = None
) -> User:
    _check_for_conflicts(username, email)

    if role is not None:
        if role not in {RoleName.restaurateur, RoleName.customer}:
            raise AuthorizationException('You can only enroll as a customer or restaurateur')

    if dangerously_set_password_hash is None:
        password_hash = bcrypt.hashpw(password_plaintext.encode("utf-8"), bcrypt.gensalt())
    else:
        password_hash = dangerously_set_password_hash

    user = users.create(username=username, email=email, password_hash=password_hash, is_active=True)

    if role is not None:
        role_service.assign_role(user.id, role)

    return user

def update_user(user_id: ULID, change_set: dict) -> User:
    user = find_user_by_id(user_id)
    change_set = {k: v for k, v in change_set.items() if v is not None}
    _check_for_conflicts(username=change_set.get('username'), email=change_set.get('email'))

    if 'password_plaintext' in change_set:
        password_hash = bcrypt.hashpw(change_set['password_plaintext'].encode("utf-8"), bcrypt.gensalt())
        del change_set['password_plaintext']
        change_set['password_hash'] = password_hash

    users.update(id=user.id, **change_set)
    return find_user_by_id(user_id)

def validate_credentials(username_or_email: str, password_plaintext: str) -> bool:
    user = find_user_by_credential(username_or_email)
    return bcrypt.checkpw(password_plaintext.encode('utf-8'), user.password_hash)

def delete_user(user_id: ULID) -> None:
    find_user_by_id(user_id)
    users.delete(id=user_id)

def deactivate_user(user_id: ULID) -> None:
    find_user_by_id(user_id)
    users.update(id=user_id, is_active=False)
