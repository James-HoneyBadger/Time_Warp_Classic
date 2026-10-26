"""Tests for the web front-end: routes, streaming and the runner service.

The server runs in a background thread on a free port, so these stay headless
and need no browser.
"""

import json
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
    assert basic == {"name": "BASIC", "key": "basic", "extension": ".bas"}


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
    frames = [line[6:] for line in text.splitlines() if line.startswith("data: ")]
    lines = [json.loads(frame)["line"] for frame in frames[:-1]]
    done = json.loads(frames[-1])

    assert lines == ["one", "two"]
    assert done["exit"] == 0
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
