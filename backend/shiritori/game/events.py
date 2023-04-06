import typing

from shiritori.game.helpers import convert_game_to_json, convert_gameword_to_json, convert_player_to_json
from shiritori.game.utils import send_message_to_layer

if typing.TYPE_CHECKING:
    from shiritori.game.models import Game, GameWord, Player

__all__ = (
    "send_lobby_update",
    "send_game_updated",
    "send_game_timer_updated",
    "send_player_joined",
    "send_player_left",
    "send_player_updated",
    "send_turn_taken",
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


def send_player_joined(game_id: str, player: typing.Union["Player", dict]):
    if not isinstance(player, dict):
        player = convert_player_to_json(player)

    send_message_to_layer(
        game_id,
        {
            "type": "player_joined",
            "data": player,
        },
    )


def send_player_updated(game_id: str, player: typing.Union["Player", dict]):
    if not isinstance(player, dict):
        player = convert_player_to_json(player)

    send_message_to_layer(
        game_id,
        {
            "type": "player_updated",
            "data": player,
        },
    )


def send_player_left(game_id: str, player_id: str):
    send_message_to_layer(
        game_id,
        {
            "type": "player_left",
            "data": player_id,
        },
    )


def send_turn_taken(game_id: str, word: typing.Union["GameWord", dict]):
    if not isinstance(word, dict):
        word = convert_gameword_to_json(word)

    send_message_to_layer(
        game_id,
        {
            "type": "turn_taken",
            "data": word,
        },
    )
