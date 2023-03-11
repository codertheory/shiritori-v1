import pytest

from shiritori.game.serializers import ShiritoriGameSerializer

pytestmark = pytest.mark.django_db


async def test_consumer_sends_payload_on_connect(game_consumer):
    consumer, game = game_consumer
    assert await consumer.receive_json_from() == {
        "type": "connected",
        "data": {
            "game": ShiritoriGameSerializer(instance=game).data,
            "self_player": None,
        },
    }
