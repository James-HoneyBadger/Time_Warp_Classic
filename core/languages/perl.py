# pylint: disable=C0415,W0718
"""
TW Perl Language Executor
=========================

Implements TW Perl, an educational interface to the Perl programming language
for the Time_Warp IDE, allowing execution of Perl scripts within the IDE environment.

Language Features:
- Full Perl syntax and semantics support
- Scalar variables: $variable
- Arrays: @array with indexing
- Hashes: %hash with key-value pairs
- Regular expressions: pattern matching with =~ and !~
- Control structures: if/elsif/else, while, for, foreach
- Subroutines: sub keyword for function definition
- File I/O: open, close, read, write operations
- String operations: concatenation, substr, length, split, join
- Built-in functions: print, chomp, split, join, sort, grep, map
- Modules: use pragma for importing modules
- Object-oriented programming with packages and methods

The executor provides a bridge to system Perl installations, allowing
execution of Perl code with output capture and error handling within the IDE.
"""

from .base import SubprocessExecutor


class PerlExecutor(SubprocessExecutor):
    """Handles Perl language script execution."""

    lang_name = "Perl"
    file_suffix = ".pl"
    executable_candidates = ["perl", "perl5"]

    def execute_command(self, command: object) -> str:
        """Execute a Perl command or script.

        Ensures a trailing newline so the Perl parser handles single-line
        statements correctly.
        """
        script_text = command if isinstance(command, str) else str(command)
        if not script_text.endswith("\n"):
            script_text += "\n"
        return self._execute_script(script_text)

    # ---- convenience aliases (backward-compat) ----

    def execute_perl_file(self, filepath: str) -> bool:
        """Execute a Perl file."""
        return self.execute_file(filepath)

    def get_perl_version(self) -> str:
        """Get Perl version information."""
        return self.get_version()

    def _parse_version(self, stdout: str) -> str:
        """Extract version from Perl's verbose --version output."""
        for line in stdout.splitlines():
            if "version" in line.lower():
                return line.strip()
        return "Perl available"

