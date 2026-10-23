import pytest
from pydantic import ValidationError
from ulid import ULID
from app.models.user import User

def test_user_valid():
    user_id = ULID()
    user = User(id=user_id)
    assert user.id == user_id

def test_user_missing_id():
 with pytest.raises(ValidationError):
     User()
