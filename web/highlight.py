"""Syntax highlighting for the browser editor.

The desktop editor colours code with Pygments; this module gives the web UI the
same colours by rendering tokens to HTML on the server.  The page paints that
HTML behind a transparent textarea, so caret and selection behave normally.

Pygments is optional: when it is not installed the source is returned escaped
as plain text and the editor still works.
"""

from __future__ import annotations

import html

try:  # pragma: no cover - exercised through the fallback tests
    from pygments import highlight as _pygments_highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name
    from pygments.util import ClassNotFound

    PYGMENTS_AVAILABLE = True
except ImportError:  # pragma: no cover - slim installs
    PYGMENTS_AVAILABLE = False
    ClassNotFound = Exception

# Language label -> Pygments alias.  PILOT and Logo have no lexer, so their
# code stays plain; BASIC uses the Commodore BASIC lexer the IDE uses.
ALIASES = {
    "pilot": "text",
    "basic": "cbmbas",
    "logo": "text",
    "pascal": "pascal",
    "prolog": "prolog",
    "forth": "forth",
    "perl": "perl",
    "python": "python",
    "javascript": "javascript",
}

# Dark token palette on the editor's background.
STYLE = "monokai"

_FORMATTER = None


def _formatter():
    global _FORMATTER
    if _FORMATTER is None:
        _FORMATTER = HtmlFormatter(nowrap=True, noclasses=True, style=STYLE)
    return _FORMATTER


def alias_for(language, override=None):
    """Return the Pygments alias for *language* (plugins pass *override*)."""
    if override:
        return str(override).strip()
    return ALIASES.get(str(language or "").strip().lower(), "text")


def escape(source):
    """Plain, safely escaped HTML for *source*."""
    return html.escape(str(source), quote=False)


def highlight(language, source, alias=None):
    """Return HTML for *source* coloured as *language*.

    Unknown languages, missing Pygments and the no-op lexers all produce
    escaped plain text, so callers never have to special-case them.
    """
    text = "" if source is None else str(source)
    if not text:
        return ""
    if not PYGMENTS_AVAILABLE:
        return escape(text)

    name = alias_for(language, alias)
    if name == "text":
        return escape(text)
    try:
        lexer = get_lexer_by_name(name, stripnl=False, stripall=False, ensurenl=False)
        return _pygments_highlight(text, lexer, _formatter())
    except (ClassNotFound, ImportError, ValueError):
        return escape(text)
