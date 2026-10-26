"""Document handling: save/save-as, dirty tracking, status bar, error jumps."""

import os
import tkinter as tk
import tkinter.filedialog as filedialog

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


def _type(app, text):
    app.editor_text.delete("1.0", "end")
    app.editor_text.insert("1.0", text)
    app.root.update()


def test_editing_marks_the_document_modified(app):
    """The title and status bar show unsaved changes."""
    _type(app, '10 PRINT "X"')

    assert app.modified is True
    assert app.root.title().startswith("Untitled *")
    assert app.status_file.cget("text").endswith("*")


def test_save_writes_the_buffer_and_clears_the_marker(app, tmp_path, monkeypatch):
    """Save writes to the chosen path and stops showing the modified marker."""
    target = tmp_path / "program.bas"
    monkeypatch.setattr(
        filedialog, "asksaveasfilename", lambda **kwargs: str(target)
    )
    _type(app, '10 PRINT "SAVED"')

    assert app.save_file() is True
    assert target.read_text(encoding="utf-8").strip() == '10 PRINT "SAVED"'
    assert app.modified is False
    assert app.current_file == str(target)
    assert app.root.title().startswith("program.bas")


def test_second_save_reuses_the_file(app, tmp_path, monkeypatch):
    """Ctrl+S after the first save does not ask for a path again."""
    target = tmp_path / "again.bas"
    monkeypatch.setattr(filedialog, "asksaveasfilename", lambda **kwargs: str(target))
    _type(app, "10 REM first")
    app.save_file()

    _type(app, "20 REM second")
    monkeypatch.setattr(
        filedialog,
        "asksaveasfilename",
        lambda **kwargs: pytest.fail("Save must not prompt once a path is known"),
    )
    assert app.save_file() is True

    assert "20 REM second" in target.read_text(encoding="utf-8")


def test_save_uses_the_language_extension(app, monkeypatch):
    """Save As proposes the extension that matches the selected language."""
    seen = {}

    def fake(**kwargs):
        seen.update(kwargs)
        return ""

    monkeypatch.setattr(filedialog, "asksaveasfilename", fake)
    app.language_var.set("BASIC")
    app.save_file_as()

    assert seen["defaultextension"] == ".bas"
    assert seen["filetypes"][0][1] == "*.bas"


def test_new_file_can_be_cancelled_when_modified(app, monkeypatch):
    """A cancelled prompt keeps the buffer intact."""
    import tkinter.messagebox as messagebox

    _type(app, "10 REM work in progress")
    monkeypatch.setattr(messagebox, "askyesnocancel", lambda *a, **k: None)

    app.new_file()

    assert app.editor_text.get("1.0", "end-1c").strip() == "10 REM work in progress"


def test_new_file_discards_when_user_declines_to_save(app, monkeypatch):
    """Answering 'No' throws the changes away, like the dialog promises."""
    import tkinter.messagebox as messagebox

    _type(app, "10 REM temporary")
    monkeypatch.setattr(messagebox, "askyesnocancel", lambda *a, **k: False)

    app.new_file()

    assert app.editor_text.get("1.0", "end-1c").strip() == ""
    assert app.modified is False


def test_status_bar_reports_cursor_position(app):
    _type(app, "10 PRINT\n20 PRINT")
    app._text_widget().mark_set(tk.INSERT, "2.0")
    app._update_cursor_status()

    assert app.status_cursor.cget("text") == "Ln 2, Col 1"


def test_error_lines_are_clickable(app):
    """Clicking '?ERROR IN n' selects that line in the editor."""
    _type(app, "10 PRINT 1\n20 PRINT 2\n30 PRINT 3")
    app.output_text.delete("1.0", "end")
    app.output_text.insert("1.0", "?ERROR IN 3: bad thing\n")
    app.root.update()

    box = app.output_text.bbox("1.0")
    assert box, "output text is not laid out yet"
    x, y, _w, h = box
    assert app._error_line_at(x + 5, y + h // 2) == 3

    app._goto_editor_line(3)
    assert app._text_widget().tag_ranges("highlight")


def test_loading_a_file_leaves_it_unmodified(app, tmp_path, monkeypatch):
    """Opening a file must not immediately show it as edited."""
    program = tmp_path / "loaded.bas"
    program.write_text('10 PRINT "LOADED"\n', encoding="utf-8")
    monkeypatch.setattr(filedialog, "askopenfilename", lambda **kwargs: str(program))

    app.load_file()
    app.root.update()   # let the queued <<Modified>> event run

    assert app.modified is False
    assert "*" not in app.root.title()


def test_find_wraps_around_from_the_caret(app):
    """Find Next at the end of the buffer wraps to the first match."""
    from gui.dialogs import FindDialog

    _type(app, "alpha beta alpha")
    app.root.update()
    dialog = FindDialog(app.root, app.editor_text, app.output_text)
    dialog.search_var.set("alpha")
    try:
        dialog._do_find()
        assert tuple(str(i) for i in app.editor_text.tag_ranges("sel")) == ("1.0", "1.5")
        dialog._do_find()
        assert tuple(str(i) for i in app.editor_text.tag_ranges("sel")) == ("1.11", "1.16")
    finally:
        dialog.dialog.destroy()


def test_replace_all_replaces_every_occurrence(app):
    from gui.dialogs import ReplaceDialog

    _type(app, "one two one")
    app.root.update()
    dialog = ReplaceDialog(app.root, app.editor_text, app.output_text)
    dialog.search_var.set("one")
    dialog.replace_var.set("1")
    try:
        dialog._replace_all()
    finally:
        dialog.dialog.destroy()

    assert app.editor_text.get("1.0", "end-1c") == "1 two 1"
