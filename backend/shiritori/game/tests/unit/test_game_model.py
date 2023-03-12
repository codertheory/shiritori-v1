import pytest
from django.core.exceptions import ValidationError

from shiritori.game.models import GameStatus, Game, Word, GameWord

pytestmark = pytest.mark.django_db


def test_create_game(un_saved_game):
    game = un_saved_game
    assert game.settings is None
    game.save()
    assert game.id is not None
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


def test_join_started_game(started_game):
    with pytest.raises(ValidationError):
        started_game.join('John')


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


def test_host_leaving_properly_deletes_and_recalculates(started_game):
    player = started_game.players.first()
    player2 = started_game.players.last()
    started_game.leave(player)
    assert started_game.host == player2
    assert started_game.player_count == 1
    assert started_game.players.first() == player2
    started_game.leave(player2)
    assert started_game.host is None
    assert started_game.player_count == 0
    assert started_game.status == GameStatus.FINISHED


def test_start_game_with_one_player(game, player):
    game.join(player)
    with pytest.raises(ValidationError):
        game.start()


def test_start_game_with_two_players(game, player, human_player_2):
    game.join(player)
    game.join(human_player_2)
    game.start()
    assert game.status == GameStatus.PLAYING
    assert game.current_player == player
    assert game.current_turn == 0
    assert game.last_word is not None


def test_start_started_game(started_game):
    with pytest.raises(ValidationError):
        started_game.start()


def test_calculate_current_player(game, player, human_player_2):
    game.join(player)
    game.join(human_player_2)
    game.start()
    setup_and_assert_current_player(1, game, human_player_2)
    setup_and_assert_current_player(2, game, player)


def setup_and_assert_current_player(current_turn, game, expected_player):
    game.current_turn = current_turn
    game.calculate_current_player()
    assert game.current_player == expected_player


def test_recalculate_host_is_called_when_leaves_game(game, player, human_player_2):
    game.join(player)
    game.join(human_player_2)
    assert game.host == player
    game.leave(player)
    assert game.host == human_player_2


def test_recalculate_host_called_when_nothing_changes(game, player, human_player_2):
    game.join(player)
    assert game.host == player
    game.join(human_player_2)
    assert game.host == player
    game.recalculate_host()
    assert game.host == player
    game.recalculate_host()
    assert game.host == player


def test_recalculate_host_with_no_players(game):
    with pytest.raises(ValidationError):
        game.recalculate_host()


def test_can_current_player_take_turn(game, player, human_player_2):
    game.join(player)
    game.join(human_player_2)
    game.start()
    game.current_player = human_player_2
    game.turn_time_left = 10
    pytest.raises(ValidationError, game.can_take_turn, player.session_key)
    game.can_take_turn(human_player_2.session_key)


def test_can_current_player_take_turn_with_no_time_left(game, player, human_player_2):
    game.join(player)
    game.join(human_player_2)
    game.start()
    game.current_player = human_player_2
    game.turn_time_left = 0
    pytest.raises(ValidationError, game.can_take_turn, human_player_2.session_key)


def test_can_current_player_take_turn_when_game_status_is_not_playing(game, player, human_player_2):
    game.join(player)
    game.join(human_player_2)
    game.start()
    game.current_player = human_player_2
    game.turn_time_left = 10
    game.status = GameStatus.WAITING
    pytest.raises(ValidationError, game.can_take_turn, human_player_2.session_key)


def test_take_turn_with_word_non_existent_word(started_game: Game,
                                               sample_words: list[str]):  # pylint: disable=unused-argument
    with pytest.raises(ValidationError) as exec_info:
        started_game.turn_time_left = 10
        session_key = started_game.current_player.session_key
        started_game.take_turn(session_key, 'invalid')
    assert exec_info.value.message == 'Word not found in dictionary.'


def test_take_turn_with_word_already_used(started_game: Game,
                                          sample_words: list[str]):  # pylint: disable=unused-argument
    with pytest.raises(ValidationError) as exec_info:
        started_game.turn_time_left = 10
        GameWord.objects.create(word=sample_words[0], game=started_game)
        session_key = started_game.current_player.session_key
        started_game.take_turn(session_key, sample_words[0])
    assert exec_info.value.message == 'Word already used.'


def test_take_turn_with_word_not_starting_with_last_word(started_game: Game,
                                                         sample_words: list[str]):  # pylint: disable=unused-argument
    with pytest.raises(ValidationError) as exec_info:
        started_game.turn_time_left = 10
        session_key = started_game.current_player.session_key
        started_game.take_turn(session_key, sample_words[2])
    assert exec_info.value.message == 'Word must start with the last letter of the previous word.'


def test_take_turn_with_word_not_long_enough(started_game: Game,
                                             sample_words: list[str]):  # pylint: disable=unused-argument
    with pytest.raises(ValidationError) as exec_info:
        started_game.turn_time_left = 10
        session_key = started_game.current_player.session_key
        Word.objects.create(word='to')
        started_game.take_turn(session_key, "to")
    assert exec_info.value.message == 'Word must be at least 3 characters long.'


def test_end_turn_updates_current_player_and_turn(started_game):
    first_player, next_player = started_game.players
    started_game.end_turn()
    assert first_player.score == -15
    assert started_game.current_player == next_player
    assert started_game.current_turn == 1
