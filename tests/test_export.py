"""Tests for exporting a program as a runner: bundles, archives and the CLI."""

import subprocess
import sys
from pathlib import Path

import pytest

from core.export import (
    BUNDLE_FORMAT,
    BundleError,
    RunBundle,
    build_standalone_runner,
    export_language_available,
    read_bundle,
    write_bundle,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRY_POINT = REPO_ROOT / "Time_Warp.py"

BASIC_PROGRAM = '10 PRINT "FROM THE RUNNER"\n20 FOR I = 1 TO 3\n30 PRINT I\n40 NEXT I\n'


# ------------------------------------------------------------------ bundles

def test_bundle_round_trip(tmp_path):
    bundle = RunBundle(language="basic", program=BASIC_PROGRAM, name="demo")
    path = write_bundle(bundle, tmp_path / "demo.twrun")

    assert read_bundle(path) == bundle
    assert '"format": "timewarp-run"' in path.read_text()


def test_bundle_requires_a_language():
    with pytest.raises(BundleError):
        RunBundle(language="  ", program="10 PRINT 1").to_json()


@pytest.mark.parametrize(
    "text",
    [
        "not json",
        '{"language": "basic", "program": "x"}',
        '{"format": "something-else", "language": "basic", "program": "x"}',
        '{"format": "timewarp-run", "version": 99, "language": "basic", "program": "x"}',
        '{"format": "timewarp-run", "version": 1, "program": "x"}',
        '{"format": "timewarp-run", "version": 1, "language": "basic"}',
    ],
)
def test_invalid_bundles_are_rejected(text):
    with pytest.raises(BundleError):
        RunBundle.from_json(text)


def test_missing_bundle_file_is_reported(tmp_path):
    with pytest.raises(BundleError):
        read_bundle(tmp_path / "nope.twrun")


def test_bundle_format_constant_matches_written_file(tmp_path):
    path = write_bundle(RunBundle("basic", "10 PRINT 1"), tmp_path / "x.twrun")

    assert BUNDLE_FORMAT in path.read_text()


# ----------------------------------------------------------------- archives

@pytest.fixture(scope="module")
def built_runner(tmp_path_factory):
    """A standalone runner for a BASIC program, built once for the module."""
    directory = tmp_path_factory.mktemp("export")
    bundle = RunBundle(language="basic", program=BASIC_PROGRAM, name="demo")
    return build_standalone_runner(bundle, directory / "demo.pyz")


def test_runner_archive_is_created(built_runner):
    assert built_runner.is_file()
    assert built_runner.stat().st_size > 10_000
    # A zipapp starts with its shebang and a zip signature.
    assert built_runner.read_bytes()[:2] == b"#!"


def test_runner_executes_the_program(built_runner):
    result = subprocess.run(
        [sys.executable, str(built_runner)],
        capture_output=True, text=True, timeout=60,
    )

    assert result.returncode == 0
    assert "FROM THE RUNNER" in result.stdout
    assert result.stdout.splitlines()[-3:] == ["1", "2", "3"]


def test_runner_reports_program_errors_with_a_nonzero_exit(tmp_path):
    bundle = RunBundle(language="basic", program='\n10 PRINT 1/0\n', name="bad")
    runner = build_standalone_runner(bundle, tmp_path / "bad.pyz")

    result = subprocess.run(
        [sys.executable, str(runner)],
        capture_output=True, text=True, timeout=60,
    )

    assert result.returncode == 1
    assert "?ERROR IN 2" in result.stdout


def test_runner_archive_does_not_depend_on_the_project(tmp_path):
    """The archive carries its own copy of the core package."""
    bundle = RunBundle(language="pilot", program="T:STANDALONE\n", name="pilot-demo")
    runner = build_standalone_runner(bundle, tmp_path / "pilot.pyz")

    result = subprocess.run(
        [sys.executable, str(runner)],
        capture_output=True, text=True, timeout=60, cwd=str(tmp_path),
    )

    assert result.returncode == 0
    assert "STANDALONE" in result.stdout


def test_export_availability_marks_external_runtimes():
    for language in ("basic", "logo", "pascal", "forth", "pilot", "prolog"):
        assert export_language_available(language)
    for language in ("python", "javascript", "perl", "Ruby"):
        assert not export_language_available(language)


# ---------------------------------------------------------------------- CLI

def _cli(*args):
    return subprocess.run(
        [sys.executable, str(ENTRY_POINT), *args],
        capture_output=True, text=True, timeout=90, cwd=str(REPO_ROOT),
    )


def test_cli_version():
    result = _cli("--version")

    assert result.returncode == 0
    assert "Time Warp Classic" in result.stdout


def test_cli_runs_a_bundle(tmp_path):
    bundle = write_bundle(
        RunBundle("basic", BASIC_PROGRAM, name="demo"), tmp_path / "demo.twrun"
    )

    result = _cli("--run", str(bundle))

    assert result.returncode == 0
    assert "FROM THE RUNNER" in result.stdout
    assert "Interpreter ready" not in result.stdout


def test_cli_runs_a_plain_source_file(tmp_path):
    source = tmp_path / "hello.bas"
    source.write_text(BASIC_PROGRAM, encoding="utf-8")

    result = _cli("--run", str(source), "--language", "basic")

    assert result.returncode == 0
    assert "FROM THE RUNNER" in result.stdout


def test_cli_requires_a_language_for_plain_files(tmp_path):
    source = tmp_path / "hello.bas"
    source.write_text(BASIC_PROGRAM, encoding="utf-8")

    result = _cli("--run", str(source))

    assert result.returncode == 2
    assert "--language" in result.stdout


def test_cli_reports_a_missing_file(tmp_path):
    result = _cli("--run", str(tmp_path / "nope.bas"), "--language", "basic")

    assert result.returncode == 2
    assert "no such file" in result.stdout


def test_cli_reports_a_broken_bundle(tmp_path):
    broken = tmp_path / "broken.twrun"
    broken.write_text("{not json", encoding="utf-8")

    result = _cli("--run", str(broken))

    assert result.returncode == 2
    assert "not a Time Warp bundle" in result.stdout


def test_cli_exit_code_reports_program_errors(tmp_path):
    source = tmp_path / "bad.bas"
    source.write_text("\n10 PRINT 1/0\n", encoding="utf-8")

    result = _cli("--run", str(source), "--language", "basic")

    assert result.returncode == 1
    assert "?ERROR IN 2" in result.stdout


def test_cli_feeds_console_input_from_stdin(tmp_path):
    """A program using INPUT reads the runner's stdin."""
    source = tmp_path / "ask.bas"
    source.write_text('10 INPUT "Name"; N$\n20 PRINT "HI "; N$\n', encoding="utf-8")

    result = subprocess.run(
        [sys.executable, str(ENTRY_POINT), "--run", str(source),
         "--language", "basic"],
        capture_output=True, text=True, timeout=90, input="Ada\n", cwd=str(REPO_ROOT),
    )

    assert result.returncode == 0
    assert "HI Ada" in result.stdout
