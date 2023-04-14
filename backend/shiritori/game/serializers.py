from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from shiritori.game.models import Game, GameSettings, GameWord, Player

__all__ = (
    "EmptySerializer",
    "ShiritoriGameWordSerializer",
    "ShiritoriGameSettingsSerializer",
    "ShiritoriPlayerSerializer",
    "JoinGameSerializer",
    "ShiritoriGameSerializer",
    "ShiritoriTurnSerializer",
    "CreateStartGameSerializer",
)


@extend_schema_field(
    {
        "type": "string",
    }
)
class StringPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    pass


class EmptySerializer(serializers.Serializer):
    def create(self, validated_data):
        pass  # Need to override because parent class is abstract

    def update(self, instance, validated_data):
        pass  # Need to override because parent class is abstract


class ShiritoriGameWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameWord
        fields = (
            "word",
            "score",
            "duration",
            "player_id",
        )


class ShiritoriGameSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSettings
        exclude = ("id",)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("data", GameSettings.get_default_settings())
        super().__init__(*args, **kwargs)


class ShiritoriPlayerSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Player
        fields = (
            "id",
            "name",
            "score",
            "type",
            "is_current",
            "is_connected",
            "is_host",
        )


class JoinGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ("name",)


class ShiritoriGameSerializer(serializers.ModelSerializer):
    settings = ShiritoriGameSettingsSerializer()
    player_count = serializers.IntegerField(read_only=True)
    word_count = serializers.IntegerField(read_only=True)
    longest_word = StringPrimaryKeyRelatedField(read_only=True, allow_null=True)
    is_finished = serializers.BooleanField(read_only=True)
    winner = StringPrimaryKeyRelatedField(read_only=True, allow_null=True)
    current_player = StringPrimaryKeyRelatedField(read_only=True, allow_null=True)
    turn_time_left = serializers.IntegerField(read_only=True)
    words = ShiritoriGameWordSerializer(many=True, read_only=True)
    players = ShiritoriPlayerSerializer(many=True, read_only=True)

    class Meta:
        model = Game
        exclude = ("task_id",)

    def create(self, validated_data):  # noqa
        settings = validated_data.pop("settings")
        settings = GameSettings.objects.create(**settings)
        return Game.objects.create(**validated_data, settings=settings)


class ShiritoriTurnSerializer(serializers.Serializer):
    word = serializers.CharField(max_length=50)


class CreateStartGameSerializer(serializers.Serializer):
    settings = ShiritoriGameSettingsSerializer(required=False)

    def save(self):
        if "settings" not in self.validated_data:
            return None
        return GameSettings.objects.create(**self.validated_data["settings"])
