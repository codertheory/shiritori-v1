from django.conf import settings
from django.db import models

from shiritori.game.models.text_choices import GameLocales
from shiritori.game.utils import chunk_list


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

    @staticmethod
    def load_dictionary(locale: GameLocales | str = GameLocales.EN) -> list["Word"]:
        """Load the dictionary for the given locale."""
        with open(f"{settings.BASE_DIR}/dictionaries/{locale}.txt", encoding="utf-8") as f:
            words = f.read().splitlines()
        created_words = []
        # Batch insert the words into the database in chunks of 1000
        for chunk in chunk_list(words, 1000):
            created_words.extend(
                Word.objects.bulk_create(
                    [Word(word=word, locale=locale) for word in chunk],
                    batch_size=1000,
                    ignore_conflicts=True,
                )
            )
        return created_words
