from django.urls import path

from shiritori.game import consumers

websocket_patterns = [
    path("ws/game/<str:game_id>/", consumers.GameConsumer.as_asgi()),
    path("ws/game_lobby/", consumers.GameLobbyConsumer.as_asgi()),
]
