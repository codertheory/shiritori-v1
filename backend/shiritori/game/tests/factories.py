import factory
from pytest_factoryboy import register

from shiritori.game.models import Game, GameLocales, GameSettings, GameStatus, GameWord, Player, PlayerType, Word
from shiritori.utils import generate_id

__all__ = (
    "GameSettingsFactory",
    "PlayerFactory",
    "GameFactory",
    "GameWordFactory",
    "WordFactory",
)


class GameSettingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GameSettings

    locale = GameLocales.EN
    word_length = factory.Faker("pyint", min_value=3, max_value=5)
    turn_time = factory.Faker("pyint", min_value=30, max_value=120)
    max_turns = factory.Faker("pyint", min_value=5, max_value=20)


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Player
        django_get_or_create = ("id",)

    class Params:  # pylint: disable=too-few-public-methods
        human = factory.Trait(
            type=PlayerType.HUMAN,
        )
        bot = factory.Trait(
            type=PlayerType.BOT,
        )
        spectator = factory.Trait(
            type=PlayerType.SPECTATOR,
        )
        host = factory.Trait(
            is_host=True,
        )

    id = factory.LazyFunction(lambda: generate_id(5))
    name = factory.Faker("name")
    session_key = factory.Faker("uuid4")
    type = PlayerType.HUMAN


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game
        django_get_or_create = ("id",)

    class Params:  # pylint: disable=too-few-public-methods
        waiting = factory.Trait(
            status=GameStatus.WAITING,
        )
        started = factory.Trait(
            status=GameStatus.PLAYING,
        )
        finished = factory.Trait(
            status=GameStatus.FINISHED,
        )

    id = factory.LazyFunction(lambda: generate_id(5))
    status = GameStatus.WAITING
    last_word = "t"

    @staticmethod
    @factory.post_generation
    def settings(obj: Game, create, extracted, **kwargs):
        if not create:
            return
        obj.settings = extracted or GameSettingsFactory()

    @staticmethod
    def generate_players(obj: Game, create, extracted, **kwargs):
        if not create:
            return
        if extracted is None:
            return
        players = PlayerFactory.create_batch(extracted, game=obj, is_current=False, is_host=False)
        was_changed = False
        if obj.is_started and not obj.current_player:
            players[0].is_current = True
            was_changed = True
        if not obj.host:
            players[0].is_host = True
            was_changed = True
        if was_changed:
            players[0].save()

    with_players = factory.PostGeneration(generate_players)


@register
class GameWordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GameWord
        django_get_or_create = (
            "word",
            "game",
        )

    word = factory.Faker("word")


@register
class WordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Word
        django_get_or_create = (
            "word",
            "locale",
        )

    word = factory.Faker("word")
    locale = GameLocales.EN
