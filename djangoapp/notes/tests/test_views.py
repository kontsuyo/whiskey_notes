import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import CustomUser
from notes.models import Whiskey


@pytest.mark.django_db
class TestWhiskeyList:
    def setup_method(self):
        self.url = reverse("whiskey-list")

    def test_unauthenticated_user_can_not_create_whiskey_object(self):
        data = {
            "name": "タリスカー",
            "country": "SC",
            "alcohol": 45.8,
            "cask": "バーボン樽",
            "price": "4700円くらい",
        }
        client = APIClient()
        response = client.post(self.url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN  # type:ignore


@pytest.mark.django_db
class TestWhiskeyDetail:
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
        response = self.client.post(reverse("whiskey-list"), data)
        assert response.status_code == status.HTTP_201_CREATED  # type:ignore

        self.whiskey = Whiskey.objects.get(name="タリスカー")
        self.detail_url = reverse(
            "whiskey-detail", kwargs={"pk": self.whiskey.id}  # type: ignore
        )

    def test_only_user_created_whiskey_object_can_update_it(self):
        another_user = APIClient()
        another_user.force_authenticate(
            user=CustomUser.objects.create_user(username="another", password="password")
        )

        update_data = {"name": "タリスカー１０年"}

        response = another_user.put(self.detail_url, update_data)
        assert response.status_code == status.HTTP_403_FORBIDDEN  # type: ignore

        response = self.client.put(self.detail_url, update_data)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_202_ACCEPTED]  # type: ignore
