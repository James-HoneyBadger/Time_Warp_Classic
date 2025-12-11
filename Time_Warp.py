#!/usr/bin/env python3
"""
Time Warp Classic - Multi-Language Programming Environment

A multi-language interpreter supporting 9 classic programming languages
with integrated turtle graphics.

Copyright © 2025 Honey Badger Universe. All rights reserved.

Supports: PILOT, BASIC, Logo, Pascal, Prolog, Forth, Perl, Python, JavaScript

Features:
- 9 programming languages with built-in examples
- Integrated turtle graphics for visual programming
- Multiple color themes and font sizes  
- File persistence for editor content
- Educational feedback and error messages
"""
# pylint: disable=C0301,C0103,R1705,W0621,W0718,W0404,C0415,W1510

import sys
import json
import os
from pathlib import Path


def main():
    """Main entry point - launches Time Warp Classic."""

    # Launch GUI
    print("🚀 Launching Time Warp Classic...")
    try:
            # Import and launch the GUI application
            import tkinter as tk
            from tkinter import scrolledtext, messagebox, filedialog
            from core.interpreter import Time_WarpInterpreter

            # Settings file for persistence
            SETTINGS_FILE = Path.home() / ".timewarp_settings.json"

            def load_settings():
                """Load user settings from file."""
                try:
                    if SETTINGS_FILE.exists():
                        with open(SETTINGS_FILE, 'r') as f:
                            return json.load(f)
                except Exception:
                    pass
                return {"theme": "dark", "font_size": "medium", "font_family": "Courier"}

            def save_settings(theme, font_size, font_family):
                """Save user settings to file."""
                try:
                    with open(SETTINGS_FILE, 'w') as f:
                        json.dump({"theme": theme, "font_size": font_size, "font_family": font_family}, f)
                except Exception:
                    pass

            # Load saved settings
            settings = load_settings()
            current_theme = settings.get("theme", "dark")
            current_font = settings.get("font_size", "medium")
            current_font_family = settings.get("font_family", "Courier")

            # Create the main GUI window
            root = tk.Tk()
            root.title("Time Warp Classic - Multi-Language Programming Environment")
            root.geometry("1200x800")
            root.config(bg="#252526")

            # Create menu bar
            menubar = tk.Menu(root)
            root.config(menu=menubar, bg="#252526")

            # File menu
            file_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="File", menu=file_menu)

            # Editor text widget (declare early for menu functions)
            editor_text = None
            output_text = None
            interpreter = None

            def load_file():
                """Load a file into the editor."""
                filename = filedialog.askopenfilename(
                    title="Open Program File",
                    filetypes=[
                        (
                            "All Supported",
                            "*.pilot;*.bas;*.logo;*.py;*.js;*.pl;*.pas;*.4th;*.pro",
                        ),
                        ("PILOT Files", "*.pilot"),
                        ("BASIC Files", "*.bas"),
                        ("Logo Files", "*.logo"),
                        ("Python Files", "*.py"),
                        ("JavaScript Files", "*.js"),
                        ("Perl Files", "*.pl"),
                        ("Pascal Files", "*.pas"),
                        ("Forth Files", "*.4th"),
                        ("Prolog Files", "*.pro"),
                        ("All Files", "*.*"),
                    ],
                )
                if filename:
                    try:
                        with open(filename, "r", encoding="utf-8") as f:
                            content = f.read()
                        editor_text.delete("1.0", tk.END)
                        editor_text.insert("1.0", content)

                        # Auto-detect language from file extension only
                        ext_to_lang = {
                            '.pil': 'PILOT',
                            '.bas': 'BASIC',
                            '.logo': 'Logo',
                            '.py': 'Python',
                            '.js': 'JavaScript',
                            '.pas': 'Pascal',
                            '.fth': 'Forth',
                            '.pro': 'Prolog',
                            '.pl': 'Perl'
                        }
                        import os
                        _, ext = os.path.splitext(filename)
                        detected_lang = ext_to_lang.get(ext.lower())
                        
                        if detected_lang:
                            language_var.set(detected_lang)
                            output_text.insert(tk.END, f"📂 Loaded: {filename} ({detected_lang})\n")
                        else:
                            output_text.insert(tk.END, f"📂 Loaded: {filename}\n")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to load file:\n{e}")

            def save_file():
                """Save the editor content to a file."""
                filename = filedialog.asksaveasfilename(
                    title="Save Program File",
                    defaultextension=".pilot",
                    filetypes=[
                        ("PILOT Files", "*.pilot"),
                        ("BASIC Files", "*.bas"),
                        ("Logo Files", "*.logo"),
                        ("Python Files", "*.py"),
                        ("JavaScript Files", "*.js"),
                        ("Perl Files", "*.pl"),
                        ("Pascal Files", "*.pas"),
                        ("Forth Files", "*.4th"),
                        ("Prolog Files", "*.pro"),
                        ("All Files", "*.*"),
                    ],
                )
                if filename:
                    try:
                        content = editor_text.get("1.0", tk.END)
                        with open(filename, "w", encoding="utf-8") as f:
                            f.write(content)
                        output_text.insert(tk.END, f"💾 Saved: {filename}\n")
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to save file:\n{e}")

            def new_file():
                """Create a new file."""
                if messagebox.askyesno("New File", "Clear current editor content?"):
                    editor_text.delete("1.0", tk.END)
                    output_text.insert(tk.END, "📄 New file created\n")

            def exit_app():
                """Exit the application."""
                if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
                    root.quit()

            file_menu.add_command(label="New File", command=new_file, accelerator="Ctrl+N")
            file_menu.add_command(
                label="Open File...", command=load_file, accelerator="Ctrl+O"
            )
            file_menu.add_separator()
            file_menu.add_command(
                label="Save File...", command=save_file, accelerator="Ctrl+S"
            )
            file_menu.add_separator()
            file_menu.add_command(label="Exit", command=exit_app, accelerator="Ctrl+Q")

            # Edit menu
            edit_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Edit", menu=edit_menu)

            def cut_text():
                """Cut selected text to clipboard."""
                try:
                    editor_text.event_generate("<<Cut>>")
                except Exception:
                    pass

            def copy_text():
                """Copy selected text to clipboard."""
                try:
                    editor_text.event_generate("<<Copy>>")
                except Exception:
                    pass

            def paste_text():
                """Paste text from clipboard."""
                try:
                    editor_text.event_generate("<<Paste>>")
                except Exception:
                    pass

            def undo_text():
                """Undo last edit."""
                try:
                    editor_text.edit_undo()
                except Exception:
                    pass

            def redo_text():
                """Redo last undone edit."""
                try:
                    editor_text.edit_redo()
                except Exception:
                    pass

            def select_all():
                """Select all text in editor."""
                editor_text.tag_add("sel", "1.0", tk.END)
                editor_text.mark_set("insert", "1.0")
                editor_text.see("insert")
                return "break"

            def clear_editor():
                """Clear the editor."""
                editor_text.delete("1.0", tk.END)

            def clear_output():
                """Clear the output window."""
                output_text.delete("1.0", tk.END)

            def clear_canvas():
                """Clear the turtle graphics canvas."""
                turtle_canvas.delete("all")
                output_text.insert(tk.END, "🎨 Canvas cleared\n")

            edit_menu.add_command(label="Undo", command=undo_text, accelerator="Ctrl+Z")
            edit_menu.add_command(label="Redo", command=redo_text, accelerator="Ctrl+Y")
            edit_menu.add_separator()
            edit_menu.add_command(label="Cut", command=cut_text, accelerator="Ctrl+X")
            edit_menu.add_command(label="Copy", command=copy_text, accelerator="Ctrl+C")
            edit_menu.add_command(label="Paste", command=paste_text, accelerator="Ctrl+V")
            edit_menu.add_separator()
            edit_menu.add_command(label="Select All", command=select_all, accelerator="Ctrl+A")

            def run_code():
                """Execute the code in the editor."""
                code = editor_text.get("1.0", tk.END)
                selected_language = language_var.get().lower()
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, "🚀 Running program...\n\n")
                try:
                    # Keep turtle canvas wired before execution
                    interpreter.ide_turtle_canvas = turtle_canvas

                    # If Logo is selected, fully reset turtle state and canvas before run
                    if selected_language == "logo":
                        if turtle_canvas is not None:
                            turtle_canvas.delete("all")
                        # Reinitialize turtle graphics to ensure a fresh origin and pen state
                        interpreter.turtle_graphics = None
                        interpreter.init_turtle_graphics()
                        interpreter.clear_turtle_screen()

                    interpreter.run_program(code, language=selected_language)
                    output_text.insert(tk.END, "\n✅ Program completed.\n")
                except Exception as e:
                    output_text.insert(tk.END, f"\n❌ Error: {e}\n")

            # Program menu
            program_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Program", menu=program_menu)

            program_menu.add_command(label="Run Program", command=run_code, accelerator="F5")
            program_menu.add_separator()

            # Examples submenu under Program
            examples_menu = tk.Menu(program_menu, tearoff=0)
            program_menu.add_cascade(label="Load Example", menu=examples_menu)

            def load_example(filepath):
                """Load an example program."""
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                    editor_text.delete("1.0", tk.END)
                    editor_text.insert("1.0", content)

                    # Auto-detect language from file extension
                    ext_to_lang = {
                        '.pilot': 'PILOT',
                        '.bas': 'BASIC',
                        '.logo': 'Logo',
                        '.py': 'Python',
                        '.js': 'JavaScript',
                        '.pas': 'Pascal',
                        '.fth': 'Forth',
                        '.4th': 'Forth',
                        '.pro': 'Prolog',
                        '.prolog': 'Prolog'
                    }
                    import os
                    _, ext = os.path.splitext(filepath)
                    detected_lang = None
                    
                    # Handle .pl ambiguity (Perl vs Prolog)
                    if ext.lower() == '.pl':
                        # Check file content to distinguish Prolog from Perl
                        # content is already loaded above
                        if ':-' in content or '?-' in content or content.count('.') > 3:
                            detected_lang = 'Prolog'
                        else:
                            detected_lang = 'Perl'
                    elif ext.lower() in ext_to_lang:
                        detected_lang = ext_to_lang[ext.lower()]
                    
                    if detected_lang:
                        language_var.set(detected_lang)
                        output_text.insert(tk.END, f"📚 Loaded example: {filepath} ({detected_lang})\n")
                    else:
                        output_text.insert(tk.END, f"📚 Loaded example: {filepath}\n")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to load example:\n{e}")

            # PILOT examples submenu
            pilot_menu = tk.Menu(examples_menu, tearoff=0)
            examples_menu.add_cascade(label="PILOT", menu=pilot_menu)
            pilot_menu.add_command(
                label="Quiz Demo",
                command=lambda: load_example("examples/pilot/quiz_pilot.pilot"),
            )

            # BASIC examples submenu
            basic_menu = tk.Menu(examples_menu, tearoff=0)
            examples_menu.add_cascade(label="BASIC", menu=basic_menu)
            basic_menu.add_command(
                label="Hello World + Turtle Graphics",
                command=lambda: load_example("examples/basic/hello_basic.bas"),
            )
            basic_menu.add_command(
                label="Index Menu",
                command=lambda: load_example("examples/basic/INDEX.bas"),
            )

            # Logo examples submenu
            logo_menu = tk.Menu(examples_menu, tearoff=0)
            examples_menu.add_cascade(label="Logo", menu=logo_menu)
            logo_menu.add_command(
                label="Colorful Spiral",
                command=lambda: load_example("examples/logo/spiral_logo.logo"),
            )

            # Pascal examples submenu
            pascal_menu = tk.Menu(examples_menu, tearoff=0)
            examples_menu.add_cascade(label="Pascal", menu=pascal_menu)
            pascal_menu.add_command(
                label="Hello World + Functions",
                command=lambda: load_example("examples/pascal/hello_pascal.pas"),
            )

            # Prolog examples submenu
            prolog_menu = tk.Menu(examples_menu, tearoff=0)
            examples_menu.add_cascade(label="Prolog", menu=prolog_menu)
            prolog_menu.add_command(
                label="Facts & Rules",
                command=lambda: load_example("examples/prolog/facts_prolog.pl"),
            )

            # Forth examples submenu
            forth_menu = tk.Menu(examples_menu, tearoff=0)
            examples_menu.add_cascade(label="Forth", menu=forth_menu)
            forth_menu.add_command(
                label="Stack Operations",
                command=lambda: load_example("examples/forth/stack_forth.fth"),
            )

            # Perl examples submenu
            perl_menu = tk.Menu(examples_menu, tearoff=0)
            examples_menu.add_cascade(label="Perl", menu=perl_menu)
            perl_menu.add_command(
                label="Patterns & Text Processing",
                command=lambda: load_example("examples/perl/patterns_perl.pl"),
            )

            # Python examples submenu
            python_menu = tk.Menu(examples_menu, tearoff=0)
            examples_menu.add_cascade(label="Python", menu=python_menu)
            python_menu.add_command(
                label="Modern Python Features",
                command=lambda: load_example("examples/python/modern_python.py"),
            )

            # JavaScript examples submenu
            js_menu = tk.Menu(examples_menu, tearoff=0)
            examples_menu.add_cascade(label="JavaScript", menu=js_menu)
            js_menu.add_command(
                label="Modern JavaScript (ES6+)",
                command=lambda: load_example("examples/javascript/interactive_javascript.js"),
            )

            # Preferences menu
            preferences_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Preferences", menu=preferences_menu)

            # Theme submenu
            theme_menu = tk.Menu(preferences_menu, tearoff=0)
            preferences_menu.add_cascade(label="Color Theme", menu=theme_menu)

            # Define theme configurations
            THEMES = {
                "light": {
                    "name": "Light",
                    "text_bg": "white", "text_fg": "black",
                    "canvas_bg": "white", "canvas_border": "#cccccc",
                    "root_bg": "#f0f0f0", "frame_bg": "#f0f0f0",
                    "editor_frame_bg": "white", "editor_frame_fg": "black",
                    "input_bg": "white", "input_fg": "black"
                },
                "dark": {
                    "name": "Dark",
                    "text_bg": "#1e1e1e", "text_fg": "#d4d4d4",
                    "canvas_bg": "#2d2d2d", "canvas_border": "#3e3e3e",
                    "root_bg": "#252526", "frame_bg": "#252526",
                    "editor_frame_bg": "#252526", "editor_frame_fg": "#d4d4d4",
                    "input_bg": "#1e1e1e", "input_fg": "#d4d4d4"
                },
                "classic": {
                    "name": "Classic",
                    "text_bg": "white", "text_fg": "black",
                    "canvas_bg": "#fffef0", "canvas_border": "#cccccc",
                    "root_bg": "#e0e0e0", "frame_bg": "#e0e0e0",
                    "editor_frame_bg": "#e0e0e0", "editor_frame_fg": "black",
                    "input_bg": "white", "input_fg": "black"
                },
                "solarized_dark": {
                    "name": "Solarized Dark",
                    "text_bg": "#002b36", "text_fg": "#839496",
                    "canvas_bg": "#073642", "canvas_border": "#586e75",
                    "root_bg": "#002b36", "frame_bg": "#002b36",
                    "editor_frame_bg": "#002b36", "editor_frame_fg": "#839496",
                    "input_bg": "#073642", "input_fg": "#839496"
                },
                "solarized_light": {
                    "name": "Solarized Light",
                    "text_bg": "#fdf6e3", "text_fg": "#657b83",
                    "canvas_bg": "#eee8d5", "canvas_border": "#93a1a1",
                    "root_bg": "#fdf6e3", "frame_bg": "#fdf6e3",
                    "editor_frame_bg": "#fdf6e3", "editor_frame_fg": "#657b83",
                    "input_bg": "#eee8d5", "input_fg": "#657b83"
                },
                "monokai": {
                    "name": "Monokai",
                    "text_bg": "#272822", "text_fg": "#f8f8f2",
                    "canvas_bg": "#3e3d32", "canvas_border": "#75715e",
                    "root_bg": "#272822", "frame_bg": "#272822",
                    "editor_frame_bg": "#272822", "editor_frame_fg": "#f8f8f2",
                    "input_bg": "#3e3d32", "input_fg": "#f8f8f2"
                },
                "dracula": {
                    "name": "Dracula",
                    "text_bg": "#282a36", "text_fg": "#f8f8f2",
                    "canvas_bg": "#44475a", "canvas_border": "#6272a4",
                    "root_bg": "#282a36", "frame_bg": "#282a36",
                    "editor_frame_bg": "#282a36", "editor_frame_fg": "#f8f8f2",
                    "input_bg": "#44475a", "input_fg": "#f8f8f2"
                },
                "nord": {
                    "name": "Nord",
                    "text_bg": "#2e3440", "text_fg": "#d8dee9",
                    "canvas_bg": "#3b4252", "canvas_border": "#4c566a",
                    "root_bg": "#2e3440", "frame_bg": "#2e3440",
                    "editor_frame_bg": "#2e3440", "editor_frame_fg": "#d8dee9",
                    "input_bg": "#3b4252", "input_fg": "#d8dee9"
                },
                "high_contrast": {
                    "name": "High Contrast",
                    "text_bg": "black", "text_fg": "white",
                    "canvas_bg": "#0a0a0a", "canvas_border": "white",
                    "root_bg": "black", "frame_bg": "black",
                    "editor_frame_bg": "black", "editor_frame_fg": "white",
                    "input_bg": "#0a0a0a", "input_fg": "white"
                }
            }

            def apply_theme(theme_key):
                """Apply a theme to all UI elements."""
                nonlocal current_theme
                theme = THEMES[theme_key]
                
                # Text widgets
                editor_text.config(bg=theme["text_bg"], fg=theme["text_fg"], 
                                 insertbackground=theme["text_fg"])
                output_text.config(bg=theme["text_bg"], fg=theme["text_fg"], 
                                 insertbackground=theme["text_fg"])
                
                # Canvas
                turtle_canvas.config(bg=theme["canvas_bg"], 
                                   highlightbackground=theme["canvas_border"])
                
                # Frames
                root.config(bg=theme["root_bg"])
                left_panel.config(bg=theme["frame_bg"])
                right_panel.config(bg=theme["frame_bg"])
                editor_frame.config(bg=theme["editor_frame_bg"], fg=theme["editor_frame_fg"])
                output_frame.config(bg=theme["editor_frame_bg"], fg=theme["editor_frame_fg"])
                graphics_frame.config(bg=theme["editor_frame_bg"], fg=theme["editor_frame_fg"])
                input_frame.config(bg=theme["frame_bg"])
                button_frame.config(bg=theme["frame_bg"])
                editor_header.config(bg=theme["frame_bg"])
                
                # Input widget
                input_entry.config(bg=theme["input_bg"], fg=theme["input_fg"], 
                                 insertbackground=theme["input_fg"])
                
                # Update labels
                for widget in editor_header.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.config(bg=theme["frame_bg"], fg=theme["text_fg"])
                for widget in input_frame.winfo_children():
                    if isinstance(widget, tk.Label):
                        widget.config(bg=theme["frame_bg"], fg=theme["text_fg"])
                
                # Save setting
                current_theme = theme_key
                save_settings(current_theme, current_font, current_font_family)

            # Add theme menu items
            for theme_key, theme_data in THEMES.items():
                theme_menu.add_command(
                    label=theme_data["name"],
                    command=lambda k=theme_key: apply_theme(k)
                )

            # Font family submenu
            font_family_menu = tk.Menu(preferences_menu, tearoff=0)
            preferences_menu.add_cascade(label="Font Family", menu=font_family_menu)

            def get_available_fonts():
                """Get list of available monospace fonts on the system."""
                import tkinter.font as tkfont
                
                # Get all available font families
                all_fonts = sorted(set(tkfont.families()))
                
                # Prioritize common monospace fonts
                priority_fonts = [
                    "Courier", "Courier New", "Consolas", "Monaco", "Menlo",
                    "DejaVu Sans Mono", "Liberation Mono", "Ubuntu Mono",
                    "Fira Code", "Source Code Pro", "JetBrains Mono",
                    "Cascadia Code", "SF Mono", "Inconsolata", "Roboto Mono",
                    "Hack", "Anonymous Pro", "Droid Sans Mono", "PT Mono"
                ]
                
                # Separate priority fonts that exist from the rest
                priority_available = [f for f in priority_fonts if f in all_fonts]
                other_fonts = [f for f in all_fonts if f not in priority_fonts]
                
                # Return priority fonts first, then others
                return priority_available + other_fonts

            def apply_font_family(family_name):
                """Apply a font family to editor and output."""
                nonlocal current_font_family
                size = FONT_SIZES[current_font]
                editor_text.config(font=(family_name, size["editor"]))
                output_text.config(font=(family_name, size["output"]))
                
                # Save setting
                current_font_family = family_name
                save_settings(current_theme, current_font, current_font_family)

            # Get available fonts and create menu items
            available_fonts = get_available_fonts()
            
            # Add first 25 fonts directly to menu
            for i, font_name in enumerate(available_fonts[:25]):
                font_family_menu.add_command(
                    label=font_name,
                    command=lambda f=font_name: apply_font_family(f)
                )
            
            # If there are more fonts, add "More Fonts..." submenu
            if len(available_fonts) > 25:
                font_family_menu.add_separator()
                more_fonts_menu = tk.Menu(font_family_menu, tearoff=0)
                font_family_menu.add_cascade(label="More Fonts...", menu=more_fonts_menu)
                
                # Add remaining fonts to submenu in batches
                for i, font_name in enumerate(available_fonts[25:]):
                    more_fonts_menu.add_command(
                        label=font_name,
                        command=lambda f=font_name: apply_font_family(f)
                    )

            # Font size submenu
            font_menu = tk.Menu(preferences_menu, tearoff=0)
            preferences_menu.add_cascade(label="Font Size", menu=font_menu)

            # Define font size configurations
            FONT_SIZES = {
                "tiny": {"name": "Tiny (8pt)", "editor": 8, "output": 8},
                "small": {"name": "Small (10pt)", "editor": 10, "output": 9},
                "medium": {"name": "Medium (12pt)", "editor": 12, "output": 11},
                "large": {"name": "Large (14pt)", "editor": 14, "output": 13},
                "xlarge": {"name": "Extra Large (16pt)", "editor": 16, "output": 15},
                "xxlarge": {"name": "Huge (18pt)", "editor": 18, "output": 17},
                "xxxlarge": {"name": "Giant (22pt)", "editor": 22, "output": 20}
            }

            def apply_font_size(size_key):
                """Apply a font size to editor and output."""
                nonlocal current_font
                size = FONT_SIZES[size_key]
                editor_text.config(font=(current_font_family, size["editor"]))
                output_text.config(font=(current_font_family, size["output"]))
                
                # Save setting
                current_font = size_key
                save_settings(current_theme, current_font, current_font_family)

            # Add font menu items
            for size_key, size_data in FONT_SIZES.items():
                font_menu.add_command(
                    label=size_data["name"],
                    command=lambda k=size_key: apply_font_size(k)
                )

            # About menu
            about_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="About", menu=about_menu)

            def show_about():
                """Show about dialog with one top/bottom separator safely sized."""
                # Use a very short ASCII separator to avoid any wrapping
                sep = "-" * 32

                about_text = (
                    f"{sep}\n"
                    "Time Warp Classic\n"
                    "Version 1.3.0\n\n"
                    "A multi-language playground for exploring\n"
                    "vintage and modern programming styles.\n\n"
                    "FEATURES:\n"
                    "  • 9 classic programming languages\n"
                    "  • Built-in example programs\n"
                    "  • Turtle graphics canvas\n"
                    "  • Multiple color themes\n"
                    "  • Customizable fonts\n"
                    "  • Persistent settings\n\n"
                    "LANGUAGES:\n"
                    "  PILOT • BASIC • Logo • Pascal\n"
                    "  Prolog • Forth • Perl • Python • JavaScript\n\n"
                    f"{sep}\n"
                    "Copyright © 2025 Honey Badger Universe"
                )

                messagebox.showinfo("Time Warp Classic", about_text)

            about_menu.add_command(label="About Time Warp Classic", command=show_about)

            # Keyboard bindings
            root.bind("<F5>", lambda e: run_code())
            root.bind("<Control-n>", lambda e: new_file())
            root.bind("<Control-o>", lambda e: load_file())
            root.bind("<Control-s>", lambda e: save_file())
            root.bind("<Control-q>", lambda e: exit_app())

            # Edit operation bindings
            root.bind("<Control-z>", lambda e: undo_text())
            root.bind("<Control-y>", lambda e: redo_text())
            root.bind("<Control-a>", lambda e: select_all())

            # Create GUI layout with PanedWindow for resizable sections
            main_paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashwidth=5, bg="#252526")
            main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            # Left panel - Editor
            left_panel = tk.Frame(main_paned, bg="#252526")
            main_paned.add(left_panel, width=400)

            # Editor frame with language selector
            editor_header = tk.Frame(left_panel, bg="#252526")
            editor_header.pack(fill=tk.X, pady=(0, 5))

            tk.Label(editor_header, text="Language:", font=("Arial", 9), bg="#252526", fg="#d4d4d4").pack(
                side=tk.LEFT, padx=(5, 5)
            )

            language_var = tk.StringVar(value="PILOT")
            language_selector = tk.OptionMenu(
                editor_header,
                language_var,
                "PILOT",
                "BASIC",
                "Logo",
                "Pascal",
                "Prolog",
                "Forth",
                "Perl",
                "Python",
                "JavaScript",
            )
            language_selector.config(width=10)
            language_selector.pack(side=tk.LEFT)

            editor_frame = tk.LabelFrame(left_panel, text="Code Editor", padx=5, pady=5, bg="#252526", fg="#d4d4d4")
            editor_frame.pack(fill=tk.BOTH, expand=True)

            # Editor text widget with undo/redo enabled
            editor_text = scrolledtext.ScrolledText(
                editor_frame, wrap=tk.WORD, font=("Courier", 11), undo=True, maxundo=-1,
                bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4"
            )
            editor_text.pack(fill=tk.BOTH, expand=True)

            # Right panel - Split between output and graphics
            right_panel = tk.Frame(main_paned, bg="#252526")
            main_paned.add(right_panel, width=800)

            # Right vertical paned window
            right_paned = tk.PanedWindow(right_panel, orient=tk.VERTICAL, sashwidth=5, bg="#252526")
            right_paned.pack(fill=tk.BOTH, expand=True)

            # Output frame (top of right panel)
            output_frame = tk.LabelFrame(right_paned, text="Output", padx=5, pady=5, bg="#252526", fg="#d4d4d4")
            right_paned.add(output_frame, height=300)

            # Output text widget
            output_text = scrolledtext.ScrolledText(
                output_frame,
                wrap=tk.WORD,
                font=("Courier", 10),
                bg="#1e1e1e",
                fg="#d4d4d4",
                insertbackground="#d4d4d4",
            )
            output_text.pack(fill=tk.BOTH, expand=True)

            # Graphics canvas frame (bottom of right panel)
            graphics_frame = tk.LabelFrame(
                right_paned, text="Turtle Graphics", padx=5, pady=5,
                bg="#252526", fg="#d4d4d4"
            )
            right_paned.add(graphics_frame, height=300)

            # Turtle graphics canvas
            turtle_canvas = tk.Canvas(
                graphics_frame,
                width=600,
                height=400,
                bg="#2d2d2d",
                highlightthickness=1,
                highlightbackground="#3e3e3e",
            )
            turtle_canvas.pack(fill=tk.BOTH, expand=True)

            # Input frame at the bottom
            input_frame = tk.Frame(root, bg="#252526")
            input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

            tk.Label(input_frame, text="Input:", font=("Arial", 10), bg="#252526", fg="#d4d4d4").pack(
                side=tk.LEFT, padx=(0, 5)
            )
            input_entry = tk.Entry(input_frame, font=("Courier", 10), bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4")
            input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

            input_buffer = []

            def submit_input():
                """Submit input from entry field."""
                value = input_entry.get()
                input_buffer.append(value)
                output_text.insert(tk.END, f">> {value}\n")
                input_entry.delete(0, tk.END)

            input_entry.bind("<Return>", lambda e: submit_input())
            tk.Button(input_frame, text="Submit", command=submit_input, bg="#3e3e3e", fg="#d4d4d4").pack(
                side=tk.LEFT
            )

            # Initialize the interpreter with output widget and canvas
            interpreter = Time_WarpInterpreter(output_text)
            interpreter.ide_turtle_canvas = turtle_canvas

            # Control buttons frame
            button_frame = tk.Frame(root, bg="#252526")
            button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

            # Create buttons
            tk.Button(
                button_frame,
                text="▶ Run",
                command=run_code,
                bg="#4CAF50",
                fg="white",
                font=("Arial", 10, "bold"),
                padx=20,
            ).pack(side=tk.LEFT, padx=5)

            tk.Button(button_frame, text="📂 Open", command=load_file, padx=20, bg="#3e3e3e", fg="#d4d4d4").pack(
                side=tk.LEFT, padx=5
            )

            tk.Button(button_frame, text="💾 Save", command=save_file, padx=20, bg="#3e3e3e", fg="#d4d4d4").pack(
                side=tk.LEFT, padx=5
            )

            tk.Button(
                button_frame, text="🗑️ Clear Editor", command=clear_editor, padx=15, bg="#3e3e3e", fg="#d4d4d4"
            ).pack(side=tk.LEFT, padx=5)

            tk.Button(
                button_frame, text="📄 Clear Output", command=clear_output, padx=15, bg="#3e3e3e", fg="#d4d4d4"
            ).pack(side=tk.LEFT, padx=5)

            tk.Button(
                button_frame, text="🎨 Clear Graphics", command=clear_canvas, padx=15, bg="#3e3e3e", fg="#d4d4d4"
            ).pack(side=tk.LEFT, padx=5)

            # Add welcome message
            welcome_msg = """Welcome to Time Warp Classic! 🚀

Supported Languages:
• PILOT   - Educational language (T:, A:, J:, Y:, N: commands)
• BASIC   - Classic line-numbered programming
• Logo    - Turtle graphics programming
• Pascal  - Structured programming
• Prolog  - Logic programming
• Forth   - Stack-based programming
• Perl    - Scripting language
• Python  - Modern programming
• JavaScript - Web scripting

Enter your code in the left panel and click Run to execute!
"""
            output_text.insert("1.0", welcome_msg)

            # Apply saved theme and font settings
            apply_theme(current_theme)
            apply_font_size(current_font)

            # Start the GUI event loop
            root.mainloop()
            sys.exit(0)
    except Exception as e:
        print(f"❌ GUI launch failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
