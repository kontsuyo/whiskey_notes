import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

UserModel = get_user_model()


@pytest.mark.django_db
class TestUserRegistration:
    def test_register_user_successfully(self):
        data = {
            "username": "testuser",
            "password": "password",
        }
        register_url = reverse("register-user")

        client = APIClient()
        response = client.post(register_url, data)
        assert response.status_code == status.HTTP_201_CREATED  # type: ignore
        assert UserModel.objects.filter(username="testuser").exists()

    def test_register_user_without_username(self):
        data = {
            "username": "",
            "password": "password",
        }
        register_url = reverse("register-user")

        client = APIClient()
        response = client.post(register_url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_register_user_without_password(self):
        data = {
            "username": "testuser",
            "password": "",
        }
        register_url = reverse("register-user")

        client = APIClient()
        response = client.post(register_url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
