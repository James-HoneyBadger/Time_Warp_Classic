# Web IDE

`--web` serves the Studio, a single-page editor, from a small HTTP server built
only on the standard library. It uses the same interpreters as the desktop IDE.
You can use it on a machine without Tk, in a container, or from a tablet on
your LAN.

```bash
python3 Time_Warp.py --web              # http://127.0.0.1:8000/
python3 Time_Warp.py --web --port 0     # pick a free port
python3 Time_Warp.py --web --timeout 30 # allow longer runs
```

From the desktop IDE, **Program → Open Web IDE** starts a server on a free port,
prints the URL in the console and opens your browser.

## Options

| Flag | Default | Meaning |
|------|---------|---------|
| `--web` | off | Serve the browser UI instead of opening a window |
| `--host` | `127.0.0.1` | Bind address; use `0.0.0.0` in a container |
| `--port` | `8000` | Port; `0` picks a free one |
| `--timeout` | `10` | Seconds of CPU-side run time before a program is stopped |

## Using the page

| Area | What it does |
|------|--------------|
| Header | Language picker, **Run**, **Stop**, **Examples…**, **Open…**, **Save**, and a status line showing elapsed time and the outcome |
| Program | Editor with a line-number gutter and Pygments highlighting. `Tab` indents and can be undone. |
| Console | Streams output as it is produced. Errors are red and `?HINT:` lines are styled as suggestions. **Clear** empties it. |
| Console bar | REPL when idle; the program's stdin while a run is active (see below) |
| Graphics | Turtle output from Logo, BASIC and PILOT, with **Save PNG** |

Keyboard shortcuts:

| Keys | Action |
|------|--------|
| `Ctrl+Enter` | Run |
| `Ctrl+.` | Stop |
| `Ctrl+S` | Save the program as a file (download) |
| `Up` / `Down` | Recall earlier lines in the console bar |

On macOS `Cmd` works in place of `Ctrl`. The divider between the editor and the
console can be dragged, or moved with the arrow keys when it has focus. Below
760 px wide the panes stack vertically.

**Your work is kept.** The editor text and language are saved to the browser's
`localStorage` as you type (key `timewarp.web.v1`) and restored on reload. If
loading an example or opening a file would replace edited text, the page asks
first.

**Open… and Save** work on files on *your* machine, never the server. Open
picks the language from the file extension (`.bas`, `.logo`, `.pas`, `.fth`,
`.pl`, `.py`, `.js`, …). Save downloads the editor text with the current
language's extension.

### Input

When a running program asks for input, the console bar turns into its stdin.
It shows a `?` prompt and, as its placeholder, the program's prompt (or else the
last line of output). Type a line and press Enter. This works for every
language:

- **Built-in interpreters** (BASIC `INPUT`, PILOT `A:`, Pascal `readln`)
  pause until you answer. Time spent waiting **does not** count
  toward `--timeout`. A program that waits more than 5 minutes is stopped with
  `Stopped: no input for 300s`.
- **Python, JavaScript, Perl and plugin languages** run as a child process.
  Each line you send is written to the child's stdin. The server can't tell when
  a child is blocked reading, so waiting **does** count toward the time limit.
  Raise `--timeout` for interactive programs in these languages. The line you
  type can appear before the program's own prompt, because the child only
  flushes its prompt once it has read the input.

If a program reads input while the console bar is idle, nobody can answer, so
direct-mode `INPUT` is refused with a hint to run it from the editor.

### Stopping

**Stop** (or `Ctrl+.`) ends the run within a fraction of a second. Built-in
languages finish with the usual `BREAK IN n` line; child processes are
terminated. The run also stops if you close or reload the tab.

### Console bar (REPL)

When nothing is running, a line typed in the console bar runs at once in an
interpreter that is kept between lines, so variables, the Forth stack and the
turtle's position carry over.

**BASIC works like direct mode on a home computer.** The program in the editor
is the program in memory:

```
> 10 PRINT "HELLO"         stores line 10 in the editor
> 20 GOTO 10
> LIST                     lists the editor's program, sorted
> RUN                      runs it, exactly like pressing Run
> 20                       deletes line 20
> PRINT 2+2                any other statement runs immediately
 4
```

`RENUMBER`, `NEW`, `TRON`/`TROFF` and the other console commands from the desktop
IDE work the same way. Unnumbered lines already in the editor are kept.

Python, JavaScript, Perl and plugin languages evaluate each line in a fresh
process, so nothing carries over between lines.

### What you will not see

`READY.`, `Interpreter ready.` and turtle chatter such as *Pen up* or *Turtle
returned to home position* belong to the desktop console and are suppressed.
Program output, errors and `?HINT:` lines are always shown.

