from collections.abc import Iterable

from django.core.exceptions import ValidationError
from django.db import models

from shiritori.game.models.word import Word
from shiritori.game.utils import calculate_score, case_insensitive_equal
from shiritori.utils.abstract_model import NanoIdModel


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
