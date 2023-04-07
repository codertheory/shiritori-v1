from unittest.mock import patch

import pytest
import pytest_asyncio
from asgiref.sync import sync_to_async

from shiritori.game.events import (
    send_game_timer_updated,
    send_game_updated,
    send_lobby_update,
    send_player_joined,
    send_player_left,
    send_turn_taken,
)
from shiritori.game.models import Game

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


@pytest_asyncio.fixture(name="event_consumer")
async def fixture_event_consumer(game_consumer):
    consumer, game, player_1 = game_consumer
    await consumer.connect()
    await consumer.receive_json_from()  # consume connected message
    await consumer.receive_json_from()  # consume player joined message
    yield consumer, game, player_1


@pytest.fixture(scope="module", autouse=True)
def mock_player_disconnect_task():
    with patch("shiritori.game.tasks.player_disconnect_task") as mock:
        yield mock


async def test_send_lobby_update(lobby_consumer, game: Game):
    await sync_to_async(send_lobby_update)(game)
    data = await lobby_consumer.receive_json_from()
    assert data == []
    data = await lobby_consumer.receive_json_from()
    assert data["type"] == "game_created"


async def test_send_game_updated(event_consumer):
    consumer, game, player_1 = event_consumer
    await sync_to_async(send_game_updated)(game)
    data = await consumer.receive_json_from()
    assert data["type"] == "game_updated"


async def test_send_game_timer_updated(event_consumer):
    consumer, game, player_1 = event_consumer
    await sync_to_async(send_game_timer_updated)(game.id, 10)
    data = await consumer.receive_json_from()
    assert data == {
        "type": "game_timer_updated",
        "data": 10,
    }


async def test_send_player_joined(event_consumer):
    consumer, game, player_1 = event_consumer
    await sync_to_async(send_player_joined)(game.id, player_1)
    data = await consumer.receive_json_from()
    assert data["type"] == "player_joined"


async def test_send_player_updated(event_consumer):
    consumer, game, player_1 = event_consumer
    await sync_to_async(send_player_joined)(game.id, player_1)
    data = await consumer.receive_json_from()
    assert data["type"] == "player_joined"


async def test_send_player_left(event_consumer):
    consumer, game, player_1 = event_consumer
    await sync_to_async(send_player_left)(game.id, player_1.id)
    data = await consumer.receive_json_from()
    assert data["type"] == "player_left"


async def test_send_turn_taken(event_consumer):
    consumer, game, player_1 = event_consumer
    await sync_to_async(send_turn_taken)(game.id, {"word": "test"})
    data = await consumer.receive_json_from()
    assert data["type"] == "turn_taken"