## HTTP API

Everything the page does is a JSON call, so the server is easy to script or
test with `curl`.

| Method | Path | Body | Returns |
|--------|------|------|---------|
| `GET` | `/` | | The editor page |
| `GET` | `/healthz` | | `{"status": "ok"}` |
| `GET` | `/api/languages` | | `{"languages": [{"name", "key", "extension", "available"}]}` |
| `GET` | `/api/examples` | | `{"examples": [{"name", "language", "path"}]}` |
| `GET` | `/api/examples/<path>` | | `{"path", "source"}` |
| `POST` | `/api/run` | `{language, program, run?, breakpoints?}` | Result object, or an event stream |
| `POST` | `/api/stop` | `{run}` | `{"stopped": true}`, or `false` if it was not running |
| `POST` | `/api/input` | `{run, text}` | `{"accepted": true, "waiting": bool}` |
| `POST` | `/api/pause` | `{run}` | `{"paused": true}` |
| `POST` | `/api/resume` | `{run}` | `{"paused": false}` |
| `POST` | `/api/step` | `{run}` | `{"stepped": true}` |
| `POST` | `/api/repl` | `{session, language, line, program?}` | One statement's result |
| `POST` | `/api/highlight` | `{language, program}` | `{"html": "..."}` |
| `GET` | `/api/drafts` | | `{"drafts": [{"name", "modified"}]}` |
| `GET` | `/api/drafts/<name>` | | `{"name", "language", "program"}` |
| `POST` | `/api/drafts` | `{name, language, program}` | `{"name"}` |
| `DELETE` | `/api/drafts/<name>` | | `{"deleted": bool}` |

Language names are case-insensitive. In `/api/languages`, `available` is
`false` when the language's external runtime (Node.js, Perl, a plugin's
executable) is not installed on the server. The page shows those languages as
"(runtime missing)".

### Running a program

```bash
curl -s localhost:8000/api/run \
  -d '{"language": "BASIC", "program": "10 PRINT 6*7"}'
```

```json
{"run": "3f2c…", "language": "BASIC", "output": ["42"], "errors": 0,
 "timed_out": false, "stopped": false, "output_capped": false,
 "seconds": 0.004, "exit": 0, "canvas": null}
```

`exit` is `1` if the program reported an error, timed out, was stopped, hit
the output cap, or stopped at a breakpoint. `canvas` holds the final frame
when something was drawn (see below).

`run` is an optional id of up to 64 characters that you choose; the server
generates one if you don't. Use it with `/api/stop` and `/api/input`. Starting a
second run with an id that is still active returns `409`.

Send `breakpoints` as a list of 1-based editor line numbers and the run stops
at the first one, printing `BREAK IN n`. While a built-in-language program
runs you can `POST /api/pause` to freeze it between lines, `/api/step` to run
one more line, and `/api/resume` to carry on. (Pausing and breakpoints apply
to the line-by-line interpreters, not the subprocess languages.)

### Streaming

With `Accept: text/event-stream` the reply is a stream of
[server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html):

```
event: start
data: {"run": "3f2c…"}

data: {"line": "WHAT IS YOUR NAME"}

event: input
data: {"prompt": "WHAT IS YOUR NAME"}

: waiting for input

data: {"line": "ADA"}

event: canvas
data: {"type": "canvas", "width": 600, ...}

event: done
data: {"run": "3f2c…", "language": "BASIC", "errors": 0, "timed_out": false,
       "stopped": false, "output_capped": false, "seconds": 3.1, "exit": 0,
       "has_canvas": false}
```

| Event | Meaning |
|-------|---------|
| `start` | Always first; carries the run id |
| *(unnamed)* | One console line |
| `input` | The program is waiting; answer with `POST /api/input` |
| `canvas` | A graphics frame (see below) |
| `done` | Always last on success; the result without `output` and `canvas` |
| `error` | The request was rejected (`{"error", "status"}`) instead of run |

While a program waits for input, a `: waiting for input` comment is sent every
5 seconds so proxies don't close the idle connection. If the client
disconnects, the server stops the run.

Example session from a shell:

```bash
curl -sN localhost:8000/api/run -H 'Accept: text/event-stream' \
  -d '{"language":"BASIC","program":"10 INPUT A\n20 PRINT A*2","run":"demo"}' &
curl -s localhost:8000/api/input -d '{"run":"demo","text":"21"}'
```

`/api/input` returns `404` once the run has finished. Input sent before the
program asks is queued and used by the next read.

### REPL

```bash
curl -s localhost:8000/api/repl \
  -d '{"session": "me", "language": "BASIC", "line": "PRINT 2+2"}'
```

The reply is `{"session", "language", "output", "status", "exit", "canvas"}`.
`exit` is `1` when the statement failed.

