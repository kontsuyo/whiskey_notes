import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import CustomUser
from notes.models import Whisky

User = get_user_model()


@pytest.mark.django_db
class TestWhiskyList:
    def setup_method(self):
        self.url = reverse("whiskies-list")

    def test_unauthenticated_user_can_not_create_whisky_object(self):
        data = {
            "name": "タリスカー",
            "country": "SC",
            "alcohol": 45.8,
            "cask": "バーボン樽",
            "price": "4700円くらい",
        }
        client = APIClient()
        response = client.post(self.url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED  # type:ignore


@pytest.mark.django_db
class TestWhiskyDetail:
    def setup_method(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(
            username="testuser", password="password"
        )

        self.client.force_authenticate(user=self.user)
        data = {
            "name": "タリスカー",
            "country": "SC",
            "alcohol": 45.8,
            "cask": "バーボン樽",
            "price": "4700円くらい",
        }
        response = self.client.post(reverse("whiskies-list"), data)
        assert response.status_code == status.HTTP_201_CREATED  # type:ignore

        self.whisky = Whisky.objects.get(name="タリスカー")
        self.detail_url = reverse(
            "whisky-detail", kwargs={"pk": self.whisky.id}  # type: ignore
        )

    def test_only_user_created_whisky_object_can_update_it(self):
        another_user = APIClient()
        another_user.force_authenticate(
            user=CustomUser.objects.create_user(username="another", password="password")
        )

        update_data = {"name": "タリスカー１０年"}

        response = another_user.put(self.detail_url, update_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN  # type: ignore

        response = self.client.put(self.detail_url, update_data)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_202_ACCEPTED]  # type: ignore


@pytest.mark.django_db
def test_tastingnote_owner_is_request_user():
    api_client = APIClient()
    user = User.objects.create_user(username="testuser", password="password")
    whisky = Whisky.objects.create(name="Sample Whisky", owner=user)

    api_client.force_authenticate(user=user)
    url = reverse("tastingnote-list")
    data = {"whisky": whisky.id, "note": "フルーティでおいしい"}  # type: ignore

    response = api_client.post(url, data)

    assert response.data["owner"] == user.username  # type: ignore
