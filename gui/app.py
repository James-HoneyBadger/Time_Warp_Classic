"""
Time Warp Classic - Main Application Window

The TimeWarpApp class owns the root Tk window, assembles layout panels,
and delegates actions to the interpreter and helper modules.
"""
# pylint: disable=C0301,W0718

import gc
import json
import os
import re
import sys
import time
import subprocess
from pathlib import Path

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

from core.interpreter import Time_WarpInterpreter
from core.features.completion import CompletionEngine, is_word_char
from core.plugins import DEFAULT_PLUGIN_DIR, PluginRegistry
from core.languages.basic_console import BasicConsole
from core.features.syntax_highlighting import SyntaxHighlightingText, LineNumberedText
from gui.completion_popup import CompletionPopup
from gui.themes import (
    THEMES, FONT_SIZES, LINE_NUMBER_BG, SUPPORTED_LANGUAGES,
)
from gui.menus import build_menu_bar, detect_language_from_extension, open_path

# Optional imports
try:
    import pygments  # noqa: F401
    _PYGMENTS = True
except ImportError:
    _PYGMENTS = False

try:
    import psutil  # noqa: F401
    _PSUTIL = True
except ImportError:
    _PSUTIL = False

SETTINGS_FILE = Path.home() / ".timewarp_settings.json"


