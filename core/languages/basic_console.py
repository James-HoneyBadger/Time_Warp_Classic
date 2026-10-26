"""Classic BASIC direct mode — the ``READY.`` console.

Lines typed into the IDE console bar while no program is running are handled
here, the way a home computer of the era did it:

* ``10 PRINT "HI"`` stores (or replaces) a program line, ``10`` deletes it
* ``LIST``, ``RUN``, ``RUN 100``, ``RENUMBER``, ``NEW`` and ``HELP`` are the
  housekeeping commands
* anything else is executed immediately, so ``PRINT 2+2`` answers at once

The module is deliberately free of Tk so it can be tested headless: the
caller supplies callbacks for reading/writing the program text and for
running it.
"""

from __future__ import annotations

import re

LINE_RE = re.compile(r"^\s*(\d+)\s*(.*)$")
ASSIGN_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]*[$%]?\s*=")
# Statements that name a line number and therefore need renumbering.
_LIST_REF_RE = re.compile(r"\b(GOTO|GOSUB)\s+(\d+(?:\s*,\s*\d+)+)", re.IGNORECASE)
_SINGLE_REF_RE = re.compile(
    r"\b(GOTO|GOSUB|THEN|ELSE|RESTORE|RUN)\s+(\d+)\b", re.IGNORECASE
)

# Statements that only make sense inside a stored program.  Typing them at
# the prompt gave "?ILLEGAL DIRECT" on the machines this emulates.
_STORED_ONLY = frozenset({
    "ELSE", "END", "FOR", "GOSUB", "GOTO", "IF", "LOOP", "NEXT", "RETURN",
    "SELECT", "CASE", "STOP", "SUB", "DEFFN", "WHILE", "WEND", "DO",
})

# Statements the BASIC executor understands and that are safe to run at the
# prompt.
_STATEMENTS = frozenset({
    "BEEP", "BOX", "CALL", "CLOSE", "DECR", "DELAY", "DIM", "DRAW", "ELLIPSE",
    "FILL", "FIND", "INCR", "INPUT", "LEFT", "LET", "LINE", "MASTERVOLUME",
    "MAX", "MIN", "NOTE", "OPEN", "PALETTE", "PLAY", "PRINT", "RANDOMIZE",
    "READ", "REM", "RIGHT", "SOUND", "SORT", "SUM", "SWAP", "TRIANGLE",
    "WRITE",
})

_HELP = [
    "DIRECT MODE",
    "10 PRINT \"HI\"    store a line",
    "10               delete line 10",
    "LIST             list program",
    "RUN [line]       run program",
    "RENUMBER         renumber by 10s",
    "NEW              clear program",
    "PRINT 2+2        execute at once",
    "TRON / TROFF     trace lines on / off",
    "HELP             this text",
]


