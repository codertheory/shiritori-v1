from django.apps import AppConfig


class GameConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shiritori.game"

    def ready(self) -> None:
        import shiritori.game.signals  # noqa: F401
