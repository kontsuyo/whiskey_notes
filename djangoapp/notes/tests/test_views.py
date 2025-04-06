import logging

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from notes.models import TastingNote, Whisky

User = get_user_model()
logger = logging.getLogger(__name__)


@pytest.mark.django_db
def test_create_whisky_authenticated(api_client, user, whisky_payload):
    api_client.force_authenticate(user=user)
    response_create = api_client.post(
        reverse("whisky-list"), data=whisky_payload, format="json"
    )
    assert response_create.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_create_whisky_unauthenticated(api_client, whisky_payload):
    response_create = api_client.post(
        reverse("whisky-list"), data=whisky_payload, format="json"
    )
    assert response_create.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_whisky_authenticated(api_client, user, whisky, whisky_payload):
    api_client.force_authenticate(user=user)
    whisky_payload["name"] = "Update Whisky"
    response_update = api_client.patch(
        reverse("whisky-detail", args=[whisky.id]), whisky_payload, format="json"
    )
    assert response_update.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_whisky_unauthenticated(api_client, whisky, whisky_payload):
    whisky_payload["name"] = "Update Whisky"
    response_update = api_client.patch(
        reverse("whisky-detail", args=[whisky.id]), whisky_payload, format="json"
    )
    assert response_update.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_other_users_whisky(api_client, user, whisky_payload):
    another_user = User.objects.create_user(
        username="another", password="password", email="another@example.com"
    )
    another_whisky = Whisky.objects.create(name="Another Whisky", owner=another_user)

    api_client.force_authenticate(user=user)
    whisky_payload["name"] = "Update Whisky"

    response_update = api_client.patch(
        reverse("whisky-detail", args=[another_whisky.id]), data=whisky_payload, format="json"  # type: ignore
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_create_tasting_note_authenticated(api_client, user, note_payload):
    api_client.force_authenticate(user=user)
    response_create = api_client.post(
        reverse("tastingnote-list"), data=note_payload, format="json"
    )
    assert response_create.status_code == 201


@pytest.mark.django_db
def test_create_tasting_note_unauthenticated(api_client, note_payload):
    response_create = api_client.post(
        reverse("tastingnote-list"), note_payload, format="json"
    )
    assert response_create.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_tasting_note_authenticated(api_client, user, note, note_payload):
    api_client.force_authenticate(user)
    note_payload["note"] = "最高！"
    response_update = api_client.patch(
        reverse("tastingnote-detail", args=[note.id]), data=note_payload, format="json"
    )
    assert response_update.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_update_tasting_note_unauthenticated(api_client, note, note_payload):
    note_payload["note"] = "good!"
    response = api_client.patch(
        reverse("tastingnote-detail", args=[note.id]), data=note_payload, format="json"
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_update_other_users_tasting_note(api_client, user, note_payload):
    api_client.force_authenticate(user=user)
    another_user = User.objects.create_user(
        username="other_user", password="password", email="another@example.com"
    )
    another_whisky = Whisky.objects.create(name="Another Whisky", owner=another_user)
    another_note = TastingNote.objects.create(
        whisky=another_whisky, owner=another_user, note="スモーキー"
    )
    note_payload["whisky"] = another_whisky.id  # type: ignore
    response_update = api_client.patch(
        reverse("tastingnote-detail", args=[another_note.id]),  # type:ignore
        data=note_payload,
        format="json",
    )
    assert response_update.status_code == status.HTTP_403_FORBIDDEN
