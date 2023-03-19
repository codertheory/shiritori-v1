import typing

import pytest
from channels.testing import WebsocketCommunicator

from shiritori.game.models import Game, GameStatus

pytestmark = [pytest.mark.django_db, pytest.mark.asyncio]


async def test_connect_lobby_with_no_games(lobby_consumer: WebsocketCommunicator):
    data = await lobby_consumer.receive_json_from()
    assert data == []


async def test_connect_lobby_with_games(
    sample_games: typing.List[Game],
    lobby_consumer: WebsocketCommunicator,
):
    data = await lobby_consumer.receive_json_from()
    assert len(data) == len(sample_games)
    sample_game_ids = [g.id for g in sample_games]
    for game in data:
        assert game["id"] in sample_game_ids
        assert game["status"] == GameStatus.WAITING
