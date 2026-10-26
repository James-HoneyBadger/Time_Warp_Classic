#!/usr/bin/env python3
"""
Time Warp Classic - Multi-Language Programming Environment

A back-to-basics Tkinter IDE for 9 vintage + modern languages
with integrated turtle graphics.

Copyright © 2025–2026 Honey Badger Universe. All rights reserved.

Supports: PILOT, BASIC, Logo, Pascal, Prolog, Forth, Perl, Python, JavaScript

Architecture:
- gui/app.py    — TimeWarpApp (tkinter IDE window)
- core/interpreter.py — Time_WarpInterpreter (central execution engine)
- core/languages/     — 6 built-in interpreters + 3 subprocess executors
- core/stubs.py       — Placeholder classes for optional subsystems

Features:
- 9 programming languages (6 built-in, 3 external runtime)
- Syntax highlighting via Pygments (with fallback)
- Integrated turtle graphics for visual programming
- 9 color themes with persistence
- Debug tools, breakpoints, error history
- Customizable fonts (7 sizes + system monospace families)
"""

import argparse
import sys
from pathlib import Path

from core.export import BUNDLE_SUFFIX, BundleError, read_bundle
from core.runner import EXIT_OK, EXIT_PROGRAM_ERROR, run_source

# Exit code for a bad invocation (unknown file, missing --language, ...).
EXIT_USAGE = 2


def _parse_args(argv=None):
    """Parse the command line; no arguments means "open the IDE"."""
    parser = argparse.ArgumentParser(
        prog="timewarp",
        description="Time Warp Classic - multi-language IDE and runner.",
    )
    parser.add_argument(
        "--run", "-r", metavar="FILE",
        help="run a .twrun bundle or a source file, print the output and exit",
    )
    parser.add_argument(
        "--language", "-l", metavar="LANG",
        help="language of a plain source file passed to --run",
    )
    parser.add_argument(
        "--version", "-V", action="store_true",
        help="print the version and exit",
    )
    parser.add_argument(
        "--web", action="store_true",
        help="serve the web IDE instead of opening the desktop window",
    )
    parser.add_argument(
        "--host", default="127.0.0.1",
        help="address for --web (default 127.0.0.1; use 0.0.0.0 in containers)",
    )
    parser.add_argument(
        "--port", type=int, default=8000,
        help="port for --web (default 8000, 0 picks a free port)",
    )
    parser.add_argument(
        "--timeout", type=float, default=10.0,
        help="seconds a web program may run before it is stopped (default 10)",
    )
    return parser.parse_args(argv)


def _run_file(path, language=None):
    """Execute *path* headlessly and return a process exit code."""
    source = Path(path)
    if not source.is_file():
        print(f"?ERROR: no such file: {path}")
        return EXIT_USAGE

    if source.suffix.lower() == BUNDLE_SUFFIX:
        try:
            bundle = read_bundle(source)
        except BundleError as exc:
            print(f"?ERROR: {exc}")
            return EXIT_USAGE
        return run_source(bundle.program, bundle.language)

    if not language:
        print(
            "?ERROR: --language is required when running a plain source file\n"
            f"        try: timewarp --run {path} --language basic"
        )
        return EXIT_USAGE
    return run_source(source.read_text(encoding="utf-8"), language)


def main(argv=None):
    """Command line entry point: run a program, or launch the IDE."""
    args = _parse_args(argv)

    if args.version:
        from core import __version__

        print(f"Time Warp Classic {__version__}")
        return EXIT_OK

    if args.run:
        return _run_file(args.run, args.language)

    if args.web:
        from web.server import serve

        serve(host=args.host, port=args.port, timeout=args.timeout)
        return EXIT_OK

    print("\U0001f680 Launching Time Warp Classic...")
    try:
        from gui.app import TimeWarpApp
        app = TimeWarpApp()
        app.run()
        return EXIT_OK
    except Exception as e:
        print(f"\u274c GUI launch failed: {e}")
        import traceback
        traceback.print_exc()
        return EXIT_PROGRAM_ERROR


if __name__ == "__main__":
    sys.exit(main())
