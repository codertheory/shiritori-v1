import random
import string
import time
import typing
import unicodedata
from typing import TypedDict

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

LENGTH_MODIFIER = 1.25
UNUSED_LETTER_MODIFIER = 1.5
MISSED_WORD_PENALTY = -0.25
# The modifiers are applied in order, so the first one that matches is used.
# The duration is in seconds. The score is multiplied by the modifier.
DURATION_MODIFIERS = {5: 1.8, 10: 1.5, 15: 1.2}


def case_insensitive_equal(a: str, b: str) -> bool:
    """
    Check if two strings are equal, ignoring case.
    :param a: str - The first string.
    :param b: str - The second string.
    :return: bool - True if the strings are equal, False otherwise.
    """
    return a.lower() == b.lower()


def chunk_list(iterable, n):
    for i in range(0, len(iterable), n):
        yield iterable[i : i + n]


def normalize_word(word: str | None) -> str:
    """
    Normalize a word. This will lowercase the word and normalize the unicode.
    """
    return unicodedata.normalize("NFKC", word.lower()) if word else None


class EventDict(TypedDict):
    type: typing.Literal[
        "game_created",
        "game_updated",
        "game_timer_updated",
        "game_start_countdown_start",
        "game_start_countdown",
        "game_start_countdown_end",
        "game_start_countdown_cancel",
        "player_connected",
        "player_disconnected",
        "player_joined",
        "player_updated",
        "player_left",
        "turn_taken",
    ]
    data: typing.Any


def calculate_score(word: str | None, duration: int | float, unused_letter: bool = False) -> float:
    """
    Calculate the score for a word.
    The score is based on the length of the word
    and the duration it took to enter.
    :param word: str - The word to calculate the score for.
    :param duration: int - The duration it took to enter the word.
    :param unused_letter: bool - Whether the word used an unused letter.
    :return: float - The score for the word.
    """
    if not isinstance(duration, (int, float)):
        raise TypeError("Duration must be an integer or float.")
    if duration < 0:
        raise ValueError("Duration must be a positive number.")

    if word is None:
        return MISSED_WORD_PENALTY * duration  # penalty for missing a word

    if isinstance(word, str) and not word:
        raise ValueError("Word must be a non-empty string.")
    score = len(word) * LENGTH_MODIFIER
    for bucket, modifier in DURATION_MODIFIERS.items():
        if duration <= bucket:
            score *= modifier
            break
    if unused_letter:
        score *= UNUSED_LETTER_MODIFIER
    return int(round(score, 2))


def generate_random_letter():
    """
    Generate a random letter.
    :return: str - A random letter.
    """
    return random.choice(string.ascii_lowercase)


def send_message_to_layer(channel_name: str, message: EventDict):
    """
    Send a message to a channel layer.
    :param channel_name: str - The channel name to send the message to.
    :param message: dict - The message to send.
    """
    return async_to_sync(asend_message_to_layer)(channel_name, message)


async def asend_message_to_layer(channel_name: str, message: EventDict):
    """
    Send a message to a channel layer.
    :param channel_name: str - The channel name to send the message to.
    :param message: dict - The message to send.
    """
    if channel_layer := get_channel_layer():
        try:
            await channel_layer.group_send(channel_name, message)
            # await channel_layer.close_pools()
        except Exception as error:
            print(f"Error sending message to channel layer: {error}")


def wait():
    time.sleep(1.25)


def mock_stream_closer():
    """
    Quites the closing error in relation to redis.
    """
    from asyncio.streams import StreamWriter

    StreamWriter.close = lambda self: None

    async def mock_wait_closed(self):
        pass

    StreamWriter.wait_closed = mock_wait_closed
