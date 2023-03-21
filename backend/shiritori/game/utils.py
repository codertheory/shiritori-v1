# The modifiers are applied in order, so the first one that matches is used.
# The duration is in seconds. The score is multiplied by the modifier.
import random
import string
import time

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

LENGTH_MODIFIER = 1.25
DURATION_MODIFIERS = {5: 1.8, 10: 1.5, 15: 1.2}


def chunk_list(iterable, n):
    for i in range(0, len(iterable), n):
        yield iterable[i : i + n]


def calculate_score(word: str, duration: int | float) -> float:
    """
    Calculate the score for a word.
    The score is based on the length of the word
    and the duration it took to enter.
    :param word: str - The word to calculate the score for.
    :param duration: int - The duration it took to enter the word.
    :return: float - The score for the word.
    """
    if not isinstance(duration, (int, float)):
        raise TypeError("Duration must be an integer or float.")
    if duration < 0:
        raise ValueError("Duration must be a positive number.")
    score = len(word) * LENGTH_MODIFIER
    for bucket, modifier in DURATION_MODIFIERS.items():
        if duration <= bucket:
            score *= modifier
            break
    return int(round(score, 2))


def generate_random_letter():
    """
    Generate a random letter.
    :return: str - A random letter.
    """
    return random.choice(string.ascii_lowercase)


def send_message_to_layer(channel_name: str, message: dict):
    """
    Send a message to a channel layer.
    :param channel_name: str - The channel name to send the message to.
    :param message: dict - The message to send.
    """
    return async_to_sync(asend_message_to_layer)(channel_name, message)


async def asend_message_to_layer(channel_name: str, message: dict):
    """
    Send a message to a channel layer.
    :param channel_name: str - The channel name to send the message to.
    :param message: dict - The message to send.
    """
    if channel_layer := get_channel_layer():
        try:
            await channel_layer.group_send(channel_name, message)
            # await channel_layer.close_pools()
        except Exception as error:  # pylint: disable=broad-except
            print(f"Error sending message to channel layer: {error}")


def wait():
    time.sleep(1.25)
