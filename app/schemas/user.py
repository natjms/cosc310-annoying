from pydantic import BaseModel
from ulid import ULID

from app.models import User


class BaseUserRequest(BaseModel):
    pass


class PatchUserRequest(BaseModel):
    id: str | None = None


class PostUserRequest(BaseUserRequest):
    pass

    
class UserResponse(BaseUserRequest):
    id: ULID

    def __init__(self, user: User):
            pass  # Create from restaurant instance.
