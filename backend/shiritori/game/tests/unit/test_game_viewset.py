from unittest.mock import patch

import pytest
from rest_framework.test import APIClient

from shiritori.game.models import Game, Player, GameStatus

pytestmark = pytest.mark.django_db


@pytest.fixture(scope='module', autouse=True)
def mock_game_worker_task():
    with patch('shiritori.game.tasks.game_worker_task') as mock:
        yield mock


def test_game_create_view(drf: APIClient, default_game_settings):
    response = drf.post("/api/game/", {"settings": default_game_settings}, format="json")
    assert response.status_code == 201
    assert response.data["id"] is not None


def test_join_game_view(drf: APIClient, game: Game):
    assert game.player_count == 0

    response = drf.post(f"/api/game/{game.id}/join/", {"name": "test"}, format="json")
    assert response.status_code == 201

    player = game.players.first()
    assert response.data["id"] == player.id

    sessionid = response.cookies.get("sessionid")
    assert sessionid is not None

    assert game.player_count == 1
    assert player.name == "test"
    assert player.session_key == sessionid.value


def test_leave_game_view(drf: APIClient, game: Game, player: Player):
    player.session_key = drf.session.session_key
    game.join(player)
    assert game.player_count == 1
    response = drf.post(f"/api/game/{game.id}/leave/")

    assert response.status_code == 204

    assert game.player_count == 0


def test_take_turn_game_view(drf: APIClient, started_game: Game, sample_words: list[str]):
    game = started_game
    player = game.players.first()
    player2 = game.players.last()
    player.session_key = drf.session.session_key
    player.save()
    assert game.current_player == player
    assert game.current_turn == 0
    assert game.word_count == 0
    response = drf.post(
        f"/api/game/{game.id}/turn/",
        {"word": sample_words[0], "duration": 5},
        format="json",
    )
    game.refresh_from_db()
    assert response.status_code == 204
    assert game.current_player == player2
    assert game.current_turn == 1
    assert game.word_count == 1
    assert game.words.first().word == "test"
    assert game.words.first().score == 9
    assert game.words.first().player == player

    # Calling take turn again will raise a 401 because the session_key is for player1

    response = drf.post(
        f"/api/game/{game.id}/turn/",
        {"word": sample_words[1], "duration": 5},
        format="json",
    )
    assert response.status_code == 400


def test_start_game_view_as_host(drf: APIClient, unstarted_game: Game):
    game = unstarted_game
    player = game.players.first()
    player.session_key = drf.session.session_key
    player.save()

    response = drf.post(f"/api/game/{game.id}/start/")
    assert response.status_code == 204

    game.refresh_from_db()
    assert game.status == GameStatus.PLAYING
    assert game.current_player == player
    assert game.current_turn == 0
    assert game.word_count == 0


def test_start_game_view_as_non_host(drf: APIClient, unstarted_game: Game):
    game = unstarted_game
    player = game.players.first()
    drf.session._set_session_key(player.session_key)  # pylint: disable=protected-access
    response = drf.post(f"/api/game/{game.id}/start/")
    assert response.status_code == 400

    game.refresh_from_db()
    assert game.status == GameStatus.WAITING
    assert game.current_player is None
    assert game.current_turn == 0
    assert game.word_count == 0
