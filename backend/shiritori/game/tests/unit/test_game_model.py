import pytest
from django.core.exceptions import ValidationError

from shiritori.game.models import GameStatus

pytestmark = pytest.mark.django_db


def test_create_game(un_saved_game):
    game = un_saved_game
    assert game.status == GameStatus.WAITING
    assert game.current_turn == 0
    assert game.last_word is not None
    assert game.current_player is None
    assert game.player_count == 0
    assert game.word_count == 0
    assert game.players.count() == 0
    assert game.words.count() == 0
    assert game.host is None
    assert game.settings is None
    game.save()
    assert game.id is not None
    assert game.created_at is not None
    assert game.updated_at is not None
    assert game.settings is not None


def test_join_game(game, player):
    game.join(player)
    assert game.player_count == 1
    assert game.players.count() == 1
    assert game.host == player
    assert game.players.first() == player


def test_join_game_with_str(game):
    player = game.join('John')
    assert game.player_count == 1
    assert game.players.count() == 1
    assert game.host == player
    assert game.players.first() == player
    assert player.name == 'John'


def test_join_started_game(started_game, player):
    started_game, _, _ = started_game
    with pytest.raises(ValidationError):
        started_game.join(player)


def test_leave_game(game, player):
    game.join(player)
    game.leave(player)
    assert game.player_count == 0
    assert game.players.count() == 0
    assert game.host is None
    assert game.status == GameStatus.FINISHED


def test_leave_game_by_session_key(game, player):
    game.join(player)
    game.leave(player.session_key)
    assert game.player_count == 0
    assert game.players.count() == 0
    assert game.host is None
    assert game.status == GameStatus.FINISHED


def test_host_leaving_properly_deletes_and_recalculates(game, player, player2):
    game.join(player)
    game.join(player2)
    game.start()
    game.leave(player)
    assert game.host == player2
    assert game.player_count == 1
    assert game.players.first() == player2
    game.leave(player2)
    assert game.host is None
    assert game.player_count == 0
    assert game.status == GameStatus.FINISHED


def test_start_game_with_one_player(game, player):
    game.join(player)
    with pytest.raises(ValidationError):
        game.start()


def test_start_game_with_two_players(game, player, player2):
    game.join(player)
    game.join(player2)
    game.start()
    assert game.status == GameStatus.PLAYING
    assert game.current_player == player
    assert game.current_turn == 0
    assert game.last_word is not None


def test_start_started_game(started_game):
    game, _, _ = started_game
    with pytest.raises(ValidationError):
        game.start()


def test_calculate_current_player(game, player, player2):
    game.join(player)
    game.join(player2)
    game.start()
    setup_and_assert_current_player(1, game, player2)
    setup_and_assert_current_player(2, game, player)


def setup_and_assert_current_player(current_turn, game, expected_player):
    game.current_turn = current_turn
    game.calculate_current_player()
    assert game.current_player == expected_player


def test_recalculate_host_is_called_when_leaves_game(game, player, player2):
    game.join(player)
    game.join(player2)
    assert game.host == player
    game.leave(player)
    assert game.host == player2


def test_recalculate_host_called_when_nothing_changes(game, player, player2):
    game.join(player)
    assert game.host == player
    game.join(player2)
    assert game.host == player
    game.recalculate_host()
    assert game.host == player
    game.recalculate_host()
    assert game.host == player


def test_recalculate_host_with_no_players(game):
    with pytest.raises(ValidationError):
        game.recalculate_host()


def test_can_current_player_take_turn(game, player, player2):
    game.join(player)
    game.join(player2)
    game.start()
    game.current_player = player2
    game.turn_time_left = 10
    pytest.raises(ValidationError, game.can_take_turn, player.session_key)
    game.can_take_turn(player2.session_key)


def test_can_current_player_take_turn_with_no_time_left(game, player, player2):
    game.join(player)
    game.join(player2)
    game.start()
    game.current_player = player2
    game.turn_time_left = 0
    pytest.raises(ValidationError, game.can_take_turn, player2.session_key)


def test_can_current_player_take_turn_when_game_status_is_not_playing(game, player, player2):
    game.join(player)
    game.join(player2)
    game.start()
    game.current_player = player2
    game.turn_time_left = 10
    game.status = GameStatus.WAITING
    pytest.raises(ValidationError, game.can_take_turn, player2.session_key)


def test_end_turn_updates_current_player_and_turn(started_game):
    game, player, player2 = started_game
    game.end_turn(duration=5)
    assert game.current_player == player2
    assert game.current_turn == 1
    assert player.score == -1.25
