"""Local web front-end for Time Warp Classic.

The same interpreter that powers the desktop IDE is served over HTTP, so a
program can be written and run from a browser.  Everything here uses the
standard library: a :class:`~http.server.ThreadingHTTPServer` with a JSON API
and Server-Sent Events for streamed output.

Run it with ``python Time_Warp.py --web`` (loopback only by default) or from
the IDE's *Program -> Open Web IDE* menu entry.
"""

from __future__ import annotations

import contextlib
import io
import json
import signal
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

import uuid

from core import __version__
from core.interpreter import Time_WarpInterpreter
from core.languages.basic_console import BasicConsole
from web.canvas import DEFAULT_HEIGHT, DEFAULT_WIDTH, RasterCanvas
from web.highlight import highlight as highlight_source
from core.languages.catalog import (
    EXT_TO_LANG, SUPPORTED_LANGUAGES, language_extension, runtime_available,
)
from core.plugins import PluginRegistry

PACKAGE_ROOT = Path(__file__).resolve().parent.parent
STATIC_DIR = Path(__file__).resolve().parent / "static"
try:  # the examples ship inside the wheel
    from examples import EXAMPLES_ROOT as EXAMPLES_DIR
except ImportError:  # pragma: no cover - source tree without the package
    EXAMPLES_DIR = PACKAGE_ROOT / "examples"

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_TIMEOUT = 10.0
MAX_PROGRAM_BYTES = 256 * 1024
MAX_CONCURRENT_RUNS = 4
# High enough that the wall-clock limit is what stops a runaway program;
# this cap only guards against a loop that outruns the clock check.
DEFAULT_ITERATIONS = 50_000_000

# REPL: one persistent interpreter per browser tab, with a short per-line
# deadline so a typo like "10 GOTO 10" cannot wedge the server.
DEFAULT_REPL_TIMEOUT = 2.0
MAX_REPL_SESSIONS = 16
REPL_SESSION_TTL = 600.0
MAX_REPL_LINE = 8 * 1024

# A program waiting at INPUT does not use up its time limit, but it does hold
# a run slot, so the wait itself is capped.
DEFAULT_INPUT_TIMEOUT = 300.0
# While waiting for input the stream sends a comment this often, which is how
# a closed tab is noticed.
KEEPALIVE_INTERVAL = 5.0
MAX_RUN_ID = 64
# A tight PRINT loop can produce lines far faster than anyone can read them;
# past this many the run is stopped rather than flooding the browser.
MAX_OUTPUT_LINES = 20_000

REPL_INPUT_MESSAGE = "?INPUT needs a running program: put it in the editor and press Run"


class BadRequest(Exception):
    """The client asked for something that cannot be served."""

    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status


class _ReplSession:
    """A persistent interpreter, so variables survive between REPL lines."""

    def __init__(self, language, timeout, plugins=None):
        self.language = language
        self.timeout = timeout
        self.plugins = plugins
        self.canvas = RasterCanvas(DEFAULT_WIDTH, DEFAULT_HEIGHT)
        self.lock = threading.Lock()
        self.interpreter = self._new_interpreter()
        self.last_used = time.monotonic()

    def _new_interpreter(self):
        with contextlib.redirect_stdout(io.StringIO()):
            interpreter = Time_WarpInterpreter()
        interpreter.console_banner = False
        interpreter.turtle_console = False
        interpreter.max_iterations = DEFAULT_ITERATIONS
        interpreter.plugins = self.plugins
        interpreter.input_buffer = []
        # Without a provider, INPUT would read the server's own stdin.
        interpreter.input_provider = self._refuse_input
        with contextlib.redirect_stdout(io.StringIO()):
            interpreter.set_language_mode(self.language.lower())
        interpreter.ide_turtle_canvas = self.canvas
        return interpreter

    def _refuse_input(self, _prompt=""):
        self.interpreter.log_output(REPL_INPUT_MESSAGE)
        return None


