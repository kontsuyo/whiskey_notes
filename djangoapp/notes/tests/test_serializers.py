import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from notes.models import Whiskey
from notes.serializers import WhiskeySerializer

User = get_user_model()


@pytest.mark.django_db
def test_whiskey_serializer_owner_field():
    user = User.objects.create_user(username="testuser")
    whiskey = Whiskey.objects.create(
        name="タリスカー",
        country="SC",
        alcohol=45.6,
        cask="バーボン樽",
        price="4500",
        owner=user,
    )

    serializer = WhiskeySerializer(whiskey, context={"request": None})
    expected_url = reverse("user-detail", args=[user.id])

    assert serializer.data["owner"] == expected_url
