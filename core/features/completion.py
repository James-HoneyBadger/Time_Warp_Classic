"""Word completion for the IDE editor.

The vocabulary and the matching rules live here, free of Tk, so they can be
tested headless; :mod:`gui.completion_popup` only renders what
:class:`CompletionEngine` returns.  Every vocabulary lists words the matching
interpreter actually accepts, so a suggestion does something once inserted.
"""

from __future__ import annotations

import re

# Characters a completable word is made of.  "$" and "%" belong to BASIC and
# PILOT names (MID$, %answer); punctuation-only Forth words (".", "!", "+")
# are deliberately absent - they cannot be completed sensibly.
WORD_CHARS = re.compile(r"[A-Za-z0-9_$%]")

_MAX_SUGGESTIONS = 12

# BASIC: statements and direct-mode commands, then the extended command set
# from the Turbo BASIC handlers.
_BASIC = (
    "LET", "IF", "THEN", "ELSE", "END", "FOR", "TO", "STEP", "NEXT",
    "PRINT", "INPUT", "REM", "GOTO", "GOSUB", "RETURN", "DIM", "DO", "LOOP",
    "WHILE", "WEND", "EXIT", "SELECT", "CASE", "SUB", "DEFFN", "STOP",
    "DATA", "READ", "RESTORE", "TRON", "TROFF", "LIST", "RUN", "NEW",
    "RENUMBER", "HELP",
    # Turtle and graphics
    "FORWARD", "FD", "BACK", "BACKWARD", "BK", "LEFT", "RIGHT",
    "PENUP", "PU", "PENDOWN", "PD", "DRAW", "PALETTE", "LINE", "BOX",
    "TRIANGLE", "ELLIPSE", "FILL", "CIRCLE", "PSET", "PRESET",
    # Sound
    "BEEP", "PLAY", "SOUND", "NOTE",
    # Math and string functions
    "SIN", "COS", "TAN", "SQRT", "ABS", "INT", "RND", "CEIL", "FIX", "EXP",
    "LOG", "LEN", "MID$", "LEFT$", "RIGHT$", "INSTR", "STR$", "VAL", "CHR$",
    "ASC", "UCASE$", "LCASE$", "HEX$",
    # Enhanced commands, arrays and files
    "INCR", "DECR", "SWAP", "RANDOMIZE", "DELAY", "CALL", "SORT", "FIND",
    "SUM", "AVG", "MIN", "MAX", "OPEN", "CLOSE", "WRITE", "EOF", "SEEK",
    "GET", "PUT",
)

# PILOT: the command letters are written with a colon, so a suggestion for
# "MA" inserts "MATH:".
_PILOT = (
    "T:", "TH:", "A:", "M:", "MT:", "Y:", "N:", "J:", "U:", "C:", "R:",
    "E:", "L:", "F:", "W:", "D:", "MATH:", "GAME:", "AUDIO:", "BRANCH:",
    "MULTIMEDIA:", "STORAGE:", "HELP:", "TIME:", "DATE:", "RESET:",
    "LIVES:", "BEEP:", "STOP:",
)

_LOGO = (
    "FORWARD", "FD", "BACK", "BK", "BACKWARD", "LEFT", "LT", "RIGHT", "RT",
    "PENUP", "PU", "PENDOWN", "PD", "CLEARSCREEN", "CS", "HOME", "REPEAT",
    "IF", "IFELSE", "STOP", "OUTPUT", "OP", "MAKE", "PRINT", "PR", "SHOW",
    "TYPE", "WAIT", "SETPC", "SETPENCOLOR", "SETCOLOR", "SETPENSIZE",
    "SETHEADING", "SETH", "SETXY", "ARC", "CIRCLE", "SQUARE", "HIDETURTLE",
    "HT", "SHOWTURTLE", "ST", "TO", "END", "SUM", "PRODUCT",
)

