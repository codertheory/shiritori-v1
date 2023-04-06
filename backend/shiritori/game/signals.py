from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from shiritori.game.events import (
    send_game_updated,
    send_player_joined,
    send_player_left,
    send_player_updated,
    send_turn_taken,
)
from shiritori.game.models import Game, GameWord, Player


@receiver(post_save, sender=Game)
def game_post_save(sender, instance: Game, created, **kwargs):
    send_game_updated(instance)


@receiver(post_save, sender=Player)
def player_post_save(sender, instance: Player, created, **kwargs):
    if created:
        send_player_joined(instance.game.id, instance)
        return
    else:
        send_player_updated(instance.game.id, instance)


@receiver(post_delete, sender=Player)
def player_post_delete(sender, instance: Player, **kwargs):
    if instance.game.player_count == 0:
        instance.game.delete()
        return

    if instance.is_host:
        instance.game.recalculate_host()

    send_player_left(instance.game.id, instance.id)


@receiver(post_save, sender=GameWord)
def game_word_post_save(sender, instance: GameWord, created, **kwargs):
    if created:
        send_turn_taken(instance.game.id, instance)
