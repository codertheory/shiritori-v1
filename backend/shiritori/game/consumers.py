from asgiref.sync import sync_to_async
from channels.exceptions import DenyConnection
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from shiritori.game.models import Game, GameStatus
from shiritori.game.serializers import ShiritoriGameSerializer


class GameLobbyConsumer(AsyncJsonWebsocketConsumer):

    @staticmethod
    def get_all_waiting_games():
        all_waiting_games = Game.objects.filter(
            status=GameStatus.WAITING
        )
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


class GameConsumer(AsyncJsonWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.game_group_name: str | None = None

    async def connect(self):
        game_id = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = f"{game_id}"
        self.groups = [self.game_group_name]

        if await Game.objects.filter(id=game_id).exclude(status=GameStatus.FINISHED).aexists():

            await self.accept()

            await sync_to_async(self.scope['session'].save)()

            await self.channel_layer.group_add(self.game_group_name, self.channel_name)
        else:
            raise DenyConnection("Game does not exist")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.game_group_name, self.channel_name)

    async def game_updated(self, event):
        await self.send_json(event)
