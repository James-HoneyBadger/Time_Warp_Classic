# Time Warp Classic

A back-to-basics IDE for nine languages, old and new, with turtle graphics.
Line-numbered BASIC, PILOT, Logo, Pascal, Prolog and Forth run on interpreters
built into the project; Python, JavaScript and Perl run on the runtimes you
already have. Use it as a Tkinter desktop app, in a browser, or from the
command line.

[![Version](https://img.shields.io/badge/version-1.6.0-blue.svg)](https://github.com/James-HoneyBadger/Time_Warp_Classic)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![education](https://img.shields.io/badge/topic-education-lightgrey)](https://github.com/topics/education)
[![ide](https://img.shields.io/badge/topic-ide-lightgrey)](https://github.com/topics/ide)
[![tkinter](https://img.shields.io/badge/topic-tkinter-lightgrey)](https://github.com/topics/tkinter)
[![turtle-graphics](https://img.shields.io/badge/topic-turtle--graphics-lightgrey)](https://github.com/topics/turtle-graphics)

```basic
10 PRINT "HELLO FROM 1964"
20 FOR I = 1 TO 3
30   PRINT "COUNT: "; I
40 NEXT I
```

## Languages

| Language | First appeared | Runs on |
|----------|----------------|---------|
| BASIC | 1964 | Built-in interpreter (line numbers, turtle commands) |
| PILOT | 1968 | Built-in interpreter |
| Logo | 1967 | Built-in interpreter (turtle graphics) |
| Pascal | 1970 | Built-in interpreter |
| Forth | 1970 | Built-in interpreter |
| Prolog | 1972 | Built-in interpreter |
| Perl | 1987 | `perl` on your `PATH` |
| Python | 1991 | The Python running Time Warp |
| JavaScript | 1995 | Node.js (`node` or `nodejs`) on your `PATH` |

If Perl or Node.js is missing, the language is marked **(runtime missing)** in
the language menu, the status bar and the web IDE, and running a program tells
you what to install. More languages can be added with a JSON plugin manifest
(see [docs/dev/PLUGINS.md](docs/dev/PLUGINS.md)).

## Install and run

Python 3.9 or newer is required (CI metadata covers 3.9–3.14). The desktop IDE
also needs Tkinter, which some Linux distributions package separately
(`python3-tk` / `python3-tkinter`).

From PyPI, inside a virtual environment:

```bash
python3 -m venv venv && source venv/bin/activate
pip install timewarp-classic
timewarp                # desktop IDE
timewarp --web          # browser IDE on http://127.0.0.1:8000/
```

From a clone:

```bash
git clone https://github.com/James-HoneyBadger/Time_Warp_Classic.git
cd Time_Warp_Classic
python3 run.py          # creates venv/, installs dependencies, launches the IDE
```

`./run.sh` (Linux/macOS) and `run.bat` (Windows) do the same job. If you
prefer to drive it yourself:

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 Time_Warp.py
```

[SETUP.md](SETUP.md) covers launcher options, Tkinter on each OS, headless
machines, Docker and troubleshooting.

## Command line

`Time_Warp.py` (installed as `timewarp`) with no arguments opens the desktop IDE.

| Option | Meaning |
|--------|---------|
| `--run FILE`, `-r FILE` | Run a source file or `.twrun` bundle, print the output, exit |
| `--language LANG`, `-l LANG` | Language of a plain source file given to `--run` |
| `--web` | Serve the browser IDE instead of opening a window |
| `--host H` | Bind address for `--web` (default `127.0.0.1`) |
| `--port P` | Port for `--web` (default `8000`; `0` picks a free port) |
| `--timeout S` | Seconds a web run may last before it is stopped (default `10`) |
| `--version`, `-V` | Print the version and exit |

```bash
python3 Time_Warp.py --run examples/forth/number_theory.fth --language forth
```

`--run` reads input (`INPUT`, `A:`, `readln`, `input()`, stdin) from the terminal, so programs can be piped or scripted.

## Desktop IDE

The Tkinter window has an editor with line numbers, an output console, a
console input bar, and a turtle graphics pane that appears for Logo and BASIC.
The menus are **File, Edit, Program, Debug, Test, Performance, Preferences,
About**.

- **Running.** F5 runs, Ctrl+. or the Stop button stops; the window stays
  responsive and output streams as it is produced. While a program runs, the
  console bar answers its `INPUT`.
- **BASIC direct mode.** With BASIC selected and nothing running, the console
  bar behaves like a home computer: `PRINT 2+2` runs immediately, numbered
  lines edit the program, and `LIST`, `RUN`, `RENUMBER`, `NEW` and `HELP` work.
  For the other languages the bar runs one statement at a time in a persistent
  session (**Program → Reset Console REPL** starts over).
- **Errors.** Messages carry the line number and, for common mistakes, a
  `?HINT:` line. Click an error in the output to jump to that line.
- **Editing.** Pygments syntax highlighting (plain text if Pygments is
  missing), find and replace with regex support, and word completion
  (Ctrl+Space, or automatically as you type; toggle in **Preferences**).
- **Debugging.** **Debug → Enable Debug Mode**, then F9 sets or clears a
  breakpoint on the current line; a run stops when it reaches one. Error
  history is kept under the same menu.
- **Preferences.** 9 colour themes (Light, Dark, Classic, Solarized Dark,
  Solarized Light, Monokai, Dracula, Nord, High Contrast), 7 font sizes
  (8–22 pt) and any installed font family, with common monospace
  families listed first. Saved to
  `~/.timewarp_settings.json`.
- **Examples.** **Program → Load Example** has two or three programs per
  language, taken from [`examples/`](examples/README.md).
- **Export.** **File → Export Runner...** writes a `.pyz` that runs the program
  with nothing but Python ([docs/dev/EXPORTING.md](docs/dev/EXPORTING.md)).
- **Plugins.** **Preferences → Plugins** reloads, creates or opens JSON
  manifests in `~/.timewarp/plugins/`.
- **Web IDE.** **Program → Open Web IDE** starts the browser IDE on a free
  local port and opens it.

| Key | Action |
|-----|--------|
| F5 | Run |
| Ctrl+. | Stop |
| F9 | Toggle breakpoint at cursor |
| Ctrl+N / Ctrl+O | New / Open |
| Ctrl+S / Ctrl+Shift+S | Save / Save As |
| Ctrl+Z / Ctrl+Y | Undo / Redo |
| Ctrl+F / Ctrl+H | Find / Replace |
| Ctrl+Space | Complete word |
| Ctrl+Q | Exit |

## Web IDE

```bash
python3 Time_Warp.py --web [--host H] [--port P] [--timeout S]
```

This serves the same interpreters on `http://127.0.0.1:8000/` by default,
using only the standard library plus Pygments; Tkinter is not needed. The page
has:

- Run (Ctrl+Enter) and Stop (Ctrl+.).
- Interactive input: while a program runs, the console bar is its stdin, in
  every language.
- BASIC direct mode in the console bar, as on the desktop.
- Open... and Save (Ctrl+S) for local files, plus autosave of the editor to
  the browser's localStorage.
- A turtle graphics canvas with Save PNG, Pygments highlighting, and an
  examples picker.

Each run is capped at 20,000 lines of output, and at most 4 programs run at
once; further requests get HTTP 429. Turtle "pen up/pen down" chatter is only
shown in the desktop console, not in the web IDE or `--run` output. Details
and the JSON API are in [docs/dev/WEB.md](docs/dev/WEB.md).

## A few programs

PILOT, asking a question and using the answer:

```pilot
T:What is your name?
A:NAME
T:Hello, {NAME}!
E:
```

Logo, a square:

```logo
REPEAT 4 [
  FORWARD 100
  RIGHT 90
]
```

Forth:

```forth
: SQUARE DUP * ;
5 SQUARE .
```

Prolog, with a query in the program:

```prolog
parent(tom, bob).
parent(bob, ann).
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
?- grandparent(tom, W).
```

Pascal:

```pascal
program Hello;
begin
  WriteLn('Hello from Pascal!');
end.
```

The [language tutorials](docs/user/LANGUAGE_TUTORIALS.md) and
[per-language references](docs/languages/) go further.

## Docker

Version tags publish two images to GHCR, for `linux/amd64` and `linux/arm64`:

```bash
# Web IDE on http://localhost:8000
docker run --rm -p 8000:8000 ghcr.io/james-honeybadger/time-warp-classic-web:latest

# Desktop IDE over X11
xhost +local:docker
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
  ghcr.io/james-honeybadger/time-warp-classic:latest
```

Build them locally from [`Dockerfile.web`](Dockerfile.web) and
[`Dockerfile`](Dockerfile). See [SETUP.md](SETUP.md#docker) for tags.

## Development

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements-dev.txt   # runtime deps + pytest, black, flake8
python3 -m pytest                     # GUI tests skip when there is no display
xvfb-run -a python3 -m pytest         # include the GUI tests on a headless box
black . && flake8
```

The **Test** menu in the IDE has a quick smoke test (expression evaluation,
variables, program loading) and **Run Full Test Suite**, which runs
`scripts/run_tests.py` (pytest, from a source checkout).

Architecture notes are in the
[technical reference](docs/dev/TECHNICAL_REFERENCE.md). Changes are listed in
[CHANGELOG.md](CHANGELOG.md).

```text
Time_Warp_Classic/
├── Time_Warp.py          # Entry point: desktop IDE, --web, --run
├── run.py, run.sh, run.bat  # Launchers that set up venv/ and start the IDE
├── gui/                  # Tkinter IDE: app, menus, dialogs, themes, completion popup
├── core/
│   ├── interpreter.py    # Time_WarpInterpreter, the shared execution engine
│   ├── runner.py         # Headless runner behind --run and the web IDE
│   ├── export.py         # .twrun bundles and .pyz runners
│   ├── plugins.py        # JSON language plugins
│   ├── error_hints.py    # ?HINT: suggestions
│   ├── languages/        # One executor per language (+ BASIC direct mode)
│   ├── features/         # Syntax highlighting, word completion
│   ├── optimizations/    # Performance menu internals
│   └── utilities/        # Safe expression evaluation
├── web/                  # HTTP server, turtle canvas encoder, highlighter, static/index.html
├── examples/             # Two or three programs per language
├── docs/                 # User, language and developer documentation
├── tests/                # pytest suite
├── scripts/              # Extra launchers and run_tests.py
├── Dockerfile, Dockerfile.web
└── pyproject.toml, requirements.txt, requirements-dev.txt
```

Contributions are welcome: fork, branch, keep `pytest` green, open a pull
request. Bugs go to
[GitHub Issues](https://github.com/James-HoneyBadger/Time_Warp_Classic/issues).

## Documentation

- [Quick start](docs/QUICK_START.md) — first program in a few minutes
- [Setup](SETUP.md) — installation, environments, Docker, releasing
- [Documentation map](docs/README.md) — everything else, by task
- [FAQ](docs/FAQ.md) and [Troubleshooting](docs/TROUBLESHOOTING.md)

## Acknowledgments

To the people whose languages this runs: John Starkweather (PILOT), John
Kemeny and Thomas Kurtz (BASIC), Seymour Papert, Wally Feurzeig and Cynthia
Solomon (Logo), Niklaus Wirth (Pascal), Alain Colmerauer (Prolog) and Chuck
Moore (Forth). And to everyone keeping old machines and old languages running.

## License

MIT. See [LICENSE](LICENSE).

© 2025–2026 Honey Badger Universe
