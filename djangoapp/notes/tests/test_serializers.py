from unittest.mock import Mock

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Whisky
from notes.serializers import TastingNoteSerializer, WhiskySerializer

User = get_user_model()


@pytest.mark.django_db
class TestWhiskySerializer:
    def setup_method(self):
        self.user = User.objects.create_user(username="testuser")
        self.whiskey = Whisky.objects.create(
            name="タリスカー",
            country="SC",
            alcohol=45.6,
            cask="バーボン樽",
            price="4500",
            owner=self.user,
        )

    def test_owner_field(self):
        serializer = WhiskySerializer(self.whiskey, context={"request": None})
        assert serializer.data["owner"] == self.user.username

    def test_url_field(self):
        serializer = WhiskySerializer(self.whiskey, context={"request": None})
        expected_url = reverse(
            "whisky-detail",
            kwargs={"pk": self.whiskey.id},  # type: ignore
        )
        assert serializer.data["url"] == expected_url


@pytest.mark.django_db
def test_tasting_note_serializer_valid_user():
    user1 = User.objects.create(username="user1")
    whisky = Whisky.objects.create(name="山崎１２年", owner=user1)

    serializer = TastingNoteSerializer(
        data={"whisky": whisky.id, "note": "うまい！"},  # type: ignore
        context={"request": Mock(user=user1)},
    )

    assert serializer.is_valid()


@pytest.mark.django_db
def test_tasting_note_serializer_invalid_user():
    user1 = User.objects.create(username="user1")
    user2 = User.objects.create(username="user2")
    whisky = Whisky.objects.create(name="山崎１２年", owner=user1)

    serializer = TastingNoteSerializer(
        data={"whisky": whisky.id, "note": "うまい！"},  # type: ignore
        context={"request": Mock(user=user2)},
    )

    assert not serializer.is_valid()
    assert "whisky" in serializer.errors
