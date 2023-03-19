from typing import Iterable, Optional, Union

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models, transaction
from django.db.models import Count, F, Q, QuerySet, Sum

from shiritori.game.events import send_game_updated
from shiritori.game.utils import calculate_score, generate_random_letter, wait
from shiritori.utils import NanoIdField
from shiritori.utils.abstract_model import AbstractModel, NanoIdModel


class GameStatus(models.TextChoices):
    WAITING = "WAITING", "Waiting"
    PLAYING = "PLAYING", "Playing"
    FINISHED = "FINISHED", "Finished"


class GameLocales(models.TextChoices):
    EN = "en", "English"


class PlayerType(models.TextChoices):
    HUMAN = "HUMAN", "human"
    BOT = "BOT", "bot"
    SPECTATOR = "SPECTATOR", "spectator"
    WINNER = "WINNER", "winner"


class Game(AbstractModel):
    id = NanoIdField(max_length=5)
    status = models.CharField(
        max_length=8,
        choices=GameStatus.choices,
        default=GameStatus.WAITING,
    )
    current_turn = models.IntegerField(default=0)
    settings = models.ForeignKey(
        "GameSettings",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    turn_time_left = models.IntegerField(default=0)
    last_word = models.CharField(max_length=255, null=True, blank=True, default=generate_random_letter)

    class Meta:
        ordering = ("-created_at",)
        db_table = "game"

    def __str__(self) -> str:
        return f"Game {self.id}"

    @staticmethod
    def get_start_able_games() -> "QuerySet[Game]":
        """
        Get a QuerySet of games that can be started.
        :return: QuerySet[Game]
        """
        player_filter = Q(player__type=PlayerType.HUMAN) | Q(player__type=PlayerType.BOT)
        return Game.objects.annotate(total_players=Count("player", filter=player_filter)).filter(
            status=GameStatus.WAITING, total_players=2
        )

    @staticmethod
    def get_startable_game_by_id(game_id: str) -> "QuerySet[Game]":
        """
        Get a queryset of a Game that can be started by ID.
        :param game_id: str - Game ID
        :return: QuerySet[Game]
        """
        return Game.get_start_able_games().filter(id=game_id)

    @property
    def players(self) -> "QuerySet[Player]":
        return self.player_set.all().exclude(type=PlayerType.SPECTATOR)

    @property
    def words(self) -> "QuerySet[GameWord]":
        return self.gameword_set.all()

    @property
    def host(self) -> Optional["Player"]:
        return self.player_set.filter(is_host=True).first()

    @property
    def current_player(self) -> Optional["Player"]:
        return self.player_set.filter(is_current=True).first()

    @current_player.setter
    def current_player(self, value: "Player") -> None:
        self.player_set.filter().update(is_current=False)
        value.is_current = True
        value.save(update_fields=["is_current"])

    @property
    def winner(self) -> Optional["Player"]:
        return self.player_set.filter(type=PlayerType.WINNER).first()

    @winner.setter
    def winner(self, value: "Player") -> None:
        self.player_set.filter(type=PlayerType.WINNER).update(type=PlayerType.HUMAN)
        value.type = PlayerType.WINNER
        value.save(update_fields=["type"])

    @property
    def player_count(self) -> int:
        return self.players.count()

    @property
    def word_count(self) -> int:
        return self.gameword_set.count()

    @property
    def last_used_word(self) -> Optional["GameWord"]:
        return self.gameword_set.last()

    @property
    def is_finished(self) -> bool:
        return self.status == GameStatus.FINISHED

    @is_finished.setter
    def is_finished(self, value: bool) -> None:
        self.status = GameStatus.FINISHED if value else GameStatus.PLAYING

    @property
    def is_started(self) -> bool:
        return self.status == GameStatus.PLAYING

    @property
    def leaderboard(self) -> QuerySet["Player"]:
        return self.player_set.annotate(
            total_score=Sum("gameword__score"),
        ).order_by("-total_score")

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        has_settings_changed = False
        if self.settings is None:
            self.settings = GameSettings.objects.create()
            has_settings_changed = True
        if self.settings and not self.settings.pk:
            self.settings.save()
            has_settings_changed = True
        if (
            has_settings_changed
            and update_fields
            and isinstance(update_fields, list)
            and "settings" not in update_fields
        ):
            update_fields.append("settings")
        super().save(force_insert, force_update, using, update_fields)

    def join(self, player: Union["Player", str]) -> "Player":
        """Add a player to the game."""
        if self.is_started or self.is_finished:
            raise ValidationError("Game has already started or is finished.")
        if isinstance(player, str):
            player = Player(
                name=player,
                game=self,
                type=PlayerType.HUMAN,
                is_host=self.player_count == 0,
            )
        else:
            player.game = self
            player.type = PlayerType.HUMAN
            player.is_host = self.player_count == 0
        player.save(update_fields=["name", "game", "type", "session_key", "is_host"])
        return player

    def leave(self, player: Union["Player", str]) -> None:
        """Remove a player from the game."""
        if isinstance(player, str):
            player = self.player_set.get(session_key=player)
        player.delete()
        if player.is_host:
            try:
                self.recalculate_host()
            except ValidationError:
                self.status = GameStatus.FINISHED
        if self.status == GameStatus.PLAYING:
            try:
                self.calculate_current_player(save=False)
            except ValidationError:
                self.status = GameStatus.FINISHED
        self.save(update_fields=["status"])

    def start(self, session_key: str = None, *, save: bool = True) -> None:
        """
        Start the game.
        :param session_key: str - The session key of the player starting the game.
        :param save: bool - Whether to save the game after starting.
        :return: None
        :raises ValidationError: If there are less than 2 players in the game.
        """
        if self.status != GameStatus.WAITING:
            raise ValidationError("Cannot start a game that is not waiting.")
        if session_key and self.host.session_key != session_key:
            raise ValidationError("Only the host can start the game.")
        if self.player_count < 2:
            raise ValidationError("Cannot start a game with less than 2 players.")
        self.status = GameStatus.PLAYING
        self.calculate_current_player(save=False)
        self.turn_time_left = self.settings.turn_time
        if save:
            self.save(update_fields=["status", "turn_time_left"])

    def calculate_current_player(self, *, save: bool = True) -> None:
        """
        Calculates the current player given the current turn.
        :param save: bool - Whether to save the game after calculating the current player.
        :return: None
        :raises ValidationError: If there are no players in the game.
        """
        player_count = self.player_count
        if player_count == 0:
            raise ValidationError("Cannot calculate current player when there are no players.")
        if player_count == 1:
            raise ValidationError("Cannot calculate current player when there is only 1 player.")

        self.current_player = self.players[self.current_turn % self.player_count]

        if save:
            self.save()

    def recalculate_host(self, *, save: bool = True) -> None:
        """
        Recalculates the host of the game.
        :param save: bool - Whether to save the game after recalculating the host.
        :return: None
        :raises ValidationError: If there are no players in the game.
        """
        host = self.host
        players = self.players

        # If no players raise ValidationError
        if not players.exists():
            raise ValidationError("Cannot recalculate host when there are no players.")

        if not host:
            if first := self.players.first():
                first.is_host = True
                if save:
                    first.save(update_fields=["is_host"])

    def can_take_turn(self, session_key: str, *, timeout: bool = False) -> None:
        """
        Checks if a player can take a turn.
        Checks the following criteria:
        1. The game is in progress.
        2. The player is the current player.
        3. The player has not exceeded their turn time.

        :param session_key: str - The session key of the player.
        :param timeout: bool - Whether to check if the player has exceeded their turn time.
        :return: None
        :raises ValidationError: If the player cannot take a turn.
        """
        if self.status != GameStatus.PLAYING:
            raise ValidationError("Game is not in progress.")
        if self.current_player.session_key != session_key:
            raise ValidationError("It is not your turn.")
        if not timeout and self.turn_time_left <= 0:
            raise ValidationError("Turn time has expired.")

    def take_turn(self, session_key: str, word: str | None, *, save: bool = True) -> None:
        """
        Take a turn in the game.
        :param session_key: The session key of the player requesting to take a turn.
        :param word: The word the player submitted.
        :param save: bool - Whether to save the game after taking the turn.
        :return: None
        :raises ValidationError: If the player cannot take a turn.
        """
        timed_out = self.turn_time_left <= 0
        self.can_take_turn(session_key, timeout=timed_out)
        game_qs = Game.objects.prefetch_related("settings").filter(pk=self.pk)
        with transaction.atomic():
            game = game_qs.first()
            duration = game.settings.turn_time - game.turn_time_left
            game_word = GameWord(
                game=self,
                player=self.current_player,
                word=word.lower() if isinstance(word, str) else None,
                duration=duration,
            )
            if not timed_out:
                game_word.validate(raise_exception=True)
            game_word.save()
            if word:
                self.last_word = word
            if self.current_turn + 1 > self.settings.max_turns:
                self.status = GameStatus.FINISHED
                self.winner = self.leaderboard.first()
                self.save(update_fields=["status", "last_word", "current_turn"])
                return
            self.current_turn += 1
            self.calculate_current_player(save=False)
            self.turn_time_left = self.settings.turn_time
            if save:
                self.save(
                    update_fields=[
                        "current_turn",
                        "last_word",
                        "turn_time_left",
                    ]
                )

    def end_turn(self) -> None:
        """
        End the current turn. and start the next turn.
        This is usually called when the turn time has expired.

        This will submit an empty word with a duration given.
        Resulting in a negative score.

        :return: None
        """
        self.take_turn(self.current_player.session_key, None)

    def get_winner(self) -> Optional["Player"]:
        """
        Get the winner of the game.
        To be called when the game is finished.
        For a player to be determined as the winner they must have the highest score.

        :return: Optional[Player] - The winner of the game.
        :raises ValidationError: If the game is not finished or started.
        """
        if not self.is_finished:
            raise ValidationError("Cannot get winner of a game that is not finished.")
        if not self.is_started:
            raise ValidationError("Cannot get winner of a game that has not started.")

        return self.leaderboard.first()

    @staticmethod
    def run_turn_loop(game_id):
        """
        Runs the turn loop for a game.

        This will be run from a celery task.

        :param game_id: The id of the game to run the turn loop for.

        """
        qs = Game.objects.filter(id=game_id)
        while not qs.filter(status=GameStatus.FINISHED).exists():
            if qs.filter(turn_time_left__gt=0).exists():
                qs.update(turn_time_left=F("turn_time_left") - 1)
                wait()  # sleep for 1.25 seconds to allow for any networking issues
            else:
                # if the game timer is 0, end the turn
                # and start the next turn
                qs.first().end_turn()
            send_game_updated(qs.first())


class Player(AbstractModel, NanoIdModel):
    name = models.CharField(max_length=255)
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


class GameWord(NanoIdModel):
    word = models.CharField(max_length=255, null=True, blank=True)
    score = models.FloatField(default=0)
    game = models.ForeignKey(
        "Game",
        on_delete=models.CASCADE,
    )
    player = models.ForeignKey(
        "Player",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    duration = models.FloatField(default=0)

    class Meta:
        db_table = "game_word"
        indexes = [
            models.Index(fields=["game", "player"]),
            models.Index(fields=["game", "word"]),
            models.Index(fields=["game", "score"]),
            models.Index(fields=["player", "score", "word"]),
        ]
        constraints = [
            models.UniqueConstraint(
                name="unique_word",
                fields=["game", "word"],
                condition=models.Q(word__isnull=False),
            ),
        ]

    @property
    def calculated_score(self):
        return calculate_score(self.word, self.duration)

    def save(
        self,
        force_insert: bool = False,
        force_update: bool = False,
        using: str | None = None,
        update_fields: Iterable[str] | None = None,
    ) -> None:
        if self.word:
            self.word = self.word.lower()  # Normalize the word.
            self.score = self.calculated_score
        else:
            self.score = -0.25 * self.duration
        super().save(force_insert, force_update, using, update_fields)

    def validate(self, *, raise_exception: bool = False) -> bool:
        """
        Validates that the word meets the following criteria:

        1. The word starts with the last word's last letter.
        2. The word is not already in the game.
        3. The word length is greater than or equal to the game's word length.
        4. The word is in the dictionary for the game's locale.

        :return: bool - Whether the word is valid.
        """
        error_message = None
        if self.game.last_word and self.word[0] != self.game.last_word[-1]:
            error_message = "Word must start with the last letter of the previous word."
        if self.game.gameword_set.filter(word=self.word).exists():
            error_message = "Word already used."
        if len(self.word) < self.game.settings.word_length:
            error_message = f"Word must be at least {self.game.settings.word_length} characters long."
        if not Word.validate(self.word, self.game.settings.locale):
            error_message = "Word not found in dictionary."
        if error_message and raise_exception:
            raise ValidationError(error_message)
        return error_message is None


class GameSettings(NanoIdModel):
    locale = models.CharField(max_length=10, choices=GameLocales.choices, default=GameLocales.EN)
    word_length = models.IntegerField(default=3, validators=[MinValueValidator(3), MaxValueValidator(5)])
    turn_time = models.IntegerField(default=60, validators=[MinValueValidator(30), MaxValueValidator(120)])
    max_turns = models.IntegerField(default=10, validators=[MinValueValidator(5), MaxValueValidator(20)])

    class Meta:
        db_table = "game_settings"

    @staticmethod
    def get_default_settings() -> dict:
        all_fields = GameSettings._meta.get_fields()  # noqa pylint: disable=protected-access
        fields = filter(lambda f: hasattr(f, "default") and f.name != "id", all_fields)
        # inspect the fields and create a dict of the defaults.
        return {field.name: field.default for field in fields}

    @classmethod
    def from_defaults(cls) -> "GameSettings":
        return cls.objects.create(**cls.get_default_settings())


class Word(models.Model):
    word = models.CharField(max_length=255)
    locale = models.CharField(max_length=10, choices=GameLocales.choices, default=GameLocales.EN)

    class Meta:
        db_table = "word"
        indexes = [
            models.Index(fields=["word", "locale"]),
            models.Index(fields=["locale"]),
            models.Index(fields=["word"]),
        ]
        constraints = [
            models.UniqueConstraint(name="unique_word_locale", fields=["word", "locale"]),
        ]

    def __str__(self):
        return f"{self.word} ({self.locale})"

    @classmethod
    def validate(cls, word: str, locale: GameLocales | str = GameLocales.EN) -> bool:
        """Validate that the word is in the dictionary for the given locale."""
        return cls.objects.filter(word__iexact=word, locale=locale).exists()
