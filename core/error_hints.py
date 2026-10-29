"""Actionable hints printed under errors the interpreter recognises.

An error message on its own rarely tells a beginner what to try next, so a
short ``?HINT:`` line is printed underneath.  Hints are advisory only: the
original error text, its line number and the error history are unchanged, and
a message with no matching rule simply gets no hint.
"""

from __future__ import annotations

import re

# Reference document each hint points at, when the language is known.
_LANGUAGE_DOCS = {
    "pilot": "docs/languages/PILOT_REFERENCE.md",
    "basic": "docs/languages/BASIC_REFERENCE.md",
    "logo": "docs/languages/LOGO_REFERENCE.md",
    "pascal": "docs/languages/PASCAL_REFERENCE.md",
    "prolog": "docs/languages/PROLOG_REFERENCE.md",
    "forth": "docs/languages/FORTH_REFERENCE.md",
    "perl": "docs/languages/PERL_REFERENCE.md",
    "python": "docs/languages/PYTHON_REFERENCE.md",
    "javascript": "docs/languages/JAVASCRIPT_REFERENCE.md",
}

# First match wins, so the specific problems come before the general ones.
_RULES = (
    (
        re.compile(r"division by ?zero", re.I),
        "a value in the expression is 0 - check the divisor before dividing",
    ),
    (
        re.compile(
            r"is not defined|undefined variable"
            r"|Global symbol .* requires explicit package",
            re.I,
        ),
        "give the name a value before using it - check the spelling too",
    ),
    (
        re.compile(
            r"IndentationError|expected an indented block|unexpected indent", re.I
        ),
        "indent the lines inside a block by the same amount",
    ),
    (
        re.compile(
            r"ModuleNotFoundError|Cannot find module|Can't locate .* in @INC", re.I
        ),
        "the program needs a module that is not installed - install it or"
        " drop the import",
    ),
    (
        re.compile(
            r"SyntaxError|syntax error|Unexpected token|Unexpected symbol", re.I
        ),
        "the line could not be parsed - check brackets, quotes and operators",
    ),
    (
        re.compile(r"Invalid jump target|Jump command error", re.I),
        "a jump must target a line number that exists in the program",
    ),
    (
        re.compile(r"Maximum iterations reached", re.I),
        "the program never finishes - check the loop condition, or stop it with Ctrl+.",
    ),
    (
        re.compile(r"timed out", re.I),
        "the program ran longer than the time limit - check for a loop that never ends",
    ),
    (
        re.compile(r"Unknown command type|is not a command", re.I),
        "the first word is not a command in this language - check the spelling",
    ),
    (
        re.compile(
            r"Type error in expression|can only concatenate|unsupported operand", re.I
        ),
        "the operands have different types - quote text or convert the number first",
    ),
)


def hint_for(message, language=None):
    """Return a one-line suggestion for *message*, or ``None``.

    *language* only selects the reference document appended to the hint; the
    rules themselves are language-neutral so one message from any runtime can
    still be explained.
    """
    text = str(message or "")
    if not text:
        return None
    for pattern, hint in _RULES:
        if pattern.search(text):
            doc = _LANGUAGE_DOCS.get(str(language or "").strip().lower())
            return f"{hint}. See {doc}." if doc else f"{hint}."
    return None
