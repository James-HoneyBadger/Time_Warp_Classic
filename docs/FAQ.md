# FAQ

Short answers. Follow the links for the long ones.

## General

### What is Time Warp Classic?

An IDE for nine languages: PILOT, BASIC, Logo, Pascal, Prolog and Forth run on
interpreters written in Python inside Time Warp; Python, JavaScript and Perl
run in their real runtimes as child processes. There is a Tk desktop app, a
browser IDE (`--web`), and a headless runner (`--run`).

### Who is it for?

People who want to type `10 PRINT "HELLO"` or drive a Logo turtle without
hunting down an emulator, and who'd still like pip, venv, pytest and a browser
in the loop. Teachers and students use it too.

### What does it cost?

Nothing. MIT licence.

### Which platforms?

Anything with Python 3.9+. The desktop IDE needs Tk; the browser IDE and
`--run` don't.

### Does it need the internet?

Only to install dependencies. The desktop app, the web server and `--run` all
run locally.

## Installing

### What's the quickest install?

`pip install timewarp-classic`, then `timewarp`. From a checkout,
`python3 run.py` builds a `venv/` and launches. See
[QUICK_START.md](QUICK_START.md).

### What does it depend on?

`pygame-ce`, `Pillow` and `pygments` (from `requirements.txt`), plus Tk for
the desktop app. JavaScript programs need Node.js (`node` or `nodejs` on
`PATH`), Perl programs need `perl`. Python programs use the interpreter that
runs Time Warp.

### How do I run the tests?

```bash
pip install -r requirements-dev.txt
python3 -m pytest
xvfb-run -a python3 -m pytest    # include GUI tests on a headless machine
```

GUI tests skip themselves when there is no display.

## Using the IDEs

### Which language does the desktop IDE start in?

PILOT. Change it with the selector above the editor. Opening a file or loading
an example switches it to match the file's extension.

### How do I run and stop a program?

Desktop: **Run** or F5; **Stop** or Ctrl+.. Browser: Ctrl+Enter and Ctrl+..
A stopped built-in program reports `BREAK IN n`.

### How do I answer `INPUT`?

Type into the console bar under the output and press Enter. That works for
BASIC `INPUT`, PILOT `A:`, Pascal `readln`, and `input()`/stdin in Python,
JavaScript and Perl, in both IDEs.

### What does the console bar do when nothing is running?

With BASIC selected it is direct mode: `PRINT 2+2` runs at once, `10 PRINT "HI"`
adds line 10 to the editor, and `LIST`, `RUN`, `RENUMBER`, `NEW`, `TRON`,
`TROFF` and `HELP` work. For the other built-in languages it is a REPL that
keeps variables between lines (**Program → Reset Console REPL** clears them).
Python, JavaScript and Perl lines each run in a fresh process.

### Where's the list of keyboard shortcuts?

