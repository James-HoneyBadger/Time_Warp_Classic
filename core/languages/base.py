"""
Subprocess-based Language Executor Base Class
=============================================

Provides the shared infrastructure used by all external-process language
executors (Python, JavaScript/Node.js, Perl).  Each concrete subclass only
needs to set a few class-level attributes and, optionally, override
``execute_command`` for any language-specific pre-processing.

The base class handles:
* Discovering the language runtime on ``$PATH``
* Writing source to a secure temporary file
* Running the subprocess with a timeout
* Capturing and routing stdout / stderr
* Cleaning up the temporary file
"""

from __future__ import annotations

import os
import subprocess
import tempfile
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.interpreter import Time_WarpInterpreter


class SubprocessExecutor:
    """Base class for language executors that delegate to an external process."""

    # ---- subclass configuration (override in each subclass) ----
    lang_name: str = "Unknown"          # e.g. "Python", "JavaScript", "Perl"
    file_suffix: str = ".txt"           # temp-file extension
    executable_candidates: list[str] = []  # e.g. ["node", "nodejs"]
    timeout: int = 30                   # subprocess timeout in seconds

    def __init__(self, interpreter: Time_WarpInterpreter) -> None:
        self.interpreter = interpreter
        self.executable: str | None = self._find_executable()

    # ---- executable discovery ----

    def _find_executable(self) -> str | None:
        """Locate the language runtime on the system PATH.

        Iterates over ``executable_candidates`` and returns the first one
        that responds to ``--version``.  Subclasses that know the exact
        path (e.g. ``sys.executable`` for Python) should override this.
        """
        for name in self.executable_candidates:
            try:
                result = subprocess.run(
                    [name, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    check=False,
                )
                if result.returncode == 0:
                    return name
            except (subprocess.TimeoutExpired, FileNotFoundError):
                continue
        return None

    # ---- public API ----

    def execute_command(self, command: object) -> str:
        """Execute a command string.  Returns ``"continue"`` or ``"error"``.

        Subclasses may override this to add language-specific pre-processing
        (e.g. ensuring a trailing newline for Perl).
        """
        script_text = command if isinstance(command, str) else str(command)
        return self._execute_script(script_text)

    def execute_file(self, filepath: str) -> bool:
        """Run an existing source file.  Returns ``True`` on success."""
        if not self.executable:
            self.interpreter.log_output(
                f"❌ {self.lang_name} runtime not found on system"
            )
            return False

        try:
            if not os.path.exists(filepath):
                self.interpreter.log_output(
                    f"❌ {self.lang_name} file not found: {filepath}"
                )
                return False

            result = subprocess.run(
                [self.executable, filepath],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False,
            )

            if result.stdout:
                self.interpreter.log_output(result.stdout)
            if result.stderr:
                self.interpreter.log_output(
                    f"{self.lang_name} Error: {result.stderr}"
                )
                return False

            return result.returncode == 0

        except Exception as e:  # noqa: BLE001
            self.interpreter.log_output(
                f"❌ Error executing {self.lang_name} file: {e}"
            )
            return False

    def get_version(self) -> str:
        """Return a human-readable version string for the runtime."""
        if not self.executable:
            return f"{self.lang_name} not available"

        try:
            result = subprocess.run(
                [self.executable, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
            if result.returncode == 0:
                return self._parse_version(result.stdout)
            return f"{self.lang_name} not available"
        except Exception:  # noqa: BLE001
            return f"{self.lang_name} not available"

    # ---- internals ----

    def _execute_script(self, script_text: str) -> str:
        """Write *script_text* to a temp file, run it, and return status."""
        if not self.executable:
            self.interpreter.log_output(
                f"❌ {self.lang_name} runtime not found on system"
            )
            self.interpreter.log_output(
                f"   Please install {self.lang_name} to run {self.lang_name} scripts"
            )
            return "error"

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=self.file_suffix, delete=False
            ) as tmp:
                tmp.write(script_text)
                temp_path = tmp.name

            try:
                result = subprocess.run(
                    [self.executable, temp_path],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout,
                    check=False,
                )
            except subprocess.TimeoutExpired:
                self.interpreter.log_output(
                    f"❌ {self.lang_name} script execution timed out"
                )
                return "error"
            finally:
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass

            if result.stdout:
                self.interpreter.log_output(result.stdout)
            if result.stderr:
                self.interpreter.log_output(
                    f"{self.lang_name} Error: {result.stderr}"
                )
                return "error"
            if result.returncode != 0:
                self.interpreter.log_output(
                    f"{self.lang_name} script exited with code {result.returncode}"
                )
                return "error"

            return "continue"

        except Exception as e:  # noqa: BLE001
            self.interpreter.log_output(
                f"❌ Error executing {self.lang_name} script: {e}"
            )
            return "error"

    def _parse_version(self, stdout: str) -> str:
        """Extract a version string from ``--version`` output.

        Default implementation returns the first non-empty line.
        Override for language-specific parsing.
        """
        for line in stdout.splitlines():
            line = line.strip()
            if line:
                return line
        return f"{self.lang_name} available"
