from django.db.models.signals import post_save
from django.dispatch import receiver

from shiritori.game.events import send_game_updated, send_lobby_update
from shiritori.game.models import Game


@receiver(post_save, sender=Game)
def game_post_save(sender, instance, created, **kwargs):  # pylint: disable=unused-argument
    send_game_updated(instance)
    send_lobby_update(instance, update_type="game_updated" if created else "game_created")
