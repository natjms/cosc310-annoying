import pytest
from pydantic import ValidationError
from ulid import ULID
from app.models.user import User

def test_user_valid():
    user_id = ULID()
    user = User(id=user_id, username="test", email="test@example.com", password_hash="valid bcrypt hash")
    assert user.id == user_id

def test_user_missing_id():
    with pytest.raises(ValidationError):
        User()
