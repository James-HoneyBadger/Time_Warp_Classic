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
- **Syntax highlighting** driven by the same Pygments lexers as the desktop
  editor (see below).
- **Graphics pane** showing turtle output (Logo, BASIC turtle commands) as
  run-length encoded pixel frames, with a *Save PNG* button.
- **REPL bar** under the console: type a statement, press Enter, see the
  result immediately. `Up`/`Down` recall earlier lines.

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
| `POST` | `/api/repl` | Runs one statement in a persistent session |
| `POST` | `/api/highlight` | Returns coloured HTML for the editor |

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

## REPL

`POST /api/repl` takes `{"session": "...", "language": "BASIC", "line": "PRINT 2+2"}`.
The server keeps one interpreter per *session* id, so variables survive between
lines:

```
> LET A = 6
> PRINT A * 7
42
```

- The page generates a session id per tab; send your own to script it.
- Changing the language starts a fresh interpreter for that session.
- Turtle commands (`FD 60`, `DRAW`) draw on the session's canvas, and every
  reply carries a full canvas frame when something was drawn.
- Replies are `{"session", "language", "output": [...], "status", "exit", "canvas"}`.
  `exit` is 1 when the statement reported an error.
- Requests are answered with `400` (blank line, unknown language), `413`
  (statement over 8 KB) or `429` (busy).
- A session is capped at 16 per server, expires after 10 idle minutes, and each
  line may run for 2 seconds before it is stopped.

Languages that delegate to another runtime (Python, JavaScript, Perl, plugins)
evaluate each line in a fresh process, so variables do not persist for them.

## Syntax highlighting

`POST /api/highlight` takes `{"language": "Python", "program": "..."}` and
returns `{"html": "<span style=\"color: …\">def</span>…"}`.

- The server renders tokens with Pygments (`web/highlight.py`), emitting inline
  colours and no wrapper element, so the page needs no stylesheet for it.
- The page paints that HTML in a `<pre>` behind the **transparent textarea**,
  which keeps the caret, selection, undo and scrolling native.
- Requests are debounced (180 ms) and stale replies are discarded, so typing
  stays responsive.
- Language labels map to lexers (`basic` uses the Commodore BASIC lexer,
  `pascal`, `prolog`, `forth`, `perl`, `python` and `javascript` have their
  own). PILOT and Logo stay plain; a plugin's `syntax` alias is used.
- Source text is escaped, so a program containing `<script>` can never inject
  markup. Unknown languages, and installs without Pygments, fall back to
  escaped plain text.

## Graphics canvas and RLE frames

Turtle output is rasterised on the server into a palette-indexed pixel buffer
and sent as **run-length encoded** frames, so a 600×400 drawing costs a few
hundred bytes per update instead of 240 000 pixels.

With a plain request the final frame is in `result.canvas`. While streaming,
each update arrives as an SSE event:

```
event: canvas
data: {"type": "canvas", "width": 600, "height": 400,
       "x": 296, "y": 196, "w": 12, "h": 10,
       "palette": ["#ffffff", "black"],
       "rle": "CgAAAAoAAAA...", "overlay": [...]}
```

| Field | Meaning |
|-------|---------|
| `width`, `height` | Full canvas size |
| `x`, `y`, `w`, `h` | Rectangle this frame updates (only what changed) |
| `palette` | CSS colours; index 0 is the background |
| `rle` | base64 of repeated *(uint16 little-endian run, uint8 palette index)* |
| `overlay` | Small vector list (turtle marker, tagged shapes, text) drawn on top |

The browser keeps a full-size `ImageData`, paints only the rectangle it is
given, then draws the overlay. The turtle marker and text stay vector so they
remain crisp and can move without repainting the pixels. Decoding is
implemented in `web/canvas.py` (`decode_rle`) as well, which is what the tests
use.

## Limits

- Programs are capped at 256 KB.
- Four programs may run concurrently; further requests wait for a free slot and
  are refused with `429` rather than queued forever.
- Each run is stopped by the wall clock (default 10 s). A 50-million-iteration
  cap is a backstop in case a loop somehow outruns the clock check.
- Every run gets a fresh interpreter, so programs cannot see each other's
  variables; REPL sessions deliberately keep theirs.
- REPL statements are capped at 8 KB, 2 seconds and 16 concurrent sessions.

## Container

Every `vX.Y.Z` tag publishes a prebuilt image for `linux/amd64` and
`linux/arm64`:

```bash
docker run --rm -p 8000:8000 ghcr.io/james-honeybadger/time-warp-classic-web:latest
```

Or build it yourself:

```bash
docker build -f Dockerfile.web -t timewarp-web .
docker run --rm -p 8000:8000 timewarp-web
```

The image contains the built-in interpreters plus Pygments for syntax
highlighting. JavaScript needs Node.js, Perl
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
