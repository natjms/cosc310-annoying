from typing import Annotated

from pydantic import BaseModel, AfterValidator, BaseModel
from ulid import ULID

import app.validators as v

class User(BaseModel):
    id: ULID
    username: str
    email: str
    password_hash: bytes
    is_active: bool

class UserResponse(BaseModel):
    id: ULID
    username: str
    email: str

class PostUserRequest(BaseModel):
    username: Annotated[str, AfterValidator(v.is_username)]
    email: Annotated[str, AfterValidator(v.is_email)]
    password_plaintext: Annotated[str, AfterValidator(v.password_is_strong)]

class PatchUserRequest(BaseModel):
    username: Annotated[str | None, AfterValidator(v.is_username)] = None
    email: Annotated[str | None, AfterValidator(v.is_email)] = None
    password_plaintext: Annotated[str | None, AfterValidator(v.password_is_strong)] = None
