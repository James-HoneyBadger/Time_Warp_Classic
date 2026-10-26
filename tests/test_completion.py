"""Headless tests for the editor's word-completion engine."""

import pytest

from core.features.completion import (
    VOCABULARIES,
    CompletionEngine,
    is_suppressed,
    is_word_char,
    language_key,
    word_prefix,
)


@pytest.fixture
def engine():
    return CompletionEngine()


def test_every_supported_language_has_a_vocabulary():
    """The IDE offers nine languages; none may be missing suggestions."""
    assert set(VOCABULARIES) == {
        "pilot", "basic", "logo", "pascal", "prolog",
        "forth", "perl", "python", "javascript",
    }
    assert all(VOCABULARIES.values())


@pytest.mark.parametrize(
    ("language", "prefix", "expected"),
    [
        ("basic", "PRIN", "PRINT"),
        ("logo", "FORW", "FORWARD"),
        ("pascal", "WRITEL", "WRITELN"),
        ("forth", "DU", "DUP"),
        ("perl", "chom", "chomp"),
        ("python", "imp", "import"),
        ("javascript", "func", "function"),
        ("prolog", "memb", "member"),
        ("pilot", "MAT", "MATH:"),
    ],
)
def test_prefix_matching_per_language(engine, language, prefix, expected):
    assert expected in engine.suggestions(language, prefix)


def test_matching_ignores_case(engine):
    assert "PRINT" in engine.suggestions("basic", "pri")
    assert "print" in engine.suggestions("python", "PRI")


def test_exact_case_matches_come_first(engine):
    words = engine.suggestions("pascal", "WRITE")
    assert words[0] == "WRITE"
    assert "WRITELN" in words


def test_limit_is_respected(engine):
    assert len(engine.suggestions("basic", "", limit=3)) == 3


def test_unknown_language_offers_nothing(engine):
    assert engine.suggestions("cobol", "PE") == []
    assert engine.completion_at("cobol", "PE", 2) is None


def test_language_labels_are_normalised(engine):
    assert language_key("JavaScript") == "javascript"
    assert engine.vocabulary("PILOT") == engine.vocabulary("pilot")


@pytest.mark.parametrize(
    ("text", "cursor", "expected"),
    [
        ("PRI", 3, (0, "PRI")),
        ("10 PRINT A", 10, (9, "A")),
        ("X = MID$", 8, (4, "MID$")),
        ("PILOT %answer", 13, (6, "%answer")),
        ("", 0, (0, "")),
        ("2D", 2, (0, "2D")),
    ],
)
def test_word_prefix(text, cursor, expected):
    assert word_prefix(text, cursor) == expected


def test_word_char_accepts_sigils_and_digits():
    for char in "aZ09_$%":
        assert is_word_char(char)
    for char in (" ", ":", "(", '"', ""):
        assert not is_word_char(char)


@pytest.mark.parametrize(
    ("language", "line"),
    [
        ("basic", "10 REM PRINT something"),
        ("basic", "' a comment"),
        ("python", "# print everything"),
        ("javascript", "// function here"),
        ("pascal", "// writeln"),
        ("prolog", "% write"),
        ("logo", "; forward"),
        ("forth", "\\ dup"),
        ("pilot", "* a comment"),
    ],
)
def test_comments_are_suppressed(language, line):
    assert is_suppressed(language, line, len(line))


@pytest.mark.parametrize(
    ("language", "line"),
    [
        ("basic", 'PRINT "PRIN'),
        ("python", "print('PRIN"),
        ("javascript", "console.log(`PRIN"),
        ("pascal", "write('PRIN"),
        ("prolog", "write('PRIN"),
    ],
)
def test_strings_are_suppressed(language, line):
    assert is_suppressed(language, line, len(line))


def test_closed_string_is_not_suppressed():
    assert not is_suppressed("basic", 'PRINT "HI" + PRI', 18)


def test_code_is_not_suppressed():
    assert not is_suppressed("python", "    imp", 7)


def test_completion_at_returns_span_and_words(engine):
    text = "10 PRI"
    result = engine.completion_at("basic", text, len(text))

    assert result is not None
    start, items = result
    assert text[start:] == "PRI"
    assert "PRINT" in items


def test_completion_at_is_silent_in_comments(engine):
    text = "10 REM PRI"
    assert engine.completion_at("basic", text, len(text)) is None


def test_forced_completion_ignores_the_comment_guard(engine):
    text = "10 REM PRI"
    result = engine.completion_at("basic", text, len(text), forced=True)

    assert result is not None and "PRINT" in result[1]


def test_completion_at_skips_a_word_that_is_already_complete(engine):
    """Typing the only match in full must not pop up a one-item list."""
    text = "PYTH"
    assert engine.completion_at("forth", text, len(text), forced=True) is None


def test_custom_vocabulary_is_used(engine):
    custom = CompletionEngine({"klingon": ("QAPLA", "QAP")})
    assert custom.suggestions("klingon", "QAP") == ["QAP", "QAPLA"]
