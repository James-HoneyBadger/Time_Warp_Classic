"""Close-button behaviour: never discard work without asking."""

import os

import pytest
import tkinter as tk

pytestmark = pytest.mark.skipif(
    not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")),
    reason="needs a graphical display (try xvfb-run -a)",
)


@pytest.fixture(scope="module")
def window():
    """One window for both tests; the last one closes it."""
    from gui.app import TimeWarpApp

    application = TimeWarpApp()
    application.root.update()
    yield application
    try:
        application.root.destroy()
    except Exception:  # noqa: BLE001
        pass


def test_close_button_asks_before_discarding_work(window, monkeypatch):
    """The window close button must not silently throw away editor contents."""
    import tkinter.messagebox as messagebox

    window.editor_text.insert("1.0", '10 PRINT "PRECIOUS"')
    asked = {}

    def deny(title, prompt, **kwargs):
        asked["prompt"] = prompt
        return False

    monkeypatch.setattr(messagebox, "askyesno", deny)
    window.on_window_close()

    assert "Unsaved" in asked["prompt"]
    assert window.root.winfo_exists()


def test_close_button_exits_when_confirmed(window, monkeypatch):
    """Confirming the prompt still closes the window."""
    import tkinter.messagebox as messagebox

    monkeypatch.setattr(messagebox, "askyesno", lambda *a, **k: True)
    window.on_window_close()

    with pytest.raises(tk.TclError):
        window.root.winfo_exists()   # the interpreter is gone
