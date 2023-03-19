from typing import Any

from asgiref.sync import sync_to_async
from djangorestframework_camel_case.settings import api_settings
from djangorestframework_camel_case.util import camelize
from rest_framework.utils.serializer_helpers import ReturnDict

from shiritori.game.models import Game, Player
from shiritori.game.serializers import ShiritoriGameSerializer, ShiritoriPlayerSerializer

__all__ = (
    "convert_to_camel",
    "convert_game_to_json",
    "convert_games_to_json",
    "convert_player_to_json",
    "get_player_from_cookie",
)


def convert_to_camel(data: ReturnDict[Any]):
    return camelize(data, **api_settings.JSON_UNDERSCOREIZE)


@sync_to_async
def convert_game_to_json(game: Game) -> ReturnDict[Game] | ReturnDict:
    return ShiritoriGameSerializer(instance=game).data


@sync_to_async
def convert_games_to_json(games: list[Game]) -> ReturnDict[Game] | ReturnDict:
    return ShiritoriGameSerializer(instance=games, many=True).data


@sync_to_async
def convert_player_to_json(player: Player) -> ReturnDict[Player] | ReturnDict:
    return ShiritoriPlayerSerializer(instance=player).data


@sync_to_async
def get_player_from_cookie(game_id: str, session_key: str) -> Player | None:
    return Player.get_by_session_key(game_id, session_key)
