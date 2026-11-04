"""Tests for the web front-end: routes, streaming and the runner service.

The server runs in a background thread on a free port, so these stay headless
and need no browser.
"""

import json
import os
import threading
import time
import urllib.error
import urllib.request

import pytest

from core.plugins import PluginRegistry
from web.server import BadRequest, RunnerService, create_server


@pytest.fixture(scope="module")
def server():
    srv = create_server(port=0, timeout=2.0)
    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    yield srv
    srv.shutdown()
    srv.server_close()


@pytest.fixture
def base(server):
    return f"http://127.0.0.1:{server.server_port}"


def _get(base, path):
    with urllib.request.urlopen(f"{base}{path}", timeout=20) as response:
        return response.status, response.read()


def _json_get(base, path):
    status, body = _get(base, path)
    return status, json.loads(body)


def _post(base, payload, accept=None, raw=None, path="/api/run"):
    headers = {"Content-Type": "application/json"}
    if accept:
        headers["Accept"] = accept
    data = raw if raw is not None else json.dumps(payload).encode()
    request = urllib.request.Request(f"{base}{path}", data=data, headers=headers)
    with urllib.request.urlopen(request, timeout=40) as response:
        return response.status, response.read(), response.headers


def _run(base, language, program):
    _status, body, _headers = _post(base, {"language": language, "program": program})
    return json.loads(body)


# ------------------------------------------------------------------- routes

def test_index_is_served(base):
    status, body = _get(base, "/")

    assert status == 200
    assert b"TIME WARP CLASSIC" in body
    assert b'id="code"' in body


def test_health_endpoint(base):
    assert _json_get(base, "/healthz") == (200, {"status": "ok"})


def test_languages_endpoint_lists_every_language(base):
    _status, data = _json_get(base, "/api/languages")
    names = [entry["name"] for entry in data["languages"]]

    assert names[:9] == [
        "PILOT", "BASIC", "Logo", "Pascal", "Prolog",
        "Forth", "Perl", "Python", "JavaScript",
    ]
    basic = next(entry for entry in data["languages"] if entry["name"] == "BASIC")
    assert basic == {
        "name": "BASIC", "key": "basic", "extension": ".bas", "available": True,
    }
    assert all(isinstance(entry["available"], bool) for entry in data["languages"])


def test_examples_are_listed_and_loadable(base):
    _status, data = _json_get(base, "/api/examples")
    examples = data["examples"]

    assert examples
    assert all(example["language"] for example in examples)

    _status, source = _json_get(base, "/api/examples/" + examples[0]["path"])
    assert source["source"].strip()


def test_example_path_traversal_is_refused(base):
    with pytest.raises(urllib.error.HTTPError) as error:
        _get(base, "/api/examples/../../etc/passwd")

    assert error.value.code == 404


def test_unknown_route_is_404(base):
    with pytest.raises(urllib.error.HTTPError) as error:
        _get(base, "/api/nope")

    assert error.value.code == 404


# ---------------------------------------------------------------- running

def test_run_returns_output_and_exit_code(base):
    result = _run(base, "BASIC", '10 PRINT "WEB"\n20 PRINT 6 * 7\n')

    assert result["output"] == ["WEB", "42"]
    assert result["exit"] == 0
    assert result["language"] == "BASIC"


def test_language_names_are_case_insensitive(base):
    assert _run(base, "basic", '10 PRINT "ok"')["exit"] == 0


def test_program_errors_set_the_exit_code(base):
    result = _run(base, "BASIC", '\n10 PRINT 1/0\n')

    assert result["exit"] == 1
    assert any("?ERROR IN 2" in line for line in result["output"])


def test_unknown_language_is_rejected(base):
    with pytest.raises(urllib.error.HTTPError) as error:
        _post(base, {"language": "cobol", "program": "x"})

    assert error.value.code == 400
    assert b"unknown language" in error.value.read()


def test_malformed_json_is_rejected(base):
    with pytest.raises(urllib.error.HTTPError) as error:
        _post(base, None, raw=b"{not json")

    assert error.value.code == 400


def test_oversized_program_is_rejected(base):
    with pytest.raises(urllib.error.HTTPError) as error:
        _post(base, {"language": "basic", "program": "x" * (300 * 1024)})

    assert error.value.code == 413


def test_turtle_chatter_is_not_streamed(base):
    result = _run(base, "logo", "PRINT [quiet]\nFD 20\nRIGHT 90\nFD 10")

    assert result["output"] == ["quiet"]


