from unittest.mock import patch

import pytest

from shiritori.game.helpers import aconvert_game_to_json, convert_to_camel

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


@pytest.fixture(scope="module", autouse=True)
def mock_player_disconnect_task():
    with patch("shiritori.game.tasks.player_disconnect_task") as mock:
        yield mock


async def test_consumer_sends_payload_on_connect(game_consumer):
    consumer, game, player_1 = game_consumer
    await consumer.connect()
    result = await consumer.receive_json_from()
    assert result == {
        "type": "connected",
        "data": {
            "game": convert_to_camel(await aconvert_game_to_json(game)),
            "selfPlayer": player_1.id,
        },
    }
