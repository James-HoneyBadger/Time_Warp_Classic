# pylint: disable=C0415,W0718
"""
TW Python Language Executor
===========================

Implements TW Python, an educational interface to the Python programming language
for the Time_Warp IDE, allowing execution of Python code within the IDE environment.

Language Features:
- Full Python 3 syntax and semantics support
- Variables: dynamic typing with automatic memory management
- Data structures: lists, tuples, dictionaries, sets
- Control structures: if/elif/else, for/while loops, try/except
- Functions: def keyword with parameters and return values
- Classes: object-oriented programming with inheritance
- Modules: import system for code organization
- Built-in functions: print(), len(), range(), enumerate(), zip()
- String operations: formatting, slicing, methods
- File I/O: open(), read(), write(), close()
- Exception handling: raise, try/except/finally blocks
- List comprehensions and generator expressions
- Lambda functions and higher-order functions

The executor provides a bridge to the Python interpreter, allowing
execution of Python code with output capture and error handling within the IDE.
"""

import sys

from .base import SubprocessExecutor


class PythonExecutor(SubprocessExecutor):
    """Handles Python language script execution."""

    lang_name = "Python"
    file_suffix = ".py"

    # Python always uses the same interpreter that runs Time_Warp.
    def _find_executable(self) -> str:
        return sys.executable

    # ---- convenience aliases (backward-compat) ----

    def execute_python_file(self, filepath: str) -> bool:
        """Execute a Python file."""
        return self.execute_file(filepath)

    def get_python_version(self) -> str:
        """Get Python version information."""
        return f"Python {sys.version}"

