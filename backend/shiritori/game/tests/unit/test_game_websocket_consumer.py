import pytest

from shiritori.game.helpers import convert_game_to_json, convert_player_to_json

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


async def test_consumer_sends_payload_on_connect(game_consumer):
    consumer, game, player_1 = game_consumer
    await consumer.connect()
    result = await consumer.receive_json_from()
    assert result == {
        "type": "connected",
        "data": {
            "game": await convert_game_to_json(game),
            "self_player": await convert_player_to_json(player_1),
        },
    }
