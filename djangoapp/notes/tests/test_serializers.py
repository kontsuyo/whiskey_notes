from unittest.mock import Mock

import pytest
from django.contrib.auth import get_user_model

from notes.serializers import TastingNoteSerializer, WhiskySerializer

User = get_user_model()


@pytest.mark.django_db
def test_whisky_serializer_owner_field(user, whisky):
    serializer = WhiskySerializer(whisky, context={"request": None})
    assert serializer.data["owner"] == user.username


@pytest.mark.django_db
def test_tastingnote_serializer_owner_field(user, note):
    serializer = TastingNoteSerializer(note, context={"request": None})
    assert serializer.data["owner"] == user.username


@pytest.mark.django_db
def test_tasting_note_serializer_valid_user(user, note_payload):
    serializer = TastingNoteSerializer(
        data=note_payload,
        context={"request": Mock(user=user)},
    )
    assert serializer.is_valid()


@pytest.mark.django_db
def test_tasting_note_serializer_invalid_user(note_payload):
    another_user = User.objects.create_user(
        username="another_user", password="pass", email="test@example.com"
    )
    serializer = TastingNoteSerializer(
        data=note_payload,
        context={"request": Mock(user=another_user)},
    )
    assert not serializer.is_valid()
    assert "whisky" in serializer.errors
