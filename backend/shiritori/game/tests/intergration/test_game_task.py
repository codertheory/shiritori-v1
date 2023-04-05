from unittest.mock import MagicMock

import pytest

from shiritori.game.models import Game


@pytest.mark.django_db
def test_game_turn_loop(mocker, started_game, sample_words):
    game: Game = started_game
    game.task_id = "test_task_id"
    game.save(force_update=True)
    sleep_mock: MagicMock = mocker.patch("shiritori.game.models.wait", return_value=None)
    mocker.patch("shiritori.game.events.send_game_timer_updated", return_value=None)
    game.run_turn_loop(game_id=game.id, task_id="test_task_id")
    game.is_finished = False
    game.save(update_fields=["status"])
    assert sleep_mock.call_count == game.settings.turn_time * game.settings.max_turns
