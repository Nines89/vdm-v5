
from core.dice_engine import roll_v5


def fixed_rng(values):
    iterator = iter(values)
    return lambda _: next(iterator)


def test_normal_success():

    result = roll_v5(
        pool=3,
        hunger=1,
        difficulty=2,
        rng=fixed_rng([7, 5, 3])
    )

    assert result["outcome"] == "success"
    assert result["successes"] == 2


def test_messy_critical():

    result = roll_v5(
        pool=3,
        hunger=1,
        difficulty=3,
        rng=fixed_rng([9, 6, 9])
    )

    assert result["outcome"] == "messy_critical"
    assert result["successes"] == 5


def test_clean_critical():

    result = roll_v5(
        pool=3,
        hunger=1,
        difficulty=3,
        rng=fixed_rng([9, 9, 5])
    )

    assert result["outcome"] == "critical"


def test_bestial_failure():

    result = roll_v5(
        pool=3,
        hunger=1,
        difficulty=2,
        rng=fixed_rng([1, 3, 0])
    )

    assert result["outcome"] == "bestial_failure"


def test_hunger_cannot_exceed_pool():

    result = roll_v5(
        pool=2,
        hunger=5,
        difficulty=1,
        rng=fixed_rng([0, 0])
    )

    assert result["hunger_dice"] == 2
    assert result["outcome"] == "bestial_failure"