_PASCAL = (
    "PROGRAM", "BEGIN", "END", "VAR", "CONST", "TYPE", "PROCEDURE",
    "FUNCTION", "IF", "THEN", "ELSE", "CASE", "OF", "WHILE", "DO", "REPEAT",
    "UNTIL", "FOR", "TO", "DOWNTO", "WRITE", "WRITELN", "READ", "READLN",
    "ARRAY", "RECORD", "INTEGER", "REAL", "STRING", "BOOLEAN", "CHAR",
    "TRUE", "FALSE", "NIL", "DIV", "MOD", "AND", "OR", "NOT",
)

# Prolog has no fixed keyword set; these are the predicates the executor
# proves itself plus the usual arithmetic operators written as words.
_PROLOG = (
    "write", "nl", "member", "readln", "readchar", "readint", "readreal",
    "assert", "retract", "consult", "listing", "fail", "true", "not",
    "repeat", "halt", "is", "mod",
)

# Forth words from the built-in dictionary (alphabetic ones; "DUP"-style
# names that start with a digit are included because digits are word chars).
_FORTH = (
    "DUP", "2DUP", "DROP", "2DROP", "SWAP", "OVER", "ROT", "NIP", "TUCK",
    "MOD", "NEGATE", "ABS", "MIN", "MAX", "AND", "OR", "XOR", "INVERT",
    "DEPTH", "PICK", "ROLL", "TRUE", "FALSE", "PI", "E", "EMIT", "SPACES",
    "SIN", "COS", "TAN", "SQRT", "LOG", "EXP", "ALLOCATE", "FREE", "RESIZE",
    "OPEN-FILE", "CLOSE-FILE", "READ-FILE", "WRITE-FILE", "FILE-POSITION",
    "REPOSITION-FILE", "COMPARE", "SEARCH", "TRY", "THROW", "CATCH",
    "VALUE", "TO", "STRUCT", "FIELD", "END-STRUCT", "OBJECT", "METHOD",
    "END-OBJECT", "IF", "ELSE", "THEN", "BEGIN", "UNTIL", "WHILE", "REPEAT",
    "DO", "LOOP", "VARIABLE", "CONSTANT", "WORDS", "CR",
)

_PERL = (
    "my", "our", "sub", "if", "elsif", "else", "unless", "while", "until",
    "for", "foreach", "print", "printf", "say", "use", "require", "strict",
    "warnings", "last", "next", "redo", "return", "chomp", "chop", "split",
    "join", "push", "pop", "shift", "unshift", "keys", "values", "each",
    "exists", "delete", "die", "warn", "open", "close", "sort", "grep",
    "map", "length", "substr", "index", "uc", "lc", "scalar", "undef",
)

_PYTHON = (
    "def", "class", "import", "from", "as", "if", "elif", "else", "for",
    "in", "while", "return", "yield", "try", "except", "finally", "raise",
    "with", "lambda", "pass", "break", "continue", "and", "or", "not", "is",
    "None", "True", "False", "global", "nonlocal", "assert", "print",
    "len", "range", "input", "int", "str", "float", "list", "dict", "set",
    "tuple", "enumerate", "zip", "sorted", "sum", "min", "max", "open",
    "type", "isinstance", "abs", "round",
)

_JAVASCRIPT = (
    "function", "const", "let", "var", "if", "else", "for", "while", "do",
    "return", "class", "new", "this", "typeof", "instanceof", "try",
    "catch", "finally", "throw", "switch", "case", "break", "continue",
    "async", "await", "delete", "in", "of", "true", "false", "null",
    "undefined", "console", "Math", "JSON", "Number", "String", "Array",
    "Object", "parseInt", "parseFloat", "isNaN", "length", "push", "pop",
)

VOCABULARIES = {
    "basic": _BASIC,
    "pilot": _PILOT,
    "logo": _LOGO,
    "pascal": _PASCAL,
    "prolog": _PROLOG,
    "forth": _FORTH,
    "perl": _PERL,
    "python": _PYTHON,
    "javascript": _JAVASCRIPT,
}

