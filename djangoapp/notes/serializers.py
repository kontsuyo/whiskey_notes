from rest_framework import serializers

from notes.models import Whiskey


class WhiskeySerializer(serializers.ModelSerializer):
    # owner = serializers.PrimaryKeyRelatedField(read_only=True)
    owner = serializers.StringRelatedField()
    # owner = serializers.HyperlinkedRelatedField(
    #     read_only=True, view_name="customuser-detail"
    # )

    class Meta:
        model = Whiskey
        fields = ["id", "name", "country", "alcohol", "cask", "img", "price", "owner"]
