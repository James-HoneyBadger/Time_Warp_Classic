"""Execution-control tests for the Time_Warp interpreter.

These cover the host hooks that make the IDE usable on long or endless
programs: cooperative pumping, user-requested stops, console input, and
the classic "RUN starts clean" behaviour.
"""

import io
from contextlib import redirect_stdout

import pytest

from core.interpreter import Time_WarpInterpreter


@pytest.fixture
def interp():
    """A headless interpreter with a bounded safety cap."""
    machine = Time_WarpInterpreter()
    machine.max_iterations = 50_000
    return machine


def test_endless_loop_is_stopped_by_host(interp):
    """A GOTO loop runs until the user stops it — no iteration cap."""
    interp.max_iterations = None
    seen = {"lines": 0}

    def pump():
        seen["lines"] += 1
        if seen["lines"] >= 40:
            interp.stop_program()

    interp.pump_callback = pump
    interp.run_program('10 GOTO 10\n20 END', language="basic")

    assert interp.interrupted is True
    assert interp.running is False
    assert seen["lines"] >= 40
    assert not any("Maximum iterations" in e["message"] for e in interp.error_history)


def test_headless_runs_keep_the_safety_cap(interp):
    """Without a host, the iteration guard still protects unattended runs."""
    interp.max_iterations = 100
    interp.run_program('10 GOTO 10\n20 END', language="basic")

    assert interp.running is False
    assert any("Maximum iterations" in e["message"] for e in interp.error_history)


def test_stop_flag_is_reset_for_each_run(interp):
    """A previous stop must not abort the next RUN."""
    interp.stop_program()
    interp.run_program('10 PRINT "HI"\n20 END', language="basic")

    assert interp.interrupted is False


def test_console_input_provider_is_used(interp):
    """INPUT reads from the host console instead of a modal dialog."""
    interp.input_provider = lambda prompt="": "42"
    interp.run_program(
        '10 INPUT "Number: "; A\n20 PRINT "Value "; A\n30 END',
        language="basic",
    )

    assert interp.stop_requested is False
    assert str(interp.variables.get("A")) == "42"


def test_cancelled_input_stops_the_program(interp):
    """Cancelling the console prompt ends the run instead of feeding a blank line."""
    calls = {"n": 0}

    def provider(prompt=""):
        calls["n"] += 1
        return None

    interp.input_provider = provider
    interp.run_program('10 INPUT A\n20 PRINT "SHOULD NOT PRINT"\n30 END', language="basic")

    assert calls["n"] == 1
    assert interp.stop_requested is True


def test_reset_discards_previous_run_state(interp):
    """Classic RUN semantics: variables do not leak between runs."""
    interp.variables["KEEP"] = 1
    interp.reset()

    assert interp.variables == {}


def test_headless_output_uses_stdout(interp):
    """The headless interpreter still reports completion to the console."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        interp.run_program('10 PRINT "DONE"\n20 END', language="basic")

    assert "DONE" in buffer.getvalue()


def test_stop_while_waiting_for_input_reports_break(interp):
    """Stopping at an INPUT prompt is a BREAK, not a normal completion."""
    def provider(prompt=""):
        interp.stop_program()
        return None

    interp.input_provider = provider
    interp.run_program('10 INPUT A\n20 PRINT "SHOULD NOT PRINT"\n30 END', language="basic")

    assert interp.interrupted is True


def test_array_access_inside_functions_is_substituted(interp):
    """INT((A(4) - A(1)) / A(1)) must evaluate, not fall back to text."""
    interp.run_program(
        "10 DIM A(4)\n20 LET A(1) = 180\n30 LET A(4) = 172", language="basic"
    )

    assert interp.evaluate_expression("A(4)") == 172
    assert interp.evaluate_expression("INT((A(4) - A(1)) / A(1) * 10000) / 100") == -4.44
    assert interp.evaluate_expression("INT(3.9)") == 3


def test_breakpoint_uses_the_line_number_shown_in_the_ide(interp):
    """A breakpoint on line 1 must stop before line 1 runs."""
    out = io.StringIO()
    interp.set_debug_mode(True)
    interp.toggle_breakpoint(1)

    with redirect_stdout(out):
        interp.run_program('10 PRINT "FIRST"\n20 PRINT "SECOND"\n', language="basic")

    printed = out.getvalue()
    assert "BREAK IN 1" in printed
    assert "FIRST" not in printed
    # A stopped run reports BREAK, not a completed one.
    assert "READY." not in printed


def test_error_line_numbers_follow_the_editor_lines(interp):
    """Leading blank lines shift the program, not the reported line."""
    out = io.StringIO()
    with redirect_stdout(out):
        interp.run_program('\n10 PRINT "A"\n20 PRINT 1/0', language="basic")

    assert "?ERROR IN 3" in out.getvalue()


def test_stop_reaches_pascal_loop_bodies(interp):
    """Stop must end a Pascal loop instead of waiting for the iteration cap."""
    interp.max_iterations = None
    ticks = {"n": 0}

    def pump():
        ticks["n"] += 1
        if ticks["n"] >= 3:
            interp.stop_program()

    interp.pump_callback = pump
    out = io.StringIO()
    with redirect_stdout(out):
        interp.run_program(
            "begin\n  while 1 = 1 do begin\n    writeln('X');\n  end;\nend.",
            language="pascal",
        )

    printed = out.getvalue()
    assert interp.interrupted is True
    assert printed.count("X") == 0
    assert "BREAK IN" in printed
    assert not any("maximum iterations" in line for line in printed.splitlines())


def test_breakpoints_toggle_and_clear(interp):
    assert interp.is_breakpoint(3) is False
    interp.toggle_breakpoint(3)
    assert interp.is_breakpoint(3) is True
    assert interp.toggle_breakpoint(3) == set()
    assert interp.is_breakpoint(3) is False

    interp.toggle_breakpoint(4)
    interp.toggle_breakpoint(5)
    interp.clear_breakpoints()
    assert interp.breakpoints == set()


def test_stop_reaches_logo_repeat(interp):
    """Logo REPEAT bodies are interruptible as well."""
    interp.max_iterations = None
    ticks = {"n": 0}

    def pump():
        ticks["n"] += 1
        if ticks["n"] >= 3:
            interp.stop_program()

    interp.pump_callback = pump
    out = io.StringIO()
    with redirect_stdout(out):
        interp.run_program("REPEAT 100000 [PRINT 1]", language="logo")

    printed = out.getvalue()
    assert interp.interrupted is True
    assert len([line for line in printed.splitlines() if line.strip() == "1"]) < 100000
    assert "BREAK IN" in printed
