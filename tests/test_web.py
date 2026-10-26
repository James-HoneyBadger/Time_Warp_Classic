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


def _post(base, payload, accept=None, raw=None):
    headers = {"Content-Type": "application/json"}
    if accept:
        headers["Accept"] = accept
    data = raw if raw is not None else json.dumps(payload).encode()
    request = urllib.request.Request(f"{base}/api/run", data=data, headers=headers)
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


def test_streaming_reports_bad_requests_as_events(base):
    _status, body, _headers = _post(
        base, {"language": "cobol", "program": "x"}, accept="text/event-stream"
    )
    text = body.decode()

    assert "event: error" in text
    assert "unknown language" in text


# --------------------------------------------------------- runner service

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