class TimeWarpApp:
    """Main GUI application for Time Warp Classic."""

    # Languages that can draw on the turtle canvas (BASIC has DRAW/turtle
    # commands, Logo is turtle-first).
    _GRAPHICS_LANGUAGES = {"logo", "basic"}

    # Characters typed before the completion list appears by itself;
    # Ctrl+Space always opens it.
    COMPLETION_MIN_PREFIX = 2

    # Keys whose release says nothing about the text: ignore them so the list
    # does not flicker away while a modifier is held.
    _MODIFIER_KEYS = frozenset({
        "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R",
        "Super_L", "Super_R", "Caps_Lock", "Num_Lock", "ISO_Level3_Shift",
    })
    # Event state bits for Control and Alt (X11/Tk values).
    _CONTROL_MASK = 0x0004
    _ALT_MASK = 0x0008

    # Default file extension per language (Save As follows the language).
    LANGUAGE_EXTENSIONS = {
        "pilot": ".pilot",
        "basic": ".bas",
        "logo": ".logo",
        "pascal": ".pas",
        "prolog": ".pro",
        "forth": ".fth",
        "perl": ".pl",
        "python": ".py",
        "javascript": ".js",
    }

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self):
        # Settings — defaults overwritten by _load_settings
        self.current_theme = "dark"
        self.current_font = "medium"
        self.current_font_family = "Courier"
        self.current_completion = True
        self._load_settings()

        self.root = tk.Tk()
        self.root.title("Time Warp Classic - Multi-Language Programming Environment")
        self.root.geometry("1200x800")
        self.root.config(bg="#252526")

        # Will be set during layout build
        self.editor_text = None
        self.output_text = None
        self.turtle_canvas = None
        self.interpreter = None
        self.language_var = None
        self.input_entry = None
        self.input_buffer = []

        # Execution state
        self._program_running = False
        self.graphics_visible = True
        self._last_pump = 0.0

        # UI responsiveness counters used by Performance -> Show Statistics
        self._pump_count = 0
        self._pumps_per_second = 0.0
        self._pump_window_start = time.monotonic()

        # Document state
        self.current_file = None
        self.modified = False

        # References for theme updates
        self._layout_widgets = {}

        # Plugin languages extend the selector, the file types and the
        # completion vocabulary; they must be known before the layout.
        self.plugin_dir = DEFAULT_PLUGIN_DIR
        self.plugins = PluginRegistry.load()
        self.languages = list(SUPPORTED_LANGUAGES) + self.plugins.names()
        self.language_extensions = dict(self.LANGUAGE_EXTENSIONS)
        for spec in self.plugins:
            if spec.extension:
                self.language_extensions.setdefault(spec.name.lower(), spec.extension)

        self._build_layout()
        self._init_interpreter()
        self._init_completion()

        build_menu_bar(self)
        self._bind_keys()

        self.apply_theme(self.current_theme)
        self.apply_font_size(self.current_font)

        self._show_welcome()
        self._report_plugins()
        self._update_graphics_visibility()

        # The window-manager close button must not discard work silently.
        self.root.protocol("WM_DELETE_WINDOW", self.on_window_close)

        editor = self._text_widget()
        editor.bind("<<Modified>>", self._on_editor_modified, add="+")
        editor.bind("<KeyRelease>", lambda _e: self._update_cursor_status(), add="+")
        editor.bind("<ButtonRelease-1>", lambda _e: self._update_cursor_status(), add="+")
        self._update_title()
        self._update_status()

    # ------------------------------------------------------------------
    # Settings persistence
    # ------------------------------------------------------------------

    def _load_settings(self):
        try:
            if SETTINGS_FILE.exists():
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    s = json.load(f)
                self.current_theme = s.get("theme", "dark")
                self.current_font = s.get("font_size", "medium")
                self.current_font_family = s.get("font_family", "Courier")
                self.current_completion = s.get("completion", True)
                return
        except Exception:
            pass
        self.current_theme = "dark"
        self.current_font = "medium"
        self.current_font_family = "Courier"
        self.current_completion = True

    def _save_settings(self):
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "theme": self.current_theme,
                        "font_size": self.current_font,
                        "font_family": self.current_font_family,
                        "completion": bool(self.current_completion),
                    },
                    f,
                )
        except Exception:
            pass

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------

    def _build_layout(self):
        main_paned = tk.PanedWindow(
            self.root, orient=tk.HORIZONTAL, sashwidth=5, bg="#252526"
        )

        # --- Left panel (editor) ---
        left_panel = tk.Frame(main_paned, bg="#252526")
        main_paned.add(left_panel, width=400)

        editor_header = tk.Frame(left_panel, bg="#252526")
        editor_header.pack(fill=tk.X, pady=(0, 5))

        tk.Label(
            editor_header, text="Language:", font=("Arial", 9),
            bg="#252526", fg="#d4d4d4",
        ).pack(side=tk.LEFT, padx=(5, 5))

        self.language_var = tk.StringVar(value="PILOT")
        self.language_selector = tk.OptionMenu(
            editor_header, self.language_var, *self.languages
        )
        self.language_selector.config(width=10)
        self.language_selector.pack(side=tk.LEFT)

        # Wire language change to syntax highlighting
        self.language_var.trace_add("write", self._on_language_change)

        editor_frame = tk.LabelFrame(
            left_panel, text="Code Editor", padx=5, pady=5,
            bg="#252526", fg="#d4d4d4",
        )
        editor_frame.pack(fill=tk.BOTH, expand=True)

        if _PYGMENTS:
            self.editor_text = SyntaxHighlightingText(
                editor_frame, language="text", theme="dark",
                bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4",
            )
        else:
            self.editor_text = LineNumberedText(
                editor_frame,
                bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4",
            )
        self.editor_text.pack(fill=tk.BOTH, expand=True)

        # --- Right panel ---
        right_panel = tk.Frame(main_paned, bg="#252526")
        main_paned.add(right_panel, width=800)

        right_paned = tk.PanedWindow(
            right_panel, orient=tk.VERTICAL, sashwidth=5, bg="#252526"
        )
        right_paned.pack(fill=tk.BOTH, expand=True)

        # Output
        output_frame = tk.LabelFrame(
            right_paned, text="Output", padx=5, pady=5,
            bg="#252526", fg="#d4d4d4",
        )
        right_paned.add(output_frame, height=300)

        self.output_text = scrolledtext.ScrolledText(
            output_frame, wrap=tk.WORD, font=("Courier", 10),
            bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4",
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        self.output_text.bind("<Button-1>", self._on_output_click, add="+")
        self.output_text.bind("<Motion>", self._on_output_hover, add="+")

        # Turtle graphics
        graphics_frame = tk.LabelFrame(
            right_paned, text="Turtle Graphics", padx=5, pady=5,
            bg="#252526", fg="#d4d4d4",
        )
        right_paned.add(graphics_frame, height=300)

        self.turtle_canvas = tk.Canvas(
            graphics_frame, width=600, height=400,
            bg="#2d2d2d", highlightthickness=1, highlightbackground="#3e3e3e",
        )
        self.turtle_canvas.pack(fill=tk.BOTH, expand=True)

        # Input bar
        input_frame = tk.Frame(self.root, bg="#252526")

        tk.Label(
            input_frame, text="Console:", font=("Arial", 10),
            bg="#252526", fg="#d4d4d4",
        ).pack(side=tk.LEFT, padx=(0, 5))

        self.input_entry = tk.Entry(
            input_frame, font=("Courier", 10),
            bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4",
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_entry.bind("<Return>", lambda e: self._submit_input())
        tk.Button(
            input_frame, text="Submit", command=self._submit_input,
            bg="#3e3e3e", fg="#d4d4d4",
        ).pack(side=tk.LEFT)

        # Button bar
        button_frame = tk.Frame(self.root, bg="#252526")

        self.run_button = tk.Button(
            button_frame, text="\u25b6 Run", command=self.run_code,
            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=16,
        )
        self.run_button.pack(side=tk.LEFT, padx=5)
        self.stop_button = tk.Button(
            button_frame, text="\u25a0 Stop", command=self.stop_program,
            bg="#8e2f2f", fg="white", font=("Arial", 10, "bold"), padx=12,
            state=tk.DISABLED,
        )
        self.stop_button.pack(side=tk.LEFT, padx=5)
        for label, cmd in [
            ("Open", self.load_file),
            ("Save", self.save_file),
            ("Clear Editor", self.clear_editor),
            ("Clear Output", self.clear_output),
            ("Clear Graphics", self.clear_canvas),
        ]:
            tk.Button(
                button_frame, text=label, command=cmd, padx=8,
                bg="#3e3e3e", fg="#d4d4d4",
            ).pack(side=tk.LEFT, padx=4)

        # Status bar (always the bottom-most row)
        status_frame = tk.Frame(self.root, bg="#1e1e1e")
        self.status_language = tk.Label(
            status_frame, text="PILOT", bg="#1e1e1e", fg="#d4d4d4",
            font=("Courier", 9), padx=8, pady=2,
        )
        self.status_language.pack(side=tk.LEFT)
        self.status_file = tk.Label(
            status_frame, text="Untitled", bg="#1e1e1e", fg="#9d9d9d",
            font=("Courier", 9), padx=8, pady=2,
        )
        self.status_file.pack(side=tk.LEFT)
        self.status_state = tk.Label(
            status_frame, text="Ready", bg="#1e1e1e", fg="#9d9d9d",
            font=("Courier", 9), padx=8, pady=2,
        )
        self.status_state.pack(side=tk.RIGHT)
        self.status_cursor = tk.Label(
            status_frame, text="Ln 1, Col 1", bg="#1e1e1e", fg="#9d9d9d",
            font=("Courier", 9), padx=8, pady=2,
        )
        self.status_cursor.pack(side=tk.RIGHT)

        # Keep widget references for theme updates
        self._layout_widgets = {
            "left_panel": left_panel,
            "right_panel": right_panel,
            "editor_frame": editor_frame,
            "output_frame": output_frame,
            "graphics_frame": graphics_frame,
            "input_frame": input_frame,
            "button_frame": button_frame,
            "editor_header": editor_header,
            "status_frame": status_frame,
        }
        self.right_paned = right_paned
        self.graphics_frame = graphics_frame

        # Pack the bottom bars first so the expanding split view cannot clip
        # them off the window.
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))
        input_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    # ------------------------------------------------------------------
    # Interpreter init
    # ------------------------------------------------------------------

    def _init_interpreter(self):
        self.interpreter = Time_WarpInterpreter(self.output_text)
        self.interpreter.ide_turtle_canvas = self.turtle_canvas
        self.interpreter.input_buffer = self.input_buffer

        # Host hooks: keep the window responsive, route INPUT to the console,
        # and let the Stop control end a program (no iteration cap needed).
        self.interpreter.pump_callback = self._pump_events
        self.interpreter.input_provider = self._request_input
        self.interpreter.max_iterations = None
        self.interpreter.plugins = self.plugins
        # Direct-mode statements must run in the language shown in the menu.
        self.interpreter.set_language_mode(self.language_var.get().lower())

        # BASIC direct mode ("READY." console)
        self.basic_console = BasicConsole(
            self.interpreter,
            get_program=self._editor_program,
            set_program=self._set_editor_program,
            run_program=self._run_from_console,
            execute_direct=self._execute_basic_direct,
        )

    # ------------------------------------------------------------------
    # Keyboard bindings
    # ------------------------------------------------------------------

    def _bind_keys(self):
        self.root.bind("<F5>", lambda e: self.run_code())
        self.root.bind("<F9>", lambda e: self.toggle_breakpoint_at_cursor())
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.load_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-Shift-S>", lambda e: self.save_file_as())
        self.root.bind("<Control-q>", lambda e: self.exit_app())
        self.root.bind("<Control-period>", lambda e: self.stop_program())
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-a>", lambda e: self.select_all())
        from gui.dialogs import FindDialog, ReplaceDialog
        self.root.bind("<Control-f>", lambda e: FindDialog(self.root, self.editor_text, self.output_text))
        self.root.bind("<Control-h>", lambda e: ReplaceDialog(self.root, self.editor_text, self.output_text))

    # ------------------------------------------------------------------
    # Language change callback
    # ------------------------------------------------------------------

    def _on_language_change(self, *_args):
        """Update syntax highlighting when the language selector changes."""
        lang = self.language_var.get()
        lang_to_syntax = {
            "PILOT": "pilot", "BASIC": "basic", "Logo": "logo",
            "Pascal": "pascal", "Prolog": "prolog", "Forth": "forth",
            "Perl": "perl", "Python": "python", "JavaScript": "javascript",
        }
        syntax = lang_to_syntax.get(lang)
        if syntax is None:
            spec = self.plugins.get(lang)
            syntax = (spec.syntax if spec and spec.syntax else "text")
        if hasattr(self.editor_text, "set_language"):
            self.editor_text.set_language(syntax)
        popup = getattr(self, "completion_popup", None)
        if popup is not None:
            popup.hide()
        self._update_graphics_visibility()
        self.interpreter.set_language_mode(lang.lower())
        self._update_status()
        if lang.lower() == "basic" and not self._program_running and self.output_text is not None:
            self.output_text.insert(tk.END, "\nREADY.\n")

    # ------------------------------------------------------------------
    # Welcome message
    # ------------------------------------------------------------------

    def _show_welcome(self):
        self.output_text.insert("1.0", (
            "TIME WARP CLASSIC\n\n"
            "Supported Languages:\n"
            "\u2022 PILOT   - Educational language (T:, A:, J:, Y:, N: commands)\n"
            "\u2022 BASIC   - Classic line-numbered programming\n"
            "\u2022 Logo    - Turtle graphics programming\n"
            "\u2022 Pascal  - Structured programming\n"
            "\u2022 Prolog  - Logic programming\n"
            "\u2022 Forth   - Stack-based programming\n"
            "\u2022 Perl    - Scripting language\n"
            "\u2022 Python  - Modern programming\n"
            "\u2022 JavaScript - Web scripting\n\n"
            "Enter your code in the left panel and click Run to execute.\n"
            "BASIC direct mode: type a statement in the Console bar and press\n"
            "Enter (LIST, RUN, NEW, RENUMBER, HELP).\n"
        ))

    # ------------------------------------------------------------------
    # File operations
    # ------------------------------------------------------------------

    def new_file(self):
        """Start a new, empty program."""
        if not self._confirm_discard():
            return
        self.editor_text.delete("1.0", tk.END)
        self._discard_breakpoints()
        self._text_widget().edit_modified(False)
        self.current_file = None
        self.modified = False
        self._update_title()
        self._update_status()
        self.output_text.insert(tk.END, "New file\n")

    def load_file(self):
        """Open a file dialog and load the selected file into the editor."""
        if not self._confirm_discard():
            return
        filename = filedialog.askopenfilename(
            title="Open Program File",
            filetypes=[
                ("All Supported", "*.pilot *.pil *.bas *.logo *.lgo *.py *.js *.pl *.pm *.pas *.pp *.fth *.4th *.fs *.pro *.prolog"),
                ("PILOT Files", "*.pilot *.pil"), ("BASIC Files", "*.bas"),
                ("Logo Files", "*.logo *.lgo"), ("Python Files", "*.py"),
                ("JavaScript Files", "*.js"), ("Perl Files", "*.pl *.pm"),
                ("Pascal Files", "*.pas *.pp"), ("Forth Files", "*.fth *.4th *.fs"),
                ("Prolog Files", "*.pro *.prolog"), ("All Files", "*.*"),
            ],
        )
        if not filename:
            return
        try:
            content = Path(filename).read_text(encoding="utf-8")
        except OSError as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")
            return

        self.editor_text.delete("1.0", tk.END)
        self.editor_text.insert("1.0", content)
        self._discard_breakpoints()
        self._text_widget().edit_modified(False)
        self.current_file = filename
        self.modified = False
        lang = self._detect_language(filename, content)
        if lang:
            self.language_var.set(lang)
        self._update_title()
        self._update_status()
        suffix = f" ({lang})" if lang else ""
        self.output_text.insert(tk.END, f"Loaded: {filename}{suffix}\n")

    def save_file(self, save_as=False):
        """Save the buffer, asking for a path on first save or Save As."""
        path = None if save_as else self.current_file
        if not path:
            path = filedialog.asksaveasfilename(
                title="Save Program File",
                initialdir=str(Path(self.current_file).parent) if self.current_file else None,
                initialfile=Path(self.current_file).name if self.current_file else None,
                defaultextension=self._default_extension(),
                filetypes=self._save_filetypes(),
            )
            if not path:
                return False

        try:
            Path(path).write_text(self._editor_program(), encoding="utf-8")
        except OSError as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")
            return False

        self.current_file = path
        self.modified = False
        self._update_title()
        self._update_status()
        self.output_text.insert(tk.END, f"Saved: {path}\n")
        return True

    def save_file_as(self):
        """Save the buffer under a new name."""
        return self.save_file(save_as=True)

    def load_example(self, filepath):
        """Load an example program from *filepath* into the editor."""
        if not self._confirm_discard():
            return
        try:
            content = Path(filepath).read_text(encoding="utf-8")
        except OSError as e:
            messagebox.showerror("Error", f"Failed to load example:\n{e}")
            return

        self.editor_text.delete("1.0", tk.END)
        self.editor_text.insert("1.0", content)
        self._discard_breakpoints()
        self._text_widget().edit_modified(False)
        # Examples are samples: Save prompts for a name instead of overwriting.
        self.current_file = None
        self.modified = False
        lang = self._detect_language(filepath, content)
        if lang:
            self.language_var.set(lang)
        self._update_title()
        self._update_status()
        suffix = f" ({lang})" if lang else ""
        self.output_text.insert(tk.END, f"Loaded example: {filepath}{suffix}\n")

    # ------------------------------------------------------------------
    # Document state, title and status bar
    # ------------------------------------------------------------------

    def _text_widget(self):
        """Return the real tk.Text widget behind the editor wrapper."""
        return getattr(self.editor_text, "text", self.editor_text)

    def _detect_language(self, filepath, content=None):
        """Detect the language for *filepath*, including plugin languages."""
        detected = detect_language_from_extension(filepath, content)
        if detected:
            return detected
        suffix = Path(filepath).suffix.lower()
        return self.plugins.extension_map().get(suffix)

    def _default_extension(self):
        """Return the file extension matching the selected language."""
        return self.language_extensions.get(self.language_var.get().lower(), ".txt")

    def _save_filetypes(self):
        """File-type filters, with the current language first."""
        ext = self._default_extension()
        filters = [(f"{self.language_var.get()} Files", f"*{ext}")]
        for language, suffix in self.language_extensions.items():
            if suffix != ext:
                filters.append((f"{language.capitalize()} Files", f"*{suffix}"))
        filters.append(("All Files", "*.*"))
        return filters

    def _on_editor_modified(self, _event=None):
        """Track whether the document has unsaved changes."""
        widget = self._text_widget()
        try:
            changed = bool(widget.edit_modified())
            widget.edit_modified(False)
        except tk.TclError:
            return
        if changed and not self.modified:
            self.modified = True
            self._update_title()
            self._update_status()

    def _has_unsaved_changes(self):
        """True when the buffer holds changes that have not been written."""
        if self.modified:
            return True
        try:
            # Authoritative flag, even before <<Modified>> has been dispatched.
            return bool(self._text_widget().edit_modified())
        except (AttributeError, tk.TclError):
            return False

    def _confirm_discard(self):
        """Offer to save unsaved work before the buffer is replaced."""
        if not self._has_unsaved_changes():
            return True
        answer = messagebox.askyesnocancel(
            "Unsaved Changes", "Save changes before continuing?"
        )
        if answer is None:
            return False
        if answer:
            self.save_file()
            return not self.modified
        return True

    def _update_title(self):
        """Show the document name and modified marker in the title bar."""
        name = Path(self.current_file).name if self.current_file else "Untitled"
        star = " *" if self.modified else ""
        self.root.title(f"{name}{star} - Time Warp Classic")

    def _update_status(self):
        """Refresh the status bar."""
        try:
            self.status_language.config(text=self.language_var.get())
            name = Path(self.current_file).name if self.current_file else "Untitled"
            self.status_file.config(text=name + (" *" if self.modified else ""))
            self.status_state.config(text="Running" if self._program_running else "Ready")
        except (AttributeError, tk.TclError):
            pass
        self._update_cursor_status()

    def _update_cursor_status(self):
        """Show the caret position (line and column) in the status bar."""
        try:
            line, column = self._text_widget().index(tk.INSERT).split(".")
            self.status_cursor.config(text=f"Ln {line}, Col {int(column) + 1}")
        except (AttributeError, ValueError, tk.TclError):
            pass

    # ------------------------------------------------------------------
    # Output -> editor navigation
    # ------------------------------------------------------------------

    def _error_line_at(self, x, y):
        """Return the line number named on the clicked output line, if any."""
        try:
            index = self.output_text.index(f"@{x},{y}")
            text = self.output_text.get(f"{index} linestart", f"{index} lineend")
        except tk.TclError:
            return None
        match = re.search(r"(?:ERROR IN|BREAK IN)\s+(\d+)", text)
        return int(match.group(1)) if match else None

    def _on_output_click(self, event):
        """Jump to the editor line named by an error or BREAK message."""
        line = self._error_line_at(event.x, event.y)
        if line is None:
            return None
        self._goto_editor_line(line)
        return "break"

    def _on_output_hover(self, event):
        """Show a hand cursor over clickable error lines."""
        try:
            self.output_text.config(
                cursor="hand2" if self._error_line_at(event.x, event.y) else ""
            )
        except tk.TclError:
            pass

    def _goto_editor_line(self, line):
        """Select *line* in the editor and scroll it into view."""
        widget = self._text_widget()
        target = f"{line}.0"
        try:
            widget.tag_remove("highlight", "1.0", tk.END)
            widget.tag_configure("highlight", background="#264f78")
            widget.tag_add("highlight", target, f"{line}.end")
            widget.mark_set(tk.INSERT, target)
            widget.see(target)
            widget.focus_set()
        except tk.TclError:
            return
        self._update_cursor_status()

    # ------------------------------------------------------------------
    # Edit operations
    # ------------------------------------------------------------------

    def cut(self):
        """Cut selected text to clipboard."""
        try:
            self.editor_text.event_generate("<<Cut>>")
        except Exception:
            pass

    def copy(self):
        """Copy selected text to clipboard."""
        try:
            self.editor_text.event_generate("<<Copy>>")
        except Exception:
            pass

    def paste(self):
        """Paste text from clipboard."""
        try:
            self.editor_text.event_generate("<<Paste>>")
        except Exception:
            pass

    def undo(self):
        """Undo the last edit operation."""
        try:
            self.editor_text.edit_undo()
        except Exception:
            pass

    def redo(self):
        """Redo the last undone edit operation."""
        try:
            self.editor_text.edit_redo()
        except Exception:
            pass

    def select_all(self):
        """Select all text in the editor."""
        self.editor_text.tag_add("sel", "1.0", tk.END)
        self.editor_text.mark_set("insert", "1.0")
        self.editor_text.see("insert")
        return "break"

    def clear_editor(self):
        """Clear the editor content."""
        self.editor_text.delete("1.0", tk.END)
        self._discard_breakpoints()

    def clear_output(self):
        """Clear the output panel."""
        self.output_text.delete("1.0", tk.END)

    def clear_canvas(self):
        """Clear the turtle graphics canvas."""
        self.turtle_canvas.delete("all")
        self.output_text.insert(tk.END, "\U0001f3a8 Canvas cleared\n")

    # ------------------------------------------------------------------
    # Code execution
    # ------------------------------------------------------------------

    def run_code(self, program_text=None, clear_output=True):
        """Execute the editor contents (or *program_text*) in the chosen language."""
        if self._program_running:
            return

        code = program_text if program_text is not None else self.editor_text.get("1.0", tk.END)
        lang = self.language_var.get().lower()
        if clear_output:
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "RUN\n\n")

        self._program_running = True
        self._set_running_state(True)
        self.completion_popup.hide()
        try:
            self.interpreter.ide_turtle_canvas = self.turtle_canvas
            if lang == "logo":
                if self.turtle_canvas is not None:
                    self.turtle_canvas.delete("all")
                self.interpreter.turtle_graphics = None
                self.interpreter.init_turtle_graphics()
                self.interpreter.clear_turtle_screen()
            # A classic RUN starts from a clean slate: variables and loop
            # stacks left over from the previous run are discarded.
            self.interpreter.reset()
            self.interpreter.run_program(code, language=lang)
        except Exception as e:
            self.output_text.insert(tk.END, f"\n\u274c Error: {e}\n")
        finally:
            self._program_running = False
            self._set_running_state(False)
            try:
                self.output_text.see(tk.END)
            except tk.TclError:
                pass  # the window was closed while the program was running

    def stop_program(self):
        """Ask the interpreter to abort the program that is running."""
        if self._program_running:
            self.interpreter.stop_program()

    def _set_running_state(self, running):
        """Enable/disable the Run and Stop controls for the current state."""
        try:
            self.run_button.config(state=tk.DISABLED if running else tk.NORMAL)
            self.stop_button.config(state=tk.NORMAL if running else tk.DISABLED)
            self.root.config(cursor="watch" if running else "")
        except tk.TclError:
            pass
        self._update_status()

    def _pump_events(self, *_args):
        """Keep the window alive while the interpreter is executing."""
        if not self._program_running:
            return
        now = time.monotonic()
        if now - self._last_pump < 0.03:
            return
        self._last_pump = now
        self._pump_count += 1
        elapsed = now - self._pump_window_start
        if elapsed >= 1.0:
            self._pumps_per_second = self._pump_count / elapsed
            self._pump_count = 0
            self._pump_window_start = now
        try:
            self.root.update()
        except tk.TclError:
            # The window went away mid-run: stop the interpreter so the run
            # loop terminates instead of spinning without a UI.
            self.interpreter.stop_program()

    def _request_input(self, prompt=""):
        """Wait for one console line from the input bar.

        Pumps UI events while waiting so Stop and window controls stay live,
        and returns ``None`` when the run is stopped instead of guessing.
        """
        if prompt:
            self.output_text.insert(tk.END, prompt)
            self.output_text.see(tk.END)
        try:
            self.input_entry.focus_set()
        except tk.TclError:
            return None

        while not self.input_buffer:
            if self.interpreter.stop_requested:
                self.output_text.insert(tk.END, "\n")
                return None
            try:
                self.root.update()
            except tk.TclError:
                return None
            time.sleep(0.02)

        value = self.input_buffer.pop(0)
        self.output_text.insert(tk.END, f"{value}\n")
        self.output_text.see(tk.END)
        return value

    def _update_graphics_visibility(self):
        """Show the turtle canvas only for languages that can draw."""
        graphics_frame = getattr(self, "graphics_frame", None)
        right_paned = getattr(self, "right_paned", None)
        if graphics_frame is None or right_paned is None or self.language_var is None:
            return
        wanted = self.language_var.get().lower() in self._GRAPHICS_LANGUAGES
        if wanted == self.graphics_visible:
            return
        try:
            if wanted:
                right_paned.add(graphics_frame, height=300)
            else:
                right_paned.forget(graphics_frame)
            self.graphics_visible = wanted
        except tk.TclError:
            pass

    # ------------------------------------------------------------------
    # Breakpoints
    # ------------------------------------------------------------------

    BREAKPOINT_TAG = "breakpoint"

    def toggle_breakpoint_at_cursor(self):
        """Set or clear a breakpoint on the line holding the caret."""
        try:
            line = int(self._text_widget().index(tk.INSERT).split(".")[0])
        except (AttributeError, ValueError, tk.TclError):
            return
        self.interpreter.toggle_breakpoint(line)
        self._refresh_breakpoint_marks()
        state = "Set" if self.interpreter.is_breakpoint(line) else "Cleared"
        self.output_text.insert(tk.END, f"{state} breakpoint on line {line}\n")

    def clear_breakpoints(self):
        """Remove every breakpoint and its marker."""
        self.interpreter.clear_breakpoints()
        self._refresh_breakpoint_marks()
        self.output_text.insert(tk.END, "Breakpoints cleared\n")

    def _refresh_breakpoint_marks(self):
        """Paint a marker on every line that has a breakpoint."""
        widget = self._text_widget()
        try:
            widget.tag_remove(self.BREAKPOINT_TAG, "1.0", tk.END)
            if not self.interpreter.breakpoints:
                return
            widget.tag_configure(self.BREAKPOINT_TAG, background="#7a1f1f")
            for index in sorted(self.interpreter.breakpoints):
                line = index + 1
                widget.tag_add(self.BREAKPOINT_TAG, f"{line}.0", f"{line}.end")
            widget.tag_raise(self.BREAKPOINT_TAG)
        except tk.TclError:
            pass

    def _discard_breakpoints(self):
        """Drop breakpoints when the program in the editor is replaced."""
        if self.interpreter is None or not self.interpreter.breakpoints:
            return
        self.interpreter.clear_breakpoints()
        self._refresh_breakpoint_marks()

    # ------------------------------------------------------------------
    # Plugins
    # ------------------------------------------------------------------

    def _refresh_plugin_state(self):
        """Rebuild everything that depends on the loaded plugin languages."""
        self.languages = list(SUPPORTED_LANGUAGES) + self.plugins.names()
        self.language_extensions = dict(self.LANGUAGE_EXTENSIONS)
        for spec in self.plugins:
            if spec.extension:
                self.language_extensions.setdefault(spec.name.lower(), spec.extension)
        if self.interpreter is not None:
            self.interpreter.plugins = self.plugins
        for spec in self.plugins:
            if spec.keywords or spec.comment:
                self.completion.register(spec.name, spec.keywords, spec.comment)

        menu = self.language_selector["menu"]
        current = self.language_var.get()
        menu.delete(0, "end")
        for language in self.languages:
            menu.add_command(
                label=language,
                command=lambda value=language: self.language_var.set(value),
            )
        if current in self.languages:
            self.language_var.set(current)

    def reload_plugins(self):
        """Re-read the plugin folder and follow any changes."""
        self.plugins = PluginRegistry.load()
        self._refresh_plugin_state()
        self._report_plugins()

    def _report_plugins(self):
        """Show which plugin languages loaded, and which manifests failed."""
        if len(self.plugins):
            names = ", ".join(self.plugins.names())
            self.output_text.insert(tk.END, f"Plugins loaded: {names}\n")
        for problem in self.plugins.problems:
            self.output_text.insert(tk.END, f"?PLUGIN: {problem}\n")
        try:
            self.output_text.see(tk.END)
        except tk.TclError:
            pass

    def open_plugins_folder(self):
        """Create the plugin folder and show it in the file manager."""
        folder = Path(self.plugin_dir)
        try:
            folder.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            self.output_text.insert(tk.END, f"?PLUGIN: {exc}\n")
            return
        self.output_text.insert(tk.END, f"Plugin folder: {folder}\n")
        open_path(folder)

    def create_example_plugin(self):
        """Write an example manifest, then pick it up immediately."""
        try:
            target = PluginRegistry.write_example(self.plugin_dir)
        except OSError as exc:
            self.output_text.insert(tk.END, f"?PLUGIN: {exc}\n")
            return
        self.output_text.insert(tk.END, f"Example plugin written to {target}\n")
        self.reload_plugins()

    # ------------------------------------------------------------------
    # Code completion
    # ------------------------------------------------------------------

    def _init_completion(self):
        """Create the completion engine and popup, and bind the editor keys."""
        self.completion = CompletionEngine()
        self.completion_popup = CompletionPopup(self.root)
        self.completion_enabled = tk.BooleanVar(value=bool(self.current_completion))
        self._completion_span = (0, 0)  # (start offset, prefix length)

        editor = self._text_widget()
        editor.bind("<Control-space>", self.show_completions, add="+")
        editor.bind("<KeyRelease>", self._on_completion_key, add="+")
        # Navigation only acts while the list is open; otherwise these keys
        # keep their normal editing behaviour.
        for sequence in ("<Up>", "<Down>", "<Return>", "<KP_Enter>", "<Tab>", "<Escape>"):
            editor.bind(sequence, self._on_completion_key_navigation, add="+")
        editor.bind("<FocusOut>", lambda _e: self.completion_popup.hide(), add="+")
        editor.bind("<Button-1>", lambda _e: self.completion_popup.hide(), add="+")

        for spec in self.plugins:
            if spec.keywords or spec.comment:
                self.completion.register(spec.name, spec.keywords, spec.comment)

        self.completion_popup.set_font(
            (self.current_font_family, FONT_SIZES[self.current_font]["editor"])
        )

    def _completion_language(self):
        """Vocabulary key for the language selected in the toolbar."""
        return self.language_var.get().lower() if self.language_var else ""

    def _caret_screen_position(self):
        """Screen coordinates just below the caret."""
        editor = self._text_widget()
        try:
            box = editor.bbox(tk.INSERT)
            if not box:
                # Caret scrolled out of view (or the window is not mapped yet):
                # anchor the list inside the editor rather than not at all.
                return editor.winfo_rootx() + 40, editor.winfo_rooty() + 40
            x, y, _width, height = box
            return editor.winfo_rootx() + x, editor.winfo_rooty() + y + height
        except tk.TclError:
            return None

    def show_completions(self, _event=None, forced=True):
        """Offer the words for the current prefix (Ctrl+Space and auto-type)."""
        if self._program_running or not self.completion_enabled.get():
            self.completion_popup.hide()
            return "break"
        if not self._completion_enabled_for_language():
            self.completion_popup.hide()
            return "break"

        editor = self._text_widget()
        text = editor.get("1.0", "end-1c")
        cursor = len(editor.get("1.0", tk.INSERT))
        found = self.completion.completion_at(
            self._completion_language(), text, cursor, forced=forced
        )
        if found is None:
            self.completion_popup.hide()
            return "break" if forced else None

        start, items = found
        if not forced and cursor - start < self.COMPLETION_MIN_PREFIX:
            self.completion_popup.hide()
            return None

        position = self._caret_screen_position()
        if position is None:
            self.completion_popup.hide()
            return None

        self._completion_span = (start, cursor - start)
        self.completion_popup.show(items, *position)
        return "break" if forced else None

    def _completion_enabled_for_language(self):
        """False when the selected language has no vocabulary yet."""
        return bool(self.completion.vocabulary(self._completion_language()))

    def _on_completion_key(self, event):
        """Refresh the list as the user types, and close it otherwise."""
        if event.keysym in self._MODIFIER_KEYS:
            return None
        if event.state & (self._CONTROL_MASK | self._ALT_MASK):
            # Shortcuts (undo, save, ...) do not add text.
            return None
        if self.completion_popup.visible and event.keysym in (
            "Up", "Down", "Return", "KP_Enter", "Tab", "Escape",
        ):
            return None
        # Tk leaves event.char empty on key *release*, so fall back to the
        # keysym for printable single characters.
        typed = event.char or (
            event.keysym if len(event.keysym) == 1 else ""
        )
        if event.keysym == "BackSpace" or is_word_char(typed):
            self.show_completions(forced=False)
        else:
            self.completion_popup.hide()
        return None

    def _on_completion_key_navigation(self, event):
        """Drive the open list; leave the key alone when it is closed."""
        popup = self.completion_popup
        if not popup.visible:
            return None
        if event.keysym in ("Up", "Down"):
            popup.move(1 if event.keysym == "Down" else -1)
            return "break"
        if event.keysym in ("Return", "KP_Enter", "Tab"):
            self._complete_with(popup.take())
            return "break"
        if event.keysym == "Escape":
            popup.hide()
            return "break"
        return None

    def _complete_with(self, word):
        """Replace the typed prefix with *word*."""
        if not word:
            return
        start, length = self._completion_span
        editor = self._text_widget()
        try:
            editor.delete(f"1.0+{start}c", f"1.0+{start + length}c")
            editor.insert(f"1.0+{start}c", word)
        except tk.TclError:
            return
        self.completion_popup.hide()
        self._update_cursor_status()

    def complete_word(self):
        """Menu entry point: open the list at the caret."""
        self._text_widget().focus_set()
        self.show_completions(forced=True)

    def toggle_completion(self):
        """Turn auto-completion on or off, remembering the choice."""
        self.current_completion = bool(self.completion_enabled.get())
        if not self.current_completion:
            self.completion_popup.hide()
        self._save_settings()

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def _submit_input(self):
        """Handle a line typed at the console.

        While a program is running the line answers INPUT; otherwise, in BASIC
        mode, it is handled by direct mode (statements run immediately,
        numbered lines edit the program).
        """
        value = self.input_entry.get()
        self.input_entry.delete(0, tk.END)
        if self._program_running:
            self.input_buffer.append(value)
            return
        if not value.strip():
            return

        self.output_text.insert(tk.END, f">{value}\n")
        if self.language_var.get().lower() != "basic":
            self.output_text.insert(
                tk.END,
                "Nothing is running. Press F5 (or Run) to execute the program.\n",
            )
            self.output_text.see(tk.END)
            return

        try:
            response = self.basic_console.submit(value)
        except Exception as exc:  # noqa: BLE001 — never lose the console to a bug
            response = [f"?ERROR: {exc}"]
        # TRON/TROFF change the interpreter directly; keep the menu in step.
        if hasattr(self, "debug_enabled"):
            self.debug_enabled.set(self.interpreter.debug_mode)
        for line in response:
            self.output_text.insert(tk.END, f"{line}\n")
        self.output_text.see(tk.END)

    def _editor_program(self):
        """Return the editor contents (the program in memory)."""
        return self.editor_text.get("1.0", "end-1c")

    def _set_editor_program(self, text):
        """Replace the editor contents (used by direct mode commands)."""
        self.editor_text.delete("1.0", tk.END)
        self.editor_text.insert("1.0", text)

    def _run_from_console(self, program_text):
        """Run a program supplied by the console (keeps the console history)."""
        self.run_code(program_text, clear_output=False)

    def _execute_basic_direct(self, statement):
        """Run a BASIC direct-mode statement with the normal input controls."""
        # A stop latched by an earlier run (or by a cancelled INPUT) must not
        # abort this statement: direct mode starts each one with a clean state.
        self.interpreter.stop_requested = False
        self.interpreter.interrupted = False
        self._program_running = True
        self._set_running_state(True)
        try:
            return self.interpreter.execute_line(statement)
        finally:
            self.interpreter.stop_requested = False
            self.interpreter.interrupted = False
            self._program_running = False
            self._set_running_state(False)

    # ------------------------------------------------------------------
    # Theme & font
    # ------------------------------------------------------------------

    def apply_theme(self, theme_key):
        """Apply the given colour theme to all GUI widgets."""
        theme = THEMES[theme_key]

        # Editor
        if hasattr(self.editor_text, "text"):
            self.editor_text.text.config(
                bg=theme["text_bg"], fg=theme["text_fg"],
                insertbackground=theme["text_fg"],
            )
            if hasattr(self.editor_text, "set_theme"):
                self.editor_text.set_theme(theme_key)
            if hasattr(self.editor_text, "line_numbers"):
                bg = LINE_NUMBER_BG.get(theme_key, "#1e1e1e")
                self.editor_text.line_numbers.config(bg=bg)
        else:
            self.editor_text.config(
                bg=theme["text_bg"], fg=theme["text_fg"],
                insertbackground=theme["text_fg"],
            )

        # Output
        self.output_text.config(
            bg=theme["text_bg"], fg=theme["text_fg"],
            insertbackground=theme["text_fg"],
        )

        # Canvas
        self.turtle_canvas.config(
            bg=theme["canvas_bg"],
            highlightbackground=theme["canvas_border"],
        )

        # Completion popup follows the editor colours
        popup = getattr(self, "completion_popup", None)
        if popup is not None:
            popup.set_colors(
                theme["text_bg"], theme["text_fg"], theme.get("select_bg", "#094771")
            )

        # Frames
        w = self._layout_widgets
        self.root.config(bg=theme["root_bg"])
        w["left_panel"].config(bg=theme["frame_bg"])
        w["right_panel"].config(bg=theme["frame_bg"])
        w["editor_frame"].config(bg=theme["editor_frame_bg"], fg=theme["editor_frame_fg"])
        w["output_frame"].config(bg=theme["editor_frame_bg"], fg=theme["editor_frame_fg"])
        w["graphics_frame"].config(bg=theme["editor_frame_bg"], fg=theme["editor_frame_fg"])
        w["input_frame"].config(bg=theme["frame_bg"])
        w["button_frame"].config(bg=theme["frame_bg"])
        w["editor_header"].config(bg=theme["frame_bg"])
        if "status_frame" in w:
            w["status_frame"].config(bg=theme["input_bg"])
            for child in w["status_frame"].winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=theme["input_bg"], fg=theme["text_fg"])

        # Input
        self.input_entry.config(
            bg=theme["input_bg"], fg=theme["input_fg"],
            insertbackground=theme["input_fg"],
        )

        # Update child labels
        for frame_key in ("editor_header", "input_frame"):
            for child in w[frame_key].winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=theme["frame_bg"], fg=theme["text_fg"])

        self.current_theme = theme_key
        self._save_settings()

    def apply_font_family(self, family):
        """Change the editor and output font family."""
        self.current_font_family = family
        size = FONT_SIZES[self.current_font]
        if hasattr(self.editor_text, "set_font"):
            self.editor_text.set_font((family, size["editor"]))
        else:
            self.editor_text.config(font=(family, size["editor"]))
        self.output_text.config(font=(family, size["output"]))
        popup = getattr(self, "completion_popup", None)
        if popup is not None:
            popup.set_font((family, size["editor"]))
        self._save_settings()

    def apply_font_size(self, size_key):
        """Change the editor and output font size."""
        self.current_font = size_key
        size = FONT_SIZES[size_key]
        if hasattr(self.editor_text, "set_font"):
            self.editor_text.set_font((self.current_font_family, size["editor"]))
        else:
            self.editor_text.config(font=(self.current_font_family, size["editor"]))
        self.output_text.config(font=(self.current_font_family, size["output"]))
        popup = getattr(self, "completion_popup", None)
        if popup is not None:
            popup.set_font((self.current_font_family, size["editor"]))
        self._save_settings()

    # ------------------------------------------------------------------
    # Testing
    # ------------------------------------------------------------------

    def run_smoke_test(self):
        """Run a quick smoke test to verify basic interpreter functionality."""
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "\U0001f9ea Running smoke test...\n")
        try:
            result = self.interpreter.evaluate_expression("2 + 3")
            tag = "\u2705" if result == 5 else "\u274c"
            self.output_text.insert(tk.END, f"{tag} Basic evaluation: {'PASS' if result == 5 else f'FAIL (got {result})'}\n")

            self.interpreter.variables["TEST_VAR"] = 42
            ok = self.interpreter.variables.get("TEST_VAR") == 42
            var_tag = "\u2705" if ok else "\u274c"
            var_msg = "PASS" if ok else "FAIL"
            self.output_text.insert(tk.END, f"{var_tag} Variable assignment: {var_msg}\n")

            loaded = self.interpreter.load_program('PRINT "Test passed!"')
            load_tag = "\u2705" if loaded else "\u274c"
            load_msg = "PASS" if loaded else "FAIL"
            self.output_text.insert(tk.END, f"{load_tag} Program loading: {load_msg}\n")

            self.output_text.insert(tk.END, "\n\U0001f389 Smoke test completed!\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"\n\u274c Smoke test failed: {e}\n")

    def run_full_test_suite(self):
        """Execute the full pytest test suite and display results."""
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "\U0001f9ea Running full test suite...\n")
        test_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "run_tests.py")
        test_script = os.path.normpath(test_script)
        if not os.path.exists(test_script):
            self.output_text.insert(tk.END, "\u274c Test script not found: scripts/run_tests.py\n")
            self.output_text.insert(tk.END, "\u2139\ufe0f  No test suite is available in this installation.\n")
            return
        try:
            result = subprocess.run(
                [sys.executable, test_script, "all", "-v"],
                capture_output=True, text=True, cwd=".",
                check=False,
                timeout=120,
            )
            self.output_text.insert(tk.END, result.stdout)
            if result.stderr:
                self.output_text.insert(tk.END, "\nErrors:\n" + result.stderr)
            tag = "\u2705" if result.returncode == 0 else "\u274c"
            msg = "All tests passed!" if result.returncode == 0 else f"Tests failed with code {result.returncode}"
            self.output_text.insert(tk.END, f"\n{tag} {msg}\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"\n\u274c Failed to run tests: {e}\n")

    # ------------------------------------------------------------------
    # Performance
    # ------------------------------------------------------------------

    def show_performance_stats(self):
        """Display interpreter, UI and memory statistics."""
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "\U0001f4ca Performance Statistics\n")
        self.output_text.insert(tk.END, "=" * 50 + "\n\n")
        try:
            self._write_interpreter_stats()
            self._write_ui_stats()
            self._write_memory_stats()
        except Exception as e:
            self.output_text.insert(
                tk.END, f"\u274c Error getting performance stats: {e}\n"
            )

    def _write_interpreter_stats(self):
        """Interpreter cache, profiler and lazy-loading figures."""
        if not hasattr(self.interpreter, "get_performance_stats"):
            return
        stats = self.interpreter.get_performance_stats()
        cache = stats.get("expression_cache", {})
        profiler = stats.get("profiler", {})
        memory = stats.get("memory", {})

        self.output_text.insert(tk.END, "Interpreter Performance:\n")
        self.output_text.insert(
            tk.END,
            f"  Expression Cache: {cache.get('hit_rate', 0):.1%} hit rate "
            f"({cache.get('hits', 0)} hits, {cache.get('misses', 0)} misses, "
            f"{cache.get('size', 0)}/{cache.get('max_size', 0)} entries)\n",
        )
        if profiler:
            operations = sum(item.get("count", 0) for item in profiler.values())
            self.output_text.insert(
                tk.END,
                f"  Profiling: on, {operations} lines timed\n",
            )
        else:
            self.output_text.insert(
                tk.END, "  Profiling: off (Performance \u2192 Toggle Profiling)\n"
            )
        self.output_text.insert(
            tk.END, f"  Memory: {memory.get('gc_objects', 0)} objects\n"
        )
        self.output_text.insert(
            tk.END,
            f"  Lazy Modules: {len(stats.get('lazy_loaded_modules', []))} loaded\n\n",
        )

    def _write_ui_stats(self):
        """Responsiveness figures measured while programs run."""
        try:
            pending_callbacks = len(self.root.tk.call("after", "info"))
        except tk.TclError:
            pending_callbacks = 0
        output_chars = len(self.output_text.get("1.0", "end-1c"))

        self.output_text.insert(tk.END, "UI Performance:\n")
        self.output_text.insert(
            tk.END, f"  Event pumps/sec: {self._pumps_per_second:.1f}\n"
        )
        self.output_text.insert(
            tk.END, f"  Pending input lines: {len(self.input_buffer)}\n"
        )
        self.output_text.insert(
            tk.END, f"  Scheduled callbacks: {pending_callbacks}\n"
        )
        self.output_text.insert(
            tk.END, f"  Output panel: {output_chars} characters\n\n"
        )

    def _write_memory_stats(self):
        """Process memory, when psutil is installed."""
        if not _PSUTIL:
            self.output_text.insert(
                tk.END,
                "Memory Usage: psutil not available "
                "(pip install psutil)\n\n",
            )
            return
        process = psutil.Process(os.getpid())
        mem = process.memory_info()
        self.output_text.insert(
            tk.END,
            "Memory Usage:\n"
            f"  RSS: {mem.rss / 1024 / 1024:.1f} MB\n"
            f"  VMS: {mem.vms / 1024 / 1024:.1f} MB\n\n",
        )

    def optimize_performance(self):
        """Apply runtime performance optimizations and report results."""
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "\u26a1 Applying Performance Optimizations...\n\n")
        try:
            if hasattr(self.interpreter, "optimize_for_production"):
                result = self.interpreter.optimize_for_production()
                self.output_text.insert(
                    tk.END,
                    "Interpreter: "
                    f"cache_cleared={result.get('cache_cleared', False)}, "
                    f"objects_collected={result.get('objects_collected', 0)}\n",
                )
            try:
                from core.optimizations import cleanup_all_resources
                result = cleanup_all_resources()
                self.output_text.insert(
                    tk.END,
                    f"Global: garbage_collected={result.get('garbage_collected', 0)}\n",
                )
            except ImportError:
                pass

            collected = gc.collect()
            self.root.update_idletasks()
            self.output_text.insert(tk.END, f"UI: {collected} objects collected, "
                                            "pending redraws flushed\n")
            self.output_text.insert(tk.END, "\n\u2705 Performance optimizations applied!\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"\u274c Error: {e}\n")

    def toggle_profiling(self):
        """Toggle runtime performance profiling on or off."""
        if not hasattr(self.interpreter, "enable_profiling"):
            self.output_text.insert(tk.END, "\u2139\ufe0f  Profiling not available\n")
            return
        enabled = not self.interpreter.enable_profiling
        setter = getattr(self.interpreter, "set_profiling", None)
        if callable(setter):
            setter(enabled)
        else:
            self.interpreter.enable_profiling = enabled
        state = "enabled" if self.interpreter.enable_profiling else "disabled"
        self.output_text.insert(tk.END, f"\U0001f50d Performance profiling {state}\n")

    # ------------------------------------------------------------------
    # Application lifecycle
    # ------------------------------------------------------------------

    def on_window_close(self):
        """Handle the window close button (clicking it by accident is common)."""
        if self._program_running:
            self.stop_program()
        self.exit_app()

    def exit_app(self):
        """Prompt the user and exit the application."""
        if self._program_running:
            self.stop_program()
        prompt = "Exit Time Warp Classic?"
        if self._has_unsaved_changes():
            prompt = "Exit Time Warp Classic?\nUnsaved changes will be lost."
        if messagebox.askyesno("Exit", prompt):
            self.root.destroy()

    def run(self):
        """Start the Tk main loop."""
        self.root.mainloop()
