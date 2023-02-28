from shiritori.game.utils import calculate_score


def test_calculate_score():
    assert calculate_score("test", 5) == 9.0
    assert calculate_score("test", 10) == 7.5
    assert calculate_score("test", 15) == 6.0
    assert calculate_score("test", 20) == 5.0
