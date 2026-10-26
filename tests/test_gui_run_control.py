"""GUI-level tests for running and stopping programs in the IDE.

These need a display, so they are skipped on headless machines unless a
virtual X server is used (``xvfb-run -a python -m pytest``).
"""

import os
import time

import pytest

pytestmark = pytest.mark.skipif(
    not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")),
    reason="needs a graphical display (try xvfb-run -a)",
)


@pytest.fixture(scope="module")
def _window():
    """One real window per module: the first X11 map costs seconds here."""
    from gui.app import TimeWarpApp

    application = TimeWarpApp()
    application.root.update()
    yield application
    try:
        application.root.destroy()
    except Exception:  # noqa: BLE001 - a test may have closed it
        pass


@pytest.fixture
def app(_window):
    """Shared window, reset to a clean document before each test."""
    for task in _window.root.tk.call("after", "info"):
        try:
            _window.root.after_cancel(task)
        except Exception:  # noqa: BLE001
            pass
    _window.language_var.set("PILOT")
    _window.editor_text.delete("1.0", "end")
    _window.output_text.delete("1.0", "end")
    _window.input_buffer.clear()
    _window.current_file = None
    _window.root.update()
    _window.modified = False
    _window.interpreter.reset()
    _window._update_title()
    _window._update_status()
    return _window


def _load(app, language, program):
    app.language_var.set(language)
    app.editor_text.delete("1.0", "end")
    app.editor_text.insert("1.0", program)


def test_endless_program_can_be_stopped_from_the_ide(app):
    """Run → Stop ends an endless loop instead of freezing or capping it."""
    _load(app, "BASIC", "10 GOTO 10\n20 END")
    app.root.after(400, app.stop_program)

    started = time.monotonic()
    app.run_code()
    elapsed = time.monotonic() - started

    assert elapsed < 15, "run_code blocked after the stop request"
    assert app._program_running is False
    assert "BREAK" in app.output_text.get("1.0", "end")
    assert str(app.stop_button["state"]) == "disabled"
    assert str(app.run_button["state"]) == "normal"


def test_input_is_read_from_the_console_bar(app):
    """INPUT pauses and resumes when the user submits a line."""
    _load(app, "BASIC", '10 INPUT A\n20 PRINT "GOT "; A\n30 END')

    def answer():
        app.input_entry.insert(0, "7")
        app._submit_input()

    app.root.after(300, answer)
    app.root.after(6000, app.stop_program)
    app.run_code()

    output = app.output_text.get("1.0", "end")
    assert "GOT 7" in output
    assert app.interpreter.interrupted is False


def test_turtle_pane_only_shows_for_drawing_languages(app):
    """The graphics canvas is hidden for languages that cannot draw."""
    def panes():
        return [str(pane) for pane in app.right_paned.panes()]

    app.language_var.set("PILOT")
    assert app.graphics_visible is False
    assert str(app.graphics_frame) not in panes()

    app.language_var.set("Logo")
    assert app.graphics_visible is True
    assert str(app.graphics_frame) in panes()


def test_run_and_stop_controls_are_visible(app):
    """The action bar must be fully visible: not clipped vertically or horizontally."""
    app.root.update()

    assert app.run_button.winfo_ismapped()
    assert app.stop_button.winfo_ismapped()
    assert app.input_entry.winfo_ismapped()

    bar = app._layout_widgets["button_frame"]
    rightmost = max(
        child.winfo_x() + child.winfo_width() for child in bar.winfo_children()
    )
    assert rightmost <= bar.winfo_width(), "action buttons overflow the window"


def test_each_run_starts_clean(app):
    """RUN discards variables from the previous run, like the originals."""
    _load(app, "BASIC", "10 LET Z = 5\n20 END")
    app.run_code()
    assert "Z" in app.interpreter.variables

    _load(app, "BASIC", "10 REM different program\n20 END")
    app.run_code()
    assert "Z" not in app.interpreter.variables


def test_console_runs_basic_statements(app):
    """Direct mode answers a bare statement typed at the console."""
    app.language_var.set("BASIC")
    app.input_entry.insert(0, "PRINT 6*7")
    app._submit_input()

    output = app.output_text.get("1.0", "end")
    assert ">PRINT 6*7" in output
    assert "42" in output


def test_direct_mode_input_is_read_from_the_console_bar(app):
    """An immediate INPUT statement can receive an answer without F5."""
    app.language_var.set("BASIC")

    def answer():
        app.input_entry.insert(0, "23")
        app._submit_input()

    app.root.after(100, answer)
    app.input_entry.insert(0, "INPUT A")
    app._submit_input()
    app.basic_console.submit("PRINT A")

    assert "23" in app.output_text.get("1.0", "end")
    assert app._program_running is False


def test_direct_mode_input_survives_an_earlier_stop(app):
    """A latched Stop must not make the next console INPUT cancel itself."""
    app.language_var.set("BASIC")
    app.interpreter.stop_requested = True  # left behind by a stopped run

    def answer():
        app.input_entry.insert(0, "7")
        app._submit_input()

    app.root.after(100, answer)
    app.input_entry.insert(0, "INPUT A")
    app._submit_input()
    app.basic_console.submit("PRINT A")

    assert "7" in app.output_text.get("1.0", "end")


def test_console_stores_numbered_lines(app):
    """A numbered line typed at the console lands in the editor."""
    app.language_var.set("BASIC")
    app.editor_text.delete("1.0", "end")
    app.input_entry.insert(0, '10 PRINT "HI"')
    app._submit_input()

    assert app.editor_text.get("1.0", "end-1c").strip() == '10 PRINT "HI"'
    assert "OK" in app.output_text.get("1.0", "end")


def test_console_run_executes_the_program_and_reports_ready(app):
    """RUN from the console executes the program in memory."""
    app.language_var.set("BASIC")
    app.editor_text.delete("1.0", "end")
    app.editor_text.insert("1.0", '10 PRINT "CONSOLE RUN"')
    app.input_entry.insert(0, "RUN")
    app._submit_input()

    output = app.output_text.get("1.0", "end")
    assert "CONSOLE RUN" in output
    assert "READY." in output
    assert app._program_running is False


def test_console_follows_the_language_selector(app):
    """After running Logo, a console statement must use the newly chosen language."""
    _load(app, "Logo", "REPEAT 2 [FORWARD 10]")
    app.run_code()

    app.language_var.set("BASIC")
    app.editor_text.delete("1.0", "end")
    app.input_entry.insert(0, "PRINT 6*7")
    app._submit_input()

    assert "42" in app.output_text.get("1.0", "end")
