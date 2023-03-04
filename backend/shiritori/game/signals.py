from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from shiritori.game.events import send_game_updated, send_lobby_update
from shiritori.game.models import Game, Player, GameWord


@receiver(post_save, sender=Game)
def game_post_save(sender, instance: Game, created, **kwargs):  # pylint: disable=unused-argument
    send_game_updated(instance)
    send_lobby_update(instance, update_type="game_updated" if created else "game_created")


@receiver(post_save, sender=Player)
def player_post_save(sender, instance: Player, created, **kwargs):  # pylint: disable=unused-argument
    send_game_updated(instance.game)
    send_lobby_update(instance.game, update_type="player_updated" if created else "player_created")


@receiver(post_delete, sender=Player)
def player_post_delete(sender, instance: Player, **kwargs):  # pylint: disable=unused-argument
    send_game_updated(instance.game)


@receiver(post_save, sender=GameWord)
def game_word_post_save(sender, instance: GameWord, created, **kwargs):  # pylint: disable=unused-argument
    if created:
        send_game_updated(instance.game)
