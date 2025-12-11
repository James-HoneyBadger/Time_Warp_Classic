#!/usr/bin/env python3
"""
Time_Warp - Multi-Language Interpreter CLI

A command-line multi-language interpreter supporting 9 programming languages
with integrated turtle graphics. Provides both direct execution and syntax
highlighting capabilities.

Supports: PILOT, BASIC, Logo, Pascal, Prolog, Forth, Perl, Python, JavaScript

Features:
- Automatic dependency checking and installation
- Command-line interface for program execution
- Syntax highlighting for code display
- Turtle graphics for visual programming
- Educational error messages and feedback

Usage:
    python Time_Warp.py --cli        # Launch CLI mode (recommended)
    python Time_Warp.py --check      # Check dependencies only
"""
# pylint: disable=C0301,C0103,R1705,W0621,W0718,W0404,C0415,W1510

import sys
import argparse
import subprocess
import importlib.util


class DependencyChecker:
    """Check and install required Python components."""

    REQUIRED_PACKAGES = [
        "pygame",  # Graphics and multimedia
        "PIL",  # Image processing (Pillow)
    ]

    OPTIONAL_PACKAGES = [
        "pygments",  # Syntax highlighting
        "pytest",  # Testing (development)
        "black",  # Code formatting (development)
        "flake8",  # Linting (development)
    ]

    def __init__(self):
        self.missing_required = []
        self.missing_optional = []
        self.python_version_ok = True

    def check_python_version(self):
        """Check if Python version is compatible."""
        if sys.version_info < (3, 9):
            self.python_version_ok = False
            print(
                f"❌ Python {sys.version_info.major}.{sys.version_info.minor} detected."
            )
            print("   Time_Warp IDE requires Python 3.9 or higher.")
            return False
        print(
            f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro} detected."
        )
        return True

    def check_package(self, package_name):
        """Check if a Python package is available."""
        try:
            if package_name == "PIL":
                # PIL is from Pillow package - use importlib to avoid unused import warning
                importlib.import_module("PIL")
                return True
            else:
                # Try to import the package
                importlib.import_module(package_name)
                return True
        except ImportError:
            return False

    def check_dependencies(self):
        """Check all required and optional dependencies."""
        print("🔍 Checking dependencies...")

        # Clear previous check results
        self.missing_required = []
        self.missing_optional = []

        # Check required packages
        for package in self.REQUIRED_PACKAGES:
            if not self.check_package(package):
                self.missing_required.append(package)
                print(f"❌ Missing required package: {package}")
            else:
                print(f"✅ Found required package: {package}")

        # Check optional packages
        for package in self.OPTIONAL_PACKAGES:
            if not self.check_package(package):
                self.missing_optional.append(package)
                print(f"⚠️  Missing optional package: {package}")
            else:
                print(f"✅ Found optional package: {package}")

        return len(self.missing_required) == 0

    def install_missing_packages(self):
        """Attempt to install missing packages using pip."""
        if not self.missing_required:
            print("✅ All required dependencies are satisfied!")
            return True

        print("\n🔧 Attempting to install missing packages...")
        print("   This may require administrator privileges.")

        success = True
        for package in self.missing_required:
            try:
                print(f"📦 Installing {package}...")
                if package == "PIL":
                    # PIL comes from Pillow
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", "Pillow"]
                    )
                else:
                    subprocess.check_call(
                        [sys.executable, "-m", "pip", "install", package]
                    )
                print(f"✅ Successfully installed {package}")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {package}")
                success = False

        return success

    def run_full_check(self):
        """Run complete dependency check and installation."""
        print("🚀 Time_Warp IDE - Dependency Check")
        print("=" * 40)

        # Check Python version
        if not self.check_python_version():
            return False

        # Check dependencies
        deps_ok = self.check_dependencies()

        # Try to install missing dependencies
        if not deps_ok:
            if self.install_missing_packages():
                print("\n🔄 Re-checking dependencies after installation...")
                deps_ok = self.check_dependencies()

        print("\n" + "=" * 40)
        if deps_ok:
            print("✅ All checks passed! Time_Warp IDE is ready to run.")
            return True
        else:
            print("❌ Some required dependencies are still missing.")
            print("   Please install them manually or check your Python environment.")
            return False