[QUICK_START.md](QUICK_START.md#keys) for the desktop,
[dev/WEB.md](dev/WEB.md#using-the-page) for the browser.

### How do I find the line an error is on?

Errors look like `?ERROR IN 120: ...`, often followed by a `?HINT:` line. In
the desktop IDE, click the error line and the editor jumps to line 120.
Python, JavaScript and Perl errors are mapped to the script's own line number.

### How do I debug?

Type `TRON` in the BASIC console bar to trace each line as it runs, `TROFF` to
stop. In the desktop IDE, **Debug → Enable Debug Mode** plus F9 sets
breakpoints, and **Debug → Show Error History** lists recent errors. The
browser IDE has no breakpoints.

### Is there a time limit?

| Where | Built-in languages | Python / JavaScript / Perl |
|-------|-------------------|----------------------------|
| Desktop IDE | None. Press Stop. | 30 s, then `?ERROR: Python script timed out after 30s` |
| `--run` | None. Press Ctrl+C. | 30 s |
| Browser IDE | `--timeout` (default 10 s), not counting time waiting for input | `--timeout` or 30 s, whichever is shorter; waiting for input counts |

### Why can't I see "pen up" messages in the browser?

The desktop console echoes turtle actions such as *Pen up*. The browser IDE
and `--run` hide them and show only program output and errors.

## Languages

### Which language first?

BASIC for the classic experience, Logo if you want pictures, PILOT for
question-and-answer programs. [user/LANGUAGE_TUTORIALS.md](user/LANGUAGE_TUTORIALS.md)
walks through all nine.

### Can I run JavaScript without Node.js?

No. Without `node`, JavaScript is listed as `JavaScript (runtime missing)` and
a run prints `?JAVASCRIPT NOT FOUND - install it to run these scripts (install
Node.js from nodejs.org)`. Perl works the same way.

### Which languages can draw?

Logo (turtle), and BASIC (turtle commands such as `FORWARD`/`RIGHT` plus
`PSET`, `LINE`, `BOX`, `CIRCLE`). The browser IDE also draws PILOT `G:`
graphics; the desktop IDE shows its canvas only for Logo and BASIC.

### Can one program mix languages?

No. One program, one language.

### Is this a faithful copy of a particular BASIC/Logo/Forth?

No. Each interpreter covers the common core of the language plus some
extras. The [language references](languages/) list what's actually
implemented.

## Files

### Which extensions does it use?

| Language | Saves as | Also opens |
|----------|----------|------------|
| PILOT | `.pilot` | `.pil` |
| BASIC | `.bas` | |
| Logo | `.logo` | `.lgo` |
| Pascal | `.pas` | `.pp` |
| Prolog | `.pro` | `.prolog` |
| Forth | `.fth` | `.4th`, `.fs` |
| Perl | `.pl` | `.pm` |
| Python | `.py` | |
| JavaScript | `.js` | |

**Save As** proposes the extension for the selected language.

### My Prolog `.pl` file opened as Perl.

`.pl` belongs to Perl. A `.pl` file is treated as Prolog only if it has `:-` or
`?-` and looks more like Prolog than Perl (statements ending in `.`, few `$`/`@`
sigils). Save Prolog as `.pro`, or pick Prolog in the selector.

### How do I know a file has unsaved changes?

A `*` after the name in the title bar and status bar. New, Open, Load Example
and closing the window ask before discarding changes.

### Where do the examples live?

`examples/<language>/` in a checkout, inside the package when pip-installed.
Use **Program → Load Example** (desktop) or the examples drop-down (browser).
See [examples/README.md](../examples/README.md).

### Can I share a program with someone who doesn't have Time Warp?

**File → Export Runner...** writes a `.pyz` that runs with plain Python 3.9+.
See [dev/EXPORTING.md](dev/EXPORTING.md).

## Customising

### Can I change the theme and font?

**Preferences → Color Theme** (nine themes), **Font Family**, **Font Size**
(8 to 22 pt) and **Auto-complete Words**. Saved to `~/.timewarp_settings.json`.
Colours and shortcuts aren't editable beyond that.

### Can I add a language?

Yes, if it has a command-line runtime. **Preferences → Plugins → Create
Example Plugin** writes a JSON manifest to `~/.timewarp/plugins/`; point it at
the executable and use **Reload Plugins**. See [dev/PLUGINS.md](dev/PLUGINS.md).
For how the built-in interpreters are put together, see
[dev/TECHNICAL_REFERENCE.md](dev/TECHNICAL_REFERENCE.md).

## The browser IDE

### Can other machines use my web IDE?

Only if you bind it with `--host 0.0.0.0`, and think first: the server has no
authentication, and Python, JavaScript and Perl programs run as real processes
with your permissions. Read [dev/WEB.md](dev/WEB.md#security).

### Is my work saved?

The editor text and language are kept in the browser's `localStorage` and
restored on reload. Use **Save** (Ctrl+S) to download a real file.

### What are the limits?

A run stops at the `--timeout`, after 20,000 lines of output, or after
5 minutes waiting for input. At most four runs at a time; a fifth gets
`too many programs are running, try again` (HTTP 429). Programs are capped at
256 KB.

## Help

### Something's broken.

[TROUBLESHOOTING.md](TROUBLESHOOTING.md) first. If that doesn't cover it, open
an issue at
<https://github.com/James-HoneyBadger/Time_Warp_Classic/issues> with what you
ran, what you saw (paste the exact error), what you expected, your OS and
`python3 --version`, and `python3 Time_Warp.py --version`.
