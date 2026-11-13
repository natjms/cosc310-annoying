from ulid import ULID

from app.schemas.user import User
from app.repositories.user import users


class UserService:
    def __init__(self, repository: Repo[User]) -> None:
        self.repository = repository

    def get_user_by_id(self, user_id: ULID | str) -> User:
        return self.repository.unique(id=user_id)

    def create_user(self) -> User:
        return self.repository.create()
