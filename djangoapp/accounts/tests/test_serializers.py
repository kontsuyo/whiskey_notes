import pytest
from django.contrib.auth import get_user_model

from accounts.serializers import CustomUserSerializer

UserModel = get_user_model()


@pytest.mark.django_db
class TestCustomUserSerializer:
    def test_create_user_success(self):
        data = {"username": "testuser", "password": "secure-password"}
        serializer = CustomUserSerializer(data=data)

        assert serializer.is_valid(), serializer.errors
        user = serializer.save()

        assert UserModel.objects.count() == 1
        assert user.username == data["username"]
        assert user.check_password(data["password"])

    def test_create_user_without_password(self):
        data = {"username": "testuser", "password": ""}
        serializer = CustomUserSerializer(data=data)

        assert not serializer.is_valid()
        assert "password" in serializer.errors

    def test_create_user_without_username(self):
        data = {"username": "", "password": "secure-password"}
        serializer = CustomUserSerializer(data=data)

        assert not serializer.is_valid()
        assert "username" in serializer.errors
