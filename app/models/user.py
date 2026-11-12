from pydantic import BaseModel
from ulid import ULID


class User(BaseModel):
    id: ULID
