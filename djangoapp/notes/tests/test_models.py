from django.contrib.auth import get_user_model
import pytest

from notes.models import Whiskey

User = get_user_model()


@pytest.mark.django_db
class TestWhiskeyModel:
    def test_register_whiskey(self):
        user = User.objects.create_user(username="whiskey-lover")

        name = "タリスカー"
        country = "SC"
        alcohol = 45.8
        cask = "バーボン樽"
        price = "4700円くらい"

        talisker = Whiskey.objects.create(
            name=name,
            country=country,
            alcohol=alcohol,
            cask=cask,
            price=price,
            owner=user,
        )
        assert Whiskey.objects.filter(id=talisker.id).exists()  # type: ignore
