import contextlib
import time

import pytest
from celery.result import AsyncResult

from shiritori.game.models import Game
from shiritori.game.tasks import game_worker_task


@pytest.mark.celery(result_backend='redis://')
@pytest.mark.django_db
def test_game_task(mocker, started_game, sample_words, celery_worker):  # pylint: disable=unused-argument
    game: Game = started_game[0]
    game.save(force_update=True)
    sleep_mock = mocker.patch("shiritori.game.tasks.wait", return_value=None)
    task: AsyncResult = game_worker_task.delay(game.id)
    time.sleep(1)
    game.is_finished = False
    game.save(update_fields=["status"])
    with contextlib.suppress(Exception):
        result = task.get(timeout=1)
    sleep_mock.assert_called_with(1.25)
    sleep_mock.assert_called_once()
    assert result is None
