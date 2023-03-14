from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status, serializers
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import action
from rest_framework.fields import CharField
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import ReadOnlyModelViewSet

from shiritori.game.auth import RequiresSessionAuth
from shiritori.game.models import Game
from shiritori.game.serializers import ShiritoriTurnSerializer, ShiritoriPlayerSerializer, ShiritoriGameSerializer, \
    CreateGameSerializer, JoinGameSerializer, EmptySerializer
from shiritori.game.tasks import game_worker_task


class GameViewSet(ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = ShiritoriGameSerializer
    authentication_classes = []
    permission_classes = []

    @staticmethod
    def get_success_headers(data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def get_serializer_class(self):
        match self.action:
            case "create":
                return CreateGameSerializer
            case "start" | "turn":
                return ShiritoriTurnSerializer
            case "join":
                return JoinGameSerializer
            case "leave":
                return EmptySerializer
            case _:
                return super().get_serializer_class()

    @extend_schema(responses={201: ShiritoriGameSerializer})
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        game = serializer.save()
        return Response(status=status.HTTP_201_CREATED, data=ShiritoriGameSerializer(game).data)

    @action(detail=True, methods=["post"], authentication_classes=[SessionAuthentication])
    def start(self, request, pk=None):  # pylint: disable=unused-argument
        game = self.get_object()
        session_key = request.session.session_key
        try:
            game.start(session_key)
            game_worker_task.delay(game.id)
        except ValidationError as error:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": "Invalid start", "errors": error})
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(responses={201: inline_serializer("Player", {"id": CharField(read_only=True)})})
    @action(detail=True, methods=["post"])
    def join(self, request, pk=None):  # pylint: disable=unused-argument
        if not request.session or not request.session.session_key:
            request.session.save()

        game = self.get_object()
        serializer: ShiritoriPlayerSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        player = serializer.save()
        player.session_key = request.session.session_key
        game.join(player)

        headers = self.get_success_headers(serializer.validated_data)
        return Response(
            data={"id": player.id},
            status=status.HTTP_201_CREATED,
            headers=headers,
        )

    @action(detail=True, methods=["post"], authentication_classes=[RequiresSessionAuth])
    def turn(self, request, pk=None):  # pylint: disable=unused-argument
        game = self.get_object()
        serializer: ShiritoriTurnSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            game.take_turn(request.session.session_key, **serializer.validated_data)
        except ValidationError as error:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"detail": error.message})

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["post"],
            authentication_classes=[RequiresSessionAuth])
    @extend_schema(responses={204: {}})
    def leave(self, request, pk=None):  # pylint: disable=unused-argument
        session_key = request.session.session_key
        game = self.get_object()
        game.leave(session_key)
        return Response(status=status.HTTP_204_NO_CONTENT)
