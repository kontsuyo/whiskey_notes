import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

User = get_user_model()


@pytest.mark.django_db
class TestUserAuthentication:
    def test_authenticate_user_successfully(self):
        data = {"username": "testuser", "password": "secure-password"}
        client = APIClient()
        client.post(reverse("register-user"), data)

        assert User.objects.filter(username="testuser").exists()

        response = client.post(
            reverse("auth-token"),
            {"username": "testuser", "password": "secure-password"},
        )
        assert response.status_code == status.HTTP_200_OK  # type: ignore

    def test_authenticate_user_with_wrong_username(self):
        data = {"username": "testuser", "password": "secure-password"}
        client = APIClient()
        client.post(reverse("register-user"), data)

        assert User.objects.filter(username="testuser").exists()

        response = client.post(
            reverse("auth-token"),
            {"username": "testuser2", "password": "secure-password"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore

    def test_authenticate_user_with_wrong_password(self):
        data = {"username": "testuser", "password": "secure-password"}
        client = APIClient()
        client.post(reverse("register-user"), data)

        assert User.objects.filter(username="testuser").exists()

        response = client.post(
            reverse("auth-token"),
            {"username": "testuser", "password": "secure_password"},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
