"""
Menu construction for Time Warp Classic.

Builds the full menu bar: File, Edit, Program, Debug, Test, Performance, Preferences, About.
"""

import os
import platform
import subprocess
import tkinter as tk
import tkinter.font as tkfont

from gui.themes import THEMES, FONT_SIZES, EXT_TO_LANG
from gui.dialogs import FindDialog, ReplaceDialog, show_error_history, show_about


def detect_language_from_extension(filepath, content=None):
    """Detect language from file extension, with .pl disambiguation."""
    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    if ext == ".pl":
        # Disambiguate Perl vs Prolog based on file content
        if content and (":-" in content or "?-" in content or content.count(".") > 3):
            return "Prolog"
        return "Perl"

    return EXT_TO_LANG.get(ext)


def _open_path(path):
    """Open a file or directory with the platform's default handler."""
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.Popen(["open", path])  # noqa: S603
        elif system == "Windows":
            getattr(os, 'startfile')(path)  # noqa: S606  # Windows-only, guarded by elif above
        else:
            subprocess.Popen(["xdg-open", path])  # noqa: S603
    except Exception:
        pass


def build_menu_bar(app):
    """Build the complete menu bar and attach it to *app*.

    Parameters
    ----------
    app : TimeWarpApp
        The application instance that owns the root window and widgets.
    """
    menubar = tk.Menu(app.root)
    app.root.config(menu=menubar)

    _build_file_menu(menubar, app)
    _build_edit_menu(menubar, app)
    _build_program_menu(menubar, app)
    _build_debug_menu(menubar, app)
    _build_test_menu(menubar, app)
    _build_performance_menu(menubar, app)
    _build_preferences_menu(menubar, app)
    _build_about_menu(menubar, app)


# ------------------------------------------------------------------
# File menu
# ------------------------------------------------------------------

def _build_file_menu(menubar, app):
    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="File", menu=menu)

    menu.add_command(label="New File", command=app.new_file, accelerator="Ctrl+N")
    menu.add_command(label="Open File...", command=app.load_file, accelerator="Ctrl+O")
    menu.add_separator()
    menu.add_command(label="Save File...", command=app.save_file, accelerator="Ctrl+S")
    menu.add_separator()
    menu.add_command(label="Exit", command=app.exit_app, accelerator="Ctrl+Q")


# ------------------------------------------------------------------
# Edit menu
# ------------------------------------------------------------------

def _build_edit_menu(menubar, app):
    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Edit", menu=menu)

    menu.add_command(label="Undo", command=app.undo, accelerator="Ctrl+Z")
    menu.add_command(label="Redo", command=app.redo, accelerator="Ctrl+Y")
    menu.add_separator()
    menu.add_command(label="Cut", command=app.cut, accelerator="Ctrl+X")
    menu.add_command(label="Copy", command=app.copy, accelerator="Ctrl+C")
    menu.add_command(label="Paste", command=app.paste, accelerator="Ctrl+V")
    menu.add_separator()
    menu.add_command(label="Select All", command=app.select_all, accelerator="Ctrl+A")
    menu.add_separator()
    menu.add_command(label="Find...", command=lambda: FindDialog(app.root, app.editor_text, app.output_text), accelerator="Ctrl+F")
    menu.add_command(label="Replace...", command=lambda: ReplaceDialog(app.root, app.editor_text, app.output_text), accelerator="Ctrl+H")


# ------------------------------------------------------------------
# Program menu (with examples)
# ------------------------------------------------------------------

_EXAMPLES = [
    ("PILOT", [
        ("Quiz Demo", "examples/pilot/quiz_pilot.pilot"),
        ("Comprehensive Demo", "examples/pilot/comprehensive_demo.pilot"),
    ]),
    ("BASIC", [
        ("Hello World + Turtle Graphics", "examples/basic/hello_basic.bas"),
        ("Comprehensive Demo", "examples/basic/comprehensive_demo.bas"),
        ("Index Menu", "examples/basic/INDEX.bas"),
    ]),
    ("Logo", [
        ("Colorful Spiral", "examples/logo/spiral_logo.logo"),
        ("Comprehensive Demo", "examples/logo/comprehensive_demo.logo"),
    ]),
    ("Pascal", [
        ("Hello World + Functions", "examples/pascal/hello_pascal.pas"),
        ("Comprehensive Demo", "examples/pascal/comprehensive_demo.pas"),
    ]),
    ("Prolog", [
        ("Facts & Rules", "examples/prolog/facts_prolog.pro"),
        ("Comprehensive Demo", "examples/prolog/comprehensive_demo.pro"),
    ]),
    ("Forth", [
        ("Stack Operations", "examples/forth/stack_forth.fth"),
        ("Comprehensive Demo", "examples/forth/comprehensive_demo.fth"),
    ]),
    ("Perl", [
        ("Patterns & Text Processing", "examples/perl/patterns_perl.pl"),
        ("Comprehensive Demo", "examples/perl/comprehensive_demo.pl"),
    ]),
    ("Python", [
        ("Modern Python Features", "examples/python/modern_python.py"),
        ("Comprehensive Demo", "examples/python/comprehensive_demo.py"),
    ]),
    ("JavaScript", [
        ("Modern JavaScript (ES6+)", "examples/javascript/interactive_javascript.js"),
        ("Comprehensive Demo", "examples/javascript/comprehensive_demo.js"),
    ]),
]


