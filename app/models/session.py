from pydantic import BaseModel
from ulid import ULID

class Session(BaseModel):
    id: ULID
    user_id: ULID
    token: str
    expiry_timestamp_utc: int

class SessionResponse(BaseModel):
    token: str
    expiry_timestamp_utc: int

class PostSessionRequest(BaseModel):
    username_or_email: str
    password_plaintext: str
