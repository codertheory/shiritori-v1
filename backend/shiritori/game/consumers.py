import sentry_sdk
from asgiref.sync import sync_to_async
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from djangorestframework_camel_case.settings import api_settings
from djangorestframework_camel_case.util import camelize

from shiritori.game import tasks
from shiritori.game.helpers import aconvert_game_to_json, aget_player_from_cookie, disconnect_player
from shiritori.game.models import Game, GameStatus, Player
from shiritori.game.serializers import ShiritoriGameSerializer

__all__ = (
    "GameLobbyConsumer",
    "GameConsumer",
)


class CamelizedWebSocketConsumer(AsyncJsonWebsocketConsumer):
    async def send_json(self, content, close=False):
        return await super().send_json(camelize(content, **api_settings.JSON_UNDERSCOREIZE), close)


class GameLobbyConsumer(CamelizedWebSocketConsumer):
    @staticmethod
    def get_all_waiting_games():
        all_waiting_games = Game.objects.filter(status=GameStatus.WAITING)
        return ShiritoriGameSerializer(all_waiting_games, many=True).data

    async def connect(self):
        await self.accept()
        await self.channel_layer.group_add("lobby", self.channel_name)
        serialized_games = await sync_to_async(self.get_all_waiting_games)()
        await self.send_json(serialized_games)

    async def disconnect(self, code):
        await self.channel_layer.group_discard("lobby", self.channel_name)

    async def game_created(self, event):
        await self.send_json(event)

    async def game_updated(self, event):
        await self.send_json(event)

    async def game_deleted(self, event):
        await self.send_json(event)


class GameConsumer(CamelizedWebSocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game_group_name: str | None = None

    async def connect(self):
        try:
            game_id = self.scope["url_route"]["kwargs"]["game_id"]
            self.game_group_name = f"{game_id}"
            self.groups = [self.game_group_name]

            if not (
                game := await Game.objects.filter(id=game_id)
                .exclude(status=GameStatus.FINISHED)
                .prefetch_related("player_set", "gameword_set")
                .afirst()
            ):
                raise DenyConnection("Game does not exist")
            await self.accept()

            if not self.scope["session"].session_key:
                await sync_to_async(self.scope["session"].save)()

            self_player: Player | None = (
                await aget_player_from_cookie(game_id, session_id)
                if (session_id := self.scope["session"].session_key)
                else None
            )
            self_player.is_connected = True
            await self_player.asave()  # type: ignore
            await self.channel_layer.group_add(self.game_group_name, self.channel_name)

            await self.channel_layer.group_send(
                game_id,
                {
                    "type": "player_connected",
                    "data": {
                        "player_id": self_player.id,
                    },
                },
            )

            game_data = await aconvert_game_to_json(game)

            await self.send_json(
                {
                    "type": "connected",
                    "data": {
                        "game": game_data,
                        "self_player": self_player.id if self_player else None,
                    },
                }
            )
        except DenyConnection as e:
            sentry_sdk.capture_exception(e)
            raise e
        except Exception as e:
            sentry_sdk.capture_exception(e)
            raise DenyConnection("Something went wrong") from e

    async def disconnect(self, code):
        game_id = self.scope["url_route"]["kwargs"]["game_id"]
        if not self.scope["session"].session_key:
            return
        player = await disconnect_player(game_id, self.scope["session"].session_key)
        if player:
            tasks.player_disconnect_task.delay(self.scope["session"].session_key)
            await self.channel_layer.group_send(
                game_id,
                {
                    "type": "player_disconnected",
                    "data": {
                        "player_id": player.id,
                    },
                },
            )
        await self.channel_layer.group_discard(self.game_group_name, self.channel_name)

    async def game_updated(self, event):
        await self.send_json(event)

    async def game_timer_updated(self, event):
        await self.send_json(event)

    async def player_connected(self, event):
        await self.send_json(event)

    async def player_disconnected(self, event):
        await self.send_json(event)