# Comment openings, matched against the start of the current line.  BASIC
# needs a pattern rather than a prefix because the comment follows the line
# number: "10 REM ..." and "10 ' ...".
_COMMENT_PATTERNS = {
    "basic": re.compile(r"^\s*(?:\d+\s*)?(?:REM\b|')", re.IGNORECASE),
    "logo": re.compile(r"^\s*;"),
    "pilot": re.compile(r"^\s*\*"),
    "forth": re.compile(r"^\s*\\"),
    "perl": re.compile(r"^\s*#"),
    "python": re.compile(r"^\s*#"),
    "javascript": re.compile(r"^\s*//"),
    "pascal": re.compile(r"^\s*//"),
    "prolog": re.compile(r"^\s*%"),
}

# String delimiters, used to stay quiet while the caret is inside a literal.
_STRING_DELIMITERS = {
    "basic": ('"',),
    "pilot": ('"',),
    "logo": ('"',),
    "pascal": ("'",),
    "forth": ('"',),
    "perl": ('"', "'"),
    "python": ('"', "'"),
    "javascript": ('"', "'", "`"),
    "prolog": ('"', "'"),
}


def language_key(language):
    """Normalise a menu label ("JavaScript") to a vocabulary key."""
    return str(language or "").strip().lower()


def is_word_char(char):
    """True when *char* can be part of a completable word."""
    return bool(char) and bool(WORD_CHARS.match(char))


def line_before(text, cursor):
    """The part of the line that precedes *cursor*."""
    start = text.rfind("\n", 0, cursor) + 1
    return text[start:cursor]


def word_prefix(text, cursor):
    """Return ``(start, prefix)`` for the word that ends at *cursor*.

    *start* is an offset into *text*, so a caller replaces the text between
    ``start`` and ``cursor`` with the chosen word.
    """
    start = cursor
    while start > 0 and WORD_CHARS.match(text[start - 1]):
        start -= 1
    return start, text[start:cursor]


def _unmatched(text, delimiter):
    """True when *text* ends inside a literal opened by *delimiter*."""
    count = 0
    escaped = False
    for char in text:
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == delimiter:
            count += 1
    return count % 2 == 1


def is_suppressed(language, text, cursor):
    """True when suggesting a word at *cursor* would only be noise.

    Covers the two cases that annoyed users of other editors: typing inside a
    comment, and typing inside a string literal.
    """
    key = language_key(language)
    line = line_before(text, cursor)

    pattern = _COMMENT_PATTERNS.get(key)
    if pattern is not None and pattern.match(line):
        return True

    # Pascal block comments stay open across lines.
    if key == "pascal":
        body = text[:cursor]
        if body.count("{") > body.count("}"):
            return True

    return any(_unmatched(line, d) for d in _STRING_DELIMITERS.get(key, ('"',)))


class CompletionEngine:
    """Prefix matching over the per-language vocabularies."""

    def __init__(self, vocabularies=None):
        source = VOCABULARIES if vocabularies is None else vocabularies
        self.vocabularies = {
            language_key(key): tuple(words) for key, words in source.items()
        }

    def vocabulary(self, language):
        """The words known for *language* (empty when it has none)."""
        return self.vocabularies.get(language_key(language), ())

    def suggestions(self, language, prefix, limit=_MAX_SUGGESTIONS):
        """Words starting with *prefix*, best match first.

        Matching ignores case; words that match the typed case exactly come
        first, then the shortest, then alphabetically.
        """
        words = self.vocabulary(language)
        if not words:
            return []
        if not prefix:
            return list(words[:limit])

        needle = prefix.lower()
        matches = [word for word in words if word.lower().startswith(needle)]
        matches.sort(key=lambda word: (not word.startswith(prefix), len(word), word.upper()))
        return matches[:limit]

    def completion_at(self, language, text, cursor, limit=_MAX_SUGGESTIONS, forced=False):
        """Return ``(start, items)`` for the caret, or None when not useful.

        ``forced`` (the Ctrl+Space shortcut) ignores the comment/string guard
        and accepts a single character, but still never returns a list whose
        only entry is exactly what is already typed.
        """
        if not forced and is_suppressed(language, text, cursor):
            return None

        start, prefix = word_prefix(text, cursor)
        items = self.suggestions(language, prefix, limit=limit)
        if not items:
            return None
        if len(items) == 1 and items[0] == prefix:
            return None
        return start, items
