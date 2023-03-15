import pytest

from shiritori.game.utils import calculate_score


def test_calculate_score():
    assert calculate_score("test", 5) == 9.0
    assert calculate_score("test", 10) == 7.5
    assert calculate_score("test", 15) == 6.0
    assert calculate_score("test", 20) == 5.0
    with pytest.raises(TypeError):
        calculate_score("test", None)  # type: ignore
    with pytest.raises(ValueError):
        calculate_score("test", -1)
