# Troubleshooting

Find the message you're seeing, then read the cause and fix. Messages are
quoted exactly as Time Warp prints them.

- [Starting up](#starting-up)
- [Running programs](#running-programs)
- [The command line runner](#the-command-line-runner)
- [The browser IDE](#the-browser-ide)
- [Still stuck](#still-stuck)

## Starting up

### `❌ GUI launch failed: No module named 'tkinter'`

**Cause:** your Python was built without Tk. Common with distro Pythons and
pyenv builds.

**Fix:** install the Tk package for the Python you are using, then start
again.

```bash
sudo apt-get install python3-tk      # Debian/Ubuntu
sudo dnf install python3-tkinter     # Fedora
brew install python-tk               # macOS with Homebrew Python
python3 -m tkinter                   # check: a small window should open
```

On Windows, rerun the python.org installer and tick "tcl/tk and IDLE".
`run.py` tries the Linux and Homebrew installs for you (after asking).

If you don't need the desktop window, `python3 Time_Warp.py --web` needs no
Tk at all.

### `no display name and no $DISPLAY environment variable`

**Cause:** no graphical session: SSH without X forwarding, a container, CI.
`run.py` warns about it up front: `No graphical display detected
(DISPLAY/WAYLAND_DISPLAY unset)`.

**Fix:** use the browser IDE (`--web`), connect with `ssh -X`, or for tests
wrap the command in `xvfb-run -a`.

### `run.py` stops at `Failed to create virtual environment`

**Cause:** the `venv` module (or `ensurepip`) isn't installed. Debian and
Ubuntu split it out.

**Fix:** `sudo apt-get install python3-venv` (Fedora: `sudo dnf install
python3-venv`), then `python3 run.py --clean`.

### `python: command not found`

**Cause:** many systems only ship `python3`.

**Fix:** use `python3` in every command in these docs.

### `ℹ️  PIL/Pillow not available - image features disabled`

**Cause:** Pillow isn't installed in this environment.

**Fix:** none needed to run programs. To silence it,
`pip install -r requirements.txt` in the environment you launch from (or let
`run.py` do it).

### Fonts, theme or completion settings look wrong

**Cause:** a bad or stale `~/.timewarp_settings.json`.

**Fix:** delete it. The defaults (Dark theme, Courier, medium size, completion
on) come back on the next start.

## Running programs

### Run prints nothing, or the output makes no sense

**Cause:** usually the wrong language is selected. The desktop IDE starts on
PILOT, so BASIC pasted into a fresh window runs as PILOT and prints nothing.

**Fix:** set the language selector before pressing Run. Opening a file or
using **Program → Load Example** sets it from the extension.

### `?ERROR IN 120: ...` followed by `?HINT: ...`

**Cause:** the program failed on line 120. The `?HINT:` line suggests the
usual reason and names the language reference to read. For example:

```
?ERROR IN 1: Division by zero in expression
?HINT: a value in the expression is 0 - check the divisor before dividing. See docs/languages/BASIC_REFERENCE.md.
```

**Fix:** click the error line in the desktop IDE to jump to line 120. For
Python, JavaScript and Perl the number is the script's own line, taken from
the traceback.

### The program never finishes

**Cause:** an endless loop. Built-in languages have no time limit on the
desktop.

**Fix:** press **Stop** or Ctrl+.. The console prints `BREAK IN n` with the
line it was on; click it.

### The program is waiting and nothing happens

**Cause:** it's waiting at `INPUT`, `A:`, `readln` or `input()`. There is no
pop-up dialog.

**Fix:** type into the console bar under the output and press Enter.

### Logo or BASIC drawing ran but printed nothing

**Cause:** that's normal. Turtle programs draw; they don't print. The desktop
console mentions pen moves such as *Pen up*; the browser IDE and `--run` hide
those lines.

**Fix:** look at the Turtle Graphics pane (shown for Logo and BASIC only).
Under `--run` there is no canvas, so use an IDE to see the picture.

### `JavaScript (runtime missing)` / `?JAVASCRIPT NOT FOUND - install it to run these scripts (install Node.js from nodejs.org)`

**Cause:** neither `node` nor `nodejs` on `PATH` answered `--version`. Perl
gives `?PERL NOT FOUND - install it to run these scripts (install Perl (apt
install perl, brew install perl, or strawberryperl.com))`. Plugin languages
report the executable named in their manifest.

**Fix:** install the runtime, check with `node --version` or `perl --version`
in the same shell, and restart Time Warp so it looks again. Python never shows
this: it uses the interpreter running Time Warp.

### `?ERROR: Python script timed out after 30s`

**Cause:** Python, JavaScript and Perl programs get 30 seconds each (the same
message names `JavaScript` or `Perl`). Built-in languages have no such limit
on the desktop.

**Fix:** make the program do less, or run the script directly with `python3`,
`node` or `perl` if it really needs longer.

### A Prolog `.pl` file opens as Perl (or the other way round)

**Cause:** `.pl` belongs to both. Time Warp picks Prolog only if the file
contains `:-` or `?-` and looks more like Prolog than Perl.

**Fix:** change the language selector, or save Prolog as `.pro`.

### A plugin language is missing from the selector

**Cause:** its manifest in `~/.timewarp/plugins/` didn't load, or was added
after start-up.

**Fix:** **Preferences → Plugins → Reload Plugins**, and see
[dev/PLUGINS.md](dev/PLUGINS.md) for the manifest format.

## The command line runner

### `?ERROR: --language is required when running a plain source file`

**Cause:** `--run` doesn't guess the language from the extension. Only a
`.twrun` bundle carries its own.

**Fix:** add it: `python3 Time_Warp.py --run hello.bas --language basic` (or
`-l basic`). The exit code was 2.

### `?ERROR: no such file: hello.bas`

**Cause:** the path is wrong relative to where you ran the command.

**Fix:** check with `ls`, or pass an absolute path.

## The browser IDE

### `OSError: [Errno 98] Address already in use`

(`[Errno 48]` on macOS.)

**Cause:** something already listens on port 8000, often an earlier
`--web` you forgot about.

**Fix:** stop the other server (`ss -ltnp 'sport = :8000'` or
`lsof -i :8000` shows who has it), or choose another port:
`--port 8001`, or `--port 0` for any free one. The URL is printed at start-up:
`Time Warp Classic web IDE: http://127.0.0.1:8001/`.

### The browser can't reach the server

**Cause:** the server isn't running, or it's bound to `127.0.0.1` inside a
container or on another machine.

**Fix:** check the terminal for the `Time Warp Classic web IDE:` line. In a
container, bind `--host 0.0.0.0` and publish the port (`-p 8000:8000`); the
`Dockerfile.web` image already does both. Read
[dev/WEB.md](dev/WEB.md#security) before exposing it beyond localhost.

### A language shows `(runtime missing)` / `JavaScript needs its runtime installed on the server`

**Cause:** the runtime is missing on the machine running the server, not
your browser's machine. The `Dockerfile.web` image does not install Node.js.

**Fix:** install it where the server runs, or extend the image as described in
[dev/WEB.md](dev/WEB.md#container), then restart the server.

### `too many programs are running, try again`

**Cause:** the server allows four runs at a time (REPL lines count too). The
fifth is refused straight away, not queued (the HTTP API answers 429). Programs still
waiting for input hold their slot. In the console bar the equivalent is
`the previous statement is still running`.

**Fix:** stop runs you've left waiting in other tabs, or wait and try again.

### `Stopped: time limit of 10s reached`

**Cause:** the run went past `--timeout` (default 10 seconds). For built-in
languages, time spent waiting for input doesn't count. For Python, JavaScript
and Perl it does, and their own 30-second cap still applies whatever
`--timeout` says.

**Fix:** restart the server with a bigger limit, e.g.
`python3 Time_Warp.py --web --timeout 60`, or answer prompts faster.

### `Stopped: no input for 300s`

**Cause:** a program sat at an input prompt for 5 minutes.

**Fix:** answer sooner, or press Stop when you walk away.

### `Stopped: output limit of 20000 lines reached`

**Cause:** the run printed more than 20,000 lines; usually a `PRINT` in a
loop that doesn't end.

**Fix:** fix the loop, or print less.

### `?INPUT needs a running program: put it in the editor and press Run`

**Cause:** you typed `INPUT` (or a line that reads input) into the idle
console bar. Nobody can answer it there.

**Fix:** put the program in the editor and press Run; the console bar then
becomes its stdin.

### `?ERROR: the connection to the server closed before the program finished`

The status line reads `connection lost`.

**Cause:** the server stopped or restarted mid-run, or a proxy closed the
stream.

**Fix:** check the server's terminal and start it again. Behind a proxy other
than nginx, turn response buffering off for `/api/run`.

### `?ERROR: ... (is the server still running?)`

The status line reads `server unreachable`.

**Cause:** the browser couldn't reach the server at all.

**Fix:** start it again. Your editor text is safe: it's kept in the browser's
`localStorage`.

### `<file> is larger than the 256 KB program limit`

**Cause:** **Open…** refuses files over 256 KB; the server answers
`program is too large` (HTTP 413) for the same reason.

**Fix:** split the program.

## Still stuck

1. Check the basics: `python3 --version` (3.9 or newer),
   `python3 Time_Warp.py --version`, `python3 -m tkinter`.
2. Run a bundled example from the command line. If this works, the
   interpreter is fine and the problem is in your program or the GUI:
   `python3 Time_Warp.py --run examples/basic/INDEX.bas -l basic`
3. Run the tests: `python3 -m pytest -q` (after
   `pip install -r requirements-dev.txt`).
4. See the [FAQ](FAQ.md), or open an issue at
   <https://github.com/James-HoneyBadger/Time_Warp_Classic/issues> with the
   exact error text, your OS, and both version numbers.
