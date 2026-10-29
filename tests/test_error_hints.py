"""Tests for the actionable hints printed under recognised errors."""

import io
from contextlib import redirect_stdout

import pytest

from core.error_hints import hint_for
from core.interpreter import Time_WarpInterpreter


@pytest.fixture
def interp():
    """A headless interpreter, like the IDE uses."""
    machine = Time_WarpInterpreter()
    machine.max_iterations = 5_000
    return machine


def run(interp, language, program):
    """Run *program* and return everything it printed."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        interp.run_program(program, language=language)
    return buffer.getvalue()


@pytest.mark.parametrize(
    "message, fragment",
    [
        ("Division by zero in expression", "divisor"),
        ("NameError: name 'total' is not defined", "give the name a value"),
        ("IndentationError: expected an indented block", "indent"),
        ("ModuleNotFoundError: No module named 'yaml'", "not installed"),
        ("Program stopped: Maximum iterations reached", "never finishes"),
        ("Perl script timed out after 30s", "time limit"),
        ("Unknown command type 'basik' for command: PRNT", "not a command"),
    ],
)
def test_known_errors_get_a_hint(message, fragment):
    hint = hint_for(message)

    assert hint and fragment in hint


def test_unknown_errors_get_no_hint():
    assert hint_for("something the rules do not cover") is None
    assert hint_for("") is None


def test_hint_points_at_the_language_reference():
    assert "docs/languages/BASIC_REFERENCE.md" in hint_for(
        "Division by zero in expression", "basic"
    )


def test_error_is_followed_by_a_hint_line(interp):
    output = run(interp, "basic", "10 PRINT 1/0")
    lines = output.splitlines()
    index = next(i for i, line in enumerate(lines) if line.startswith("?ERROR IN 1"))

    assert lines[index + 1].startswith("?HINT:")
    assert interp.error_history[-1]["hint"]


def test_hints_can_be_switched_off(interp):
    interp.error_hints = False

    output = run(interp, "basic", "10 PRINT 1/0")

    assert "?ERROR IN 1" in output
    assert "?HINT:" not in output
    assert interp.error_history[-1]["hint"] is None