class BasicConsole:
    """Immediate-mode interpreter for the IDE console bar."""

    def __init__(
        self, interpreter, get_program, set_program, run_program, execute_direct=None
    ):
        self.interpreter = interpreter
        self._get_program = get_program
        self._set_program = set_program
        self._run_program = run_program
        self._execute_direct = execute_direct or interpreter.execute_line

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def submit(self, line):
        """Handle one console line and return the lines to display."""
        text = line.strip()
        if not text:
            return []

        match = LINE_RE.match(text)
        if match:
            return self._store_line(int(match.group(1)), match.group(2).strip())

        keyword, rest = _split_keyword(text)
        if keyword == "LIST":
            return self._list()
        if keyword == "RUN":
            return self._run(rest)
        if keyword == "NEW":
            return self._new()
        if keyword == "RENUMBER":
            return self._renumber()
        if keyword == "HELP":
            return list(_HELP)
        if keyword in ("TRON", "TROFF"):
            self.interpreter.set_debug_mode(keyword == "TRON")
            return []
        return self._execute(text, keyword)

    # ------------------------------------------------------------------
    # Program storage
    # ------------------------------------------------------------------

    def _entries(self):
        """Split the program into sorted numbered lines and unnumbered text."""
        numbered, unnumbered = [], []
        for raw in self._get_program().splitlines():
            match = LINE_RE.match(raw)
            if match:
                numbered.append((int(match.group(1)), match.group(2).strip()))
            elif raw.strip():
                unnumbered.append(raw.rstrip())
        numbered.sort(key=lambda entry: entry[0])
        return numbered, unnumbered

    @staticmethod
    def _render(numbered, unnumbered=()):
        lines = [f"{number} {text}".rstrip() for number, text in numbered]
        lines.extend(unnumbered)
        return "\n".join(lines) + ("\n" if lines else "")

    def _store_line(self, number, statement):
        numbered, unnumbered = self._entries()
        numbered = [(num, text) for num, text in numbered if num != number]
        if statement:
            numbered.append((number, statement))
            numbered.sort(key=lambda entry: entry[0])
        self._set_program(self._render(numbered, unnumbered))
        return ["OK"]

    # ------------------------------------------------------------------
    # Housekeeping commands
    # ------------------------------------------------------------------

    def _list(self):
        numbered, unnumbered = self._entries()
        if not numbered and not unnumbered:
            return ["?NO PROGRAM"]
        return [f"{number} {text}".rstrip() for number, text in numbered] + unnumbered

    def _run(self, argument):
        numbered, unnumbered = self._entries()
        if not numbered and not unnumbered:
            return ["?NO PROGRAM"]

        if argument:
            try:
                start = int(argument.split()[0])
            except (ValueError, IndexError):
                return ["?SYNTAX ERROR"]
            numbered = [entry for entry in numbered if entry[0] >= start]
            if not numbered:
                return [f"?NO LINE {start}"]
            unnumbered = []

        self._run_program(self._render(numbered, unnumbered))
        return []

    def _new(self):
        self._set_program("")
        self.interpreter.reset()
        return ["OK"]

    def _renumber(self):
        numbered, unnumbered = self._entries()
        if not numbered:
            return ["?NO PROGRAM"]

        mapping = {
            old: 10 * (index + 1) for index, (old, _text) in enumerate(numbered)
        }
        renumbered = [
            (mapping[old], _renumber_references(text, mapping))
            for old, text in numbered
        ]
        self._set_program(self._render(renumbered, unnumbered))
        return ["OK"]

    # ------------------------------------------------------------------
    # Direct execution
    # ------------------------------------------------------------------

    def _execute(self, text, keyword):
        if keyword in _STORED_ONLY:
            return ["?ILLEGAL DIRECT"]
        if keyword not in _STATEMENTS:
            if not ASSIGN_RE.match(text):
                return ["?SYNTAX ERROR"]
            text = f"LET {text}"

        try:
            self._execute_direct(text)
        except Exception as exc:  # noqa: BLE001 — surface it instead of dying
            return [f"?ERROR: {exc}"]
        return []


def _split_keyword(text):
    """Return (upper-case leading keyword, remainder)."""
    match = re.match(r"^([A-Za-z]+)\s*(.*)$", text)
    if not match:
        return "", text
    return match.group(1).upper(), match.group(2).strip()


def _renumber_references(text, mapping):
    """Rewrite ``GOTO 100`` / ``ON X GOSUB 10,20`` targets after RENUMBER."""
    pieces = re.split(r'("(?:[^"]|"")*")', text)
    renumbered = []
    for index, piece in enumerate(pieces):
        if index % 2:
            renumbered.append(piece)
            continue

        comment_match = re.search(r"\bREM\b", piece, re.IGNORECASE)
        if comment_match:
            code = piece[:comment_match.start()]
            comment = piece[comment_match.start():]
        else:
            code, comment = piece, ""

        def many(match):
            keyword, targets = match.group(1), match.group(2)
            numbers = [int(value) for value in re.findall(r"\d+", targets)]
            return f"{keyword} " + ", ".join(str(mapping.get(n, n)) for n in numbers)

        def single(match):
            keyword, number = match.group(1), int(match.group(2))
            return f"{keyword} {mapping.get(number, number)}"

        code = _LIST_REF_RE.sub(many, code)
        code = _SINGLE_REF_RE.sub(single, code)
        renumbered.append(code + comment)

    return "".join(renumbered)
