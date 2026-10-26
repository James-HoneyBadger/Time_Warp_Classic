"""Streaming, stdin and error-line reporting for Python/Perl/JavaScript."""

import shutil
import time

import pytest

from core.interpreter import Time_WarpInterpreter

requires_perl = pytest.mark.skipif(shutil.which("perl") is None, reason="needs perl")
requires_node = pytest.mark.skipif(
    shutil.which("node") is None and shutil.which("nodejs") is None,
    reason="needs node",
)


@pytest.fixture
def interp():
    machine = Time_WarpInterpreter()
    machine.max_iterations = None
    return machine


def _record(interp):
    """Wrap log_output so we can see when each line arrived."""
    arrivals = []
    started = time.monotonic()
    original = interp.log_output

    def timed(text):
        arrivals.append((time.monotonic() - started, str(text)))
        original(text)

    interp.log_output = timed
    return arrivals


def test_python_output_streams_while_running(interp):
    """Output appears as it is printed, not in one burst at exit."""
    arrivals = _record(interp)
    interp.run_program(
        'import time\nprint("first")\ntime.sleep(1.2)\nprint("second")\n',
        language="python",
    )

    first = next(t for t, line in arrivals if line == "first")
    second = next(t for t, line in arrivals if line == "second")
    assert second - first >= 0.6


def test_python_script_reads_console_input(interp):
    """input() is fed from lines typed at the IDE console."""
    interp.input_buffer.extend(["Ada"])
    arrivals = _record(interp)

    interp.run_program('name = input("Name: ")\nprint("Hi " + name)\n', language="python")

    assert any("Hi Ada" in line for _t, line in arrivals)
    assert interp.input_buffer == []


def test_python_error_reports_the_script_line(interp):
    interp.run_program("x = 1\ny = 1 / 0\n", language="python")

    assert interp.error_history
    assert interp.error_history[0]["line"] == 2
    assert "ZeroDivisionError" in interp.error_history[0]["message"]


@requires_perl
def test_perl_error_reports_the_script_line(interp):
    interp.run_program('my $x = 1;\ndie "boom";\n', language="perl")

    assert interp.error_history
    assert interp.error_history[0]["line"] == 2
    assert "boom" in interp.error_history[0]["message"]


@requires_perl
def test_perl_output_streams(interp):
    arrivals = _record(interp)
    interp.run_program('print "one\\n";\nsleep(1);\nprint "two\\n";\n', language="perl")

    first = next(t for t, line in arrivals if line.strip() == "one")
    second = next(t for t, line in arrivals if line.strip() == "two")
    assert second - first >= 0.6


@requires_node
def test_javascript_error_uses_the_user_script_frame(interp):
    """Node's internal frames must not become the reported line."""
    interp.run_program('let x = 1;\nthrow new Error("boom");\n', language="javascript")

    assert interp.error_history
    assert interp.error_history[0]["line"] == 2


def test_stop_resets_for_the_next_subprocess_run(interp):
    """A stopped Python run must not abort the following one."""
    ticks = {"n": 0}

    def pump():
        ticks["n"] += 1
        if ticks["n"] > 3:
            interp.stop_program()

    interp.pump_callback = pump
    interp.run_program("import time\ntime.sleep(5)\n", language="python")
    assert interp.interrupted is True

    interp.pump_callback = None
    interp.run_program('print("second run")\n', language="python")

    assert interp.interrupted is False


def test_runtime_version_is_reported(interp):
    """get_version() must not report a working runtime as unavailable."""
    version = interp.python_executor.get_version()

    assert "not available" not in version
