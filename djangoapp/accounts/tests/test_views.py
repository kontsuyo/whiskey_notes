import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()


@pytest.mark.django_db
def test_register_user(api_client, user_payload):
    # register new user
    response_register = api_client.post(
        reverse("register-user"), user_payload, format="json"
    )
    assert response_register.status_code == status.HTTP_201_CREATED  # type: ignore
    assert "user" in response_register.data  # type: ignore
    assert response_register.data["user"]["username"] == user_payload["username"]  # type: ignore

    # missing fields
    response_register = api_client.post(
        reverse("register-user"), {"username": "testuser"}, format="json"
    )
    assert response_register.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
    assert "password" in response_register.data  # type: ignore
    assert "email" in response_register.data

    # invalid email
    response_register = api_client.post(
        reverse("register-user"),
        {
            "username": "testuser",
            "password": "strongpassword123",
            "email": "invalid-email",
        },
        format="json",
    )
    assert response_register.status_code == status.HTTP_400_BAD_REQUEST  # type: ignore
    assert "email" in response_register.data  # type: ignore
