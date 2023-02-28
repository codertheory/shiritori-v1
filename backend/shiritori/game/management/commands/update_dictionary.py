from django.core.management import BaseCommand

from shiritori.game.models import Word


class Command(BaseCommand):
    help = 'Updates the word dictionary'

    def add_arguments(self, parser):
        # Add a locale argument that can support multiple locales
        parser.add_argument('locale', nargs='+', type=str, default=['en'])

    def handle(self, *args, **options):
        for locale in options['locale']:
            with open(f'dictionaries/{locale}.txt', 'r', encoding='utf-8') as f:
                words = f.read().splitlines()
            self.stdout.write(f'Updating {locale} dictionary with {len(words)} words')
            results = Word.objects.bulk_create([Word(word=word, locale=locale) for word in words],
                                               ignore_conflicts=True)
            self.stdout.write(self.style.SUCCESS(f'Successfully updated {locale} dictionary with {len(results)} words'))
