from app.models.user import User
from app.repositories.repo import Repo

users = Repo("users", User, indexed_fields=[])
