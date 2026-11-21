from pydantic import BaseModel
from ulid import ULID

from app.models.role import RoleName
from app.models.user import UserResponse


class Session(BaseModel):
    id: ULID
    user_id: ULID
    token: str
    expiry_timestamp_utc: int


class SessionResponse(BaseModel):
    token: str
    expiry_timestamp_utc: int
    user: UserResponse
    roles: set[RoleName]


class PostSessionRequest(BaseModel):
    username_or_email: str
    password_plaintext: str
