#!/usr/bin/env python3
"""
Time_Warp CLI - Command Line Interface for Time_Warp IDE

A command-line interface for running Time_Warp programs without the GUI.
Supports all Time_Warp languages: PILOT, BASIC, Logo, Python, JavaScript,
Perl, Pascal, Forth, and Prolog.

Usage:
    python timewarp-cli.py [command] [options]

Commands:
    run <file>        Run a program file
    cat <file>        Display a program file with syntax highlighting
    list              List available example programs
    info <language>   Show information about a language
    help              Show this help message
    version           Show version information

Examples:
    python timewarp-cli.py run examples/basic/hello_world.bas
    python timewarp-cli.py cat examples/basic/hello_world.bas
    python timewarp-cli.py list
    python timewarp-cli.py info basic
"""
# pylint: disable=C0301,C0103,E0401,C0413,W0718,R1705,R0911

import os
import sys
import argparse
from pathlib import Path

# Add the project root to Python path so we can import core modules
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.interpreter import Time_WarpInterpreter  # noqa: E402

# Try to import pygments for syntax highlighting
try:
    from pygments import highlight
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.formatters import TerminalFormatter

    SYNTAX_HIGHLIGHTING_AVAILABLE = True
except ImportError:
    SYNTAX_HIGHLIGHTING_AVAILABLE = False


