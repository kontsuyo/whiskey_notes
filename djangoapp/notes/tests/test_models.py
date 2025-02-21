import pytest

from notes.models import Whiskey


@pytest.mark.django_db
class TestWhiskeyModel:
    def test_register_whiskey(self):
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
        )
        assert Whiskey.objects.filter(id=talisker.id).exists()  # type: ignore
