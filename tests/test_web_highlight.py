"""Tests for server-side syntax highlighting used by the browser editor."""

import web.highlight as highlight_module
from web.highlight import ALIASES, escape, highlight


def test_python_tokens_are_coloured():
    html = highlight("Python", "def f(x):\n    return x + 1\n")

    assert "<span" in html
    assert "def" in html and "return" in html


def test_basic_uses_the_commodore_lexer():
    html = highlight("BASIC", '10 PRINT "HI"')

    assert "<span" in html
    assert "PRINT" in html


def test_language_names_are_case_insensitive():
    assert highlight("python", "print(1)") == highlight("PYTHON", "print(1)")


def test_unknown_language_is_plain_text():
    html = highlight("Cobol", 'DISPLAY "HI".')

    assert "<span" not in html
    assert "DISPLAY" in html


def test_no_lexer_languages_stay_plain():
    for language in ("PILOT", "Logo"):
        assert "<span" not in highlight(language, 'PRINT "HI"')


def test_source_is_escaped():
    html = highlight("Python", "print('<script>alert(1)</script>')")

    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_escape_helper_escapes_angle_brackets():
    assert escape("<b>&</b>") == "&lt;b&gt;&amp;&lt;/b&gt;"


def test_empty_source_returns_empty_html():
    assert highlight("Python", "") == ""
    assert highlight("Python", None) == ""


def test_plugin_alias_is_honoured():
    html = highlight("TinyRuby", "def x\n  1\nend", alias="ruby")

    assert "<span" in html


def test_all_builtin_languages_have_an_alias():
    expected = {
        "pilot", "basic", "logo", "pascal", "prolog",
        "forth", "perl", "python", "javascript",
    }

    assert set(ALIASES) == expected


def test_missing_pygments_falls_back_to_plain_text(monkeypatch):
    monkeypatch.setattr(highlight_module, "PYGMENTS_AVAILABLE", False)

    html = highlight("Python", "def f(): pass")

    assert "<span" not in html
    assert "def f(): pass" in html
