import asyncio
import contextlib
import os
import random

import pytest
import pytest_asyncio
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from django.conf import settings
from django.db.models.signals import post_delete, post_save
from pytest_factoryboy import register
from pytest_mock import MockerFixture
from rest_framework.test import APIClient

from shiritori.game.consumers import GameConsumer, GameLobbyConsumer
from shiritori.game.models import Game, GameSettings, GameStatus
from shiritori.game.tests.factories import GameFactory, PlayerFactory, WordFactory


# function executed right after test items collected but before test run
def pytest_collection_modifyitems(config, items):
    if not config.getoption("-m"):
        skip_me = pytest.mark.skip(reason="use `-m e2e` to run this test")
        for item in items:
            if "e2e" in item.keywords:
                item.add_marker(skip_me)


# Constants
SAMPLE_WORDS = [
    "test",
    "toothbrush",
    "hello",
]

# Game Factory fixtures
register(GameFactory)
register(GameFactory, _name="unstarted_game", status=GameStatus.WAITING, with_players=2)
register(GameFactory, _name="started_game", status=GameStatus.PLAYING, with_players=2)
register(GameFactory, _name="finished_game", status=GameStatus.FINISHED, with_players=2, with_words=SAMPLE_WORDS)

# Player Factory Fixtures
register(PlayerFactory, human=True)
register(PlayerFactory, _name="human_player", human=True)
register(PlayerFactory, _name="human_player_2", human=True)
register(PlayerFactory, _name="bot_player", bot=True)
register(PlayerFactory, _name="spectator_player", spectator=True)
register(PlayerFactory, _name="host_player", host=True)


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
    for word in SAMPLE_WORDS:
        WordFactory(word=word)
    yield SAMPLE_WORDS


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
    consumer.scope["url_route"] = {"kwargs": {"game_id": game.id}}
    consumer.scope["cookies"] = {"sessionid": player_1.session_key}
    mock_session = mocker.Mock()
    mock_session.session_key = player_1.session_key
    consumer.scope["session"] = mock_session
    yield consumer, game, player_1
    await consumer.disconnect()
    await game.adelete()


@pytest.fixture(autouse=True)  # Automatically use in tests.
def mute_signals():
    post_save.receivers = []
    post_delete.receivers = []


@pytest.fixture(autouse=True)
def mock_shuffle(request: pytest.FixtureRequest, mocker: MockerFixture):
    ignore = request.node.get_closest_marker("real_shuffle")
    if ignore is None:
        mocker.patch("shiritori.game.models.game.random.shuffle")
    else:
        import random

        random.seed(42)


@pytest_asyncio.fixture(name="live_nuxt_client")
async def launch_live_nuxt_client():
    async def generate_nuxt_client(server_port):
        port = random.randint(8000, 9000)
        env_vars = {
            "NUXT_PORT": str(port),
            "NUXT_PUBLIC_API_HOST": f"localhost:{server_port}",
            "NUXT_PUBLIC_ENV": "test",
        }

        frontend_directory = settings.BASE_DIR.parent / "frontend"
        proc = await asyncio.create_subprocess_exec(
            "pnpm",
            "run",
            "dev",
            "--port",
            str(port),
            cwd=frontend_directory,
            env={**os.environ, **env_vars},
            stderr=None,
            stdout=None,
        )
        await asyncio.sleep(3)  # Wait for nuxt to start
        return proc, port

    return generate_nuxt_client


@pytest_asyncio.fixture(name="puppeteer_browser")
async def puppeteer_browser(live_server, live_nuxt_client):
    # TODO: Use https://github.com/luizyao/pytest-pyppeteer
    os.environ.setdefault("PYPPETEER_CHROMIUM_REVISION", "1140660")
    from pyppeteer import launch

    browser = await launch(
        {
            "headless": "new",
            "defaultViewport": {
                "width": 1920,
                "height": 1080,
            },
        }
    )
    proc, port = await live_nuxt_client(live_server.thread.port)
    page = (await browser.pages())[0]
    await page.goto(f"http://localhost:{port}")
    yield browser, page
    await browser.close()
    if proc is not None:
        with contextlib.suppress(TypeError):
            await proc.terminate()
            await proc.communicate()
