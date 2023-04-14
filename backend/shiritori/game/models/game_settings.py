from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from shiritori.game.models.text_choices import GameLocales
from shiritori.utils.abstract_model import NanoIdModel


class GameSettings(NanoIdModel):
    locale = models.CharField(max_length=10, choices=GameLocales.choices, default=GameLocales.EN)
    word_length = models.IntegerField(default=3, validators=[MinValueValidator(3), MaxValueValidator(5)])
    turn_time = models.IntegerField(default=60, validators=[MinValueValidator(5), MaxValueValidator(120)])
    max_turns = models.IntegerField(default=10, validators=[MinValueValidator(5), MaxValueValidator(20)])

    class Meta:
        db_table = "game_settings"

    @staticmethod
    def get_default_settings() -> dict:
        all_fields = GameSettings._meta.get_fields()  # noqa - protected access
        fields = filter(lambda f: hasattr(f, "default") and f.name != "id", all_fields)
        # inspect the fields and create a dict of the defaults.
        return {field.name: field.default for field in fields}

    @classmethod
    def from_defaults(cls) -> "GameSettings":
        return cls.objects.create(**cls.get_default_settings())
