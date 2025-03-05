from rest_framework import serializers

from notes.models import Whiskey


class WhiskeySerializer(serializers.ModelSerializer):
    owner = serializers.HyperlinkedRelatedField(read_only=True, view_name="user-detail")

    class Meta:
        model = Whiskey
        fields = ["id", "name", "country", "alcohol", "cask", "img", "price", "owner"]
