from enum import StrEnum

from pydantic import BaseModel
from ulid import ULID


class RoleName(StrEnum):
    admin = "admin"
    customer = "customer"
    restaurateur = "restaurateur"


class Role(BaseModel):
    id: ULID
    user_id: ULID
    role: RoleName