def test_runaway_program_stops_on_the_time_limit(server, base):
    started = time.monotonic()
    result = _run(base, "BASIC", "10 GOTO 10")
    elapsed = time.monotonic() - started

    assert result["timed_out"] is True
    assert result["exit"] == 1
    assert elapsed < 15
    assert any("time limit" in line for line in result["output"])


# --------------------------------------------------------------- streaming

def test_streaming_run_uses_server_sent_events(base):
    _status, body, headers = _post(
        base,
        {"language": "BASIC", "program": '10 PRINT "one"\n20 PRINT "two"'},
        accept="text/event-stream",
    )
    text = body.decode()

    assert headers["Content-Type"].startswith("text/event-stream")
    frames = [
        json.loads(line[6:]) for line in text.splitlines() if line.startswith("data: ")
    ]
    lines = [frame["line"] for frame in frames if "line" in frame]
    done = frames[-1]

    assert text.startswith("event: start")
    assert frames[0]["run"]
    assert lines == ["one", "two"]
    assert done["exit"] == 0
    assert done["run"] == frames[0]["run"]
    assert "event: done" in text


def test_streaming_draws_send_rle_canvas_frames(base):
    """A turtle program streams canvas frames next to its output."""
    _status, body, _headers = _post(
        base,
        {"language": "Logo", "program": "FD 50\nRT 90\nFD 50"},
        accept="text/event-stream",
    )
    blocks = [block for block in body.decode().split("\n\n") if block.strip()]
    canvas_frames = [
        json.loads(block.split("data: ", 1)[1])
        for block in blocks
        if "event: canvas" in block
    ]

    assert canvas_frames, "no canvas frames were streamed"
    assert canvas_frames[-1]["width"] == 600
    assert all(frame["palette"] for frame in canvas_frames)
    assert any(frame["w"] > 0 for frame in canvas_frames)
    assert any('"has_canvas": true' in block for block in blocks)


def test_streaming_reports_bad_requests_as_events(base):
    _status, body, _headers = _post(
        base, {"language": "cobol", "program": "x"}, accept="text/event-stream"
    )
    text = body.decode()

    assert "event: error" in text
    assert "unknown language" in text


# --------------------------------------------------------- runner service

def test_service_run_does_not_write_to_stdout(capsys):
    """A run's output belongs to the response, not the server log."""
    RunnerService().run("BASIC", '10 PRINT "quiet"')

    assert capsys.readouterr().out == ""


def test_service_output_limit_is_configurable():
    """A small max_output_lines stops a chatty program and reports it."""
    service = RunnerService(max_output_lines=3)
    result = service.run("BASIC", "10 FOR I = 1 TO 10\n20 PRINT I\n30 NEXT I")

    assert result["output_capped"] is True
    assert result["exit"] == 1
    assert any("output limit of 3 lines" in line for line in result["output"])
    assert len(result["output"]) == 4  # three lines plus the stop notice


def test_service_breakpoints_stop_at_the_given_line():
    """A breakpoint (editor line number) stops the run and reports it."""
    service = RunnerService()
    result = service.run(
        "BASIC", "10 FOR I = 1 TO 5\n20 PRINT I\n30 NEXT I", breakpoints=[2]
    )

    assert result["interrupted"] is True
    assert result["exit"] == 1
    assert any("BREAK IN 2" in line for line in result["output"])


def test_service_pause_step_and_resume():
    """Pause freezes a run, step lets one line through, resume finishes it."""
    import threading

    service = RunnerService(max_output_lines=1_000_000)
    lines = []
    done = {}

    def target():
        done.update(service.run(
            "BASIC",
            "10 FOR I = 1 TO 100000\n20 PRINT I\n30 NEXT I",
            emit=lines.append,
            run_id="pausetest",
        ))

    thread = threading.Thread(target=target)
    thread.start()
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline and len(lines) < 10:
        time.sleep(0.01)
    assert len(lines) >= 10, lines

    service.pause("pausetest")
    time.sleep(0.3)
    count = len(lines)
    time.sleep(0.3)
    assert len(lines) == count, "program kept running while paused"

    for _ in range(10):
        service.step("pausetest")
        time.sleep(0.05)
        if len(lines) > count:
            break
    assert len(lines) > count, "step produced no output"

    service.resume("pausetest")
    thread.join(timeout=15)
    assert not thread.is_alive(), "program did not finish after resume"
    assert done["exit"] == 0


def test_service_rejects_blank_language():
    service = RunnerService()

    with pytest.raises(BadRequest):
        service.run("", "10 PRINT 1")


