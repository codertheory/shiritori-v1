import typing

from django.core.exceptions import ValidationError
from django.db import models

from shiritori.game.models.word import Word
from shiritori.game.utils import calculate_score, case_insensitive_equal, normalize_word
from shiritori.utils.abstract_model import NanoIdModel

if typing.TYPE_CHECKING:
    from shiritori.game.models.game import Game
    from shiritori.game.models.player import Player


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

    @classmethod
    def create(
        cls, game: "Game", player: "Player", word: str | None, duration: int | float, timed_out: bool = False
    ) -> typing.Self:
        """
        Build a new GameWord instance.
        :param game: Game - The game the word is for.
        :param player: Player - The player that entered the word.
        :param word: str - The word that was entered.
        :param duration: int - The duration it took to enter the word.
        :param timed_out: bool - Whether the word was entered because the timer ran out.
        :return: GameWord - The new GameWord instance.
        """
        word = normalize_word(word)
        current_used_letters = game.used_letters
        is_new_letter = word and word[-1] not in current_used_letters
        calculated_score = calculate_score(word, duration, is_new_letter)
        game_word = cls(
            game=game,
            player=player,
            word=word,
            duration=duration,
            score=calculated_score,
        )
        if not timed_out:
            game_word.validate(raise_exception=True)
        game_word.save()
        return game_word

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
        if self.game.last_word and not case_insensitive_equal(self.word[0], self.game.last_word[-1]):
            error_message = "Word must start with the last letter of the previous word."
        if self.game.gameword_set.filter(word__iexact=self.word).exists():
            error_message = "Word already used."
        if len(self.word) < self.game.settings.word_length:
            error_message = f"Word must be at least {self.game.settings.word_length} characters long."
        if not Word.validate(self.word, self.game.settings.locale):
            error_message = "Word not found in dictionary."
        if error_message and raise_exception:
            raise ValidationError(error_message)
        return error_message is None
