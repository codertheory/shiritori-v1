from celery import shared_task, Task
from channels.exceptions import ChannelFull
from django.db import OperationalError

from shiritori.game.events import send_game_updated
from shiritori.game.models import Game

__all__ = (
    "send_game_updated_task",
    "game_worker_task",
    "start_game_task",
)

TASK_TIME_LIMIT = 60 * 60 * 24  # 24 hours


@shared_task(
    max_retries=3,
    time_limit=TASK_TIME_LIMIT,
    soft_time_limit=TASK_TIME_LIMIT,
    ignore_result=True,
    throws=(ChannelFull,),
)
def send_game_updated_task(game_id):
    game = Game.objects.filter(id=game_id)
    if not game.exists():
        return
    send_game_updated(game.first())


@shared_task(
    time_limit=TASK_TIME_LIMIT,
    soft_time_limit=TASK_TIME_LIMIT,
    ignore_result=True,
    bind=True,
)
def game_worker_task(self: Task, game_id):
    try:
        Game.run_turn_loop(game_id)
    except OperationalError as error:
        self.retry(exc=error, args=(game_id,))
    except Exception as error:  # pylint: disable=broad-except
        print(error)


@shared_task(
    time_limit=TASK_TIME_LIMIT,
    soft_time_limit=TASK_TIME_LIMIT,
    ignore_result=True,

)
def start_game_task(game_id):
    game = Game.get_startable_game_by_id(game_id)
    if not game.exists():
        return
    game.first().start()
    send_game_updated_task.delay(game_id)
    game_worker_task.delay(game_id)
