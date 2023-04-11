import pytest

from shiritori.game.utils import calculate_score


@pytest.mark.parametrize(
    "word, duration, expected_score",
    [
        ("test", 3.1, 9),
        ("test", 10, 7),
        ("test", 15, 6),
        ("test", 20, 5),
    ],
)
def test_calculate_score(word, duration, expected_score):
    assert calculate_score(word, duration) == expected_score


def test_calculate_score_with_none_raises_type_error():
    with pytest.raises(TypeError):
        calculate_score("test", None)  # type: ignore


def test_calculate_score_with_negative_duration_raises_value_error():
    with pytest.raises(ValueError):
        calculate_score("test", -1)


def test_calculate_score_with_empty_word_raises_value_error():
    with pytest.raises(ValueError):
        calculate_score("", 10)
