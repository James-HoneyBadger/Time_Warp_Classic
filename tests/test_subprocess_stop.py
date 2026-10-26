"""Stop/streaming tests for the subprocess-backed languages."""

import time

import pytest

from core.interpreter import Time_WarpInterpreter


@pytest.fixture
def interp():
    """Headless interpreter (console output goes to stdout)."""
    return Time_WarpInterpreter()


def test_python_script_output_is_streamed(interp, capsys):
    """Python programs run and their output reaches the IDE console."""
    interp.run_program('print("first")\nprint("second")\n', language="python")

    captured = capsys.readouterr().out
    assert "first" in captured
    assert "second" in captured
    assert interp.interrupted is False


def test_python_script_can_be_stopped(interp):
    """A runaway script is killed when the host requests a stop."""
    ticks = {"n": 0}

    def pump():
        ticks["n"] += 1
        if ticks["n"] > 3:
            interp.stop_program()

    interp.pump_callback = pump
    started = time.monotonic()
    interp.run_program("import time\ntime.sleep(30)\n", language="python")
    elapsed = time.monotonic() - started

    assert interp.interrupted is True
    assert elapsed < 10
