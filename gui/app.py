"""
Time Warp Classic - Main Application Window

The TimeWarpApp class owns the root Tk window, assembles layout panels,
and delegates actions to the interpreter and helper modules.
"""
# pylint: disable=C0301,W0718

import json
import os
import sys
import subprocess
from pathlib import Path

import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

from core.interpreter import Time_WarpInterpreter
from core.features.syntax_highlighting import SyntaxHighlightingText, LineNumberedText
from gui.themes import (
    THEMES, FONT_SIZES, LINE_NUMBER_BG, SUPPORTED_LANGUAGES,
)
from gui.menus import build_menu_bar, detect_language_from_extension

# Optional imports
try:
    from core.optimizations.gui_optimizer import (  # pylint: disable=ungrouped-imports
        initialize_gui_optimizer,
    )
    _GUI_OPT = True
except ImportError:
    _GUI_OPT = False
    initialize_gui_optimizer = None  # type: ignore[assignment]

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

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(self):
        # Settings — defaults overwritten by _load_settings
        self.current_theme = "dark"
        self.current_font = "medium"
        self.current_font_family = "Courier"
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
        self.gui_optimizer = None
        self.input_buffer = []

        # References for theme updates
        self._layout_widgets = {}

        # Initialize GUI optimizer
        if _GUI_OPT and callable(initialize_gui_optimizer):
            self.gui_optimizer = initialize_gui_optimizer(self.root)

        self._build_layout()
        self._init_interpreter()

        build_menu_bar(self)
        self._bind_keys()

        self.apply_theme(self.current_theme)
        self.apply_font_size(self.current_font)

        self._show_welcome()

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
                return
        except Exception:
            pass
        self.current_theme = "dark"
        self.current_font = "medium"
        self.current_font_family = "Courier"

    def _save_settings(self):
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "theme": self.current_theme,
                        "font_size": self.current_font,
                        "font_family": self.current_font_family,
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
        main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

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
        language_selector = tk.OptionMenu(editor_header, self.language_var, *SUPPORTED_LANGUAGES)
        language_selector.config(width=10)
        language_selector.pack(side=tk.LEFT)

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
        input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Label(
            input_frame, text="Input:", font=("Arial", 10),
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
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

        tk.Button(
            button_frame, text="\u25b6 Run", command=self.run_code,
            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), padx=20,
        ).pack(side=tk.LEFT, padx=5)
        for label, cmd in [
            ("\U0001f4c2 Open", self.load_file),
            ("\U0001f4be Save", self.save_file),
            ("\U0001f5d1\ufe0f Clear Editor", self.clear_editor),
            ("\U0001f4c4 Clear Output", self.clear_output),
            ("\U0001f3a8 Clear Graphics", self.clear_canvas),
        ]:
            tk.Button(
                button_frame, text=label, command=cmd, padx=15,
                bg="#3e3e3e", fg="#d4d4d4",
            ).pack(side=tk.LEFT, padx=5)

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
        }

    # ------------------------------------------------------------------
    # Interpreter init
    # ------------------------------------------------------------------

    def _init_interpreter(self):
        self.interpreter = Time_WarpInterpreter(self.output_text)
        self.interpreter.ide_turtle_canvas = self.turtle_canvas

    # ------------------------------------------------------------------
    # Keyboard bindings
    # ------------------------------------------------------------------

    def _bind_keys(self):
        self.root.bind("<F5>", lambda e: self.run_code())
        self.root.bind("<Control-n>", lambda e: self.new_file())
        self.root.bind("<Control-o>", lambda e: self.load_file())
        self.root.bind("<Control-s>", lambda e: self.save_file())
        self.root.bind("<Control-q>", lambda e: self.exit_app())
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
            "PILOT": "text", "BASIC": "text", "Logo": "text",
            "Pascal": "pascal", "Prolog": "prolog", "Forth": "text",
            "Perl": "perl", "Python": "python", "JavaScript": "javascript",
        }
        if hasattr(self.editor_text, "set_language"):
            self.editor_text.set_language(lang_to_syntax.get(lang, "text"))

    # ------------------------------------------------------------------
    # Welcome message
    # ------------------------------------------------------------------

    def _show_welcome(self):
        self.output_text.insert("1.0", (
            "Welcome to Time Warp Classic! \U0001f680\n\n"
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
            "Enter your code in the left panel and click Run to execute!\n"
        ))

    # ------------------------------------------------------------------
    # File operations
    # ------------------------------------------------------------------

    def new_file(self):  # noqa: C0116 — thin UI wrappers
        """Create a new empty file in the editor."""
        if messagebox.askyesno("New File", "Clear current editor content?"):
            self.editor_text.delete("1.0", tk.END)
            self.output_text.insert(tk.END, "\U0001f4c4 New file created\n")

    def load_file(self):
        """Open a file dialog and load the selected file into the editor."""
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
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            self.editor_text.delete("1.0", tk.END)
            self.editor_text.insert("1.0", content)
            lang = detect_language_from_extension(filename, content)
            if lang:
                self.language_var.set(lang)
                self.output_text.insert(tk.END, f"\U0001f4c2 Loaded: {filename} ({lang})\n")
            else:
                self.output_text.insert(tk.END, f"\U0001f4c2 Loaded: {filename}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{e}")

    def save_file(self):
        """Save the current editor content to a file."""
        filename = filedialog.asksaveasfilename(
            title="Save Program File",
            defaultextension=".pilot",
            filetypes=[
                ("PILOT Files", "*.pilot"), ("BASIC Files", "*.bas"),
                ("Logo Files", "*.logo"), ("Python Files", "*.py"),
                ("JavaScript Files", "*.js"), ("Perl Files", "*.pl"),
                ("Pascal Files", "*.pas"), ("Forth Files", "*.fth"),
                ("Prolog Files", "*.pro"), ("All Files", "*.*"),
            ],
        )
        if not filename:
            return
        try:
            content = self.editor_text.get("1.0", tk.END)
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            self.output_text.insert(tk.END, f"\U0001f4be Saved: {filename}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{e}")

    def load_example(self, filepath):
        """Load an example program from *filepath* into the editor."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            self.editor_text.delete("1.0", tk.END)
            self.editor_text.insert("1.0", content)
            lang = detect_language_from_extension(filepath, content)
            if lang:
                self.language_var.set(lang)
                self.output_text.insert(tk.END, f"\U0001f4da Loaded example: {filepath} ({lang})\n")
            else:
                self.output_text.insert(tk.END, f"\U0001f4da Loaded example: {filepath}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load example:\n{e}")

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

    def run_code(self):
        """Execute the current editor content using the selected language."""
        code = self.editor_text.get("1.0", tk.END)
        lang = self.language_var.get().lower()
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "\U0001f680 Running program...\n\n")
        try:
            self.interpreter.ide_turtle_canvas = self.turtle_canvas
            if lang == "logo":
                if self.turtle_canvas is not None:
                    self.turtle_canvas.delete("all")
                self.interpreter.turtle_graphics = None
                self.interpreter.init_turtle_graphics()
                self.interpreter.clear_turtle_screen()
            self.interpreter.run_program(code, language=lang)
            self.output_text.insert(tk.END, "\n\u2705 Program completed.\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"\n\u274c Error: {e}\n")

    # ------------------------------------------------------------------
    # Input
    # ------------------------------------------------------------------

    def _submit_input(self):
        """Handle user input submission from the input entry field."""
        value = self.input_entry.get()
        self.input_buffer.append(value)
        self.output_text.insert(tk.END, f">> {value}\n")
        self.input_entry.delete(0, tk.END)

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
        """Display interpreter and GUI performance statistics."""
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "\U0001f4ca Performance Statistics\n")
        self.output_text.insert(tk.END, "=" * 50 + "\n\n")
        try:
            if hasattr(self.interpreter, "get_performance_stats"):
                stats = self.interpreter.get_performance_stats()
                self.output_text.insert(tk.END, "Interpreter Performance:\n")
                self.output_text.insert(tk.END, f"  Expression Cache: {stats.get('expression_cache', {}).get('hit_rate', 0):.2%} hit rate\n")
                self.output_text.insert(tk.END, f"  Profiling: {stats.get('profiler', {})}\n")
                self.output_text.insert(tk.END, f"  Memory: {stats.get('memory', {}).get('gc_objects', 0)} objects\n")
                self.output_text.insert(tk.END, f"  Lazy Modules: {len(stats.get('lazy_loaded_modules', []))} loaded\n\n")
            if self.gui_optimizer:
                gs = self.gui_optimizer.get_performance_stats()
                self.output_text.insert(tk.END, "GUI Performance:\n")
                self.output_text.insert(tk.END, f"  Updates/sec: {gs.get('updates_per_second', 0):.1f}\n")
                self.output_text.insert(tk.END, f"  Pending Tasks: {gs.get('pending_ui_tasks', 0)}\n\n")
            if _PSUTIL:
                process = psutil.Process(os.getpid())
                mem = process.memory_info()
                self.output_text.insert(tk.END, f"Memory Usage:\n  RSS: {mem.rss / 1024 / 1024:.1f} MB\n  VMS: {mem.vms / 1024 / 1024:.1f} MB\n\n")
            else:
                self.output_text.insert(tk.END, "Memory Usage: psutil not available\n\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"\u274c Error getting performance stats: {e}\n")

    def optimize_performance(self):
        """Apply runtime performance optimizations and report results."""
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "\u26a1 Applying Performance Optimizations...\n\n")
        try:
            if hasattr(self.interpreter, "optimize_for_production"):
                r = self.interpreter.optimize_for_production()
                self.output_text.insert(tk.END, f"Interpreter: cache_cleared={r.get('cache_cleared', False)}, objects_collected={r.get('objects_collected', 0)}\n")
            if self.gui_optimizer and hasattr(self.gui_optimizer, "optimize_for_performance"):
                r = self.gui_optimizer.optimize_for_performance()
                self.output_text.insert(tk.END, f"GUI: canvases_flushed={r.get('canvases_flushed', 0)}, tasks_remaining={r.get('ui_tasks_remaining', 0)}\n")
            try:
                from core.optimizations import cleanup_all_resources
                r = cleanup_all_resources()
                self.output_text.insert(tk.END, f"Global: garbage_collected={r.get('garbage_collected', 0)}\n")
            except ImportError:
                pass
            self.output_text.insert(tk.END, "\n\u2705 Performance optimizations applied!\n")
        except Exception as e:
            self.output_text.insert(tk.END, f"\u274c Error: {e}\n")

    def toggle_profiling(self):
        """Toggle runtime performance profiling on or off."""
        if hasattr(self.interpreter, "enable_profiling"):
            self.interpreter.enable_profiling = not self.interpreter.enable_profiling
            state = "enabled" if self.interpreter.enable_profiling else "disabled"
            self.output_text.insert(tk.END, f"\U0001f50d Performance profiling {state}\n")
        else:
            self.output_text.insert(tk.END, "\u2139\ufe0f  Profiling not available\n")

    # ------------------------------------------------------------------
    # Application lifecycle
    # ------------------------------------------------------------------

    def exit_app(self):
        """Prompt the user and exit the application."""
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.root.quit()

    def run(self):
        """Start the Tk main loop."""
        self.root.mainloop()
