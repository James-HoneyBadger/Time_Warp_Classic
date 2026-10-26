#!/usr/bin/env python3
"""Run the Time Warp Classic test suite.

Usage:
    python3 scripts/run_tests.py            # whole suite
    python3 scripts/run_tests.py all -v     # same, verbose (used by the IDE)
    python3 scripts/run_tests.py gui        # one file/module filter

The project's pytest configuration enforces an 80% coverage gate. The IDE
menu only reports pass/fail, so this runner clears ``addopts``; run
``python -m pytest`` directly for coverage numbers.
"""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = PROJECT_ROOT / "tests"


def main(argv):
    """Forward the arguments to pytest against the tests directory."""
    if not TESTS_DIR.is_dir():
        print(f"No test suite found at {TESTS_DIR}")
        return 1

    selectors = [arg for arg in argv if arg not in {"all", "tests"}]
    command = [
        sys.executable, "-m", "pytest",
        "-o", "addopts=",
        "-q",
        "--disable-warnings",
        str(TESTS_DIR),
        *selectors,
    ]
    print("Running:", " ".join(command), flush=True)
    return subprocess.run(command, cwd=PROJECT_ROOT, check=False).returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
