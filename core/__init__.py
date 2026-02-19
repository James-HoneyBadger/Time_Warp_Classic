"""
Time Warp Classic Core Module
==============================

Copyright © 2025–2026 Honey Badger Universe. All rights reserved.

Core functionality for Time Warp Classic, providing the main interpreter engine
and language execution capabilities.

This module serves as the central hub for:
- Time_WarpInterpreter: Main execution engine for all supported languages
- Language executors: Individual language implementations
- Utility functions: Helper classes and shared functionality

The core module handles program execution independently of the GUI.
All GUI components are in the gui/ package.

Supported Languages (built-in interpreters):
- TW PILOT (1968): Educational CAI language
- TW BASIC (1964): Classic line-numbered programming
- TW Logo (1967): Turtle graphics programming
- TW Pascal (1970): Structured programming
- TW Prolog (1972): Logic programming
- TW Forth (1970): Stack-based programming

Supported Languages (external runtime executors via SubprocessExecutor):
- Perl (1987): Delegates to system `perl`
- Python (1991): Delegates to `sys.executable`
- JavaScript (1995): Delegates to `node`/`nodejs`

Usage:
    from core.interpreter import Time_WarpInterpreter
    interpreter = Time_WarpInterpreter()
    interpreter.run_program("T:Hello World!")
"""

__version__ = "1.3.0"
__author__ = "Honey Badger Universe"

from .interpreter import Time_WarpInterpreter
from . import languages
from . import utilities

__all__ = ["Time_WarpInterpreter", "languages", "utilities"]
