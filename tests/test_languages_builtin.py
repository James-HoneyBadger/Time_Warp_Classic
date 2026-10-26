"""Behavioural tests for the six built-in language interpreters.

Each test runs a small program through the interpreter the way the IDE does
and checks the printed output.  They cover the constructs the reference
documentation promises, including the block forms of Pascal control flow.
"""

import io
from contextlib import redirect_stdout

import pytest

from core.interpreter import Time_WarpInterpreter

pytestmark = pytest.mark.language


@pytest.fixture
def run():
    """Run a program headlessly and return its output lines."""

    def _run(language, program, answer="5"):
        machine = Time_WarpInterpreter()
        machine.max_iterations = 20_000
        machine.input_provider = lambda prompt="": answer
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            machine.run_program(program, language=language)
        return [
            line
            for line in buffer.getvalue().splitlines()
            if line.strip() and "Interpreter ready" not in line
        ]

    return _run


def has_error(lines):
    return any("?ERROR" in line or "Traceback" in line for line in lines)


# --------------------------------------------------------------------- BASIC

def test_basic_print_and_arithmetic(run):
    lines = run("basic", '10 PRINT "HI"\n20 PRINT 3 * 7')

    assert "HI" in lines
    assert "21" in lines
    assert not has_error(lines)


def test_basic_if_then(run):
    lines = run("basic", '10 LET A = 5\n20 IF A > 3 THEN PRINT "BIG"\n30 PRINT "DONE"')

    assert "BIG" in lines and "DONE" in lines


def test_basic_for_next_loop(run):
    lines = run("basic", "10 FOR I = 1 TO 3\n20 PRINT I\n30 NEXT I\n40 PRINT \"END\"")

    assert [line for line in lines if line in {"1", "2", "3"}] == ["1", "2", "3"]
    assert "END" in lines


def test_basic_gosub_and_return(run):
    lines = run(
        "basic",
        '10 GOSUB 100\n20 PRINT "BACK"\n30 END\n100 PRINT "SUB"\n110 RETURN',
    )

    assert lines.index("SUB") < lines.index("BACK")


@pytest.mark.parametrize("closer", ["WEND", "END WHILE"])
def test_basic_while_loop_can_end_the_program(run, closer):
    """A WHILE whose closer is the last line must finish cleanly."""
    lines = run(
        "basic",
        f"10 LET N = 0\n20 WHILE N < 3\n30 LET N = N + 1\n40 PRINT N\n50 {closer}",
    )

    assert not has_error(lines)
    assert [line for line in lines if line in {"1", "2", "3"}] == ["1", "2", "3"]


def test_basic_string_functions_accept_the_dollar_forms(run):
    lines = run(
        "basic",
        '10 PRINT LEFT$("ABCDEF", 3)\n20 PRINT MID$("ABCDEF", 2, 3)'
        '\n30 PRINT RIGHT$("ABCDEF", 2)\n40 PRINT LEN("ABCD")',
    )

    assert not has_error(lines)
    assert lines[:4] == ["ABC", "BCD", "EF", "4"]


def test_basic_arrays_and_input(run):
    lines = run(
        "basic",
        "10 DIM A(3)\n20 LET A(1) = 7\n30 PRINT A(1)\n40 INPUT B\n50 PRINT B",
        answer="42",
    )

    assert "7" in lines
    assert "42" in lines


# --------------------------------------------------------------------- PILOT

def test_pilot_text_output(run):
    lines = run("pilot", "T:HELLO\nE:")

    assert "HELLO" in lines


def test_pilot_match_text_is_conditional(run):
    """MT: prints only when the previous M: matched the input."""
    program = "T:Capital of France?\nA:[answer]\nM:Paris\nMT:Correct\nE:"

    assert "Correct" in run("pilot", program, answer="Paris")
    assert "Correct" not in run("pilot", program, answer="Lyon")


def test_pilot_compute_and_interpolate(run):
    lines = run("pilot", "C:[x]=2+3\nT:Value [x]\nE:")

    assert "Value 5" in lines


@pytest.mark.parametrize(
    ("answer", "expected", "unexpected"),
    [("Y", "Great!", "OK"), ("N", "OK", "Great!")],
)
def test_pilot_documented_yes_no_flow(run, answer, expected, unexpected):
    """A: + M: + Y:/N: run the instruction after the colon, per the manual."""
    lines = run(
        "pilot",
        "T:Do you like programming? (Y/N)\nA:[answer]\nM:Y\n"
        "Y:T:Great!\nN:T:OK\nE:",
        answer=answer,
    )

    assert not has_error(lines)
    assert expected in lines
    assert unexpected not in lines


# ---------------------------------------------------------------------- Logo

def test_logo_repeat_loop(run):
    lines = run("logo", 'REPEAT 3 [PRINT "LOOP"]')

    assert len([line for line in lines if "LOOP" in line]) == 3


def test_logo_procedure_definition_and_call(run):
    lines = run("logo", 'TO GREET\nPRINT "HELLO"\nEND\nGREET')

    assert any("HELLO" in line for line in lines)


