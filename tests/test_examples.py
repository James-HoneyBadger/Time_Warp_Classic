"""Run every shipped example program and require clean output.

Examples are the project's showcase, so a regression here is user-visible.
They also give the built-in interpreters broad end-to-end coverage.
"""

import io
import shutil
from contextlib import redirect_stdout
from pathlib import Path

import pytest

from core.interpreter import Time_WarpInterpreter

pytestmark = [pytest.mark.integration, pytest.mark.language]

EXAMPLES_DIR = Path(__file__).resolve().parents[1] / "examples"

LANGUAGE_BY_FOLDER = {
    "basic": "basic",
    "logo": "logo",
    "pascal": "pascal",
    "prolog": "prolog",
    "forth": "forth",
    "pilot": "pilot",
    "perl": "perl",
    "python": "python",
    "javascript": "javascript",
}

RUNTIME_BY_LANGUAGE = {"perl": "perl", "python": None, "javascript": "node"}

FAILURE_MARKERS = ("?ERROR", "Traceback", "NOT FOUND", "not available")


def _examples():
    if not EXAMPLES_DIR.is_dir():
        return []
    found = []
    for path in sorted(EXAMPLES_DIR.glob("*/*")):
        if path.is_file() and path.suffix.lstrip(".").lower() in {
            "bas", "logo", "pas", "pro", "fth", "pilot", "pl", "py", "js"
        }:
            found.append(path)
    return found


EXAMPLES = _examples()


@pytest.fixture(autouse=True)
def _headless_display(monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")


@pytest.mark.parametrize("path", EXAMPLES, ids=lambda p: f"{p.parent.name}/{p.name}")
def test_example_runs_cleanly(path):
    language = LANGUAGE_BY_FOLDER[path.parent.name]
    runtime = RUNTIME_BY_LANGUAGE.get(language)
    if runtime and shutil.which(runtime) is None:
        pytest.skip(f"{runtime} is not installed")

    machine = Time_WarpInterpreter()
    machine.max_iterations = 200_000
    machine.input_provider = lambda prompt="": "5"

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        machine.run_program(path.read_text(encoding="utf-8"), language=language)
    output = buffer.getvalue()

    assert not machine.interrupted, "example did not finish on its own"
    for marker in FAILURE_MARKERS:
        assert marker not in output, f"{path.name} reported {marker!r}"


def test_examples_are_discovered():
    assert len(EXAMPLES) >= 18


def test_every_language_has_an_example():
    folders = {path.parent.name for path in EXAMPLES}
    assert folders == set(LANGUAGE_BY_FOLDER)
