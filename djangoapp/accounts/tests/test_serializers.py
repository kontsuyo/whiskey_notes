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
def test_register_serializer_valid_data(user_payload):
    user_payload["password_confirm"] = user_payload["password"]
    serializer = RegisterSerializer(data=user_payload)
    assert serializer.is_valid()
    logger.info(f"serializer.data:           {serializer.data}")
    logger.info(f"serializer.validated_data: {serializer.validated_data}")
    user_create = serializer.create(validated_data=serializer.validated_data)
    assert user_create.username == user_payload["username"]
    assert user_create.check_password(user_payload["password"])
    assert user_create.email == user_payload["email"]


@pytest.mark.django_db
def test_register_serializer_password_mismatch(user_payload):
    user_payload["password_confirm"] = "different_password"
    serializer = RegisterSerializer(data=user_payload)
    assert not serializer.is_valid()
    assert "Passwords do not match" in str(serializer.errors)


@pytest.mark.django_db
def test_user_update_serializer(user_payload):
    # password mismatch
    user_payload["password_confirm"] = "different_password"
    serializer_update = UserUpdateSerializer(data=user_payload)
    assert not serializer_update.is_valid()
    logger.info(f"serializer.errors: {serializer_update.errors}")
    assert "Passwords do not match" in str(serializer_update.errors)

    # password & password_confirm are write only
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

    # update user details
    assert serializer_update.data["username"] == update_data["username"]
    assert serializer_update.data["email"] == update_data["email"]