def test_service_refuses_more_than_four_concurrent_runs():
    service = RunnerService()
    for _ in range(4):
        service._slots.acquire()
    try:
        with pytest.raises(BadRequest) as error:
            service.run("BASIC", "10 PRINT 1")
        assert error.value.status == 429
    finally:
        for _ in range(4):
            service._slots.release()


def test_service_lists_plugin_languages(tmp_path):
    import sys

    (tmp_path / "tiny.json").write_text(
        json.dumps(
            {"name": "TinyPython", "executable": sys.executable, "extension": ".tpy"}
        ),
        encoding="utf-8",
    )
    service = RunnerService(plugins=PluginRegistry.load([tmp_path]))

    names = [entry["name"] for entry in service.languages()]
    assert "TinyPython" in names
    assert "BASIC" in names


def test_service_runs_a_plugin_language(tmp_path):
    import sys

    (tmp_path / "tiny.json").write_text(
        json.dumps(
            {
                "name": "TinyPython",
                "executable": sys.executable,
                "extension": ".tpy",
                "args": ["-u"],
            }
        ),
        encoding="utf-8",
    )
    service = RunnerService(plugins=PluginRegistry.load([tmp_path]))

    result = service.run("TinyPython", 'print("plugin in the browser")')

    assert "plugin in the browser" in result["output"]
    assert result["exit"] == 0

    # Each run has its own interpreter; output must not go to the first one.
    second = service.run("TinyPython", 'print("second run")')
    assert "second run" in second["output"]


# --------------------------------------------------------------- drafts

def test_service_saves_and_lists_drafts(tmp_path):
    service = RunnerService(drafts_dir=tmp_path / "drafts")

    service.save_draft("hello", "BASIC", '10 PRINT "HI"')

    names = [entry["name"] for entry in service.drafts()]
    assert names == ["hello"]
    source = service.draft_source("hello")
    assert source["language"] == "BASIC"
    assert source["program"] == '10 PRINT "HI"'


def test_service_deletes_drafts(tmp_path):
    service = RunnerService(drafts_dir=tmp_path / "drafts")
    service.save_draft("temp", "Logo", "FD 10")

    assert service.delete_draft("temp") is True
    assert service.delete_draft("temp") is False
    assert service.drafts() == []


def test_service_rejects_unsafe_draft_names(tmp_path):
    service = RunnerService(drafts_dir=tmp_path / "drafts")

    with pytest.raises(BadRequest):
        service.save_draft("../escape", "BASIC", "10 PRINT 1")
    with pytest.raises(BadRequest):
        service.draft_source("a/b")


# ------------------------------------------------------------------- REPL

def _repl(base, session, language, line):
    """POST one REPL line and return the decoded result."""
    status, body, _headers = _post(
        base,
        {"session": session, "language": language, "line": line},
        path="/api/repl",
    )
    return status, json.loads(body)


def test_repl_evaluates_a_statement(base):
    status, result = _repl(base, "a", "BASIC", "PRINT 2+2")

    assert status == 200
    assert result["output"] == ["4"]
    assert result["exit"] == 0


def test_repl_keeps_variables_between_lines(base):
    _repl(base, "keep", "BASIC", "LET A = 6")
    _status, result = _repl(base, "keep", "BASIC", "PRINT A * 7")

    assert result["output"] == ["42"]


def test_repl_sessions_are_isolated(base):
    _repl(base, "one", "BASIC", "LET A = 99")
    _status, result = _repl(base, "two", "BASIC", "PRINT A")

    # A fresh session has no A, so BASIC prints the name itself.
    assert result["output"] == ["A"]


def test_repl_reports_errors(base):
    _status, result = _repl(base, "errors", "BASIC", "PRINT 1/0")

    assert result["exit"] == 1
    assert any("Division by zero" in line for line in result["output"])


def test_repl_rejects_a_blank_line(base):
    with pytest.raises(urllib.error.HTTPError) as error:
        _repl(base, "a", "BASIC", "   ")

    assert error.value.code == 400


def test_repl_rejects_an_unknown_language(base):
    with pytest.raises(urllib.error.HTTPError) as error:
        _repl(base, "a", "cobol", "x")

    assert error.value.code == 400


def test_repl_turtle_line_returns_a_canvas(base):
    _status, result = _repl(base, "draw", "Logo", "FD 60")

    assert result["canvas"] is not None
    assert result["canvas"]["w"] > 0


