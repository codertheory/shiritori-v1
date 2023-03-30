from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from shiritori.game.events import send_game_updated, send_lobby_update
from shiritori.game.models import Game, GameWord, Player


@receiver(post_save, sender=Game)
def game_post_save(sender, instance: Game, created, **kwargs):
    send_game_updated(instance)
    send_lobby_update(instance)


@receiver(post_save, sender=Player)
def player_post_save(sender, instance: Player, created, **kwargs):
    send_game_updated(instance.game)
    send_lobby_update(instance.game)


@receiver(post_delete, sender=Player)
def player_post_delete(sender, instance: Player, **kwargs):
    send_game_updated(instance.game)


@receiver(post_save, sender=GameWord)
def game_word_post_save(sender, instance: GameWord, created, **kwargs):
    if created:
        send_game_updated(instance.game)
