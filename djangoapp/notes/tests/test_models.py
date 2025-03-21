import pytest
from django.contrib.auth import get_user_model

from notes.models import TastingNote, Whisky

User = get_user_model()


@pytest.mark.django_db
class TestWhiskyModel:
    def test_register_whisky(self):
        user = User.objects.create_user(username="whisky-lover")

        name = "タリスカー"
        country = "SC"
        alcohol = 45.8
        cask = "バーボン樽"
        price = "4700円くらい"

        talisker = Whisky.objects.create(
            name=name,
            country=country,
            alcohol=alcohol,
            cask=cask,
            price=price,
            owner=user,
        )
        assert Whisky.objects.filter(id=talisker.id).exists()  # type: ignore


@pytest.mark.django_db
def test_tastingnote_str_representation():
    user = User.objects.create_user(username="testuser", password="password")
    whisky = Whisky.objects.create(name="Sample Whisky", owner=user)
    note = TastingNote.objects.create(whisky=whisky, note="good!", owner=user)

    assert str(note) == "good!"
