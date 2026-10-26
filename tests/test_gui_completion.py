"""GUI-level tests for word completion in the editor.

These need a display, so they are skipped on headless machines unless a
virtual X server is used (``xvfb-run -a python -m pytest``).
"""

import os
import tkinter as tk
from unittest import mock

import pytest

pytestmark = pytest.mark.skipif(
    not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")),
    reason="needs a graphical display (try xvfb-run -a)",
)


class _Key:
    """Stand-in for a Tk key event."""

    def __init__(self, keysym, char="", state=0):
        self.keysym = keysym
        self.char = char
        self.state = state


@pytest.fixture(scope="module")
def _window(tmp_path_factory):
    """One window for the module, with settings kept out of the home folder."""
    settings = tmp_path_factory.mktemp("settings") / "timewarp_settings.json"
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
    """Shared window, reset to a clean BASIC document before each test."""
    _window.completion_popup.hide()
    _window.language_var.set("BASIC")
    _window.editor_text.delete("1.0", "end")
    _window.output_text.delete("1.0", "end")
    _window.completion_enabled.set(True)
    _window.current_completion = True
    _window.root.update()
    return _window


def _type(app, text, cursor=None):
    """Insert *text* and put the caret at *cursor* (default: after it)."""
    app.editor_text.insert("1.0", text)
    app.editor_text.mark_set(tk.INSERT, cursor or f"1.0+{len(text)}c")
    app.root.update()


def test_typing_a_prefix_opens_the_list(app):
    _type(app, "10 PRI")
    app._on_completion_key(_Key("I", "I"))

    assert app.completion_popup.visible
    assert app.completion_popup.items[0] == "PRINT"


def test_enter_inserts_the_selected_word(app):
    _type(app, "10 PRI")
    app._on_completion_key(_Key("I", "I"))

    assert app._on_completion_key_navigation(_Key("Return")) == "break"
    assert app.editor_text.get("1.0", "end-1c") == "10 PRINT"
    assert not app.completion_popup.visible


def test_arrow_keys_move_the_selection(app):
    _type(app, "10 PE")  # PENDOWN / PENUP, so there is something to move to
    app.show_completions(forced=False)
    assert len(app.completion_popup.items) >= 2
    first = app.completion_popup.current()

    app._on_completion_key_navigation(_Key("Down"))
    assert app.completion_popup.current() != first

    app._on_completion_key_navigation(_Key("Up"))
    assert app.completion_popup.current() == first


def test_tab_commits_like_enter(app):
    _type(app, "10 PRIN")
    app.show_completions(forced=False)

    assert app._on_completion_key_navigation(_Key("Tab")) == "break"
    assert app.editor_text.get("1.0", "end-1c").startswith("10 PRINT")


def test_escape_closes_without_changing_the_text(app):
    _type(app, "10 PRI")
    app.show_completions(forced=False)

    assert app._on_completion_key_navigation(_Key("Escape")) == "break"
    assert not app.completion_popup.visible
    assert app.editor_text.get("1.0", "end-1c") == "10 PRI"


def test_navigation_keys_pass_through_when_the_list_is_closed(app):
    _type(app, "10")
    assert app._on_completion_key_navigation(_Key("Down")) is None
    assert app._on_completion_key_navigation(_Key("Return")) is None


def test_ctrl_space_offers_every_word(app):
    _type(app, "")
    app.show_completions(forced=True)

    assert app.completion_popup.visible
    assert len(app.completion_popup.items) > 1


def test_short_prefixes_do_not_pop_up_unasked(app):
    _type(app, "10 P")
    app._on_completion_key(_Key("P", "P"))

    assert not app.completion_popup.visible


def test_no_list_inside_a_comment(app):
    _type(app, "10 REM PRI")
    app._on_completion_key(_Key("I", "I"))

    assert not app.completion_popup.visible


def test_preference_turns_completion_off(app, monkeypatch):
    monkeypatch.setattr(app, "_save_settings", lambda: None)
    app.completion_enabled.set(False)
    app.toggle_completion()

    _type(app, "10 PRI")
    app.show_completions(forced=True)

    assert not app.completion_popup.visible
    assert app.current_completion is False


def test_list_closes_when_a_program_starts(app):
    _type(app, "10 PRI")
    app.show_completions(forced=False)
    assert app.completion_popup.visible

    app.run_code()

    assert not app.completion_popup.visible


def test_language_switch_changes_the_vocabulary(app):
    _type(app, "")
    app.language_var.set("Pascal")
    app.show_completions(forced=True)
    pascal_words = set(app.completion_popup.items)
    app.completion_popup.hide()

    app.language_var.set("BASIC")
    app.show_completions(forced=True)
    basic_words = set(app.completion_popup.items)

    assert "BEGIN" in pascal_words or "WRITELN" in pascal_words
    assert "PRINT" in basic_words or "GOTO" in basic_words


def _press(app, keysym):
    """Send a real key press/release pair through Tk's event loop."""
    editor = app._text_widget()
    editor.event_generate("<KeyPress>", keysym=keysym, when="now")
    editor.event_generate("<KeyRelease>", keysym=keysym, when="now")
    app.root.update()


def test_typing_opens_the_list_through_real_key_events(app):
    """The KeyRelease path carries no char, so it must use the keysym."""
    _type(app, "")
    app._text_widget().focus_force()
    app.root.update()

    for keysym in ("1", "0", "space", "P", "R", "I"):
        _press(app, keysym)

    assert app.editor_text.get("1.0", "end-1c").startswith("10 PRI")
    assert app.completion_popup.visible
    assert "PRINT" in app.completion_popup.items


def test_tab_commits_through_real_key_events(app):
    _type(app, "")
    app._text_widget().focus_force()
    app.root.update()
    for keysym in ("P", "R", "I"):
        _press(app, keysym)

    app._text_widget().event_generate("<Tab>", when="now")
    app.root.update()

    assert app.editor_text.get("1.0", "end-1c") == "PRINT"


def test_typing_a_space_closes_the_list(app):
    _type(app, "")
    app._text_widget().focus_force()
    app.root.update()
    for keysym in ("P", "R", "I"):
        _press(app, keysym)
    assert app.completion_popup.visible

    _press(app, "space")

    assert not app.completion_popup.visible


def _menu(app, label):
    """Return the submenu of the top-level *label*."""
    menubar = app.root.nametowidget(app.root["menu"])
    for index in range(menubar.index("end") + 1):
        if menubar.type(index) == "cascade" and menubar.entrycget(index, "label") == label:
            return app.root.nametowidget(menubar.entrycget(index, "menu"))
    raise AssertionError(f"no {label!r} menu in the menu bar")


def _item(app, menu_label, item_label):
    menu = _menu(app, menu_label)
    for index in range(menu.index("end") + 1):
        if menu.type(index) == "separator":
            continue
        if menu.entrycget(index, "label") == item_label:
            return menu, index
    raise AssertionError(f"no {item_label!r} entry in the {menu_label} menu")


def test_edit_menu_offers_complete_word(app):
    _type(app, "10 PRI")
    menu, index = _item(app, "Edit", "Complete Word")

    menu.invoke(index)
    app.root.update()

    assert app.completion_popup.visible


def test_preferences_menu_toggles_completion(app, monkeypatch):
    monkeypatch.setattr(app, "_save_settings", lambda: None)
    menu, index = _item(app, "Preferences", "Auto-complete Words")

    menu.invoke(index)  # turn it off
    app.root.update()
    assert app.completion_enabled.get() is False

    menu.invoke(index)  # and back on
    app.root.update()
    assert app.completion_enabled.get() is True
