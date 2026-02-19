# pylint: disable=C0415,W0718,R0801
"""
TW JavaScript Language Executor
===============================

Implements TW JavaScript, an educational interface to the JavaScript programming
language for the Time_Warp IDE, allowing execution of JavaScript code via Node.js.

Language Features:
- Full JavaScript (ES6+) syntax and semantics support
- Variables: var, let, const with different scoping rules
- Data types: primitives (string, number, boolean) and objects
- Functions: function declarations, expressions, and arrow functions
- Objects: object literals, prototypes, and classes
- Arrays: array literals with methods like push(), pop(), map(), filter()
- Control structures: if/else, switch, for/while/do-while loops
- Asynchronous programming: promises, async/await
- Modules: CommonJS (require/module.exports) and ES6 modules
- Built-in objects: Math, Date, JSON, RegExp
- String methods: substring(), replace(), split(), join()
- Error handling: try/catch/finally blocks
- DOM manipulation (limited in Node.js environment)
- File system operations via Node.js fs module

The executor provides a bridge to Node.js, allowing execution of JavaScript
code with output capture and error handling within the IDE environment.
"""

from .base import SubprocessExecutor


class JavaScriptExecutor(SubprocessExecutor):
    """Handles JavaScript language script execution via Node.js."""

    lang_name = "JavaScript"
    file_suffix = ".js"
    executable_candidates = ["node", "nodejs"]

    # ---- convenience aliases (backward-compat) ----

    def execute_javascript_file(self, filepath: str) -> bool:
        """Execute a JavaScript file."""
        return self.execute_file(filepath)

    def get_node_version(self) -> str:
        """Get Node.js version information."""
        ver = self.get_version()
        if ver and not ver.endswith("not available"):
            return f"Node.js {ver}"
        return "Node.js not available"
