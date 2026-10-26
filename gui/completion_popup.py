"""Floating completion list for the editor.

The popup is a borderless ``Toplevel`` holding a ``Listbox``.  It never takes
the keyboard focus, so the editor keeps receiving keys and the application
drives the list with :meth:`CompletionPopup.move` and commits with
:meth:`CompletionPopup.take`.
"""

from __future__ import annotations

import tkinter as tk

MAX_VISIBLE_ROWS = 8
MIN_WIDTH = 90
DEFAULT_COLORS = {
    "bg": "#252526",
    "fg": "#d4d4d4",
    "select_bg": "#094771",
    "select_fg": "#ffffff",
}


class CompletionPopup:
    """A small, focus-free list of completion candidates."""

    def __init__(self, root):
        self.root = root
        self._window = None
        self._listbox = None
        self._items = ()
        self._shown = False
        self._colors = dict(DEFAULT_COLORS)
        self._font = ("Courier", 10)

    # ------------------------------------------------------------------
    # Construction and palette
    # ------------------------------------------------------------------

    def _build(self):
        """Create the window on first use (reused afterwards)."""
        window = tk.Toplevel(self.root)
        window.overrideredirect(True)
        try:
            window.attributes("-topmost", True)
        except tk.TclError:
            pass

        self._listbox = tk.Listbox(
            window,
            activestyle="none",
            borderwidth=1,
            relief=tk.SOLID,
            highlightthickness=0,
            exportselection=False,
            font=self._font,
        )
        self._listbox.pack(fill=tk.BOTH, expand=True)
        window.withdraw()
        self._window = window
        self._apply_colors()

    def _apply_colors(self):
        if self._listbox is None:
            return
        self._listbox.config(
            bg=self._colors["bg"],
            fg=self._colors["fg"],
            selectbackground=self._colors["select_bg"],
            selectforeground=self._colors["select_fg"],
        )

    def set_colors(self, bg, fg, select_bg, select_fg="#ffffff"):
        """Update the palette after a theme change."""
        self._colors = {
            "bg": bg, "fg": fg, "select_bg": select_bg, "select_fg": select_fg,
        }
        self._apply_colors()

    def set_font(self, font):
        """Match the list font to the editor font."""
        self._font = font
        if self._listbox is not None:
            self._listbox.config(font=font)

    # ------------------------------------------------------------------
    # State
    # ------------------------------------------------------------------

    @property
    def visible(self):
        """True while the list is on screen."""
        return self._shown

    @property
    def items(self):
        """The words currently offered."""
        return self._items

    def current(self):
        """The highlighted word, or None when the list is empty."""
        if not self._items:
            return None
        selection = self._listbox.curselection()
        return self._items[selection[0]] if selection else self._items[0]

    # ------------------------------------------------------------------
    # Commands
    # ------------------------------------------------------------------

    def show(self, items, x, y):
        """Display *items* with its top-left corner at screen (x, y)."""
        items = tuple(items)
        if not items:
            self.hide()
            return
        if self._window is None:
            self._build()

        self._items = items
        self._listbox.delete(0, tk.END)
        for item in items:
            self._listbox.insert(tk.END, item)
        self._listbox.config(height=min(len(items), MAX_VISIBLE_ROWS))
        self._listbox.selection_clear(0, tk.END)
        self._listbox.selection_set(0)
        self._listbox.see(0)

        self._window.update_idletasks()
        width = max(self._listbox.winfo_reqwidth(), MIN_WIDTH)
        height = self._listbox.winfo_reqheight()
        x, y = self._clamp(x, y, width, height)
        self._window.geometry(f"{width}x{height}+{x}+{y}")
        self._window.deiconify()
        self._window.lift()
        self._shown = True

    def hide(self):
        """Take the list off screen."""
        if self._window is not None:
            self._window.withdraw()
        self._shown = False
        self._items = ()

    def move(self, delta):
        """Move the highlight by *delta*, wrapping at both ends."""
        if not self._items:
            return
        selection = self._listbox.curselection()
        index = (selection[0] if selection else 0) + delta
        index %= len(self._items)
        self._listbox.selection_clear(0, tk.END)
        self._listbox.selection_set(index)
        self._listbox.see(index)

    def take(self):
        """Return the highlighted word and hide the list."""
        word = self.current()
        self.hide()
        return word

    # ------------------------------------------------------------------
    # Geometry
    # ------------------------------------------------------------------

    def _clamp(self, x, y, width, height):
        """Keep the window inside the screen."""
        try:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
        except tk.TclError:
            return x, y
        x = max(0, min(int(x), screen_width - width))
        y = max(0, min(int(y), screen_height - height))
        return x, y
