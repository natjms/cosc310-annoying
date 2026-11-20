from pydantic import BaseModel
from ulid import ULID
from enum import StrEnum


class RoleName(StrEnum):
    admin = "admin"
    customer = "customer"
    restaurateur = "restaurateur"


class Role(BaseModel):
    id: ULID
    user_id: ULID
    role: RoleName
