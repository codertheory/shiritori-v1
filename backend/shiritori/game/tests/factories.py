import factory

from shiritori.game.models import Game, Player, GameWord, Word, GameLocales

__all__ = (
    'GameFactory',
    'PlayerFactory',
    'GameWordFactory',
    'WordFactory',
)

from shiritori.utils import generate_id


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game
        django_get_or_create = ('id',)

    id = factory.LazyFunction(lambda: generate_id(5))


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player
        django_get_or_create = ('id',)

    id = factory.LazyFunction(lambda: generate_id(5))
    name = factory.Faker('name')
    session_key = factory.Faker('uuid4')


class GameWordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GameWord
        django_get_or_create = ('word', 'game',)

    word = factory.Faker('word')


class WordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Word
        django_get_or_create = ('word', 'locale',)

    word = factory.Faker('word')
    locale = GameLocales.EN
