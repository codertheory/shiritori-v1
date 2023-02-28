import pytest
import pytest_asyncio
from channels.testing import WebsocketCommunicator
from rest_framework.test import APIClient

from shiritori.game.consumers import GameLobbyConsumer
from shiritori.game.models import Game, GameSettings
from shiritori.game.tests.factories import GameFactory, PlayerFactory, WordFactory


@pytest.fixture
def drf():
    return APIClient()


@pytest.fixture
def un_saved_game():
    instance = GameFactory.build()
    yield instance
    if instance.id:
        instance.delete()


@pytest.fixture
def game():
    instance = GameFactory(last_word='t', turn_time_left=5)
    yield instance
    instance.delete()


@pytest.fixture
def started_game():
    new_game = GameFactory(last_word='t', turn_time_left=5)
    player_1 = PlayerFactory()
    player_2 = PlayerFactory()
    new_game.join(player_1)
    new_game.join(player_2)
    new_game.start()
    yield new_game, player_1, player_2
    new_game.delete()


@pytest.fixture
def unstarted_game():
    new_game = GameFactory(last_word='t', turn_time_left=5)
    player_1 = PlayerFactory()
    player_2 = PlayerFactory()
    new_game.join(player_1)
    new_game.join(player_2)
    yield new_game, player_1, player_2
    new_game.delete()


@pytest.fixture()
def player():
    instance = PlayerFactory()
    yield instance
    if instance.id:
        instance.delete()


@pytest.fixture()
def player2():
    instance = PlayerFactory()
    yield instance
    if instance.id:
        instance.delete()


@pytest.fixture()
def sample_words():
    words = [
        "test",
        "toothbrush",
        "hello",
    ]
    for word in words:
        WordFactory(word=word)
    yield words


@pytest.fixture()
def default_game_settings():
    yield GameSettings.get_default_settings()


@pytest_asyncio.fixture
async def sample_games():
    batch = GameFactory.build_batch(3)
    await Game.objects.abulk_create(batch)
    yield batch
    await Game.objects.filter(id__in=[g.id for g in batch]).adelete()


@pytest_asyncio.fixture(name="lobby_consumer")
async def game_lobby_consumer():
    consumer = WebsocketCommunicator(GameLobbyConsumer.as_asgi(), "/ws/game_lobby/")
    await consumer.connect()
    yield consumer
    await consumer.disconnect()
