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

import sys


def main():
    """Main entry point - launches Time Warp Classic."""
    print("\U0001f680 Launching Time Warp Classic...")
    try:
        from gui.app import TimeWarpApp
        app = TimeWarpApp()
        app.run()
        sys.exit(0)
    except Exception as e:
        print(f"\u274c GUI launch failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
