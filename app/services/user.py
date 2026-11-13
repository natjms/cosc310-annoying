from ulid import ULID
import bcrypt

from app.models.user import User
from app.repositories.user import users
from app.repositories.repo import UniqueError
from app.exceptions import MissingValueException, ResourceConflictException

def find_user_by_id(user_id: ULID | str) -> User:
    return users.unique(id=user_id)

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

def register_user(username: str, email: str, password_plaintext: str) -> User:
    user = None
    try:
        user = find_user_by_email(email)
    except MissingValueException:
        pass

    try:
        user = find_user_by_username(username)
    except MissingValueException:
        pass

    if user is not None:
        raise ResourceConflictException("The given username or email is already in use")

    password_hash = bcrypt.hashpw(password_plaintext.encode("utf-8"), bcrypt.gensalt())

    return users.create(username=username, email=email, password_hash=password_hash)

def validate_credentials(username_or_email: str, password_plaintext: str) -> bool:
    user = find_user_by_credential(username_or_email)
    return bcrypt.checkpw(password_plaintext.encode('utf-8'), user.password_hash)

def delete_user(user_id: ULID | str) -> None:
	users.delete(id=user_id)
