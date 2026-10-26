"""GUI tests for File -> Export Runner.

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
    _window.language_var.set("BASIC")
    _window.editor_text.delete("1.0", "end")
    _window.output_text.delete("1.0", "end")
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


def _has_item(app, menu_label, item_label):
    menu = _menu(app, menu_label)
    for index in range(menu.index("end") + 1):
        if menu.type(index) == "separator":
            continue
        if menu.entrycget(index, "label") == item_label:
            return True
    return False


def test_file_menu_offers_export_runner(app):
    assert _has_item(app, "File", "Export Runner...")


def test_export_writes_a_runnable_archive(app, tmp_path):
    app.editor_text.insert("1.0", '10 PRINT "EXPORTED"\n')
    target = tmp_path / "hello.pyz"

    result = app.export_runner(target=target)

    assert result == target
    assert target.is_file() and target.stat().st_size > 10_000
    assert "Runner written to" in _output(app)


def test_export_asks_for_a_path_when_none_is_given(app, tmp_path):
    app.editor_text.insert("1.0", "10 PRINT 1\n")
    target = str(tmp_path / "chosen.pyz")

    with mock.patch("gui.app.filedialog.asksaveasfilename", return_value=target) as ask:
        app.export_runner()

    assert ask.called
    assert (tmp_path / "chosen.pyz").is_file()


def test_export_can_be_cancelled(app, tmp_path):
    app.editor_text.insert("1.0", "10 PRINT 1\n")

    with mock.patch("gui.app.filedialog.asksaveasfilename", return_value=""):
        result = app.export_runner()

    assert result is None
    assert list(tmp_path.iterdir()) == []


def test_empty_editor_is_refused(app):
    with mock.patch("gui.app.messagebox.showinfo") as info:
        result = app.export_runner(target="ignored.pyz")

    assert result is None
    assert info.called


def test_external_runtime_is_noted(app, tmp_path):
    app.language_var.set("Python")
    app.editor_text.insert("1.0", 'print("hi")\n')

    app.export_runner(target=tmp_path / "py.pyz")

    assert "need that runtime installed" in _output(app)


def test_build_failure_is_reported(app, tmp_path):
    app.editor_text.insert("1.0", "10 PRINT 1\n")

    with mock.patch(
        "gui.app.build_standalone_runner", side_effect=OSError("disk full")
    ), mock.patch("gui.app.messagebox.showerror") as error:
        result = app.export_runner(target=tmp_path / "fail.pyz")

    assert result is None
    assert error.called
