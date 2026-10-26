"""Language metadata shared by the IDE, the CLI and the web UI.

These lists live outside ``gui`` so hosts without Tk (the web server, exported
runners) can use them.  ``gui.themes`` re-exports the first two for the code
that already imports them from there.
"""

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