def test_logo_print_outputs_bracket_text(run):
    lines = run("logo", "PRINT [Mandala Art Generator Complete]")

    assert "Mandala Art Generator Complete" in lines


# -------------------------------------------------------------------- Pascal

def test_pascal_writeln_and_arithmetic(run):
    lines = run("pascal", "begin\n  x := 4;\n  writeln(x * 2);\nend.")

    assert "8" in lines


def test_pascal_inline_if_else(run):
    lines = run(
        "pascal",
        "begin\n  x := 2;\n  if x > 5 then writeln('BIG') else writeln('SMALL');\nend.",
    )

    assert "SMALL" in lines and "BIG" not in lines


@pytest.mark.parametrize(("value", "expected"), [(7, "BIG"), (2, "")])
def test_pascal_block_if_respects_the_condition(run, value, expected):
    """A BEGIN...END body must not run when the condition is false."""
    lines = run(
        "pascal",
        f"begin\n  x := {value};\n  if x > 5 then\n  begin\n"
        "    writeln('BIG');\n    writeln('SECOND');\n  end;\n  writeln('AFTER');\nend.",
    )

    assert "AFTER" in lines
    if expected:
        assert expected in lines and "SECOND" in lines
    else:
        assert "BIG" not in lines and "SECOND" not in lines


def test_pascal_block_if_else(run):
    lines = run(
        "pascal",
        "begin\n  x := 2;\n  if x > 5 then\n  begin\n    writeln('BIG');\n  end\n"
        "  else\n  begin\n    writeln('SMALL');\n  end;\n  writeln('AFTER');\nend.",
    )

    assert "SMALL" in lines and "BIG" not in lines and "AFTER" in lines


def test_pascal_nested_if(run):
    lines = run(
        "pascal",
        "begin\n  x := 7;\n  y := -1;\n  if x > 5 then\n  begin\n"
        "    if y > 0 then\n    begin\n      writeln('NESTED');\n    end;\n"
        "    writeln('OUTER');\n  end;\n  writeln('AFTER');\nend.",
    )

    assert "NESTED" not in lines
    assert "OUTER" in lines and "AFTER" in lines


def test_pascal_while_block(run):
    lines = run(
        "pascal",
        "begin\n  n := 0;\n  while n < 3 do\n  begin\n    n := n + 1;\n"
        "    writeln(n);\n  end;\n  writeln('DONE');\nend.",
    )

    assert [line for line in lines if line in {"1", "2", "3"}] == ["1", "2", "3"]
    assert "DONE" in lines


def test_pascal_repeat_until_block(run):
    lines = run(
        "pascal",
        "begin\n  n := 0;\n  repeat\n    n := n + 1;\n    writeln(n);\n"
        "  until n >= 3;\n  writeln('DONE');\nend.",
    )

    assert [line for line in lines if line in {"1", "2", "3"}] == ["1", "2", "3"]
    assert "DONE" in lines


def test_pascal_for_block_and_downto(run):
    lines = run(
        "pascal",
        "begin\n  for i := 1 to 3 do\n  begin\n    writeln(i);\n  end;\n"
        "  for j := 3 downto 1 do\n  begin\n    writeln(j);\n  end;\nend.",
    )

    numbers = [line for line in lines if line in {"1", "2", "3"}]
    assert numbers == ["1", "2", "3", "3", "2", "1"]


# -------------------------------------------------------------------- Prolog

def test_prolog_fact_query_prints_bound_value(run):
    lines = run("prolog", "parent(tom, bob).\nparent(bob, ann).\n?- parent(tom, X).")

    assert not has_error(lines)
    assert any(line.strip() == "X = bob" for line in lines)
    assert not any("'type':" in line for line in lines)


def test_prolog_rule_resolves_through_intermediate_variables(run):
    lines = run(
        "prolog",
        "parent(tom, bob).\nancestor(X, Y) :- parent(X, Y).\n?- ancestor(tom, Who).",
    )

    assert any(line.strip() == "Who = bob" for line in lines)


def test_prolog_ground_query_reports_yes(run):
    lines = run("prolog", "parent(tom, bob).\n?- parent(tom, bob).")

    assert any(line.strip() == "yes" for line in lines)


def test_prolog_failing_query(run):
    lines = run("prolog", "parent(tom, bob).\n?- parent(ann, X).")

    assert any("no solutions" in line for line in lines)


# --------------------------------------------------------------------- Forth

def test_forth_stack_arithmetic(run):
    lines = run("forth", "2 3 + .")

    assert "5" in lines


def test_forth_word_definition(run):
    lines = run("forth", ": SQUARE DUP * ;\n5 SQUARE .")

    assert "25" in lines


def test_forth_conditional(run):
    lines = run("forth", ': TEST DUP 5 > IF ." BIG" ELSE ." SMALL" THEN ;\n7 TEST')

    assert any("BIG" in line for line in lines)


def test_forth_variables(run):
    lines = run("forth", "VARIABLE X\n10 X !\nX @ .")

    assert "10" in lines
