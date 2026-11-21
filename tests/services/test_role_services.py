import pytest
from ulid import ULID

from app.models import RoleName
from app.repositories import roles as role_repository
from app.repositories import users as user_repository
from app.services import user as user_service
from app.services.role import *


@pytest.fixture
def test_data():
    user = user_service.register_user("test", "test@example.com", "password")

    yield (user,)

    user_repository.delete_all()
    role_repository.delete_all()

@pytest.mark.parametrize(
    "role_name",
    [r for r in RoleName]
)
def test_assign_and_revoke_role(role_name, test_data):
    (user,) = test_data

    assert not user_has_role(user.id, role_name)

    assign_role(user.id, role_name)
    assert user_has_role(user.id, role_name)

    revoke_role(user.id, role_name)
    assert not user_has_role(user.id, role_name)

def test_double_assign_role_is_idempotent(test_data):
    (user,) = test_data

    assign_role(user.id, RoleName.customer)
    assign_role(user.id, RoleName.customer)
    roles = find_user_roles(user.id)

    assert len([r for r in roles if r == RoleName.customer]) == 1

def test_revoke_without_role_does_nothing(test_data):
    (user,) = test_data

    assert len(find_user_roles(user.id)) == 0
    revoke_role(user.id, RoleName.customer)
    assert len(find_user_roles(user.id)) == 0

def test_at_least_one_matching_role(test_data):
    (user,) = test_data
    assert not user_has_any_roles_of(user.id, {RoleName.customer, RoleName.admin})

    assign_role(user.id, RoleName.customer)
    assert user_has_any_roles_of(user.id, {RoleName.customer})
    assert user_has_any_roles_of(user.id, {RoleName.customer, RoleName.admin})

    assign_role(user.id, RoleName.admin)
    assert user_has_any_roles_of(user.id, {RoleName.customer, RoleName.admin})

def test_has_all_required_roles(test_data):
    (user,) = test_data

    assert not user_has_all_roles_of(user.id, {RoleName.customer, RoleName.admin})

    assign_role(user.id, RoleName.customer)
    assert user_has_all_roles_of(user.id, {RoleName.customer})
    assert not user_has_all_roles_of(user.id, {RoleName.customer, RoleName.admin})

    assign_role(user.id, RoleName.admin)
    assert user_has_all_roles_of(user.id, {RoleName.customer})
    assert user_has_all_roles_of(user.id, {RoleName.customer, RoleName.admin})

def test_has_all_empty_list_is_invalid():
    with pytest.raises(ValueError):
        user_has_all_roles_of(ULID(), set())

def test_has_any_empty_list_is_invalid():
    with pytest.raises(ValueError):
        user_has_any_roles_of(ULID(), set())
