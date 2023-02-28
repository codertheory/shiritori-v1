from rest_framework import serializers

from shiritori.game.models import Game, Player, GameSettings, GameWord

__all__ = (
    "ShiritoriGameSettingsSerializer",
    "ShiritoriPlayerSerializer",
    "ShiritoriGameSerializer",
    "ShiritoriTurnSerializer",
    "ShiritoriGameWordSerializer",
    "CreateGameSerializer",
)


class ShiritoriGameSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSettings
        exclude = ("id",)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('data', GameSettings.get_default_settings())
        super().__init__(*args, **kwargs)


class ShiritoriPlayerSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Player
        fields = (
            "id",
            "name",
            "score",
        )


class ShiritoriGameSerializer(serializers.ModelSerializer):
    settings = ShiritoriGameSettingsSerializer(read_only=True)
    player_count = serializers.IntegerField(read_only=True)
    word_count = serializers.IntegerField(read_only=True)
    is_finished = serializers.BooleanField(read_only=True)
    winner = ShiritoriPlayerSerializer(read_only=True)
    current_player = ShiritoriPlayerSerializer(read_only=True)
    turn_time_left = serializers.IntegerField(read_only=True)

    class Meta:
        model = Game
        fields = "__all__"


class ShiritoriTurnSerializer(serializers.Serializer):
    word = serializers.CharField(max_length=50)
    duration = serializers.IntegerField()

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
        )


class CreateGameSerializer(serializers.Serializer):
    settings = ShiritoriGameSettingsSerializer()

    def create(self, validated_data):
        pass  # Need to override because parent class is abstract

    def update(self, instance, validated_data):
        pass  # Need to override because parent class is abstract

    def save(self, **kwargs):
        settings = GameSettings.objects.create(**self.validated_data["settings"])
        return Game.objects.create(settings=settings)
