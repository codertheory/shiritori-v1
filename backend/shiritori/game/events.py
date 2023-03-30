import typing

from shiritori.game.helpers import convert_game_to_json
from shiritori.game.utils import send_message_to_layer

if typing.TYPE_CHECKING:
    from shiritori.game.models import Game

__all__ = (
    "send_lobby_update",
    "send_game_updated",
    "send_game_timer_updated",
)


def send_lobby_update(game: typing.Union["Game", dict]):
    if game is None:
        return

    if not isinstance(game, dict):
        game = convert_game_to_json(game)
    send_message_to_layer(
        "lobby",
        {
            "type": "game_created",
            "data": game,
        },
    )


def send_game_updated(game: typing.Union["Game", dict]):
    if game is None:
        return

    if not isinstance(game, dict):
        game = convert_game_to_json(game)
    send_message_to_layer(
        game["id"],
        {
            "type": "game_updated",
            "data": game,
        },
    )


def send_game_timer_updated(game_id: str, turn_time_left: int):
    send_message_to_layer(
        game_id,
        {
            "type": "game_timer_updated",
            "data": turn_time_left,
        },
    )
