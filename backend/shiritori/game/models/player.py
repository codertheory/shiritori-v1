from typing import Optional

from django.core.validators import RegexValidator
from django.db import models
from django.db.models import QuerySet

from shiritori.game.models.game_word import GameWord
from shiritori.game.models.text_choices import PlayerType
from shiritori.utils.abstract_model import AbstractModel, NanoIdModel


class Player(AbstractModel, NanoIdModel):
    name = models.CharField(
        max_length=15, validators=[RegexValidator(r"^[0-9a-zA-Z]*$", "Only alphanumeric characters are allowed.")]
    )
    game = models.ForeignKey(
        "Game",
        on_delete=models.CASCADE,
        null=True,
    )
    type = models.CharField(
        max_length=25,
        choices=PlayerType.choices,
        default=PlayerType.HUMAN,
    )
    is_current = models.BooleanField(default=False)
    is_host = models.BooleanField(default=False)
    is_connected = models.BooleanField(default=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "player"
        constraints = [
            models.UniqueConstraint(
                name="unique_session_key",
                fields=["game", "session_key"],
            ),
            models.UniqueConstraint(
                name="unique_name",
                fields=["game", "name"],
            ),
            # There can only be one current player per game.
            models.UniqueConstraint(
                name="unique_current_player",
                fields=["game", "is_current"],
                condition=models.Q(is_current=True),
            ),
            # There can only be one host per game.
            models.UniqueConstraint(
                name="unique_host",
                fields=["game", "is_host"],
                condition=models.Q(is_host=True),
            ),
            # There can only be one winner per game.
            models.UniqueConstraint(
                name="unique_winner",
                fields=["game", "type"],
                condition=models.Q(type=PlayerType.WINNER),
            ),
        ]
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["game", "type"]),
            models.Index(fields=["game", "session_key"]),
            models.Index(fields=["game", "name"]),
        ]

    def __str__(self):
        return self.name

    @property
    def score(self):
        result = self.gameword_set.aggregate(models.Sum("score")).get("score__sum") or 0
        return int(round(result, 0))

    @property
    def words(self) -> "QuerySet[GameWord]":
        return self.gameword_set.all()

    @classmethod
    def get_by_session_key(cls, game_id: str, session_key: str) -> Optional["Player"]:
        """
        Get a player by their session key.
        :param game_id: The game id of the player.
        :param session_key: The session key of the player.
        :return: Optional[Player] - The player with the session key.
        """
        return cls.objects.filter(game_id=game_id, session_key=session_key).first()
