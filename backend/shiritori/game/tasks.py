import time

from celery import shared_task
from channels.exceptions import ChannelFull
from django.db.models import F

from shiritori.game.events import send_game_updated
from shiritori.game.models import Game, GameStatus

__all__ = (
    "send_game_updated_task",
    "game_worker_task",
    "start_game_task",
)

TASK_TIME_LIMIT = 60 * 60 * 24  # 24 hours


def wait():
    time.sleep(1.25)


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

)
def game_worker_task(game_id):
    game = Game.objects.filter(id=game_id)
    if not game.exists():
        return
    while not game.filter(status=GameStatus.FINISHED).exists():
        if game.filter(turn_time_left__gt=0).exists():
            game.update(turn_time_left=F("turn_time_left") - 1)
            send_game_updated(game.first())
            wait()  # sleep for 1.25 seconds to allow for any networking issues
        else:
            # if the game timer is 0, end the turn
            # and start the next turn
            game.first().end_turn()
            send_game_updated_task.delay(game_id)


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
