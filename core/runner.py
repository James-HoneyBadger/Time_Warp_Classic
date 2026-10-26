"""Headless execution of a program.

This is the engine behind exported runners and the ``--run`` command line: it
uses the same interpreter as the IDE but writes to stdout, so no window is
opened and no display is required.
"""

from __future__ import annotations

import contextlib
import io
import sys

from core.interpreter import Time_WarpInterpreter

# Exit codes shared by the CLI and exported runners.
EXIT_OK = 0
EXIT_PROGRAM_ERROR = 1


def run_source(program, language, stream=None):
    """Run *program* in *language* and return a process exit code.

    Output goes to *stream* (stdout by default).  The code is
    :data:`EXIT_OK` when the program finished without reporting an error and
    :data:`EXIT_PROGRAM_ERROR` otherwise.
    """
    with contextlib.redirect_stdout(io.StringIO()):
        # The constructor announces itself; that is IDE chrome, not output.
        interpreter = Time_WarpInterpreter()
    interpreter.max_iterations = None
    interpreter.console_banner = False
    interpreter.turtle_console = False

    if stream is not None:
        _redirect_stdout(interpreter, stream)

    try:
        interpreter.run_program(program, language=language)
    except Exception as exc:  # noqa: BLE001 - a runner reports, never crashes
        print(f"?ERROR: {exc}", file=stream or sys.stdout)
        return EXIT_PROGRAM_ERROR

    return EXIT_PROGRAM_ERROR if interpreter.error_history else EXIT_OK


def _redirect_stdout(interpreter, stream):
    """Send the interpreter's console output to *stream* instead of stdout."""
    def log_output(text):
        print(text, file=stream)

    interpreter.log_output = log_output
