from django.db import models


class GameStatus(models.TextChoices):
    WAITING = "WAITING", "Waiting"
    PLAYING = "PLAYING", "Playing"
    FINISHED = "FINISHED", "Finished"


class GameLocales(models.TextChoices):
    EN = "en", "English"


class PlayerType(models.TextChoices):
    HUMAN = "HUMAN", "human"
    BOT = "BOT", "bot"
    SPECTATOR = "SPECTATOR", "spectator"
    WINNER = "WINNER", "winner"
