import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from notes.models import TastingNote, Whisky

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="password")


@pytest.fixture
def whisky(user):
    return Whisky.objects.create(name="Sample Whisky", owner=user)


@pytest.mark.django_db
def test_create_tasting_note(api_client, user, whisky):
    api_client.force_authenticate(user=user)
    url = reverse("tastingnote-list")
    data = {"whisky": whisky.id, "note": "フルーティでおいしい"}

    response = api_client.post(url, data)

    assert response.status_code == 201
    assert response.data["note"] == "フルーティでおいしい"


@pytest.mark.django_db
def test_create_tasting_note_without_note(api_client, user, whisky):
    api_client.force_authenticate(user=user)
    url = reverse("tastingnote-list")
    data = {"whisky": whisky.id}

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "note" in response.data


@pytest.mark.django_db
def test_create_tasting_note_without_authentication(api_client, user, whisky):
    url = reverse("tastingnote-list")
    data = {"whisky": whisky.id}

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_tasting_note(api_client, user, whisky):
    api_client.force_authenticate(user=user)
    note = TastingNote.objects.create(whisky=whisky, owner=user, note="スモーキー")
    url = reverse("tastingnote-detail", args=[note.id])  # type: ignore
    data = {"whisky": whisky.id, "note": "アップデート"}

    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_tasting_note_without_authentication(api_client, user, whisky):
    note = TastingNote.objects.create(whisky=whisky, owner=user, note="スモーキー")
    url = reverse("tastingnote-detail", args=[note.id])  # type: ignore
    data = {"whisky": whisky.id, "note": "アップデート"}

    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_other_users_tasting_note(api_client, user, whisky):
    api_client.force_authenticate(user=user)
    another_user = User.objects.create_user(username="other_user", password="password")
    another_whisky = Whisky.objects.create(name="Another Whisky", owner=another_user)
    another_note = TastingNote.objects.create(
        whisky=another_whisky, owner=another_user, note="スモーキー"
    )
    url = reverse("tastingnote-detail", args=[another_note.id])  # type: ignore
    data = {"whisky": another_whisky.id, "note": "アップデート"}  # type: ignore

    response = api_client.put(url, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_get_non_existent_tasting_note(api_client):
    url = reverse("tastingnote-detail", args=[99999999])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
