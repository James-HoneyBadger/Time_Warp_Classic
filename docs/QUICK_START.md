# Quick Start

From nothing to a running program in a few minutes. You need Python 3.9 or
newer. The desktop IDE also needs Tk (`tkinter`); the browser IDE does not.

## 1. Install and launch

Pick one.

**From PyPI**

```bash
python3 -m venv ~/.venvs/timewarp && . ~/.venvs/timewarp/bin/activate
pip install timewarp-classic
timewarp            # desktop IDE
timewarp --web      # browser IDE at http://127.0.0.1:8000/
```

**From a source checkout**

```bash
git clone https://github.com/James-HoneyBadger/Time_Warp_Classic.git
cd Time_Warp_Classic
python3 run.py      # or ./run.sh on Linux/macOS, run.bat on Windows
```

`run.py` creates `venv/` in the checkout, installs `requirements.txt` into it
(network needed the first time), checks for `tkinter`, and starts
`Time_Warp.py`. Options: `--clean` rebuilds the venv, `--no-install` skips the
install step. If you manage your own environment, `pip install -r
requirements.txt` and `python3 Time_Warp.py` do the same job.

**In a container (browser IDE only)**

```bash
docker run --rm -p 8000:8000 ghcr.io/james-honeybadger/time-warp-classic-web:latest
```

Then open <http://127.0.0.1:8000/>. The image is built from `Dockerfile.web`
and does not install Node.js; [dev/WEB.md](dev/WEB.md#container) explains how
to add runtimes. The X11 desktop image is described in the
[main README](../README.md).

Something failed? Go to [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

## 2. First programs

The language selector sits above the editor. The desktop IDE starts on PILOT,
so change it before you paste.

**BASIC**

```basic
10 PRINT "HELLO FROM 1982"
20 FOR I = 1 TO 3
30 PRINT I; " SQUARED IS "; I*I
40 NEXT I
50 END
```

Choose **BASIC**, paste, press **Run** (F5). Output:

```
HELLO FROM 1982
1 SQUARED IS 1
2 SQUARED IS 4
3 SQUARED IS 9
```

Line numbers are optional; the bundled BASIC examples don't use them.

**Logo**

```logo
REPEAT 4 [FORWARD 100 RIGHT 90]
```

Choose **Logo** and run. A square appears on the turtle canvas. The desktop
shows the canvas for Logo and BASIC and hides it for the other languages.

**Python**

```python
def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)

for i in range(1, 6):
    print(f"{i}! = {factorial(i)}")
```

Python runs in a child process using the same interpreter that started Time
Warp. JavaScript needs `node` and Perl needs `perl` on your `PATH`. Without
them the language is shown as `(runtime missing)`.

## 3. The desktop IDE

| Area | Use |
|------|-----|
| Code Editor (left) | Your program. Line numbers, Pygments highlighting, word completion. |
| Output (top right) | Program output and errors. Click a `?ERROR IN n` or `BREAK IN n` line to jump to line *n*. |
| Turtle Graphics (bottom right) | Logo and BASIC drawings. |
| Console bar | Answers `INPUT`/`A:`/`input()` while a program runs. When idle, it's BASIC direct mode or a one-line REPL for other languages. |
| Buttons | Run, Stop, Open, Save, Clear Editor, Clear Output, Clear Graphics |
| Status bar | Language, file name (`*` = unsaved), `Ready`/`Running`, `Ln 12, Col 5` |

Menus: **File, Edit, Program, Debug, Test, Performance, Preferences, About**.
**Program → Load Example** has two programs per language.

### Keys

| Key | Action |
|-----|--------|
| F5 | Run |
| Ctrl+. | Stop (the console prints `BREAK IN n`) |
| F9 | Toggle a breakpoint on the current line |
| Ctrl+N / Ctrl+O | New / Open |
| Ctrl+S / Ctrl+Shift+S | Save / Save As |
| Ctrl+Z / Ctrl+Y | Undo / Redo |
| Ctrl+F / Ctrl+H | Find / Replace |
| Ctrl+Space | Word completions (arrows to move, Enter or Tab to accept, Esc to close) |
| Ctrl+Q | Exit |

### BASIC direct mode

With **BASIC** selected and nothing running, the console bar behaves like a
home computer at the `READY.` prompt:

```
PRINT 2+2          runs at once
10 PRINT "HI"      stores line 10 in the editor
10                 deletes line 10
LIST               RUN   RUN 100   RENUMBER   NEW   TRON   TROFF   HELP
```

### Preferences

**Preferences** sets the colour theme (nine of them), font family, font size
and auto-completion. Choices are saved to `~/.timewarp_settings.json`.

## 4. The browser IDE

```bash
python3 Time_Warp.py --web                  # http://127.0.0.1:8000/
python3 Time_Warp.py --web --port 0         # any free port
python3 Time_Warp.py --web --timeout 30     # allow 30 s per run (default 10)
```

**Program → Open Web IDE** in the desktop app starts one on a free port and
opens your browser.

- **Run** is Ctrl+Enter, **Stop** is Ctrl+., **Save** is Ctrl+S (downloads
  the file). **Open…** loads a file from your machine.
- While a program runs, the console bar is its stdin. Type the answer to
  `INPUT` and press Enter.
- When idle, the console bar is BASIC direct mode (numbered lines edit the
  program in the editor; `LIST`, `RUN`) or a one-line REPL.
- The editor is autosaved in the browser's `localStorage`.
- Turtle drawings appear in the Graphics pane; **Save PNG** keeps one.
- Limits per server: the `--timeout` per run, 20,000 output lines per run, four
  runs at once.

Full details, the HTTP API and the security notes: [dev/WEB.md](dev/WEB.md).
Don't expose it beyond localhost without reading the security section; it
has no authentication.

## 5. The command line

```bash
python3 Time_Warp.py --run hello.bas --language basic
python3 Time_Warp.py -r examples/logo/mandala_art.logo -l logo
python3 Time_Warp.py --version
```

`--run` prints the output and exits with `0` on success, `1` if the program
reported an error, `2` for a usage problem such as a missing file. A plain
source file always needs `--language`; a `.twrun` bundle carries its own.
BASIC `INPUT` and PILOT `A:` read from your terminal, so you can pipe answers
in.

**File → Export Runner...** in the desktop IDE writes a single `.pyz` that
runs your program anywhere Python 3.9+ is installed: `python3 myprog.pyz`.
See [dev/EXPORTING.md](dev/EXPORTING.md).

## Next

- [examples/README.md](../examples/README.md): the bundled programs
- [user/LANGUAGE_TUTORIALS.md](user/LANGUAGE_TUTORIALS.md): a walk through each language
- [languages/](languages/): one reference per language
- [dev/PLUGINS.md](dev/PLUGINS.md): add a language you already have installed (Ruby, Lua, ...) via **Preferences → Plugins**
- [FAQ.md](FAQ.md) and [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