class _ActiveRun:
    """Book-keeping for a run that can still be stopped or sent input."""

    def __init__(self, run_id, interpreter):
        self.run_id = run_id
        self.interpreter = interpreter
        self.stopped = False
        self.waiting_for_input = False

    def stop(self):
        self.stopped = True
        self.interpreter.stop_program()


class RunnerService:
    """Language metadata and program execution, independent of HTTP."""

    def __init__(self, timeout=DEFAULT_TIMEOUT, plugins=None, examples_dir=None,
                 repl_timeout=DEFAULT_REPL_TIMEOUT, max_sessions=MAX_REPL_SESSIONS,
                 session_ttl=REPL_SESSION_TTL, input_timeout=DEFAULT_INPUT_TIMEOUT):
        self.timeout = timeout
        self.plugins = plugins if plugins is not None else PluginRegistry()
        self.examples_dir = Path(examples_dir or EXAMPLES_DIR)
        self.repl_timeout = repl_timeout
        self.max_sessions = max_sessions
        self.session_ttl = session_ttl
        self.input_timeout = input_timeout
        self._slots = threading.BoundedSemaphore(MAX_CONCURRENT_RUNS)
        self._lock = threading.Lock()
        self._sessions = {}
        self._runs = {}

    # ---- metadata -----------------------------------------------------

    def languages(self):
        """Selectable languages with their extension and run-time readiness."""
        entries = [
            {
                "name": language,
                "key": language.lower(),
                "extension": language_extension(language),
                "available": runtime_available(language),
            }
            for language in SUPPORTED_LANGUAGES
        ]
        entries.extend(
            {
                "name": spec.name,
                "key": spec.name.lower(),
                "extension": spec.extension or ".txt",
                "available": runtime_available(spec.name, spec.executable),
            }
            for spec in self.plugins
        )
        return entries

    def _known_language(self, language):
        key = str(language or "").strip().lower()
        if not key:
            return None
        for language_name in SUPPORTED_LANGUAGES:
            if language_name.lower() == key:
                return language_name
        spec = self.plugins.get(key)
        return spec.name if spec else None

    def examples(self):
        """Shipped example programs, grouped by language folder."""
        found = []
        if not self.examples_dir.is_dir():
            return found
        for path in sorted(self.examples_dir.rglob("*")):
            # Only programs inside a language folder; the package files and
            # README at the root are not examples.
            if not path.is_file() or path.parent == self.examples_dir:
                continue
            if path.name.startswith("_"):
                continue
            suffix = path.suffix.lower()
            if suffix in EXT_TO_LANG:
                language = EXT_TO_LANG[suffix]
                found.append(
                    {
                        "name": f"{language}: {path.stem.replace('_', ' ')}",
                        "language": language,
                        "path": path.relative_to(self.examples_dir).as_posix(),
                    }
                )
        return found

    def example_source(self, relative_path):
        """Source text of one example, refusing paths outside the folder."""
        base = self.examples_dir.resolve()
        candidate = (base / unquote(str(relative_path))).resolve()
        if base not in candidate.parents or not candidate.is_file():
            raise BadRequest("no such example", status=404)
        return candidate.read_text(encoding="utf-8")

    # ---- REPL ---------------------------------------------------------

    def repl(self, session, language, line, program=None):
        """Run one statement in a persistent session and return its output.

        For BASIC the line goes through classic direct mode: ``10 PRINT 1``
        edits *program* (the editor text), ``LIST``/``RUN``/``NEW`` work on
        it, and the reply carries the edited ``program`` or the text to
        ``run`` so the page can act on it.
        """
        if not isinstance(line, str) or not line.strip():
            raise BadRequest("enter a statement to run")
        if len(line.encode("utf-8", "replace")) > MAX_REPL_LINE:
            raise BadRequest("statement is too long", status=413)
        if program is not None and not isinstance(program, str):
            raise BadRequest("'program' must be text")
        if program and len(program.encode("utf-8", "replace")) > MAX_PROGRAM_BYTES:
            raise BadRequest("program is too large", status=413)

        resolved = self._known_language(language)
        if resolved is None:
            raise BadRequest(f"unknown language: {language}")

        if not self._slots.acquire(blocking=False):
            raise BadRequest("too many programs are running, try again", status=429)

        try:
            entry = self._session(session, resolved)
            if not entry.lock.acquire(timeout=self.repl_timeout + 1.0):
                raise BadRequest("the previous statement is still running", status=429)
            try:
                return self._repl_line(entry, line, program)
            finally:
                entry.last_used = time.monotonic()
                entry.lock.release()
        finally:
            self._slots.release()

    def _session(self, session, language):
        key = str(session or "default")[:MAX_RUN_ID] or "default"
        with self._lock:
            entry = self._sessions.get(key)
            if entry is None or entry.language != language:
                entry = _ReplSession(language, self.repl_timeout, self.plugins)
                entry.key = key
                self._sessions[key] = entry
                self._trim_sessions()
            entry.last_used = time.monotonic()
            return entry

    def _repl_line(self, entry, line, program):
        lines = []
        interpreter = entry.interpreter
        interpreter.log_output = lambda text: lines.append(str(text))
        # A previous line may have been stopped by the deadline.
        interpreter.stop_requested = False
        interpreter.interrupted = False
        interpreter.input_buffer = []

        started = time.monotonic()

        def pump():
            if time.monotonic() - started > self.repl_timeout:
                interpreter.stop_program()

        interpreter.pump_callback = pump

        edits = {"program": None, "run": None}
        status = "continue"
        try:
            if entry.language == "BASIC":
                editor = {"text": program or ""}

                def set_program(text):
                    editor["text"] = text
                    edits["program"] = text

                console = BasicConsole(
                    interpreter,
                    get_program=lambda: editor["text"],
                    set_program=set_program,
                    run_program=lambda text: edits.__setitem__("run", text),
                )
                lines.extend(console.submit(line))
            else:
                status = interpreter.execute_line(line)
        except Exception as exc:  # noqa: BLE001 - report to the console
            lines.append(f"?ERROR: {exc}")
            status = "error"

        if status == "end":
            interpreter.running = False

        failed = status == "error" or any(
            text.startswith("?") and not text.startswith("?HINT") for text in lines
        )
        frame = entry.canvas.frame(force=True) if entry.canvas.has_drawing else None
        reply = {
            "session": entry.key,
            "language": entry.language,
            "output": lines,
            "status": status,
            "exit": 1 if failed else 0,
            "canvas": frame,
        }
        if edits["program"] is not None:
            reply["program"] = edits["program"]
        if edits["run"] is not None:
            reply["run"] = edits["run"]
        return reply

    def _trim_sessions(self):
        """Drop idle sessions, then the least recently used ones."""
        now = time.monotonic()
        for key, entry in list(self._sessions.items()):
            if now - entry.last_used > self.session_ttl:
                del self._sessions[key]
        while len(self._sessions) > self.max_sessions:
            oldest = min(self._sessions, key=lambda key: self._sessions[key].last_used)
            del self._sessions[oldest]

    # ---- run control --------------------------------------------------

    def stop(self, run_id):
        """Stop a running program; returns False when it is not running."""
        with self._lock:
            active = self._runs.get(str(run_id or ""))
        if active is None:
            return False
        active.stop()
        return True

    def send_input(self, run_id, text):
        """Queue one line of input for a running program.

        Built-in languages read it at their next INPUT; Python, JavaScript,
        Perl and plugin languages receive it on stdin.  Returns whether the
        program was waiting for it.
        """
        if not isinstance(text, str):
            raise BadRequest("'text' must be text")
        if len(text.encode("utf-8", "replace")) > MAX_REPL_LINE:
            raise BadRequest("input is too long", status=413)
        with self._lock:
            active = self._runs.get(str(run_id or ""))
        if active is None:
            raise BadRequest("that program is no longer running", status=404)
        active.interpreter.input_buffer.append(text.rstrip("\r\n"))
        return active.waiting_for_input

    # ---- execution ----------------------------------------------------

    def run(self, language, program, emit=None, emit_frame=None, run_id=None,
            on_input=None, keepalive=None):
        """Run *program* and return a result summary.

        Each console line is passed to *emit* as it is produced, which is what
        makes the browser output stream.  *emit_frame* receives run-length
        encoded canvas frames while a turtle program draws.  *on_input* is
        told the prompt whenever the program waits for a line of input (which
        arrives through :meth:`send_input`), and *keepalive* is called while
        it waits.  Waiting for input does not count against the time limit.
        """
        if not isinstance(program, str):
            raise BadRequest("'program' must be text")
        if len(program.encode("utf-8", "replace")) > MAX_PROGRAM_BYTES:
            raise BadRequest("program is too large", status=413)

        resolved = self._known_language(language)
        if resolved is None:
            raise BadRequest(f"unknown language: {language}")

        run_id = str(run_id or uuid.uuid4().hex)[:MAX_RUN_ID]
        with self._lock:
            if run_id in self._runs:
                raise BadRequest("a run with that id is already active", status=409)

        lines = []
        raw_sink = emit or lines.append
        produced = {"lines": 0, "capped": False}

        def sink(text):
            if produced["capped"]:
                return
            produced["lines"] += 1
            if produced["lines"] > MAX_OUTPUT_LINES:
                produced["capped"] = True
                raw_sink(f"Stopped: output limit of {MAX_OUTPUT_LINES} lines reached")
                if active is not None:
                    active.interpreter.stop_program()
                return
            raw_sink(text)

        if not self._slots.acquire(blocking=False):
            raise BadRequest("too many programs are running, try again", status=429)
        started = time.monotonic()
        paused = {"seconds": 0.0}
        timed_out = {"value": False}
        canvas = RasterCanvas(
            DEFAULT_WIDTH, DEFAULT_HEIGHT, on_change=emit_frame
        )
        final_canvas = None
        active = None
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                # The constructor announces itself; that belongs to the IDE,
                # not to a long-running server's log.
                interpreter = Time_WarpInterpreter()
            interpreter.console_banner = False
            interpreter.turtle_console = False
            interpreter.max_iterations = DEFAULT_ITERATIONS
            interpreter.plugins = self.plugins
            interpreter.input_buffer = []

            active = _ActiveRun(run_id, interpreter)
            with self._lock:
                self._runs[run_id] = active

            def pump():
                elapsed = time.monotonic() - started - paused["seconds"]
                if elapsed > self.timeout:
                    if not timed_out["value"]:
                        timed_out["value"] = True
                        sink(f"Stopped: time limit of {self.timeout:g}s reached")
                    interpreter.stop_program()

            def provide_input(prompt=""):
                waited_from = time.monotonic()
                last_ping = waited_from
                active.waiting_for_input = True
                try:
                    if on_input is not None:
                        on_input(str(prompt or ""))
                    while not interpreter.input_buffer:
                        if interpreter.stop_requested:
                            return None
                        now = time.monotonic()
                        if now - waited_from > self.input_timeout:
                            sink(f"Stopped: no input for {self.input_timeout:g}s")
                            return None
                        if keepalive is not None and now - last_ping >= KEEPALIVE_INTERVAL:
                            last_ping = now
                            keepalive()
                        time.sleep(0.02)
                    value = interpreter.input_buffer.pop(0)
                    sink(value)
                    return value
                finally:
                    active.waiting_for_input = False
                    paused["seconds"] += time.monotonic() - waited_from

            interpreter.pump_callback = pump
            interpreter.input_provider = provide_input
            interpreter.log_output = lambda text: sink(str(text))
            interpreter.ide_turtle_canvas = canvas
            interpreter.run_program(program, language=resolved)
            errors = len(interpreter.error_history)
            if canvas.has_drawing:
                final_canvas = canvas.frame(force=True)
                if emit_frame is not None and final_canvas is not None:
                    emit_frame(final_canvas)
        except Exception as exc:  # noqa: BLE001 - report, never drop the client
            sink(f"?ERROR: {exc}")
            errors = 1
        finally:
            with self._lock:
                self._runs.pop(run_id, None)
            self._slots.release()

        stopped = bool(active and active.stopped)
        capped = produced["capped"]
        return {
            "run": run_id,
            "language": resolved,
            "output": lines,
            "errors": errors,
            "timed_out": timed_out["value"],
            "stopped": stopped,
            "output_capped": capped,
            "seconds": round(time.monotonic() - started, 3),
            "exit": 1 if (errors or timed_out["value"] or stopped or capped) else 0,
            "canvas": final_canvas,
        }