def _build_program_menu(menubar, app):
    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Program", menu=menu)

    menu.add_command(label="Run Program", command=app.run_code, accelerator="F5")
    menu.add_separator()

    examples_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Load Example", menu=examples_menu)

    for lang_name, examples in _EXAMPLES:
        sub = tk.Menu(examples_menu, tearoff=0)
        examples_menu.add_cascade(label=lang_name, menu=sub)
        for label, filepath in examples:
            sub.add_command(
                label=label,
                command=lambda fp=filepath: app.load_example(fp),
            )


# ------------------------------------------------------------------
# Debug menu
# ------------------------------------------------------------------

def _build_debug_menu(menubar, app):
    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Debug", menu=menu)

    app.debug_enabled = tk.BooleanVar(value=False)
    menu.add_checkbutton(
        label="Enable Debug Mode",
        variable=app.debug_enabled,
        command=lambda: app.interpreter.set_debug_mode(app.debug_enabled.get()),
    )
    menu.add_separator()
    menu.add_command(
        label="Clear All Breakpoints",
        command=lambda: app.interpreter.breakpoints.clear(),
    )
    menu.add_separator()
    menu.add_command(
        label="Show Error History",
        command=lambda: show_error_history(app.root, app.interpreter),
    )
    menu.add_command(
        label="Clear Error History",
        command=lambda: setattr(app.interpreter, "error_history", []),
    )


# ------------------------------------------------------------------
# Test menu
# ------------------------------------------------------------------

def _build_test_menu(menubar, app):
    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Test", menu=menu)

    menu.add_command(label="Run Smoke Test", command=app.run_smoke_test)
    menu.add_command(label="Run Full Test Suite", command=app.run_full_test_suite)


# ------------------------------------------------------------------
# Performance menu
# ------------------------------------------------------------------

def _build_performance_menu(menubar, app):
    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Performance", menu=menu)

    menu.add_command(label="Show Statistics", command=app.show_performance_stats)
    menu.add_command(label="Optimize Performance", command=app.optimize_performance)
    menu.add_command(label="Toggle Profiling", command=app.toggle_profiling)


# ------------------------------------------------------------------
# Preferences menu
# ------------------------------------------------------------------

def _build_preferences_menu(menubar, app):
    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Preferences", menu=menu)

    # Theme submenu
    theme_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Color Theme", menu=theme_menu)
    for key, data in THEMES.items():
        theme_menu.add_command(label=data["name"], command=lambda k=key: app.apply_theme(k))

    # Font family submenu
    font_family_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Font Family", menu=font_family_menu)

    available = _get_available_fonts()
    for font_name in available[:25]:
        font_family_menu.add_command(
            label=font_name, command=lambda f=font_name: app.apply_font_family(f)
        )
    if len(available) > 25:
        font_family_menu.add_separator()
        more = tk.Menu(font_family_menu, tearoff=0)
        font_family_menu.add_cascade(label="More Fonts...", menu=more)
        for font_name in available[25:]:
            more.add_command(
                label=font_name, command=lambda f=font_name: app.apply_font_family(f)
            )

    # Font size submenu
    font_menu = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="Font Size", menu=font_menu)
    for key, data in FONT_SIZES.items():
        font_menu.add_command(label=data["name"], command=lambda k=key: app.apply_font_size(k))


def _get_available_fonts():
    """Return available monospace fonts, prioritizing common families."""
    all_fonts = sorted(set(tkfont.families()))
    priority = [
        "Courier", "Courier New", "Consolas", "Monaco", "Menlo",
        "DejaVu Sans Mono", "Liberation Mono", "Ubuntu Mono",
        "Fira Code", "Source Code Pro", "JetBrains Mono",
        "Cascadia Code", "SF Mono", "Inconsolata", "Roboto Mono",
        "Hack", "Anonymous Pro", "Droid Sans Mono", "PT Mono",
    ]
    priority_available = [f for f in priority if f in all_fonts]
    other_fonts = [f for f in all_fonts if f not in priority]
    return priority_available + other_fonts


# ------------------------------------------------------------------
# About menu
# ------------------------------------------------------------------

def _build_about_menu(menubar, app):
    menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="About", menu=menu)
    menu.add_command(label="About Time Warp Classic", command=lambda: show_about(app.root))