class TimeWarpCLI:
    """Command Line Interface for Time_Warp IDE"""

    def __init__(self):
        self.interpreter = Time_WarpInterpreter()
        self.project_root = Path(__file__).parent.parent
        self.examples_dir = self.project_root / "examples"

        # Language information
        self.language_info = {
            "pilot": {
                "name": "PILOT",
                "description": "Programmed Inquiry, Learning Or Teaching - Educational language",
                "extensions": [".pilot"],
                "features": [
                    "Interactive lessons",
                    "Conditional responses",
                    "Turtle graphics",
                ],
            },
            "basic": {
                "name": "BASIC",
                "description": "Beginner's All-purpose Symbolic Instruction Code",
                "extensions": [".bas", ".basic"],
                "features": [
                    "Line-numbered syntax",
                    "Turbo BASIC extensions",
                    "Structured programming",
                ],
            },
            "logo": {
                "name": "Logo",
                "description": "Educational programming language with turtle graphics",
                "extensions": [".logo"],
                "features": [
                    "Turtle graphics",
                    "Procedural programming",
                    "Educational focus",
                ],
            },
            "python": {
                "name": "Python",
                "description": "Modern high-level scripting language",
                "extensions": [".py"],
                "features": [
                    "Clean syntax",
                    "Extensive libraries",
                    "General-purpose",
                ],
            },
            "javascript": {
                "name": "JavaScript",
                "description": "Web scripting language with modern features",
                "extensions": [".js"],
                "features": [
                    "Async programming",
                    "Object-oriented",
                    "Web development",
                ],
            },
            "perl": {
                "name": "Perl",
                "description": "Powerful text processing and system administration language",
                "extensions": [".pl", ".perl"],
                "features": [
                    "Regular expressions",
                    "Text processing",
                    "System scripting",
                ],
            },
            "pascal": {
                "name": "Pascal",
                "description": "Structured programming language emphasizing readability",
                "extensions": [".pas", ".pp"],
                "features": [
                    "Strong typing",
                    "Structured programming",
                    "Educational",
                ],
            },
            "forth": {
                "name": "Forth",
                "description": "Stack-based programming language",
                "extensions": [".fs", ".forth"],
                "features": [
                    "Stack manipulation",
                    "Low-level control",
                    "Efficiency",
                ],
            },
            "prolog": {
                "name": "Prolog",
                "description": "Logic programming language based on formal logic",
                "extensions": [".pl", ".prolog"],
                "features": [
                    "Pattern matching",
                    "Logical queries",
                    "AI applications",
                ],
            },
        }

    def _detect_language(self, file_path):
        """Detect language from file extension only."""
        ext = Path(file_path).suffix.lower()
        mapping = {
            ".pil": "pilot",
            ".bas": "basic",
            ".logo": "logo",
            ".py": "python",
            ".js": "javascript",
            ".pas": "pascal",
            ".fth": "forth",
            ".pro": "prolog",
            ".pl": "perl",
        }
        return mapping.get(ext)

    def run_program(self, file_path):
        """Run a program from a file"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"❌ Error: File '{file_path}' not found")
                return 1

            # Read the program
            with open(file_path, "r", encoding="utf-8") as f:
                program_code = f.read().strip()

            if not program_code:
                print(f"❌ Error: File '{file_path}' is empty")
                return 1

            language = self._detect_language(file_path)

            print(f"🚀 Running: {file_path}")
            if language:
                print(f"🌐 Detected language: {language}")
            print("=" * 50)

            # Run the program with an explicit language when we can
            self.interpreter.run_program(program_code, language=language)

            print("=" * 50)
            print("✅ Program execution completed")
            return 0

        except Exception as e:
            print(f"❌ Error running program: {str(e)}")
            return 1

    def display_file(self, file_path):
        """Display a program file with syntax highlighting"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"❌ Error: File '{file_path}' not found")
                return 1

            # Read the program
            with open(file_path, "r", encoding="utf-8") as f:
                program_code = f.read().strip()

            if not program_code:
                print(f"❌ Error: File '{file_path}' is empty")
                return 1

            try:
                print(f"📄 {file_path}")
                print("=" * 50)

                # Display with syntax highlighting if available
                if SYNTAX_HIGHLIGHTING_AVAILABLE:
                    highlighted_code = self._highlight_code(program_code, file_path)
                    print(highlighted_code)
                else:
                    print(
                        "⚠️  Syntax highlighting not available (install pygments: pip install pygments)"
                    )
                    print(program_code)

                print("=" * 50)
            except BrokenPipeError:
                # Handle broken pipe gracefully (e.g., when piped to head)
                sys.exit(0)

            return 0

        except Exception as e:
            print(f"❌ Error displaying file: {str(e)}")
            return 1

    def _highlight_code(self, code, file_path):
        """Apply syntax highlighting to code"""
        try:
            # Determine lexer based on file extension
            file_ext = Path(file_path).suffix.lower()

            # Map extensions to pygments lexers
            lexer_map = {
                ".py": "python",
                ".js": "javascript",
                ".pl": "perl",
                ".perl": "perl",
                ".pas": "pascal",
                ".pp": "pascal",
                ".bas": "text",  # No specific lexer for BASIC
                ".basic": "text",  # No specific lexer for BASIC
                ".fs": "forth",
                ".forth": "forth",
                ".prolog": "prolog",
                ".logo": "text",  # No specific lexer for Logo
                ".pilot": "text",  # No specific lexer for PILOT
            }

            lexer_name = lexer_map.get(file_ext, "text")

            # For languages without specific lexers, try guessing
            if lexer_name == "text":
                try:
                    lexer = guess_lexer(code)
                except Exception:
                    lexer = get_lexer_by_name("text")
            else:
                # Try to get the specific lexer
                try:
                    lexer = get_lexer_by_name(lexer_name)
                except Exception:
                    # Fallback to guessing the lexer
                    try:
                        lexer = guess_lexer(code)
                    except Exception:
                        # Final fallback to plain text
                        lexer = get_lexer_by_name("text")

            # Format with terminal colors
            formatter = TerminalFormatter()
            highlighted = highlight(code, lexer, formatter)

            # If highlighting didn't add any colors (plain text), add a note
            if highlighted.strip() == code.strip():
                return (
                    code + "\n\n⚠️  No syntax highlighting available for this language"
                )

            return highlighted

        except Exception as e:
            # If highlighting fails, return plain text
            print(f"⚠️  Syntax highlighting failed: {e}")
            return code

    def list_examples(self):
        """List all available example programs"""
        if not self.examples_dir.exists():
            print("❌ Examples directory not found")
            return 1

        print("📚 Time_Warp Example Programs")
        print("=" * 50)

        # Get all language directories
        languages = sorted([d for d in self.examples_dir.iterdir() if d.is_dir()])

        for lang_dir in languages:
            lang_name = lang_dir.name
            if lang_name in self.language_info:
                info = self.language_info[lang_name]
                print(f"\n{info['name']} Programs ({lang_name}/):")

                # List files in this language directory
                files = list(lang_dir.glob("*"))
                if files:
                    for file_path in sorted(files):
                        if file_path.is_file():
                            print(f"  • {file_path.name}")
                else:
                    print("  (no examples)")

        print(
            f"\n💡 Total: {sum(1 for f in self.examples_dir.rglob('*') if f.is_file())} example programs"
        )
        print("💡 Use 'python timewarp-cli.py run <file>' to execute any program")
        return 0

    def show_language_info(self, language):
        """Show information about a specific language"""
        lang = language.lower()

        if lang not in self.language_info:
            print(f"❌ Unknown language: {language}")
            print("Available languages:")
            for name, info in self.language_info.items():
                print(f"  • {name} ({info['name']})")
            return 1

        info = self.language_info[lang]
        print(f"📖 {info['name']} ({lang})")
        print("=" * 50)
        print(f"Description: {info['description']}")
        print(f"File extensions: {', '.join(info['extensions'])}")
        print("Features:")
        for feature in info["features"]:
            print(f"  • {feature}")

        # Show example count
        lang_dir = self.examples_dir / lang
        if lang_dir.exists():
            example_count = len(list(lang_dir.glob("*")))
            print(f"Examples available: {example_count} programs")

        return 0

    def show_help(self):
        """Show help information"""
        print(__doc__)
        return 0

    def show_version(self):
        """Show version information"""
        print("Time_Warp CLI v1.1")
        print("Time_Warp IDE - Multi-Language Programming Environment")
        print(
            "Supports: PILOT, BASIC, Logo, Python, JavaScript, Perl, Pascal, Forth, Prolog"
        )
        return 0


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Time_Warp CLI - Command Line Interface for Time_Warp IDE",
        add_help=False,
    )

    parser.add_argument("command", nargs="?", help="Command to execute")
    parser.add_argument("args", nargs="*", help="Command arguments")
    parser.add_argument("-h", "--help", action="store_true", help="Show help message")

    args = parser.parse_args()

    # Handle help
    if args.help or args.command == "help":
        cli = TimeWarpCLI()
        return cli.show_help()

    # Initialize CLI
    cli = TimeWarpCLI()

    # Handle commands
    if not args.command:
        print("❌ No command specified. Use 'help' for usage information.")
        return 1

    command = args.command.lower()

    if command == "run":
        if not args.args:
            print("❌ 'run' command requires a file path")
            print("Example: python timewarp-cli.py run examples/basic/hello_world.bas")
            return 1
        return cli.run_program(args.args[0])

    elif command == "cat":
        if not args.args:
            print("❌ 'cat' command requires a file path")
            print("Example: python timewarp-cli.py cat examples/basic/hello_world.bas")
            return 1
        return cli.display_file(args.args[0])

    elif command == "list":
        return cli.list_examples()

    elif command == "info":
        if not args.args:
            print("❌ 'info' command requires a language name")
            print("Example: python timewarp-cli.py info basic")
            return 1
        return cli.show_language_info(args.args[0])

    elif command == "version":
        return cli.show_version()

    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: run, cat, list, info, help, version")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n⚡ Operation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"💥 CLI error: {str(e)}")
        sys.exit(1)
