from shiritori.game.models import Game
from shiritori.game.serializers import ShiritoriGameSerializer
from shiritori.game.utils import send_message_to_layer

__all__ = (
    "send_lobby_update",
    "send_game_updated",
)


def send_lobby_update(game: Game | dict, *, update_type: str = "game_created"):
    if game is None:
        return

    if isinstance(game, Game):
        game = ShiritoriGameSerializer(game).data
    send_message_to_layer(
        "lobby",
        {
            "type": update_type,
            "data": game,
        }
    )


def send_game_updated(game: Game | dict, *, update_type: str = "game_updated"):
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
