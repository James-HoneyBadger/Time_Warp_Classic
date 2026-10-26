"""Exiting the IDE while a program is still running must not hang."""

import os
import time

import pytest

pytestmark = pytest.mark.skipif(
    not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")),
    reason="needs a graphical display (try xvfb-run -a)",
)


def test_exit_during_a_run_stops_the_interpreter():
    """Destroying the window mid-run must end the run loop, not spin forever."""
    import tkinter.messagebox as messagebox

    from gui.app import TimeWarpApp

    app = TimeWarpApp()
    app.root.update()
    app.language_var.set("BASIC")
    app.editor_text.delete("1.0", "end")
    app.editor_text.insert("1.0", "10 GOTO 10")

    messagebox.askyesno = lambda *args, **kwargs: True
    app.root.after(400, app.exit_app)

    started = time.monotonic()
    app.run_code()
    elapsed = time.monotonic() - started

    assert elapsed < 10, "run_code never returned after the window was closed"
    assert app._program_running is False
    assert app.interpreter.stop_requested is True
    assert app.interpreter.interrupted is True
