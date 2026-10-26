"""Tests for BASIC direct mode (the READY. console)."""

import pytest

from core.interpreter import Time_WarpInterpreter
from core.languages.basic_console import BasicConsole


class FakeEditor:
    """Minimal stand-in for the IDE editor."""

    def __init__(self, text=""):
        self.text = text

    def get(self):
        return self.text

    def set(self, text):
        self.text = text


@pytest.fixture
def console():
    interpreter = Time_WarpInterpreter()
    interpreter.max_iterations = None
    editor = FakeEditor()
    runs = []

    machine = BasicConsole(
        interpreter,
        get_program=editor.get,
        set_program=editor.set,
        run_program=runs.append,
    )
    machine.editor = editor
    machine.runs = runs
    return machine


def test_statements_run_immediately(console, capsys):
    """A bare statement answers at the prompt."""
    console.submit('PRINT 2+2')

    assert "4" in capsys.readouterr().out


def test_bare_assignment_is_accepted(console, capsys):
    """A = 5 works like LET A = 5, as it did on the real machines."""
    assert console.submit("A = 5") == []
    console.submit("PRINT A")

    assert "5" in capsys.readouterr().out


def test_numbered_line_is_stored(console):
    """Typing a numbered line edits the program in memory."""
    assert console.submit('10 PRINT "HI"') == ["OK"]
    assert console.editor.get() == '10 PRINT "HI"\n'


def test_numbered_lines_stay_sorted(console):
    console.submit('20 PRINT "B"')
    console.submit('10 PRINT "A"')

    assert console.editor.get().splitlines() == ['10 PRINT "A"', '20 PRINT "B"']


def test_number_alone_deletes_the_line(console):
    console.submit('10 PRINT "A"')
    console.submit('20 PRINT "B"')
    console.submit("10")

    assert console.editor.get().splitlines() == ['20 PRINT "B"']


def test_list_shows_the_program(console):
    console.submit('10 PRINT "A"')
    assert console.submit("LIST") == ['10 PRINT "A"']


def test_list_without_program(console):
    assert console.submit("LIST") == ["?NO PROGRAM"]


def test_run_passes_the_program_on(console):
    console.submit('10 PRINT "A"')
    assert console.submit("RUN") == []
    assert console.runs == ['10 PRINT "A"\n']


def test_run_from_line_slices_the_program(console):
    console.submit('10 PRINT "A"')
    console.submit('20 PRINT "B"')
    console.submit("RUN 20")

    assert console.runs == ['20 PRINT "B"\n']


def test_run_unknown_line_reports(console):
    console.submit('10 PRINT "A"')
    assert console.submit("RUN 100") == ["?NO LINE 100"]


def test_renumber_relabels_lines(console):
    console.submit('1 PRINT "A"')
    console.submit('2 PRINT "B"')
    assert console.submit("RENUMBER") == ["OK"]

    assert console.editor.get().splitlines() == ['10 PRINT "A"', '20 PRINT "B"']


def test_new_clears_program_and_variables(console):
    console.submit('10 PRINT "A"')
    console.submit("LET X = 1")
    assert console.submit("NEW") == ["OK"]

    assert console.editor.get() == ""
    assert console.interpreter.variables == {}


def test_structural_statements_are_rejected(console):
    assert console.submit("GOTO 10") == ["?ILLEGAL DIRECT"]
    assert console.submit("FOR I = 1 TO 3") == ["?ILLEGAL DIRECT"]


def test_unknown_statement_reports_a_syntax_error(console):
    assert console.submit("FLY ME TO THE MOON") == ["?SYNTAX ERROR"]


def test_help_lists_the_commands(console):
    lines = console.submit("HELP")

    assert lines[0] == "DIRECT MODE"
    assert any("RENUMBER" in line for line in lines)


def test_tron_and_troff_toggle_tracing(console):
    """TRON/TROFF switch the interpreter's line trace on and off."""
    console.submit("TRON")
    assert console.interpreter.debug_mode is True

    console.submit("TROFF")
    assert console.interpreter.debug_mode is False


def test_renumber_updates_line_references(console):
    """RENUMBER must retarget GOTO/GOSUB/THEN, not just the line numbers."""
    console.submit('10 GOTO 100')
    console.submit('20 PRINT "SKIPPED"')
    console.submit('100 PRINT "END"')

    assert console.submit("RENUMBER") == ["OK"]
    assert console.editor.get().splitlines() == [
        '10 GOTO 30',
        '20 PRINT "SKIPPED"',
        '30 PRINT "END"',
    ]


def test_renumber_updates_computed_gosub_lists(console):
    console.submit("10 ON X GOSUB 500, 600")
    console.submit("500 RETURN")
    console.submit("600 RETURN")

    console.submit("RENUMBER")

    assert console.editor.get().splitlines()[0] == "10 ON X GOSUB 20, 30"


def test_renumber_leaves_strings_and_comments_unchanged(console):
    console.submit('10 PRINT "GOTO 100"')
    console.submit("20 REM GOTO 100")
    console.submit('100 PRINT "END"')

    assert console.submit("RENUMBER") == ["OK"]
    assert console.editor.get().splitlines() == [
        '10 PRINT "GOTO 100"',
        "20 REM GOTO 100",
        '30 PRINT "END"',
    ]
