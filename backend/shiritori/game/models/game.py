import random
from collections.abc import Iterable
from typing import Optional, Union

from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models import Count, F, Q, QuerySet, Sum
from django.db.models.functions import Length, Right

from shiritori.game.models.game_settings import GameSettings
from shiritori.game.models.game_word import GameWord
from shiritori.game.models.player import Player
from shiritori.game.models.text_choices import GameStatus, PlayerType
from shiritori.game.utils import generate_random_letter, wait
from shiritori.utils import NanoIdField
from shiritori.utils.abstract_model import AbstractModel


class Game(AbstractModel):
    id = NanoIdField(max_length=5)
    status = models.CharField(
        max_length=8,
        choices=GameStatus.choices,
        default=GameStatus.WAITING,
    )
    current_turn = models.IntegerField(default=0)
    current_round = models.IntegerField(default=0)
    settings = models.ForeignKey(
        "GameSettings",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    turn_time_left = models.IntegerField(default=0)
    last_word = models.CharField(max_length=255, null=True, blank=True, default=generate_random_letter)
    task_id = models.CharField(max_length=255, null=True, blank=True)

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
        qs = self.player_set.all().exclude(type=PlayerType.SPECTATOR)
        if self.is_started:
            qs = qs.order_by("order")
        return qs

    @property
    def words(self) -> "QuerySet[GameWord]":
        return self.gameword_set.all()

    @property
    def host(self) -> Optional["Player"]:
        return self.player_set.filter(is_host=True).first()

    @property
    def current_player(self) -> Optional["Player"]:
        return self.player_set.filter(is_current=True).first()

    @property
    def next_player(self) -> Optional["Player"]:
        return self.players[self.current_turn % self.player_count]

    @property
    def last_player(self) -> Optional["Player"]:
        return self.players.filter(is_connected=True).last()

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
    def longest_word(self) -> Optional["GameWord"]:
        return self.gameword_set.order_by(Length("word").desc()).first()

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
        return self.players.annotate(
            total_score=Sum("gameword__score"),
        ).order_by("-total_score")

    @property
    def max_turns(self):
        return self.settings.max_turns * self.player_count

    @property
    def used_letters(self) -> "QuerySet[str]":
        return (
            self.gameword_set.annotate(
                last_letter=Right("word", 1),
            )
            .values_list("last_letter", flat=True)
            .distinct()
        )

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

    def join(self, player: Union["Player", str], session_key: str = None) -> "Player":
        """Add a player to the game."""
        if self.is_started or self.is_finished:
            raise ValidationError("Game has already started or is finished.")
        if isinstance(player, str):
            player = Player(
                name=player,
                game=self,
                type=PlayerType.HUMAN,
                session_key=session_key,
                is_host=self.player_count == 0,
            )
        else:
            player.game = self
            player.type = PlayerType.HUMAN
            player.is_host = self.player_count == 0
            if not player.session_key:
                player.session_key = session_key
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

    def start(
        self, session_key: str = None, game_settings: Optional["GameSettings"] = None, *, save: bool = True
    ) -> None:
        """
        Start the game.
        :param session_key: str - The session key of the player starting the game.
        :param game_settings: GameSettings - The settings to use for the game.
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
        self.shuffle_player_order()
        self.status = GameStatus.PLAYING
        self.calculate_current_player(save=False)
        if game_settings:
            self.settings = game_settings
        self.turn_time_left = self.settings.turn_time
        if save:
            update_fields = ["status", "turn_time_left"]
            if game_settings:
                update_fields.append("settings")
            self.save(update_fields=update_fields)

    def restart(self, session_key: str = None) -> None:
        """
        Restart the game.
        """
        if session_key:
            is_host = self.players.filter(session_key=session_key, is_host=True).exists()
            if not is_host:
                raise ValidationError("Only the host can restart the game.")
        self.players.update(is_current=False, order=None)
        self.gameword_set.all().delete()
        self.status = GameStatus.WAITING
        self.current_turn = 0
        self.turn_time_left = 0
        self.task_id = None
        self.last_word = generate_random_letter()
        self.save(update_fields=["status", "current_turn", "turn_time_left", "task_id", "last_word"])

    def finish(self):
        self.status = GameStatus.FINISHED
        self.winner = self.leaderboard.first()
        self.save(update_fields=["status", "last_word", "current_turn"])

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

        if self.next_player and self.next_player.is_connected is False:
            self.skip_turn()
        else:
            self.current_player = self.next_player

        if save:
            self.save()

    def shuffle_player_order(self):
        """
        Shuffles the order of the players.
        """
        if self.is_started:
            raise ValidationError("Cannot shuffle player order when game has started.")
        if self.is_finished:
            raise ValidationError("Cannot shuffle player order when game is finished.")
        if self.player_count < 2:
            raise ValidationError("Cannot shuffle player order when there are less than 2 players.")
        players = list(self.players.all())
        random.shuffle(players)
        for index, player in enumerate(players):
            player.order = index
            # Let it be known, that for some reason bulk_update does not work here. ¯\_(ツ)_/¯
            player.save(update_fields=["order"])

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

    def can_take_turn(self, session_key: str) -> None:
        """
        Checks if a player can take a turn.
        Checks the following criteria:
        1. The game is in progress.
        2. The player is the current player.
        3. The player has not exceeded their turn time.

        :param session_key: str - The session key of the player.
        :return: None
        :raises ValidationError: If the player cannot take a turn.
        """
        if self.status != GameStatus.PLAYING:
            raise ValidationError("Game is not in progress.")
        if self.current_player.session_key != session_key:
            raise ValidationError("It is not your turn.")
        if self.turn_time_left <= 0:
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
        self.can_take_turn(session_key)
        self._handle_turn(word, save=save)

    def _handle_turn(self, word: str | None, *, save: bool = True) -> None:
        """
        Underlying method for taking a turn.
        :param word: The word the player submitted.
        :param save: bool - Whether to save the game after taking the turn.
        :return: None
        """
        with transaction.atomic():
            self.create_word(word)
            if self.current_turn + 1 > self.max_turns:
                self.finish()
            self.update_turn()
            self.calculate_current_player(save=False)
            self.reset_turn_time()
            if save:
                self.save(
                    update_fields=[
                        "current_turn",
                        "current_round",
                        "last_word",
                        "turn_time_left",
                    ]
                )

    def create_word(self, word: str) -> GameWord:
        """
        Create a word for the current turn.
        :param word: The word the player submitted.
        """
        timed_out = self.turn_time_left <= 0
        duration = self.settings.turn_time - self.turn_time_left
        game_word = GameWord.create(
            game=self,
            player=self.current_player,
            word=word,
            duration=duration,
            timed_out=timed_out,
        )
        if word:
            self.last_word = game_word.word
        return game_word

    def update_turn(self):
        """
        Update the current turn.
        This will also update the current round if the current player is the last player.
        :return: None
        """
        self.current_turn += 1
        if self.current_player == self.last_player:
            self.current_round += 1

    def reset_turn_time(self):
        """
        Reset the turn time back to the default turn time.
        :return: None
        """
        self.turn_time_left = self.settings.turn_time

    def skip_turn(self):
        """
        Skip the current turn.
        This is usually called when the player has disconnected.

        This will not result in a penalty.

        :return: None
        """
        connected_players = self.players.filter(is_connected=True)
        try:
            current_player_index = list(connected_players).index(self.current_player)
        except ValueError as error:
            raise ValidationError("Current player is not connected.") from error
        if connected_players.count() >= 2:
            next_index = (current_player_index + 1) % connected_players.count()
            self.current_player = connected_players[next_index]

    def end_turn(self) -> None:
        """
        End the current turn. and start the next turn.
        This is usually called when the turn time has expired.

        This will submit an empty word with a duration given.
        Resulting in a negative score.

        :return: None
        """
        self._handle_turn(None)

    @staticmethod
    def run_turn_loop(game_id: str, task_id: str):
        """
        Runs the turn loop for a game.

        This will be run from a celery task.

        :param game_id: The id of the game to run the turn loop for.
        :param task_id: The id of the task running the turn loop.

        """
        from shiritori.game.events import send_game_timer_updated

        qs: QuerySet["Game"] = Game.objects.filter(id=game_id)
        while qs.filter(Q(status=GameStatus.PLAYING) & Q(task_id=task_id)).exists():
            if qs.filter(turn_time_left__gt=0).exists():
                qs.update(turn_time_left=F("turn_time_left") - 1)
                wait()  # sleep for 1.25 seconds to allow for any networking issues
            else:
                # if the game timer is 0, end the turn
                # and start the next turn
                qs.first().end_turn()
            if game := qs.values("id", "turn_time_left").first():
                send_game_timer_updated(game["id"], game["turn_time_left"])
