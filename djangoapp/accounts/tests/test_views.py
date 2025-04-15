import logging

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()
logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_register_user(api_client, user_payload):
    # register new user
    response_register = api_client.post(
        reverse("register-user"), user_payload, format="json"
    )
    assert response_register.status_code == status.HTTP_201_CREATED
    assert "user" in response_register.data
    assert response_register.data["user"]["username"] == user_payload["username"]

    # missing fields
    response_register = api_client.post(
        reverse("register-user"), {"username": "testuser"}, format="json"
    )
    assert response_register.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response_register.data
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
    assert response_register.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response_register.data


@pytest.mark.django_db
def test_login_user(api_client, user):
    # login with valid credentials
    response_login = api_client.post(
        reverse("login-user"),
        {"username": user.username, "password": "password"},
        format="json",
    )
    logger.info(f"response_login: {response_login.data}")
    assert response_login.status_code == status.HTTP_200_OK
    assert "token" in response_login.data


@pytest.mark.django_db
def test_update_user(api_client, user):
    # update user details
    api_client.force_authenticate(user=user)
    update_data = {
        "username": "updateduser",
        "password": "newpassword123",
        "password_confirm": "newpassword123",
        "email": "new-email@sample.com",
    }
    response_update = api_client.patch(
        reverse("user-update", kwargs={"username": user.username}),
        update_data,
        format="json",
    )
    logger.info(f"response_update: {response_update.data}")
    assert response_update.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.check_password(update_data["password"])

    # user not found
    response_update = api_client.patch(
        reverse("user-update", kwargs={"username": "nonexistentuser"}),
        update_data,
        format="json",
    )
    assert response_update.status_code == status.HTTP_404_NOT_FOUND
    assert response_update.data["error"] == "User not found"
    logger.info(f"response_update: {response_update.data}")