def test_repl_switches_language_and_starts_over(server):
    service = server.service
    service.repl("switch", "BASIC", "LET A = 5")
    result = service.repl("switch", "Logo", "PRINT 1")

    assert result["language"] == "Logo"
    assert result["session"] == "switch"


def test_repl_sessions_are_capped():
    service = RunnerService(max_sessions=2)
    service.repl("one", "BASIC", "LET A = 1")
    service.repl("two", "BASIC", "LET A = 2")
    service.repl("three", "BASIC", "LET A = 3")

    assert len(service._sessions) == 2
    assert "one" not in service._sessions


def test_repl_stops_a_runaway_statement():
    service = RunnerService(repl_timeout=0.5)
    started = time.monotonic()
    result = service.repl("loop", "BASIC", "10 GOTO 10")
    elapsed = time.monotonic() - started

    assert elapsed < 10
    assert result["status"] in ("continue", "end", "error")


def test_server_stops_on_sigterm(tmp_path):
    """``docker stop`` sends SIGTERM; the server must exit cleanly."""
    import subprocess
    import sys
    from pathlib import Path

    entry = Path(__file__).resolve().parent.parent / "Time_Warp.py"
    environment = dict(os.environ, PYTHONUNBUFFERED="1")
    process = subprocess.Popen(
        [sys.executable, str(entry), "--web", "--port", "0"],
        cwd=str(entry.parent),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=environment,
    )
    try:
        # Optional-dependency notices (no Pillow, ...) may come first.
        banner = ""
        for _ in range(5):
            banner = process.stdout.readline()
            if "web IDE" in banner or not banner:
                break
        assert "web IDE" in banner, banner
        started = time.monotonic()
        process.terminate()  # SIGTERM
        assert process.wait(timeout=10) == 0
        assert time.monotonic() - started < 8
    finally:
        if process.poll() is None:
            process.kill()


# -------------------------------------------------------------- highlight

def _highlight(base, language, program):
    status, body, _headers = _post(
        base,
        {"language": language, "program": program},
        path="/api/highlight",
    )
    return status, json.loads(body)


def test_highlight_endpoint_returns_coloured_html(base):
    status, result = _highlight(base, "Python", "def f():\n    return 1\n")

    assert status == 200
    assert "<span" in result["html"]


def test_highlight_endpoint_escapes_markup(base):
    _status, result = _highlight(base, "Python", "x = '<script>'")

    assert "<script>" not in result["html"]
    assert "&lt;script&gt;" in result["html"]


def test_highlight_endpoint_accepts_unknown_languages(base):
    status, result = _highlight(base, "Cobol", 'DISPLAY "HI".')

    assert status == 200
    assert "DISPLAY" in result["html"]


def test_highlight_endpoint_rejects_huge_programs(base):
    with pytest.raises(urllib.error.HTTPError) as error:
        _highlight(base, "Python", "x" * (300 * 1024))

    assert error.value.code == 413


def test_examples_exclude_package_files(base):
    """Only programs in a language folder are offered as examples."""
    _status, data = _json_get(base, "/api/examples")
    paths = [entry["path"] for entry in data["examples"]]

    assert paths
    assert all("/" in path for path in paths)
    assert not any(path.endswith("__init__.py") for path in paths)


# ------------------------------------------------------ input and stopping

def _answer(service, run_id, values):
    """Feed *values* to a run as soon as it is registered."""
    def feed():
        for value in values:
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                try:
                    service.send_input(run_id, value)
                    break
                except BadRequest:
                    time.sleep(0.02)
    thread = threading.Thread(target=feed, daemon=True)
    thread.start()
    return thread


@pytest.mark.parametrize(
    "language, program, answer, expected",
    [
        ("BASIC", '10 INPUT "NAME"; N$\n20 PRINT "HI "; N$', "ADA", "HI ADA"),
        ("Pascal",
         "program t;\nvar a: integer;\nbegin\nreadln(a);\nwriteln(a*2);\nend.",
         "21", "42"),
    ],
)
def test_input_reaches_a_running_program(language, program, answer, expected):
    service = RunnerService(timeout=5)
    prompts = []
    feeder = _answer(service, "in-1", [answer])

    result = service.run(language, program, run_id="in-1", on_input=prompts.append)
    feeder.join(5)

    assert prompts, "the program never asked for input"
    assert answer in result["output"]
    assert expected in result["output"]
    assert result["exit"] == 0


