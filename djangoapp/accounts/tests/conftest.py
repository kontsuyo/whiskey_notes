import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser",
        password="password",
        email="test@sample.com",
    )


@pytest.fixture
def another_user():
    return User.objects.create_user(
        username="anotheruser",
        password="password",
        email="another@sample.com",
    )


@pytest.fixture
def api_client():
    yield APIClient()


@pytest.fixture
def user_payload():
    return {
        "username": "testuser",
        "password": "password1234",
        "password_confirm": "password1234",
        "email": "test@sample.com",
    }


@pytest.fixture
def update_data():
    return {
        "username": "updateduser",
        "password": "newpassword123",
        "password_confirm": "newpassword123",
        "email": "new-email@sample.com",
    }


something = {
    "username": "fuga",
    "password": "fuga",
    "password_confirm": "fuga",
    "email": "something@sample.com",
}