For BASIC, send the editor text as `program`. The reply then includes
`program` when a numbered line or `NEW`/`RENUMBER` changed it, and `run` with
the program text when `RUN` was typed. Executing that text is the client's job;
the page does it with `/api/run`.

Each `session` id has its own interpreter. Changing the language starts a new
one. The page uses one session per tab.

### Syntax highlighting

`POST /api/highlight` returns the program as HTML with inline colours from the
same Pygments lexers the desktop editor uses (`web/highlight.py`). There is no
wrapper element and no stylesheet. The page paints the HTML in a `<pre>` behind
a transparent `<textarea>`, so caret, selection, undo and scrolling stay native.

- Requests are debounced and stale replies dropped. Until colours arrive, or if
  the request fails, the text is shown plain rather than hidden.
- `basic` uses Pygments' Commodore BASIC lexer. Pascal, Prolog, Forth, Perl,
  Python and JavaScript have their own lexers, and a plugin's `syntax` alias is
  honoured. PILOT and Logo stay plain.
- Source text is always escaped, so a program containing `<script>` cannot
  inject markup. Without Pygments installed, every language is escaped plain
  text.

## Graphics frames

Turtle output is rasterised on the server into a palette-indexed buffer of
600×400 pixels. It is sent as **run-length encoded** frames, so an update
costs a few hundred bytes rather than 240,000 pixels.

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
| `x`, `y`, `w`, `h` | The rectangle this frame updates (only what changed) |
| `palette` | CSS colours; index 0 is the background |
| `rle` | base64 of repeated *(uint16 little-endian run length, uint8 palette index)* |
| `overlay` | Vector items drawn on top: turtle marker, ovals, rectangles, lines, text |

The page keeps a full-size `ImageData`, repaints only the rectangle it is
given, then draws the overlay, so the turtle and text stay sharp.
`web/canvas.py` has a matching `decode_rle` that the tests use.

## Limits

| Limit | Value | When exceeded |
|-------|-------|---------------|
| Program size | 256 KB | `413` |
| Concurrent runs (incl. REPL lines) | 4 | `429` immediately, not queued |
| Run time | `--timeout`, default 10 s, not counting built-in input waits | `Stopped: time limit…`, `timed_out: true` |
| Waiting for input | `--input-timeout`, default 300 s | `Stopped: no input for 300s` |
| Output | `--max-output-lines`, default 20,000 lines per run | Run stopped, `output_capped: true` |
| Loop backstop | `--max-iterations`, default 50 million | Run stopped |
| REPL line | 8 KB, 2 s | `413`, or the line is stopped |
| REPL sessions | 16, expire after 10 idle minutes | Least recently used is dropped |

Malformed requests (a bad `Content-Length`, a body that isn't UTF-8 or isn't a
JSON object, an unknown language) are answered with `400`. Every run gets a
fresh interpreter; only REPL sessions keep state.

The browser console keeps the last 5,000 lines, so a long run stays responsive.

## Container

Each `vX.Y.Z` tag publishes an image for `linux/amd64` and `linux/arm64`:

```bash
docker run --rm -p 8000:8000 ghcr.io/james-honeybadger/time-warp-classic-web:latest
```

Or build it yourself:

```bash
docker build -f Dockerfile.web -t timewarp-web .
docker run --rm -p 8000:8000 timewarp-web
```

The image contains the built-in interpreters and Pygments. JavaScript needs
Node.js, Perl needs Perl, and plugin languages need their own runtimes. Enable
the `apt-get` line in `Dockerfile.web` or extend the image. `HEALTHCHECK` polls
`/healthz`. To expose plugin languages, set `TIMEWARP_PLUGIN_PATH` to a mounted
folder.

If you put the server behind nginx, streaming already works: responses carry
`X-Accel-Buffering: no`. Other proxies may need response buffering turned off
for `/api/run`.

## Security

The server runs arbitrary programs for anyone who can reach it, and it has
**no authentication**.

- The default `--host 127.0.0.1` keeps it to your machine.
- Bind `0.0.0.0` only on a network you control, ideally behind a proxy that adds
  authentication and rate limiting.
- The built-in interpreters have no file or network access from programs.
  **Python, JavaScript and Perl run as real processes** and can do anything the
  server's user can. Don't offer those languages to people you don't trust.
- Run ids are not secrets. Anyone who can reach the server can stop or feed
  input to any run whose id they know.

## Not included

Breakpoints and pausing are built in (click a gutter line number, or use the
Pause/Step/Resume buttons). There is no error-history dialog and no themes
yet. Files are opened and saved through the browser or as server-side drafts
(`/api/drafts`), so there is no general server-side file browser.
