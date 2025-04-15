import logging

import pytest
from django.contrib.auth import get_user_model

from accounts.serializers import (
    CustomUserSerializer,
    RegisterSerializer,
    UserUpdateSerializer,
)

UserModel = get_user_model()
logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_password_is_write_only_field(user_payload):
    serializer = CustomUserSerializer(data=user_payload)
    assert serializer.is_valid()
    logger.info(serializer.data)
    assert "password" not in serializer.data


@pytest.mark.django_db
def test_register_serializer_password_and_password_confirm_are_write_only(user_payload):
    serializer_register = RegisterSerializer(data=user_payload)
    assert serializer_register.is_valid()
    assert "password" not in serializer_register.data
    assert "password_confirm" not in serializer_register.data


@pytest.mark.django_db
def test_register_serializer_password_mismatch(user_payload):
    user_payload["password_confirm"] = "different_password"
    serializer_register = RegisterSerializer(data=user_payload)
    assert not serializer_register.is_valid()
    assert "Passwords do not match" in str(serializer_register.errors)
    logger.info("password mismatch")
    logger.info(f"serializer.errors: {serializer_register.errors}")


@pytest.mark.django_db
def test_register_serializer_create_user(user_payload):
    serializer_register = RegisterSerializer(data=user_payload)
    assert serializer_register.is_valid()
    user = serializer_register.save()
    assert user.username == user_payload["username"]
    assert user.email == user_payload["email"]
    assert user.check_password(user_payload["password"])
    logger.info("User created successfully")


@pytest.mark.django_db
def test_user_update_serializer_password_and_password_confirm_are_write_only():
    update_data = {
        "username": "updateduser",
        "password": "newpassword123",
        "password_confirm": "newpassword123",
        "email": "new-email@sample.com",
    }
    serializer_update = UserUpdateSerializer(data=update_data)
    assert serializer_update.is_valid()
    logger.info(serializer_update.data)
    assert "password" not in serializer_update.data
    assert "password_confirm" not in serializer_update.data


@pytest.mark.django_db
def test_user_update_serializer_password_mismatch(user_payload):
    user_payload["password_confirm"] = "different_password"
    serializer_update = UserUpdateSerializer(data=user_payload)
    assert not serializer_update.is_valid()
    logger.info(f"serializer.errors: {serializer_update.errors}")
    assert "Passwords do not match" in str(serializer_update.errors)


@pytest.mark.django_db
def test_user_update_serializer_update_user(user):
    update_data = {
        "username": "updateduser",
        "password": "newpassword123",
        "password_confirm": "newpassword123",
        "email": "new-email@sample.com",
    }
    serializer_update = UserUpdateSerializer(instance=user, data=update_data)
    assert serializer_update.is_valid()
    user_update = serializer_update.save()
    assert user_update.username == update_data["username"]
    assert user_update.email == update_data["email"]
    assert user_update.check_password(update_data["password"])
