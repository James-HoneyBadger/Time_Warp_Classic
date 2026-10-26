"""GUI tests for plugin languages: selector, menus, syntax and execution.

These need a display, so they are skipped on headless machines unless a
virtual X server is used (``xvfb-run -a python -m pytest``).
"""

import json
import os
import sys
import tkinter as tk
from unittest import mock

import pytest

pytestmark = pytest.mark.skipif(
    not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")),
    reason="needs a graphical display (try xvfb-run -a)",
)


MANIFEST = {
    "name": "TinyPython",
    "executable": sys.executable,
    "extension": ".tppy",
    "args": ["-u"],
    "syntax": "python",
    "comment": "#",
    "keywords": ["def", "import", "print"],
}


@pytest.fixture(scope="module")
def _window(tmp_path_factory):
    """A window whose plugin folder and settings live in a temp directory."""
    plugin_dir = tmp_path_factory.mktemp("plugins")
    (plugin_dir / "tiny.json").write_text(json.dumps(MANIFEST), encoding="utf-8")
    settings = tmp_path_factory.mktemp("settings") / "settings.json"

    with mock.patch("core.plugins.DEFAULT_PLUGIN_DIR", plugin_dir), mock.patch(
        "gui.app.DEFAULT_PLUGIN_DIR", plugin_dir
    ), mock.patch("gui.app.SETTINGS_FILE", settings):
        from gui.app import TimeWarpApp

        application = TimeWarpApp()
        application.root.update()
        application.plugin_dir = plugin_dir
        yield application
        try:
            application.root.destroy()
        except Exception:  # noqa: BLE001 - a test may have closed it
            pass


@pytest.fixture
def app(_window):
    """Shared window, re-reading the temp plugin folder before each test."""
    _window.completion_popup.hide()
    _window.language_var.set("PILOT")
    _window.editor_text.delete("1.0", "end")
    _window.output_text.delete("1.0", "end")
    _window.reload_plugins()
    _window.root.update()
    return _window


def _output(app):
    return app.output_text.get("1.0", "end")


def _menu(app, label):
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


def _invoke_submenu(app, menu_label, submenu_label, item_label):
    menu = _menu(app, menu_label)
    for index in range(menu.index("end") + 1):
        if menu.type(index) == "separator":
            continue
        if menu.type(index) == "cascade" and menu.entrycget(index, "label") == submenu_label:
            submenu = app.root.nametowidget(menu.entrycget(index, "menu"))
            for sub_index in range(submenu.index("end") + 1):
                if submenu.entrycget(sub_index, "label") == item_label:
                    submenu.invoke(sub_index)
                    app.root.update()
                    return
            raise AssertionError(
                f"no {item_label!r} entry in {menu_label} -> {submenu_label}"
            )
    raise AssertionError(f"no {submenu_label!r} submenu in the {menu_label} menu")


def test_plugin_language_appears_in_the_selector(app):
    menu = app.language_selector["menu"]

    labels = [
        menu.entrycget(index, "label") for index in range(menu.index("end") + 1)
    ]
    assert "TinyPython" in labels
    assert "Python" in labels  # built-ins are still there


def test_plugin_is_announced_on_startup(app):
    assert "Plugins loaded: TinyPython" in _output(app)


def test_plugin_extension_drives_save_and_detection(app):
    app.language_var.set("TinyPython")

    assert app._default_extension() == ".tppy"
    assert any("*.tppy" in flt for _name, flt in app._save_filetypes())
    assert app._detect_language("script.tppy") == "TinyPython"


def test_plugin_keywords_are_offered_by_completion(app):
    app.language_var.set("TinyPython")
    app.editor_text.insert("1.0", "im")
    app.editor_text.mark_set(tk.INSERT, "1.0+2c")
    app.root.update()

    app.show_completions(forced=False)

    assert "import" in app.completion_popup.items


def test_plugin_comment_marker_suppresses_completion(app):
    app.language_var.set("TinyPython")
    app.editor_text.insert("1.0", "# im")
    app.editor_text.mark_set(tk.INSERT, "1.0+4c")
    app.root.update()

    app.show_completions(forced=False)

    assert not app.completion_popup.visible


def test_plugin_program_runs_from_the_ide(app):
    app.language_var.set("TinyPython")
    app.editor_text.insert("1.0", 'print("plugin ran")\n')
    app.root.update()

    app.run_code()

    assert "plugin ran" in _output(app)


def test_create_example_plugin_loads_it(app):
    _invoke_submenu(app, "Preferences", "Plugins", "Create Example Plugin")

    assert (app.plugin_dir / "example-python.json").is_file()
    assert "PyPlugin" in app.languages  # the example manifest's own language
    assert "TinyPython" in app.languages
    assert app.plugins.problems == []


def test_reload_drops_a_removed_plugin(app):
    manifest = app.plugin_dir / "tiny.json"
    saved = manifest.read_text()
    try:
        manifest.unlink()
        app.reload_plugins()
        assert "TinyPython" not in app.languages
    finally:
        manifest.write_text(saved, encoding="utf-8")
        app.reload_plugins()

    assert "TinyPython" in app.languages


def test_program_menu_opens_the_web_ide(app):
    """Program -> Open Web IDE serves the page and reports the URL."""
    import json
    import urllib.request

    with mock.patch("gui.app.webbrowser.open") as opener:
        url = app.open_web_ide()

    try:
        assert url and url.startswith("http://127.0.0.1:")
        assert opener.called
        assert "Web IDE running at" in _output(app)

        with urllib.request.urlopen(url + "api/languages", timeout=20) as response:
            data = json.loads(response.read())
        assert any(entry["name"] == "BASIC" for entry in data["languages"])
        assert any(entry["name"] == "TinyPython" for entry in data["languages"])
    finally:
        app.stop_web_ide()
