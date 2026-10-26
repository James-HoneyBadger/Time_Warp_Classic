# Web IDE

The same interpreter that powers the desktop IDE is available in a browser. A
small standard-library HTTP server exposes it, so there is nothing to install
beyond Python itself.

```bash
python Time_Warp.py --web            # http://127.0.0.1:8000/
python Time_Warp.py --web --port 0   # pick a free port
```

From the desktop IDE: **Program → Open Web IDE** starts the server on a free
port, prints the URL in the console and opens the page.

## Options

| Flag | Default | Meaning |
|------|---------|---------|
| `--web` | off | Serve the browser UI instead of opening a window |
| `--host` | `127.0.0.1` | Bind address; `0.0.0.0` for containers |
| `--port` | `8000` | Port, `0` picks a free one |
| `--timeout` | `10` | Seconds a single run may last before it is stopped |

## The page

- Language selector covering the nine built-ins and any loaded plugins.
- Editor with a line-number gutter, `Ctrl+Enter` to run, `Tab` for indentation.
- Console that streams output line by line while the program runs, with error
  lines in red and the elapsed time in the status bar.
- Example picker that loads the programs from `examples/`.

`READY.`, `Interpreter ready.` and turtle chatter are IDE chrome and are not
shown; program output and `?ERROR IN n` lines are.

## HTTP API

Everything the page does is a plain JSON call, which makes the server easy to
script.

| Method | Path | Returns |
|--------|------|---------|
| `GET` | `/` | The editor page |
| `GET` | `/healthz` | `{"status": "ok"}` |
| `GET` | `/api/languages` | `{"languages": [{"name", "key", "extension"}]}` |
| `GET` | `/api/examples` | `{"examples": [{"name", "language", "path"}]}` |
| `GET` | `/api/examples/<path>` | `{"path", "source"}` |
| `POST` | `/api/run` | Result object, or an event stream (see below) |

`POST /api/run` takes `{"language": "BASIC", "program": "10 PRINT 1"}`.
Language names are case-insensitive. With `Accept: application/json` (the
default) the reply is:

```json
{"language": "BASIC", "output": ["1"], "errors": 0,
 "timed_out": false, "seconds": 0.012, "exit": 0}
```

With `Accept: text/event-stream` the reply is a stream of frames:

```
data: {"line": "1"}

event: done
data: {"language": "BASIC", "errors": 0, "timed_out": false, "seconds": 0.012, "exit": 0}
```

Invalid input is answered with `400` (`unknown language`, malformed JSON), `413`
(program over 256 KB) or `429` (more than four runs at once). A run that
exceeds the time limit stops itself and reports `timed_out: true`.

## Limits

- Programs are capped at 256 KB.
- Four programs may run concurrently; further requests wait for a free slot and
  are refused with `429` rather than queued forever.
- Each run is stopped by the wall clock (default 10 s). A 50-million-iteration
  cap is a backstop in case a loop somehow outruns the clock check.
- Every run gets a fresh interpreter, so programs cannot see each other's
  variables.

## Container

```bash
docker build -f Dockerfile.web -t timewarp-web .
docker run --rm -p 8000:8000 timewarp-web
```

The image contains the built-in interpreters. JavaScript needs Node.js, Perl
needs Perl, and plugin languages need their runtime — uncomment the `apt-get`
line in the Dockerfile or extend the image. `HEALTHCHECK` uses `/healthz`.

Set `TIMEWARP_PLUGIN_PATH` to a mounted folder to expose plugin languages.

## Security

The server runs arbitrary programs on behalf of whoever can reach it, and it
has **no authentication**.

- The default `--host 127.0.0.1` keeps it local to your machine.
- Only bind `0.0.0.0` inside a network you control, ideally behind a proxy that
  adds authentication and rate limiting.
- The built-in interpreters are sandboxed by design (no file or network access
  from the expression evaluator), but **Python, JavaScript and Perl run real
  subprocesses** and can do anything the user of the container can do. Do not
  expose those languages to untrusted users.

## Not included

The web edition focuses on write → run → read output. There is no file
open/save, no turtle canvas, no breakpoints or single-stepping, and no
debugger; use the desktop IDE for those.