def main():
    """Main entry point - launches Time_Warp CLI."""
    parser = argparse.ArgumentParser(
        description="Time_Warp - Multi-Language Interpreter CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python Time_Warp.py list               # List example programs
  python Time_Warp.py run file.bas       # Run a program
  python Time_Warp.py cat file.py        # Display with syntax highlighting
  python Time_Warp.py --check            # Check dependencies only
        """,
    )

    parser.add_argument(
        "command",
        nargs="?",  # Optional positional argument
        help="CLI command to execute",
    )

    parser.add_argument(
        "args",
        nargs="*",  # Zero or more additional arguments
        help="Arguments for the CLI command",
    )

    parser.add_argument(
        "--check", action="store_true", help="Check dependencies and exit"
    )

    args = parser.parse_args()

    # Initialize dependency checker
    deps_checker = DependencyChecker()

    # Check dependencies first
    if not deps_checker.run_full_check():
        print("\n❌ Dependency check failed. Please resolve issues above.")
        sys.exit(1)

    # If just checking dependencies, exit
    if args.check:
        sys.exit(0)

    # If no command specified, launch GUI
    if not args.command:
        print("🚀 Launching Time_Warp IDE GUI...")
        try:
            # Import and launch the GUI application
            import tkinter as tk
            from tkinter import scrolledtext, messagebox, filedialog
            from core.interpreter import Time_WarpInterpreter

            # Create the main GUI window
            root = tk.Tk()
            root.title("Time_Warp IDE - Multi-Language Programming Environment")
            root.geometry("1200x800")

            # Create menu bar
            menubar = tk.Menu(root)
            root.config(menu=menubar)

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

                        # Auto-detect language from file extension
                        ext_to_lang = {
                            '.pilot': 'PILOT',
                            '.bas': 'BASIC',
                            '.logo': 'Logo',
                            '.py': 'Python',
                            '.js': 'JavaScript',
                            '.pl': 'Perl',
                            '.pas': 'Pascal',
                            '.fth': 'Forth',
                            '.4th': 'Forth',
                            '.pro': 'Prolog'
                        }
                        import os
                        _, ext = os.path.splitext(filename)
                        if ext.lower() in ext_to_lang:
                            language_var.set(ext_to_lang[ext.lower()])
                            output_text.insert(tk.END, f"📂 Loaded: {filename} ({ext_to_lang[ext.lower()]})\n")
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
                        '.pl': 'Perl',
                        '.pas': 'Pascal',
                        '.fth': 'Forth',
                        '.4th': 'Forth',
                        '.pro': 'Prolog'
                    }
                    import os
                    _, ext = os.path.splitext(filepath)
                    if ext.lower() in ext_to_lang:
                        language_var.set(ext_to_lang[ext.lower()])
                        output_text.insert(tk.END, f"📚 Loaded example: {filepath} ({ext_to_lang[ext.lower()]})\n")
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

            # View menu
            view_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="View", menu=view_menu)

            def clear_canvas():
                """Clear the turtle graphics canvas."""
                turtle_canvas.delete("all")
                output_text.insert(tk.END, "🎨 Canvas cleared\n")

            def toggle_output():
                """Toggle output panel visibility."""
                if output_frame.winfo_viewable():
                    right_paned.forget(output_frame)
                else:
                    right_paned.add(output_frame, before=graphics_frame)

            def toggle_graphics():
                """Toggle graphics panel visibility."""
                if graphics_frame.winfo_viewable():
                    right_paned.forget(graphics_frame)
                else:
                    right_paned.add(graphics_frame)

            view_menu.add_checkbutton(label="Output Panel", command=toggle_output)
            view_menu.add_checkbutton(
                label="Graphics Panel", command=toggle_graphics
            )
            view_menu.add_separator()
            view_menu.add_command(label="Clear Canvas", command=clear_canvas)
            view_menu.add_command(label="Clear Output", command=clear_output)
            view_menu.add_command(label="Clear Editor", command=clear_editor)

            # Preferences menu
            preferences_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Preferences", menu=preferences_menu)

            # Theme submenu
            theme_menu = tk.Menu(preferences_menu, tearoff=0)
            preferences_menu.add_cascade(label="Color Theme", menu=theme_menu)

            def set_theme_light():
                """Set light theme."""
                output_text.config(bg="white", fg="black")
                editor_text.config(bg="white", fg="black")

            def set_theme_dark():
                """Set dark theme."""
                output_text.config(bg="#1e1e1e", fg="#d4d4d4")
                editor_text.config(bg="#1e1e1e", fg="#d4d4d4")

            def set_theme_classic():
                """Set classic theme."""
                output_text.config(bg="#f0f0f0", fg="black")
                editor_text.config(bg="white", fg="black")

            theme_menu.add_command(label="Light Theme", command=set_theme_light)
            theme_menu.add_command(label="Dark Theme", command=set_theme_dark)
            theme_menu.add_command(label="Classic Theme", command=set_theme_classic)

            # Font submenu
            font_menu = tk.Menu(preferences_menu, tearoff=0)
            preferences_menu.add_cascade(label="Font Size", menu=font_menu)

            def set_font_small():
                """Set small font size."""
                editor_text.config(font=("Courier", 9))
                output_text.config(font=("Courier", 9))

            def set_font_medium():
                """Set medium font size."""
                editor_text.config(font=("Courier", 11))
                output_text.config(font=("Courier", 10))

            def set_font_large():
                """Set large font size."""
                editor_text.config(font=("Courier", 14))
                output_text.config(font=("Courier", 13))

            def set_font_xlarge():
                """Set extra large font size."""
                editor_text.config(font=("Courier", 16))
                output_text.config(font=("Courier", 15))

            font_menu.add_command(label="Small (9pt)", command=set_font_small)
            font_menu.add_command(label="Medium (11pt)", command=set_font_medium)
            font_menu.add_command(label="Large (14pt)", command=set_font_large)
            font_menu.add_command(label="Extra Large (16pt)", command=set_font_xlarge)

            # Help menu
            help_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="Help", menu=help_menu)

            def show_about():
                """Show about dialog."""
                messagebox.showinfo(
                    "About Time_Warp IDE",
                    "Time_Warp IDE\n"
                    "Version 1.3.0\n\n"
                    "A Multi-Language Programming Environment\n"
                    "for Vintage and Modern Languages\n\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "Supported Languages:\n"
                    "  PILOT  •  BASIC  •  Logo\n"
                    "  Pascal  •  Prolog  •  Forth\n"
                    "  Perl  •  Python  •  JavaScript\n\n"
                    "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                    "© 2025 Time_Warp Project\n"
                    "Educational Software",
                )

            def show_help():
                """Show help information."""
                help_text = """━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Time_Warp IDE - Getting Started
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

QUICK START:
  1. Select your programming language
  2. Write code in the editor panel
  3. Press F5 or use Program → Run
  4. View output and graphics

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

KEYBOARD SHORTCUTS:
  F5             Run Program
  F1             Show Help
  
  Ctrl+N         New File
  Ctrl+O         Open File
  Ctrl+S         Save File
  Ctrl+Q         Exit
  
  Ctrl+Z         Undo
  Ctrl+Y         Redo
  Ctrl+X         Cut
  Ctrl+C         Copy
  Ctrl+V         Paste
  Ctrl+A         Select All

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUPPORTED LANGUAGES:
  PILOT      Educational language with
             interactive prompts
  
  BASIC      Classic line-numbered
             programming with graphics
  
  Logo       Turtle graphics for
             creative visual programs
  
  Pascal     Structured programming
             with strong typing
  
  Prolog     Logic programming with
             facts and rules
  
  Forth      Stack-based language
             with RPN notation
  
  Perl       Text processing and
             pattern matching
  
  Python     Modern, general-purpose
             programming
  
  JavaScript Modern web scripting
             with ES6+ features

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MENU GUIDE:
  File         Create, open, save files
  Edit         Standard text operations
  Program      Run code & load examples
  View         Toggle panels, clear displays
  Preferences  Customize theme & fonts
  Help         Documentation & about

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For example programs, visit:
  Program → Load Example

Enjoy programming through the ages!"""
                messagebox.showinfo("Getting Started - Time_Warp IDE", help_text)

            help_menu.add_command(label="Getting Started", command=show_help, accelerator="F1")
            help_menu.add_separator()
            help_menu.add_command(label="About Time_Warp IDE", command=show_about)

            # Keyboard bindings
            root.bind("<F5>", lambda e: run_code())
            root.bind("<Control-n>", lambda e: new_file())
            root.bind("<Control-o>", lambda e: load_file())
            root.bind("<Control-s>", lambda e: save_file())
            root.bind("<Control-q>", lambda e: exit_app())
            root.bind("<F1>", lambda e: show_help())

            # Edit operation bindings
            root.bind("<Control-z>", lambda e: undo_text())
            root.bind("<Control-y>", lambda e: redo_text())
            root.bind("<Control-a>", lambda e: select_all())

            # Create GUI layout with PanedWindow for resizable sections
            main_paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashwidth=5)
            main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

            # Left panel - Editor
            left_panel = tk.Frame(main_paned)
            main_paned.add(left_panel, width=400)

            # Editor frame with language selector
            editor_header = tk.Frame(left_panel)
            editor_header.pack(fill=tk.X, pady=(0, 5))

            tk.Label(editor_header, text="Language:", font=("Arial", 9)).pack(
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

            editor_frame = tk.LabelFrame(left_panel, text="Code Editor", padx=5, pady=5)
            editor_frame.pack(fill=tk.BOTH, expand=True)

            # Editor text widget with undo/redo enabled
            editor_text = scrolledtext.ScrolledText(
                editor_frame, wrap=tk.WORD, font=("Courier", 11), undo=True, maxundo=-1
            )
            editor_text.pack(fill=tk.BOTH, expand=True)

            # Right panel - Split between output and graphics
            right_panel = tk.Frame(main_paned)
            main_paned.add(right_panel, width=800)

            # Right vertical paned window
            right_paned = tk.PanedWindow(right_panel, orient=tk.VERTICAL, sashwidth=5)
            right_paned.pack(fill=tk.BOTH, expand=True)

            # Output frame (top of right panel)
            output_frame = tk.LabelFrame(right_paned, text="Output", padx=5, pady=5)
            right_paned.add(output_frame, height=300)

            # Output text widget
            output_text = scrolledtext.ScrolledText(
                output_frame,
                wrap=tk.WORD,
                font=("Courier", 10),
                bg="#1e1e1e",
                fg="#d4d4d4",
            )
            output_text.pack(fill=tk.BOTH, expand=True)

            # Graphics canvas frame (bottom of right panel)
            graphics_frame = tk.LabelFrame(
                right_paned, text="Turtle Graphics", padx=5, pady=5
            )
            right_paned.add(graphics_frame, height=300)

            # Turtle graphics canvas
            turtle_canvas = tk.Canvas(
                graphics_frame,
                width=600,
                height=400,
                bg="white",
                highlightthickness=1,
                highlightbackground="#cccccc",
            )
            turtle_canvas.pack(fill=tk.BOTH, expand=True)

            # Input frame at the bottom
            input_frame = tk.Frame(root)
            input_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

            tk.Label(input_frame, text="Input:", font=("Arial", 10)).pack(
                side=tk.LEFT, padx=(0, 5)
            )
            input_entry = tk.Entry(input_frame, font=("Courier", 10))
            input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

            input_buffer = []

            def submit_input():
                """Submit input from entry field."""
                value = input_entry.get()
                input_buffer.append(value)
                output_text.insert(tk.END, f">> {value}\n")
                input_entry.delete(0, tk.END)

            input_entry.bind("<Return>", lambda e: submit_input())
            tk.Button(input_frame, text="Submit", command=submit_input).pack(
                side=tk.LEFT
            )

            # Initialize the interpreter with output widget and canvas
            interpreter = Time_WarpInterpreter(output_text)
            interpreter.ide_turtle_canvas = turtle_canvas

            # Control buttons frame
            button_frame = tk.Frame(root)
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

            tk.Button(button_frame, text="📂 Open", command=load_file, padx=20).pack(
                side=tk.LEFT, padx=5
            )

            tk.Button(button_frame, text="💾 Save", command=save_file, padx=20).pack(
                side=tk.LEFT, padx=5
            )

            tk.Button(
                button_frame, text="🗑️ Clear Editor", command=clear_editor, padx=15
            ).pack(side=tk.LEFT, padx=5)

            tk.Button(
                button_frame, text="📄 Clear Output", command=clear_output, padx=15
            ).pack(side=tk.LEFT, padx=5)

            tk.Button(
                button_frame, text="🎨 Clear Graphics", command=clear_canvas, padx=15
            ).pack(side=tk.LEFT, padx=5)

            # Add welcome message
            welcome_msg = """Welcome to Time_Warp IDE! 🚀

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

            # Start the GUI event loop
            root.mainloop()
            sys.exit(0)
        except Exception as e:
            print(f"❌ GUI launch failed: {e}")
            import traceback

            traceback.print_exc()
            print("   Falling back to CLI mode...")
            print("   Try: python Time_Warp.py help")
            sys.exit(1)

    # Launch CLI mode with provided arguments
    print("🚀 Launching Time_Warp CLI...")
    try:
        # Build CLI command with arguments
        cli_args = ["scripts/timewarp-cli.py"]
        if args.command:
            cli_args.append(args.command)
        if args.args:
            cli_args.extend(args.args)

        # Run the CLI script with arguments
        import subprocess

        result = subprocess.run(
            [sys.executable] + cli_args, capture_output=False, text=True
        )
        if result.returncode != 0:
            print(f"❌ CLI exited with code {result.returncode}")
    except Exception as e:
        print(f"❌ CLI not available: {e}")
        print("   Try: python scripts/timewarp-cli.py")
        sys.exit(1)


if __name__ == "__main__":
    main()
