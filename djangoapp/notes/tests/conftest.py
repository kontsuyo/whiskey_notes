import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from notes.models import TastingNote, Whisky

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(
        username="testuser", password="password", email="test@sample.com"
    )


@pytest.fixture
def whisky(user):
    return Whisky.objects.create(name="Sample Whisky", owner=user)


@pytest.fixture
def note(whisky, user):
    return TastingNote.objects.create(whisky=whisky, note="good!", owner=user)


@pytest.fixture
def api_client():
    yield APIClient()


@pytest.fixture
def whisky_payload():
    return {
        "name": "タリスカー１０年",
        "country": "SC",
        "alcohol": 45.8,
        "cask": "バーボン樽",
        "price": "4700円くらい",
    }


@pytest.fixture
def note_payload(whisky):
    return {
        "whisky": whisky.id,
        "note": "美味しかった。",
    }
