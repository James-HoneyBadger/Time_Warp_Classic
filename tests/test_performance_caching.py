"""Expression-cache behaviour behind Performance → Show Statistics."""

import pytest

from core.interpreter import Time_WarpInterpreter


@pytest.fixture
def interp():
    return Time_WarpInterpreter()


def test_repeated_expression_is_cached(interp):
    assert interp.evaluate_expression("2+2") == 4
    assert interp.evaluate_expression("2+2") == 4

    stats = interp.get_performance_stats()["expression_cache"]
    assert stats["hits"] == 1
    assert stats["misses"] == 1


def test_changing_a_variable_invalidates_the_cache(interp):
    interp.variables["A"] = 5
    assert interp.evaluate_expression("A*2") == 10

    interp.variables["A"] = 9
    assert interp.evaluate_expression("A*2") == 18


def test_rnd_is_never_reused_from_the_cache(interp):
    first = interp.evaluate_expression("RND(1)")
    second = interp.evaluate_expression("RND(1)")

    assert first != second


def test_rnd_inside_a_cached_expression_still_varies(interp):
    interp.variables["A"] = 1
    values = {interp.evaluate_expression("RND(1) + A") for _ in range(5)}

    assert len(values) == 5