class _Handler(BaseHTTPRequestHandler):
    """Routes the browser and the JSON API to a :class:`RunnerService`."""

    server_version = f"TimeWarpClassic/{__version__}"
    protocol_version = "HTTP/1.0"

    @property
    def service(self):
        return self.server.service

    def log_message(self, fmt, *args):  # noqa: A003 - quiet by default
        if getattr(self.server, "verbose", False):
            super().log_message(fmt, *args)

    # ---- responses ----------------------------------------------------

    def _send(self, status, body, content_type="application/json", extra=None):
        payload = body if isinstance(body, bytes) else str(body).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(payload)

    def _json(self, status, data):
        self._send(status, json.dumps(data), "application/json")

    def _error(self, status, message):
        self._json(status, {"error": message})

    # ---- routes -------------------------------------------------------

    def do_GET(self):  # noqa: N802 - BaseHTTPRequestHandler API
        path = urlparse(self.path).path
        try:
            if path in ("/", "/index.html"):
                return self._serve_index()
            if path == "/healthz":
                return self._json(200, {"status": "ok"})
            if path == "/api/languages":
                return self._json(200, {"languages": self.service.languages()})
            if path == "/api/examples":
                return self._json(200, {"examples": self.service.examples()})
            if path.startswith("/api/examples/"):
                relative = path[len("/api/examples/"):]
                source = self.service.example_source(relative)
                return self._json(200, {"path": relative, "source": source})
            if path == "/favicon.ico":
                return self._send(204, b"", "image/x-icon")
            return self._error(404, f"no route for {path}")
        except BadRequest as exc:
            return self._error(exc.status, str(exc))
        except Exception as exc:  # noqa: BLE001
            return self._error(500, str(exc))

    def do_POST(self):  # noqa: N802 - BaseHTTPRequestHandler API
        path = urlparse(self.path).path
        if path not in ("/api/run", "/api/repl", "/api/highlight",
                        "/api/stop", "/api/input"):
            return self._error(404, f"no route for {path}")

        try:
            request = self._read_request()
            language = request.get("language")

            if path == "/api/highlight":
                program = request.get("program", "")
                if not isinstance(program, str):
                    raise BadRequest("'program' must be text")
                if len(program.encode("utf-8", "replace")) > MAX_PROGRAM_BYTES:
                    raise BadRequest("program is too large", status=413)
                spec = self.service.plugins.get(language) if language else None
                html_text = highlight_source(
                    language, program, alias=spec.syntax if spec else None
                )
                return self._json(200, {"html": html_text})

            if path == "/api/repl":
                result = self.service.repl(
                    request.get("session"), language, request.get("line", ""),
                    program=request.get("program"),
                )
                return self._json(200, result)

            if path == "/api/stop":
                stopped = self.service.stop(request.get("run"))
                return self._json(200, {"stopped": stopped})

            if path == "/api/input":
                waiting = self.service.send_input(
                    request.get("run"), request.get("text", "")
                )
                return self._json(200, {"accepted": True, "waiting": waiting})

            program = request.get("program", "")
            run_id = request.get("run")
            if run_id is not None and not isinstance(run_id, str):
                raise BadRequest("'run' must be text")
            if "text/event-stream" in (self.headers.get("Accept") or ""):
                self._stream_run(language, program, run_id)
            else:
                self._json(200, self.service.run(language, program, run_id=run_id))
        except BadRequest as exc:
            self._error(exc.status, str(exc))
        except json.JSONDecodeError:
            self._error(400, "request body is not valid JSON")
        except Exception as exc:  # noqa: BLE001
            self._error(500, str(exc))

    def _read_request(self):
        """Read and decode the JSON request body."""
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            raise BadRequest("Content-Length is not a number") from None
        if length < 0:
            raise BadRequest("Content-Length is negative")
        if length > MAX_PROGRAM_BYTES * 2 + 1024:
            raise BadRequest("request is too large", status=413)
        body = self.rfile.read(length) if length else b"{}"
        try:
            text = body.decode("utf-8")
        except UnicodeDecodeError:
            raise BadRequest("request body is not UTF-8") from None
        request = json.loads(text or "{}")
        if not isinstance(request, dict):
            raise BadRequest("expected a JSON object")
        return request

    # ---- helpers ------------------------------------------------------

    def _serve_index(self):
        index = STATIC_DIR / "index.html"
        if not index.is_file():
            raise BadRequest("index.html is missing from the install", status=500)
        self._send(200, index.read_bytes(), "text/html; charset=utf-8")

    def _stream_run(self, language, program, run_id=None):
        """Run the program, streaming each console line as it appears.

        A write that fails means the browser went away (tab closed, Stop
        pressed and the fetch aborted), so the run is stopped instead of
        carrying on for nobody.
        """
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Accel-Buffering", "no")
        self.send_header("Connection", "close")
        self.end_headers()

        run_id = str(run_id or uuid.uuid4().hex)[:MAX_RUN_ID]
        state = {"closed": False}

        def write(text):
            if state["closed"]:
                return
            try:
                self.wfile.write(text.encode("utf-8"))
                self.wfile.flush()
            except OSError:
                state["closed"] = True
                self.service.stop(run_id)

        def event(name, data):
            write(f"event: {name}\ndata: {json.dumps(data)}\n\n")

        def emit(line):
            write(f"data: {json.dumps({'line': line})}\n\n")

        write(f"event: start\ndata: {json.dumps({'run': run_id})}\n\n")
        try:
            result = self.service.run(
                language, program, emit=emit,
                emit_frame=lambda frame: event("canvas", frame),
                run_id=run_id,
                on_input=lambda prompt: event("input", {"prompt": prompt}),
                keepalive=lambda: write(": waiting for input\n\n"),
            )
        except BadRequest as exc:
            event("error", {"error": str(exc), "status": exc.status})
            return

        done = {
            key: value
            for key, value in result.items()
            if key not in ("output", "canvas")
        }
        done["has_canvas"] = result.get("canvas") is not None
        self.wfile.write(
            f"event: done\ndata: {json.dumps(done)}\n\n".encode("utf-8")
        )
        self.wfile.flush()


