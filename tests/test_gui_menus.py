"""GUI tests for the Debug and Performance menu entries.

These need a display, so they are skipped on headless machines unless a
virtual X server is used (``xvfb-run -a python -m pytest``).
"""

import os
import tkinter as tk

import pytest

pytestmark = pytest.mark.skipif(
    not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")),
    reason="needs a graphical display (try xvfb-run -a)",
)


@pytest.fixture(scope="module")
def _window():
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
    _window.language_var.set("BASIC")
    _window.editor_text.delete("1.0", "end")
    _window.output_text.delete("1.0", "end")
    _window.input_buffer.clear()
    _window.interpreter.reset()
    _window.interpreter.set_debug_mode(False)
    _window.interpreter.set_profiling(False)
    _window.interpreter.breakpoints.clear()
    _window.interpreter.error_history = []
    _window.debug_enabled.set(False)
    _window.root.update()
    return _window


def _menu(app, label):
    """Return the submenu of the top-level *label* (e.g. "Debug")."""
    menubar = app.root.nametowidget(app.root["menu"])
    for index in range(menubar.index("end") + 1):
        if menubar.type(index) == "cascade" and menubar.entrycget(index, "label") == label:
            return app.root.nametowidget(menubar.entrycget(index, "menu"))
    raise AssertionError(f"no {label!r} menu in the menu bar")


def _invoke(app, menu_label, item_label):
    menu = _menu(app, menu_label)
    for index in range(menu.index("end") + 1):
        if menu.type(index) == "separator":
            continue
        if menu.entrycget(index, "label") == item_label:
            menu.invoke(index)
            app.root.update()
            return
    raise AssertionError(f"no {item_label!r} entry in the {menu_label} menu")


def _output(app):
    return app.output_text.get("1.0", "end")


def _program(app, text):
    app.editor_text.delete("1.0", "end")
    app.editor_text.insert("1.0", text)


def _first_text(widget):
    for child in widget.winfo_children():
        if isinstance(child, tk.Text):
            return child
        found = _first_text(child)
        if found is not None:
            return found
    return None


# --------------------------------------------------------------------- Debug

def test_debug_menu_toggles_debug_mode(app):
    _invoke(app, "Debug", "Enable Debug Mode")
    assert app.interpreter.debug_mode is True
    assert app.debug_enabled.get() is True

    _invoke(app, "Debug", "Enable Debug Mode")
    assert app.interpreter.debug_mode is False


def test_breakpoint_stops_the_run_and_menu_clears_it(app):
    _program(app, '10 PRINT "ALPHA"\n20 PRINT "BETA"\n')
    app.interpreter.toggle_breakpoint(2)
    app.interpreter.set_debug_mode(True)
    app.run_code()

    run_output = _output(app)
    assert "BREAK IN 2" in run_output
    assert "ALPHA" in run_output and "BETA" not in run_output

    _invoke(app, "Debug", "Clear All Breakpoints")
    assert app.interpreter.breakpoints == set()


def test_toggle_breakpoint_at_cursor_marks_the_line(app):
    _program(app, '10 PRINT "ALPHA"\n20 PRINT "BETA"\n')
    app._text_widget().mark_set(tk.INSERT, "2.0")

    _invoke(app, "Debug", "Toggle Breakpoint at Cursor")

    assert app.interpreter.is_breakpoint(2)
    assert "Set breakpoint on line 2" in _output(app)
    marks = [str(index) for index in app._text_widget().tag_ranges(app.BREAKPOINT_TAG)]
    assert len(marks) == 2 and marks[0].startswith("2.")

    _invoke(app, "Debug", "Toggle Breakpoint at Cursor")
    assert not app.interpreter.is_breakpoint(2)
    assert app._text_widget().tag_ranges(app.BREAKPOINT_TAG) == ()


def test_f9_toggles_a_breakpoint(app):
    _program(app, '10 PRINT "ALPHA"\n')
    app._text_widget().mark_set(tk.INSERT, "1.0")
    app.root.focus_force()

    app.root.event_generate("<F9>")
    app.root.update()

    assert app.interpreter.is_breakpoint(1)


def test_replacing_the_document_drops_breakpoints(app):
    _program(app, '10 PRINT "ALPHA"\n')
    app.interpreter.toggle_breakpoint(1)
    app._refresh_breakpoint_marks()

    app.clear_editor()

    assert app.interpreter.breakpoints == set()
    assert app._text_widget().tag_ranges(app.BREAKPOINT_TAG) == ()


def test_show_error_history_lists_recorded_errors(app):
    app.interpreter.log_error("boom", 7)
    before = set(app.root.winfo_children())

    _invoke(app, "Debug", "Show Error History")

    dialogs = [
        widget for widget in app.root.winfo_children()
        if widget not in before and isinstance(widget, tk.Toplevel)
    ]
    assert dialogs, "no history window appeared"
    try:
        text = _first_text(dialogs[0]).get("1.0", "end")
    finally:
        dialogs[0].destroy()
    assert "Line 7" in text and "boom" in text


def test_clear_error_history(app):
    app.interpreter.log_error("boom", 7)
    _invoke(app, "Debug", "Clear Error History")

    assert app.interpreter.error_history == []


def test_console_tron_updates_the_debug_menu(app):
    app.input_entry.insert(0, "TRON")
    app._submit_input()

    assert app.interpreter.debug_mode is True
    assert app.debug_enabled.get() is True

    app.input_entry.insert(0, "TROFF")
    app._submit_input()
    assert app.debug_enabled.get() is False


# --------------------------------------------------------------- Performance

def test_show_statistics_reports_interpreter_data(app):
    _invoke(app, "Performance", "Show Statistics")

    text = _output(app)
    assert "Performance Statistics" in text
    assert "Expression Cache" in text
    assert "\u274c" not in text


def test_optimize_performance_reports_results(app):
    _invoke(app, "Performance", "Optimize Performance")

    text = _output(app)
    assert "cache_cleared=True" in text
    assert "UI:" in text and "objects collected" in text
    assert "\u2705 Performance optimizations applied!" in text


def test_profiling_toggle_records_timings(app):
    _invoke(app, "Performance", "Toggle Profiling")
    assert app.interpreter.enable_profiling is True

    _program(app, '10 PRINT "PROFILED"\n20 END\n')
    app.run_code()
    assert "PROFILED" in _output(app)

    _invoke(app, "Performance", "Show Statistics")
    assert "Profiling: on" in _output(app)
    assert "lines timed" in _output(app)

    _invoke(app, "Performance", "Toggle Profiling")
    assert app.interpreter.enable_profiling is False


def test_statistics_report_ui_and_cache_figures(app):
    app.interpreter.evaluate_expression("2 + 2")
    app.interpreter.evaluate_expression("2 + 2")

    _invoke(app, "Performance", "Show Statistics")

    text = _output(app)
    assert "Expression Cache:" in text and "1 hits" in text
    assert "Event pumps/sec:" in text
    assert "Output panel:" in text
    assert "Memory Usage:" in text
