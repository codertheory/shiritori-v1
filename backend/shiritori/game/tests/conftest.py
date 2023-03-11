import pytest
import pytest_asyncio
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from django.db.models.signals import post_save, post_delete
from pytest_factoryboy import register
from rest_framework.test import APIClient
from pytest_mock import MockerFixture

from shiritori.game.consumers import GameLobbyConsumer, GameConsumer
from shiritori.game.models import Game, GameStatus, GameSettings
from shiritori.game.tests.factories import GameFactory, PlayerFactory, WordFactory

# Game Factory fixtures
register(GameFactory)
register(GameFactory, _name='unstarted_game', status=GameStatus.WAITING, with_players=2)
register(GameFactory, _name='started_game', status=GameStatus.PLAYING, with_players=2)
register(GameFactory, _name='finished_game', status=GameStatus.FINISHED, with_players=2)

# Player Factory Fixtures
register(PlayerFactory, human=True)
register(PlayerFactory, _name='human_player', human=True)
register(PlayerFactory, _name='human_player_2', human=True)
register(PlayerFactory, _name='bot_player', bot=True)
register(PlayerFactory, _name='spectator_player', spectator=True)
register(PlayerFactory, _name='host_player', host=True)


@pytest.fixture
def drf():
    return APIClient()


@pytest.fixture
def un_saved_game():
    instance = GameFactory.build()
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


@pytest_asyncio.fixture(name="game_consumer")
async def game_consumer(mocker: MockerFixture):
    game = await sync_to_async(GameFactory)(with_players=2)
    player_1 = await game.players.afirst()
    consumer = WebsocketCommunicator(
        GameConsumer.as_asgi(),
        f"/ws/game/{game.id}/",
    )
    consumer.scope['url_route'] = {'kwargs': {'game_id': game.id}}
    consumer.scope['cookies'] = {'sessionid': player_1.session_key}
    mock_session = mocker.Mock()
    mock_session.session_key = player_1.session_key
    consumer.scope['session'] = mock_session
    yield consumer, game, player_1
    await consumer.disconnect()
    await sync_to_async(game.delete)()


@pytest.fixture(autouse=True)  # Automatically use in tests.
def mute_signals(request):
    post_save.receivers = []
    post_delete.receivers = []
