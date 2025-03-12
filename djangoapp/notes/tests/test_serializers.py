import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Whiskey
from notes.serializers import WhiskeySerializer

User = get_user_model()


@pytest.mark.django_db
class TestWhiskeySerializer:
    def setup_method(self):
        self.user = User.objects.create_user(username="testuser")
        self.whiskey = Whiskey.objects.create(
            name="タリスカー",
            country="SC",
            alcohol=45.6,
            cask="バーボン樽",
            price="4500",
            owner=self.user,
        )

    def test_owner_field(self):
        serializer = WhiskeySerializer(self.whiskey, context={"request": None})
        assert serializer.data["owner"] == self.user.username

    def test_url_field(self):
        serializer = WhiskeySerializer(self.whiskey, context={"request": None})
        expected_url = reverse(
            "whiskey-detail",
            kwargs={"pk": self.whiskey.id},  # type: ignore
        )
        assert serializer.data["url"] == expected_url
