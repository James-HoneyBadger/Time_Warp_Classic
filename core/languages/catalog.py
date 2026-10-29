"""Language metadata shared by the IDE, the CLI and the web UI.

These lists live outside ``gui`` so hosts without Tk (the web server, exported
runners) can use them.  ``gui.themes`` re-exports the first two for the code
that already imports them from there.
"""

import shutil
from pathlib import Path

SUPPORTED_LANGUAGES = [
    "PILOT", "BASIC", "Logo", "Pascal", "Prolog",
    "Forth", "Perl", "Python", "JavaScript",
]

# Canonical extension first, then alternates.
EXT_TO_LANG = {
    ".pilot": "PILOT",
    ".pil": "PILOT",
    ".bas": "BASIC",
    ".logo": "Logo",
    ".lgo": "Logo",
    ".py": "Python",
    ".js": "JavaScript",
    ".pl": "Perl",
    ".pm": "Perl",
    ".pas": "Pascal",
    ".pp": "Pascal",
    ".fth": "Forth",
    ".4th": "Forth",
    ".fs": "Forth",
    ".pro": "Prolog",
    ".prolog": "Prolog",
}

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


def language_extension(language):
    """Default suffix for *language* (``.txt`` when it is unknown)."""
    return LANGUAGE_EXTENSIONS.get(str(language or "").strip().lower(), ".txt")


def extension_language(extension):
    """Language for *extension* (``None`` when it is unknown)."""
    return EXT_TO_LANG.get(str(extension or "").strip().lower())


# Languages run by an external process need a runtime on PATH.  Python is not
# listed: it always runs through the interpreter that started the IDE.
RUNTIME_COMMANDS = {
    "perl": ("perl",),
    "javascript": ("node", "nodejs"),
}

INSTALL_HINTS = {
    "perl": "install Perl (apt install perl, brew install perl, or strawberryperl.com)",
    "javascript": "install Node.js from nodejs.org",
}


def required_runtime(language):
    """Commands that can provide *language*'s runtime; empty when none is needed."""
    return RUNTIME_COMMANDS.get(str(language or "").strip().lower(), ())


def runtime_available(language, executable=None):
    """True when *language* can run here.

    *executable* is looked up instead of the built-in table when it is given,
    which is how plugin languages report whether their runtime exists.
    """
    if executable:
        text = str(executable)
        return bool(shutil.which(text) or Path(text).is_file())
    commands = required_runtime(language)
    return not commands or any(shutil.which(name) for name in commands)


def missing_runtime_hint(language):
    """One-line installation suggestion for *language*'s runtime (may be '')."""
    return INSTALL_HINTS.get(str(language or "").strip().lower(), "")
