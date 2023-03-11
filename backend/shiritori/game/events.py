import typing

from shiritori.game.utils import send_message_to_layer

if typing.TYPE_CHECKING:
    from shiritori.game.models import Game

__all__ = (
    "send_lobby_update",
    "send_game_updated",
)


def send_lobby_update(game: typing.Union["Game", dict], *, update_type: str = "game_created"):
    if game is None:
        return

    if isinstance(game, Game):
        from shiritori.game.serializers import ShiritoriGameSerializer
        game = ShiritoriGameSerializer(game).data
    send_message_to_layer(
        "lobby",
        {
            "type": update_type,
            "data": game,
        }
    )


def send_game_updated(game: typing.Union["Game", dict], *, update_type: str = "game_updated"):
    from shiritori.game.serializers import ShiritoriGameSerializer
    from shiritori.game.models import Game
    if game is None:
        return

    if isinstance(game, Game):
        game = ShiritoriGameSerializer(game).data
    send_message_to_layer(
        game['id'],
        {
            "type": update_type,
            "data": game,
        }
    )
