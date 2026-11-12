from ulid import ULID

from app.models.user import User
from app.repositories.user import users


def find_user_by_id(user_id: ULID | str) -> User:
    return users.unique(id=user_id)


def create_user() -> User:
    return users.create()


def delete_user(user_id: ULID | str) -> None:
    users.delete(id=user_id)
