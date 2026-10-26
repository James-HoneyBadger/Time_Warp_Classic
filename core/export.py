"""Export a program as a one-click runner.

Two artifacts are supported:

``.twrun``
    A small JSON bundle holding the language and the source.  The IDE and
    ``Time_Warp.py --run`` can open it, and it is easy to keep in version
    control.

``.pyz``
    A standalone runner built with :mod:`zipapp` from the standard library:
    the ``core`` package plus the embedded program.  Running it executes the
    program and exits, with no IDE, no project files and no third-party
    packages.  Built-in languages are fully contained; Python, JavaScript,
    Perl and plugin languages still need their runtime installed, exactly as
    they do inside the IDE.
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
import zipapp
from dataclasses import dataclass
from pathlib import Path

BUNDLE_FORMAT = "timewarp-run"
BUNDLE_VERSION = 1
BUNDLE_SUFFIX = ".twrun"
RUNNER_SUFFIX = ".pyz"

# Repository root: the folder that holds ``core/``.
PACKAGE_ROOT = Path(__file__).resolve().parent.parent

_MAIN_SOURCE = '''"""Standalone Time Warp Classic program runner."""
import sys

import program_data
from core.runner import run_source


def main():
    """Run the embedded program and return its exit code."""
    print(f"Time Warp Classic - {program_data.NAME}")
    return run_source(program_data.PROGRAM, program_data.LANGUAGE)


if __name__ == "__main__":
    sys.exit(main())
'''


class BundleError(ValueError):
    """A bundle could not be read or was not written by this app."""


@dataclass(frozen=True)
class RunBundle:
    """A program packaged for running without the editor."""

    language: str
    program: str
    name: str = "program"

    def to_json(self):
        """Serialise the bundle, including its format marker."""
        if not str(self.language or "").strip():
            raise BundleError("a bundle needs a language")
        return json.dumps(
            {
                "format": BUNDLE_FORMAT,
                "version": BUNDLE_VERSION,
                "language": str(self.language).strip(),
                "name": self.name or "program",
                "program": self.program,
            },
            indent=2,
        ) + "\n"

    @classmethod
    def from_json(cls, text):
        """Parse a bundle, rejecting foreign or newer files."""
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise BundleError(f"not a Time Warp bundle: {exc}") from exc
        if not isinstance(data, dict) or data.get("format") != BUNDLE_FORMAT:
            raise BundleError("not a Time Warp bundle")
        version = data.get("version", BUNDLE_VERSION)
        if version > BUNDLE_VERSION:
            raise BundleError(
                f"bundle version {version} is newer than this app supports"
            )
        language = data.get("language")
        program = data.get("program")
        if not isinstance(language, str) or not language.strip():
            raise BundleError("bundle is missing its language")
        if not isinstance(program, str):
            raise BundleError("bundle is missing its program text")
        return cls(
            language=language.strip(),
            program=program,
            name=str(data.get("name") or "program"),
        )


def write_bundle(bundle, path):
    """Write *bundle* to *path* and return the path."""
    target = Path(path)
    target.write_text(bundle.to_json(), encoding="utf-8")
    return target


def read_bundle(path):
    """Read a bundle from *path*."""
    try:
        text = Path(path).read_text(encoding="utf-8")
    except OSError as exc:
        raise BundleError(f"cannot read {path}: {exc}") from exc
    return RunBundle.from_json(text)


def _program_module(bundle):
    """Python source for the embedded program."""
    return (
        '"""Program embedded by the Time Warp Classic exporter."""\n'
        f"NAME = {bundle.name!r}\n"
        f"LANGUAGE = {bundle.language!r}\n"
        f"PROGRAM = {bundle.program!r}\n"
    )


def build_standalone_runner(bundle, target, package_root=None):
    """Build an executable ``.pyz`` runner for *bundle* at *target*.

    The archive holds a copy of the ``core`` package and the program, so it
    runs with nothing more than a Python interpreter.
    """
    root = Path(package_root or PACKAGE_ROOT)
    core = root / "core"
    if not core.is_dir():
        raise BundleError(f"cannot find the core package under {root}")

    target = Path(target)
    with tempfile.TemporaryDirectory(prefix="timewarp-export-") as workspace:
        staging = Path(workspace) / "runner"
        staging.mkdir()
        shutil.copytree(
            core,
            staging / "core",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"),
        )
        (staging / "program_data.py").write_text(
            _program_module(bundle), encoding="utf-8"
        )
        (staging / "__main__.py").write_text(_MAIN_SOURCE, encoding="utf-8")
        zipapp.create_archive(
            staging,
            target=target,
            interpreter="/usr/bin/env python3",
            compressed=True,
        )

    if os.name == "posix":
        target.chmod(0o755)
    return target


def export_language_available(language):
    """True for languages an exported runner can execute on its own.

    The bundled runtime covers the six built-in interpreters.  The others
    (Python, JavaScript, Perl and plugin languages) need their external
    runtime, which the archive cannot carry.
    """
    return str(language or "").strip().lower() in {
        "pilot", "basic", "logo", "pascal", "prolog", "forth",
    }
