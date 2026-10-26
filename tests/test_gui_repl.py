"""GUI tests for the console REPL (non-BASIC languages).

These need a display, so they are skipped on headless machines unless a
virtual X server is used (``xvfb-run -a python -m pytest``).
"""

import os
from unittest import mock

import pytest

pytestmark = pytest.mark.skipif(
    not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")),
    reason="needs a graphical display (try xvfb-run -a)",
)


@pytest.fixture(scope="module")
def _window(tmp_path_factory):
    settings = tmp_path_factory.mktemp("settings") / "settings.json"
    with mock.patch("gui.app.SETTINGS_FILE", settings):
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
    _window.language_var.set("Pascal")
    _window.output_text.delete("1.0", "end")
    _window.reset_repl()
    _window.turtle_canvas.delete("all")
    _window.root.update()
    return _window


def _submit(app, line):
    app.input_entry.insert(0, line)
    app._submit_input()
    app.root.update()


def _output(app):
    return app.output_text.get("1.0", "end")


def test_repl_evaluates_a_statement(app):
    _submit(app, "writeln(2 + 2);")

    assert ">writeln(2 + 2);" in _output(app)
    assert "\n4\n" in _output(app)


def test_repl_keeps_variables_between_lines(app):
    _submit(app, "x := 6;")
    _submit(app, "writeln(x * 7);")

    assert "\n42\n" in _output(app)
    assert app.repl_language == "pascal"


def test_repl_reports_errors(app, monkeypatch):
    _submit(app, "writeln(1);")  # start the session first

    def boom(_line):
        raise RuntimeError("boom")

    monkeypatch.setattr(app.repl_interpreter, "execute_line", boom)
    _submit(app, "anything")

    assert "?ERROR: boom" in _output(app)


def test_repl_does_not_print_the_startup_banner(app):
    _submit(app, "writeln(1);")

    assert "Interpreter ready" not in _output(app)


def test_repl_restarts_when_the_language_changes(app):
    _submit(app, "x := 6;")
    first = app.repl_interpreter

    app.language_var.set("Logo")
    _submit(app, "PRINT 1")

    assert app.repl_language == "logo"
    assert app.repl_interpreter is not first


def test_repl_draws_on_the_turtle_canvas(app):
    app.language_var.set("Logo")
    app.root.update()

    _submit(app, "FD 40")

    assert app.turtle_canvas.find_all(), "the turtle drew nothing"


def test_reset_repl_forgets_the_session(app):
    _submit(app, "x := 6;")
    app.reset_repl()

    assert app.repl_interpreter is None
    assert "REPL reset." in _output(app)


def test_basic_still_uses_direct_mode(app):
    app.language_var.set("BASIC")
    app.root.update()

    _submit(app, "PRINT 2+2")

    assert "\n4\n" in _output(app)
    assert app.repl_interpreter is None  # direct mode, not the REPL