class TimeWarpWebServer(ThreadingHTTPServer):
    """Threaded server carrying the runner service for the handlers."""

    daemon_threads = True
    allow_reuse_address = True

    def __init__(self, address, service, verbose=False):
        super().__init__(address, _Handler)
        self.service = service
        self.verbose = verbose


def create_server(host=DEFAULT_HOST, port=DEFAULT_PORT, timeout=DEFAULT_TIMEOUT,
                  plugins=None, verbose=False):
    """Build (but do not start) a server; port 0 picks a free port."""
    service = RunnerService(timeout=timeout, plugins=plugins)
    return TimeWarpWebServer((host, port), service, verbose=verbose)


def serve(host=DEFAULT_HOST, port=DEFAULT_PORT, timeout=DEFAULT_TIMEOUT,
          plugins=None, verbose=False):
    """Run the web IDE until interrupted; returns the port that was used."""
    server = create_server(host, port, timeout, plugins, verbose)
    browser_host = "127.0.0.1" if host in ("0.0.0.0", "::") else host
    print(f"Time Warp Classic web IDE: http://{browser_host}:{server.server_port}/")
    print("Press Ctrl+C to stop.")

    def _terminate(_signum, _frame):
        # Docker stops a container with SIGTERM.  A process running as PID 1
        # has no default signal dispositions, so the handler is required for
        # a clean shutdown instead of a ten-second SIGKILL.
        raise KeyboardInterrupt

    try:
        signal.signal(signal.SIGTERM, _terminate)
    except (ValueError, OSError):  # pragma: no cover - not the main thread
        pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping.")
    finally:
        server.server_close()
    return server.server_port
