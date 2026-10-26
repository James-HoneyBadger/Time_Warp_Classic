"""Shipped example programs, one folder per language.

The folder is a package so the examples travel with the wheel: installed
copies live inside ``site-packages``, where a relative "examples/..." path
would not resolve.  The IDE and the web UI therefore ask
:func:`example_path` for the file they want.
"""

from pathlib import Path

EXAMPLES_ROOT = Path(__file__).resolve().parent


def examples_root():
    """Folder holding the example programs."""
    return EXAMPLES_ROOT


def example_path(relative):
    """Absolute path for an example such as ``basic/INDEX.bas``.

    A leading ``examples/`` is accepted and ignored, so callers that already
    use repository-relative paths keep working.
    """
    text = str(relative).replace("\\", "/").lstrip("/")
    if text.startswith("examples/"):
        text = text[len("examples/"):]
    return EXAMPLES_ROOT / text
