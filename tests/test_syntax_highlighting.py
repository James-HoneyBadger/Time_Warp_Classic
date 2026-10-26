"""Editor highlighting for the classic languages.

BASIC and Forth use Pygments lexers; Logo and PILOT use the built-in rule
set.  These tests need a Tk display.
"""

import os

import pytest

pytestmark = pytest.mark.skipif(
    not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")),
    reason="needs a graphical display (try xvfb-run -a)",
)


@pytest.fixture(scope="module")
def widget():
    import tkinter as tk

    from core.features.syntax_highlighting import SyntaxHighlightingText

    root = tk.Tk()
    root.withdraw()
    editor = SyntaxHighlightingText(root, language="text")
    editor.pack()
    yield editor
    try:
        root.destroy()
    except Exception:  # noqa: BLE001
        pass


def _highlight(widget, language, source):
    widget.text.delete("1.0", "end")
    widget.text.insert("1.0", source)
    widget.set_language(language)
    widget._last_highlighted_text = ""
    widget._highlight_text()
    return widget


def _tagged(widget, tag):
    return [str(index) for index in widget.text.tag_ranges(tag)]


def test_basic_gets_syntax_tags(widget):
    _highlight(widget, "basic", '10 PRINT "HELLO"\n20 GOTO 10')

    assert _tagged(widget, "syntax_keyword"), "no BASIC keywords highlighted"


def test_forth_gets_syntax_tags(widget):
    _highlight(widget, "forth", ": SQUARE DUP * ;\n5 SQUARE .")

    assert _tagged(widget, "syntax_keyword"), "no Forth keywords highlighted"


def test_logo_rules_highlight_keywords_and_comments(widget):
    _highlight(widget, "logo", "REPEAT 4 [FORWARD 100]  ; draw a square")

    assert _tagged(widget, "syntax_keyword")
    assert _tagged(widget, "syntax_comment")
    assert _tagged(widget, "syntax_number")


def test_pilot_rules_highlight_commands_and_variables(widget):
    _highlight(widget, "pilot", "T:Hello [name]\nA:[name]\n* comment line")

    assert _tagged(widget, "syntax_keyword")
    assert _tagged(widget, "syntax_variable")
    assert _tagged(widget, "syntax_comment")


def test_language_switch_clears_old_tags(widget):
    _highlight(widget, "logo", "REPEAT 4 [FORWARD 10]")
    assert _tagged(widget, "syntax_keyword")

    _highlight(widget, "text", "plain text only")

    assert not _tagged(widget, "syntax_keyword")
