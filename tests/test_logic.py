from petals.logic import calculate_petals

def test_all_threes():
    dice = [3, 3, 3, 3, 3]
    assert calculate_petals(dice) == 10

def test_all_fives():
    dice = [5, 5, 5, 5, 5]
    assert calculate_petals(dice) == 20

def test_mixed():
    dice = [1, 2, 3, 4, 5]
    assert calculate_petals(dice) == 6
    