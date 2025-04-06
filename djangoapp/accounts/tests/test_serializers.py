import logging

import pytest
from django.contrib.auth import get_user_model

from accounts.serializers import TastingNoteUserSerializer

UserModel = get_user_model()
logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_validate_data_at_create_user(user_payload):
    serializer = TastingNoteUserSerializer(data=user_payload)
    assert serializer.is_valid()
    logger.info(f"serializer.data:           {serializer.data}")
    logger.info(f"serializer.validated_data: {serializer.validated_data}")
    user_create = serializer.create(validated_data=serializer.validated_data)
    assert user_create.username == user_payload["username"]
    assert user_create.check_password(user_payload["password"])
    assert user_create.email == user_payload["email"]


@pytest.mark.django_db
def test_password_is_write_only_field(user_payload):
    serializer = TastingNoteUserSerializer(data=user_payload)
    assert serializer.is_valid()
    logger.info(serializer.data)
    assert "password" not in serializer.data
