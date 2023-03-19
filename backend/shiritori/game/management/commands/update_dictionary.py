from django.core.management import BaseCommand

from shiritori.game.models import Word


def chunk_list(iterable, n):
    for i in range(0, len(iterable), n):
        yield iterable[i : i + n]


class Command(BaseCommand):
    help = "Updates the word dictionary"

    def add_arguments(self, parser):
        # Add a locale argument that can support multiple locales
        parser.add_argument("locale", nargs="+", type=str, default=["en"])

    def handle(self, *args, **options):
        for locale in options["locale"]:
            with open(f"dictionaries/{locale}.txt", "r", encoding="utf-8") as f:
                words = f.read().splitlines()
            self.stdout.write(self.style.HTTP_INFO(f"Updating {locale} dictionary with {len(words)} words"))
            # Batch insert the words into the database in chunks of 1000
            for chunk in chunk_list(words, 1000):
                Word.objects.bulk_create(
                    [Word(word=word, locale=locale) for word in chunk],
                    batch_size=1000,
                    ignore_conflicts=True,
                )
            self.stdout.write(self.style.SUCCESS(f"Successfully updated {locale} dictionary with {len(words)} words"))
