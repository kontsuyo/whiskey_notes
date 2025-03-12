from rest_framework import serializers

from notes.models import Whiskey


class WhiskeySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.CharField(read_only=True, source="owner.username")

    class Meta:
        model = Whiskey
        fields = [
            "url",
            "id",
            "name",
            "country",
            "alcohol",
            "cask",
            "img",
            "price",
            "owner",
        ]