def test_input_reaches_a_subprocess_program_on_stdin():
    import sys

    if sys.platform.startswith("win"):
        pytest.skip("stdin streaming is exercised on POSIX")
    service = RunnerService(timeout=10)
    feeder = _answer(service, "py-1", ["grace"])

    result = service.run(
        "Python", 'name = input()\nprint("hi", name)\n', run_id="py-1"
    )
    feeder.join(5)

    assert "hi grace" in result["output"]


def test_waiting_for_input_does_not_use_the_time_limit():
    service = RunnerService(timeout=0.5)
    timer = threading.Timer(1.0, service.send_input, args=("slow", "7"))
    timer.start()

    result = service.run("BASIC", "10 INPUT A\n20 PRINT A*6", run_id="slow")

    assert result["timed_out"] is False
    assert "42" in result["output"]


def test_input_never_reads_the_server_stdin(monkeypatch):
    def refuse(*_args):
        raise AssertionError("input() was called on the server")

    monkeypatch.setattr("builtins.input", refuse)
    service = RunnerService(timeout=1, input_timeout=0.3)

    result = service.run("PILOT", "A:\nT:after", run_id="pilot-1")

    assert any("no input" in line for line in result["output"])


def test_a_running_program_can_be_stopped():
    service = RunnerService(timeout=10)
    threading.Timer(0.3, service.stop, args=("loop-1",)).start()
    started = time.monotonic()

    result = service.run("BASIC", "10 LET X = X + 1\n20 GOTO 10", run_id="loop-1")

    assert time.monotonic() - started < 5
    assert result["stopped"] is True
    assert result["exit"] == 1
    assert any(line.startswith("BREAK") for line in result["output"])


def test_stop_and_input_for_unknown_runs(base):
    status, body, _headers = _post(base, {"run": "nope"}, path="/api/stop")
    assert status == 200
    assert json.loads(body) == {"stopped": False}

    with pytest.raises(urllib.error.HTTPError) as error:
        _post(base, {"run": "nope", "text": "x"}, path="/api/input")
    assert error.value.code == 404


def test_stop_endpoint_interrupts_a_streaming_run(base):
    result = {}

    def runner():
        _status, body, _headers = _post(
            base,
            {"language": "BASIC", "program": "10 GOTO 10", "run": "http-stop"},
            accept="text/event-stream",
        )
        result["text"] = body.decode()

    thread = threading.Thread(target=runner)
    thread.start()
    time.sleep(0.4)
    _post(base, {"run": "http-stop"}, path="/api/stop")
    thread.join(10)

    assert '"stopped": true' in result["text"]


def test_output_flood_is_capped():
    service = RunnerService(timeout=10, max_output_lines=50)

    result = service.run("BASIC", '10 PRINT "X"\n20 GOTO 10')

    assert len(result["output"]) == 51
    assert result["output_capped"] is True
    assert "output limit" in result["output"][-1]


def test_turtle_chatter_is_quiet_for_logo_basic_and_pilot():
    service = RunnerService()

    assert service.run("Logo", "PU HOME PD SETPENCOLOR [1 2 3] HT\nFD 10")["output"] == []
    assert service.run("BASIC", "10 PENUP\n20 PENDOWN")["output"] == []
    assert service.run("PILOT", "G:PENUP\nG:COLOR,red")["output"] == []


# ------------------------------------------------------- BASIC direct mode

def test_repl_basic_numbered_line_edits_the_program():
    service = RunnerService()

    result = service.repl("d1", "BASIC", '10 PRINT "A"', program='20 PRINT "B"\n')

    assert result["output"] == ["OK"]
    assert result["program"] == '10 PRINT "A"\n20 PRINT "B"\n'


def test_repl_basic_list_and_run_use_the_editor_program():
    service = RunnerService()
    program = "20 PRINT 2\n10 PRINT 1\n"

    listed = service.repl("d2", "BASIC", "LIST", program=program)
    ran = service.repl("d2", "BASIC", "RUN", program=program)

    assert listed["output"] == ["10 PRINT 1", "20 PRINT 2"]
    assert ran["run"] == "10 PRINT 1\n20 PRINT 2\n"


def test_repl_input_is_refused_instead_of_reading_stdin(monkeypatch):
    def refuse(*_args):
        raise AssertionError("input() was called on the server")

    monkeypatch.setattr("builtins.input", refuse)
    service = RunnerService()

    result = service.repl("d3", "BASIC", "INPUT A")
    after = service.repl("d3", "BASIC", "PRINT 2+2")

    assert any("needs a running program" in line for line in result["output"])
    assert after["output"] == ["4"]

