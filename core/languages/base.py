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
* Streaming stdout / stderr into the IDE console line by line
* Feeding console input to the script's stdin
* Reporting the failing script line as a clickable ``?ERROR IN n`` message
* Cleaning up the temporary file
"""

from __future__ import annotations

import os
import queue
import re
import shutil
import subprocess
import tempfile
import threading
import time
from typing import TYPE_CHECKING

from .catalog import missing_runtime_hint

if TYPE_CHECKING:
    from core.interpreter import Time_WarpInterpreter


# Lines that name the script line an error happened on, per runtime.
_ERROR_LINE_PATTERNS = (
    re.compile(r'File "[^"]*", line (\d+)'),   # Python traceback
    re.compile(r"at .*?:(\d+):\d+"),            # Node.js stack
    re.compile(r"\bline (\d+)\b"),             # Perl "... at script line 3"
)


class SubprocessExecutor:
    """Base class for language executors that delegate to an external process."""

    # ---- subclass configuration (override in each subclass) ----
    lang_name: str = "Unknown"          # e.g. "Python", "JavaScript", "Perl"
    file_suffix: str = ".txt"           # temp-file extension
    executable_candidates: list[str] = []  # e.g. ["node", "nodejs"]
    extra_args: tuple[str, ...] = ()    # runtime flags, e.g. ("-u",) for Python
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
            self.interpreter.log_output(self.missing_runtime_message())
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

    def missing_runtime_message(self) -> str:
        """Explain that the runtime is missing, and how to install it.

        Plugin languages override this to name the manifest's executable.
        """
        message = (
            f"?{self.lang_name.upper()} NOT FOUND - install it to run these scripts"
        )
        hint = missing_runtime_hint(self.lang_name)
        return f"{message} ({hint})" if hint else message

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
        """Write *script_text* to a temp file, run it, and return status.

        Output is streamed line by line so long-running scripts show progress,
        console input reaches the script's stdin, and the run is abandoned as
        soon as the host requests a stop.
        """
        if not self.executable:
            self.interpreter.log_output(self.missing_runtime_message())
            return "error"

        try:
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=self.file_suffix, delete=False
            ) as tmp:
                tmp.write(script_text)
                temp_path = tmp.name

            try:
                returncode, stop_reason, error_line, error_message = self._run_streaming(
                    [self.executable, *self.extra_args, temp_path],
                    script_path=temp_path,
                )
            finally:
                try:
                    os.unlink(temp_path)
                except OSError:
                    pass

            if stop_reason == "stopped":
                return "stopped"
            if stop_reason == "timeout":
                self.interpreter.log_error(
                    f"{self.lang_name} script timed out after {self.timeout}s",
                    error_line,
                )
                return "error"
            if returncode:
                message = error_message or f"{self.lang_name} script exited with code {returncode}"
                self.interpreter.log_error(message, error_line)
                return "error"

            return "continue"

        except Exception as e:  # noqa: BLE001
            self.interpreter.log_error(f"Error executing {self.lang_name} script: {e}")
            return "error"

    def _run_streaming(
        self, command: list[str], script_path: str = ""
    ) -> tuple[int | None, str, int | None, str]:
        """Run *command*, streaming merged output into the IDE console.

        Returns ``(returncode, stop_reason, error_line, error_message)``.
        *stop_reason* is ``""`` for a normal exit, ``"stopped"`` when the user
        interrupted the run, or ``"timeout"`` when the runtime exceeded
        :attr:`timeout`.  *error_line* is the script line named in the
        runtime's error output, when one could be found.
        """
        deadline = None if self.timeout is None else time.monotonic() + self.timeout
        proc = subprocess.Popen(  # noqa: S603 - command is built from known names
            self._buffered_command(command),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=self._child_env(),
        )
        lines: queue.Queue[str | None] = queue.Queue()
        error_line = None
        error_message = ""

        def _reader() -> None:
            try:
                if proc.stdout is not None:
                    for line in proc.stdout:
                        lines.put(line)
            finally:
                lines.put(None)

        threading.Thread(target=_reader, daemon=True).start()

        try:
            while True:
                try:
                    line = lines.get(timeout=0.05)
                except queue.Empty:
                    line = ""

                if line is None:
                    break
                if line:
                    text = line.rstrip("\n")
                    self.interpreter.log_output(text)
                    error_line, error_message = self._inspect_error(
                        text, error_line, error_message, os.path.basename(script_path)
                    )

                self._feed_console_input(proc)
                if self.interpreter.pump():
                    proc.kill()
                    return None, "stopped", error_line, error_message
                if deadline is not None and time.monotonic() > deadline:
                    proc.kill()
                    return None, "timeout", error_line, error_message

            return proc.wait(), "", error_line, error_message
        finally:
            if proc.poll() is None:
                proc.kill()
                proc.wait()
            for stream in (proc.stdin, proc.stdout):
                try:
                    if stream is not None:
                        stream.close()
                except OSError:
                    pass

    def _buffered_command(self, command: list[str]) -> list[str]:
        """Force line buffering so output appears as it is produced."""
        if os.name != "posix":
            return command
        stdbuf = shutil.which("stdbuf")
        if not stdbuf:
            return command
        return [stdbuf, "-oL", "-eL", *command]

    def _child_env(self) -> dict[str, str]:
        """Environment for the child process (unbuffered, UTF-8)."""
        env = os.environ.copy()
        env.setdefault("PYTHONUNBUFFERED", "1")
        env.setdefault("PYTHONIOENCODING", "utf-8")
        return env

    def _parse_version(self, stdout: str) -> str:
        """Extract a version string from ``--version`` output."""
        for line in stdout.splitlines():
            line = line.strip()
            if line:
                return line
        return f"{self.lang_name} available"

    def _feed_console_input(self, proc: subprocess.Popen) -> None:
        """Forward lines typed at the IDE console to the script's stdin."""
        buffer = getattr(self.interpreter, "input_buffer", None)
        if not buffer or proc.stdin is None:
            return
        while buffer:
            line = buffer.pop(0)
            try:
                proc.stdin.write(f"{line}\n")
                proc.stdin.flush()
            except (BrokenPipeError, ValueError, OSError):
                return
            self.interpreter.log_output(str(line))

    @staticmethod
    def _inspect_error(text, error_line, error_message, script_name=""):
        """Remember the script line and message named in runtime error output.

        Frames naming the script itself are trusted; runtime-internal frames
        (``node:internal/...``) are not, so the line number stays useful.
        """
        stripped = text.strip()
        if not stripped:
            return error_line, error_message

        if script_name and script_name in stripped:
            for pattern in _ERROR_LINE_PATTERNS:
                match = pattern.search(stripped)
                if match:
                    error_line = int(match.group(1))
                    break
            if not stripped.startswith("at "):
                # Perl appends " at /tmp/script.pl line N." - drop the path.
                error_message = re.sub(r"\s+at .*? line \d+\.?\s*$", "", stripped)
        elif "error" in stripped.lower() or "exception" in stripped.lower():
            error_message = stripped

        return error_line, error_message
