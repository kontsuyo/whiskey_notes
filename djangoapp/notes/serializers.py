from rest_framework import serializers

from notes.models import TastingNote, Whisky


class WhiskySerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.CharField(read_only=True, source="owner.username")

    class Meta:
        model = Whisky
        fields = [
            "url",
            "id",
            "created",
            "name",
            "country",
            "alcohol",
            "cask",
            "img",
            "price",
            "owner",
        ]


class TastingNoteSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(read_only=True, source="owner.username")

    class Meta:
        model = TastingNote
        fields = [
            "id",
            "post_date",
            "whisky",
            "note",
            "owner",
        ]

    def validate_whisky(self, value):
        request_user = self.context["request"].user
        if value.owner != request_user:
            raise serializers.ValidationError("このウィスキーに感想は追加できません。")
        return value
