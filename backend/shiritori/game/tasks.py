import time

from celery import Task, shared_task
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import OperationalError
from django.db.models import Q

from shiritori.game.events import (
    send_game_start_countdown,
    send_game_start_countdown_end,
    send_game_start_countdown_start,
)
from shiritori.game.models import Game, GameStatus, Player, Word
from shiritori.game.utils import mock_stream_closer

__all__ = ("game_worker_task", "load_dictionary_task", "player_disconnect_task", "start_game_task")

TASK_TIME_LIMIT = 60 * 60 * 24  # 24 hours


@shared_task(
    time_limit=TASK_TIME_LIMIT,
    soft_time_limit=TASK_TIME_LIMIT,
    ignore_result=True,
    bind=True,
)
def game_worker_task(self: Task, game_id):
    mock_stream_closer()
    Game.objects.filter(~Q(task_id=self.request.id), id=game_id).update(task_id=self.request.id)
    try:
        Game.run_turn_loop(game_id, self.request.id)
        Game.objects.filter(id=game_id, task_id=self.request.id).update(task_id=None)
    except ValidationError:
        pass
    except OperationalError:
        self.retry(countdown=5)


@shared_task(
    time_limit=TASK_TIME_LIMIT,
    soft_time_limit=TASK_TIME_LIMIT,
    ignore_result=True,
)
def load_dictionary_task(locale: str = "en"):
    words = Word.load_dictionary(locale)
    return {"status": "success", "word_count": len(words), "locale": locale}


@shared_task(
    time_limit=TASK_TIME_LIMIT,
    soft_time_limit=TASK_TIME_LIMIT,
    ignore_result=True,
)
def player_disconnect_task(player_id: str):
    time.sleep(5 if settings.DEBUG else 60)
    if player := Player.objects.filter(id=player_id, is_connected=False).first():
        player.leave()


@shared_task(
    time_limit=TASK_TIME_LIMIT,
    soft_time_limit=TASK_TIME_LIMIT,
    ignore_result=True,
)
def start_game_task(game_id: str):
    game = Game.objects.filter(id=game_id, status=GameStatus.WAITING).first()
    if not game:
        return
    send_game_start_countdown_start(game_id)
    for timer in range(3, 0, -1):
        send_game_start_countdown(game_id, timer)
        time.sleep(1.25)
    send_game_start_countdown_end(game_id)
    game.start()
    game_worker_task.delay(game_id)
