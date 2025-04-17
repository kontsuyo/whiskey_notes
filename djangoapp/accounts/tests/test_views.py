import logging

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

User = get_user_model()
logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_register_new_user(api_client, user_payload):
    # register new user
    response_register = api_client.post(
        reverse("register-user"), user_payload, format="json"
    )
    assert response_register.status_code == status.HTTP_201_CREATED
    assert "user" in response_register.data
    assert response_register.data["user"]["username"] == user_payload["username"]


@pytest.mark.django_db
def test_register_user_with_invalid_data(api_client):
    # missing fields
    response_register = api_client.post(
        reverse("register-user"), {"username": "testuser"}, format="json"
    )
    assert response_register.status_code == status.HTTP_400_BAD_REQUEST
    assert "password" in response_register.data
    assert "email" in response_register.data


@pytest.mark.django_db
def test_register_user_with_invalid_email(api_client):
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
def test_login_user_with_valid_credentials(api_client, user):
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
def test_logout_user(api_client, user):
    # logout user
    api_client.force_authenticate(user=user)
    response_logout = api_client.post(reverse("logout-user"), format="json")
    assert response_logout.status_code == status.HTTP_200_OK
    assert response_logout.data["message"] == "User logged out successfully"


@pytest.mark.django_db
def test_logout_user_without_authentication(api_client):
    # logout without authentication
    response_logout = api_client.post(reverse("logout-user"), format="json")
    assert response_logout.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_get_user_details(api_client, user):
    # get user details
    response_detail = api_client.get(
        reverse("user-detail", kwargs={"username": user.username}),
        format="json",
    )
    logger.info(f"response_detail: {response_detail.data}")
    assert response_detail.status_code == status.HTTP_200_OK
    assert response_detail.data["user"]["username"] == user.username


@pytest.mark.django_db
def test_update_user_details(api_client, user, update_data):
    # update user details
    api_client.force_authenticate(user=user)
    response_update = api_client.patch(
        reverse("user-update", kwargs={"username": user.username}),
        update_data,
        format="json",
    )
    logger.info(f"response_update: {response_update.data}")
    assert response_update.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.check_password(update_data["password"])


@pytest.mark.django_db
def test_update_user_without_authentication(api_client, update_data):
    response_update = api_client.patch(
        reverse("user-update", kwargs={"username": "unauthenticateduser"}),
        update_data,
        format="json",
    )
    assert response_update.status_code == status.HTTP_401_UNAUTHORIZED
    logger.info(f"response_update: {response_update.data}")


@pytest.mark.django_db
def test_delete_user(api_client, user):
    # delete user
    api_client.force_authenticate(user=user)
    response_delete = api_client.delete(
        reverse("user-delete", kwargs={"username": user.username}),
        format="json",
    )
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_user_without_authentication(api_client, user):
    # delete user without authentication
    response_delete = api_client.delete(
        reverse("user-delete", kwargs={"username": user.username}),
        format="json",
    )
    assert response_delete.status_code == status.HTTP_401_UNAUTHORIZED
    logger.info(f"response_delete: {response_delete.data}")


@pytest.mark.django_db
def test_delete_user_by_another_user(api_client, user, another_user):
    # delete user by another user
    api_client.force_authenticate(user=another_user)
    response_delete = api_client.delete(
        reverse("user-delete", kwargs={"username": user.username}),
        format="json",
    )
    assert response_delete.status_code == status.HTTP_403_FORBIDDEN
    logger.info(f"response_delete: {response_delete.data}")
