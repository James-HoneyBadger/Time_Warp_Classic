# Exporting and Headless Runs

Three ways to run a Time Warp program without the IDE window. All three end
up in the same function, `core.runner.run_source()`.

| Form | What it is | Run with |
|------|------------|----------|
| Source file | Plain `.bas`, `.pilot`, `.logo`, ... | `timewarp --run FILE --language LANG` |
| `.twrun` bundle | Small JSON file: language + source | `timewarp --run FILE.twrun` |
| `.pyz` runner | Python zipapp with the interpreter and program inside | `python3 FILE.pyz` |

`timewarp` is the console script installed by `pip install .`. From a
checkout, use `python3 Time_Warp.py` instead.

## Headless runs from the command line

```bash
python3 Time_Warp.py --run hello.bas --language basic
python3 Time_Warp.py -r hello.twrun            # the bundle names its language
python3 Time_Warp.py --version                 # Time Warp Classic 1.6.0
```

| Flag | Meaning |
|------|---------|
| `--run FILE`, `-r FILE` | Run *FILE* and exit. A `.twrun` suffix means a bundle. |
| `--language LANG`, `-l LANG` | Language of a plain source file. Required for one, ignored for a bundle. |
| `--version`, `-V` | Print the version and exit. |

The language name is matched case-insensitively against the nine built-ins
(`pilot`, `basic`, `logo`, `pascal`, `prolog`, `forth`, `python`,
`javascript`, `perl`). The name is not checked. Anything else, including a
typo or a plugin language, makes the interpreter pick a language for each
line by its content (PILOT if nothing else matches), so a wrong name may
still produce output. Plugins are never loaded for headless runs.

### Exit codes

| Code | Name | When |
|------|------|------|
| `0` | `EXIT_OK` (`core/runner.py`) | The program finished and logged no errors |
| `1` | `EXIT_PROGRAM_ERROR` (`core/runner.py`) | The program logged an error (`?ERROR ...`), or the interpreter raised |
| `2` | `EXIT_USAGE` (`Time_Warp.py`) | No such file, `--language` missing for a plain file, or the bundle could not be read |

```
$ printf '10 PRINT 1/0\n' > e.bas
$ python3 Time_Warp.py -r e.bas -l basic; echo "exit=$?"
?ERROR IN 1: Division by zero in expression
?HINT: a value in the expression is 0 - check the divisor before dividing. See docs/languages/BASIC_REFERENCE.md.
exit=1
```

Usage errors print one line starting with `?ERROR:`. Examples:
`?ERROR: no such file: x.bas`,
`?ERROR: --language is required when running a plain source file`, and
`?ERROR: not a Time Warp bundle`.

### What a headless run prints

`run_source()` runs with `console_banner` and `turtle_console` turned off and
no iteration cap. As a result:

- you get only the program's own output plus `?ERROR` and `?HINT` lines.
  `Interpreter ready.`, `READY.` and `Language mode set to` are not printed;
- turtle commands draw onto an in-memory stub and print nothing. A Logo
  square produces no output at all, but `PRINT` still prints;
- an infinite loop runs until you interrupt it. There is no 10,000-line cap
  as there is for a bare interpreter, and no web-style time limit.

Interactive input in the built-in languages works from a terminal.
`INPUT`/`A:` prints the prompt to stdout and reads a line from stdin, so
piping answers in works too:

```bash
printf 'Ada\n' | python3 Time_Warp.py -r ask.bas -l basic
```

When Pillow is not installed, the interpreter prints
`ℹ️  PIL/Pillow not available - image features disabled` to stdout on
import. That line comes before the program's output. Filter it out if you
compare output in scripts, or install Pillow.

## Bundles (`.twrun`)

A bundle is UTF-8 JSON:

```json
{
  "format": "timewarp-run",
  "version": 1,
  "language": "basic",
  "name": "hello",
  "program": "10 PRINT \"HELLO\"\n20 PRINT 6 * 7\n"
}
```

| Key | Rule on load |
|-----|--------------|
| `format` | Must be `"timewarp-run"`, otherwise `not a Time Warp bundle` |
| `version` | Missing means `1`. Anything above `1` is refused as newer than this app supports. |
| `language` | Non-empty string, otherwise `bundle is missing its language` |
| `program` | String, otherwise `bundle is missing its program text` |
| `name` | Optional. Defaults to `"program"`. |

Bundles hold no interpreter code, so they stay small and diff well in
version control. The IDE has no menu item for bundles; write them from
Python (see the [API](#python-api)).

## Standalone runners (`.pyz`)

**File → Export Runner...** in the IDE packs the editor's program and the
`core/` package into a single
[zipapp](https://docs.python.org/3/library/zipapp.html). The program is
stored with the language chosen in the selector, lower-cased, and the name
comes from the file name you pick. The console confirms:

```
Runner written to /home/you/hello.pyz
Run it with: python hello.pyz
```

Running it:

```
$ python3 hello.pyz          # any OS with Python 3.9+
Time Warp Classic - hello
HELLO
42
$ ./hello.pyz                # POSIX: shebang /usr/bin/env python3, mode 755
```

The first line is the runner's banner. After it, output and exit codes are
the same as `--run`.

Contents:

```
hello.pyz
├── __main__.py        # prints the banner, then run_source(PROGRAM, LANGUAGE)
├── program_data.py    # NAME, LANGUAGE, PROGRAM
└── core/              # copy of the core package (no __pycache__ / .pyc)
```

The runner needs nothing from your checkout, and no third-party packages:
without Pygments, Pillow or pygame-ce it works the same, apart from the
Pillow notice. To change the program, export again.

### Language support in runners and `--run`

| Language | Works? |
|----------|--------|
| PILOT, BASIC, Logo, Pascal, Prolog, Forth | Yes, with only Python. `export_language_available()` returns `True` for these. |
| Python, JavaScript, Perl | Only if the runtime is installed where the runner runs. The child reads the runner's own stdin, so `input()` and pipes work. |
| Plugin languages | No. The plugin folder is not read, so the name falls through to line-by-line detection. |

Export from the IDE prints
`Note: <Language> programs need that runtime installed to run.` for every
language outside the first row. For a plugin language that note is
misleading, because the runner cannot run it at all.

Limitations of the subprocess languages under `--run` and in runners:

- If the runtime is missing, the run prints a line such as
  `?JAVASCRIPT NOT FOUND - install it to run these scripts (install Node.js from nodejs.org)`
  and still exits `0`.
- Each script still has the executor's 30-second limit, which includes time
  spent waiting for input from the terminal.

## Python API

`core/export.py`:

| Name | Notes |
|------|-------|
| `RunBundle(language, program, name="program")` | Frozen dataclass. `to_json()` serialises it (raises `BundleError` without a language). `RunBundle.from_json(text)` validates and parses. |
| `write_bundle(bundle, path)` | Writes the JSON and returns the `Path`. |
| `read_bundle(path)` | Returns a `RunBundle`, or raises `BundleError` (also for unreadable files). |
| `build_standalone_runner(bundle, target, package_root=None)` | Builds the `.pyz` and returns its `Path`. *package_root* is the folder holding `core/`, which defaults to the checkout. |
| `export_language_available(language)` | `True` for the six built-in interpreters. |
| `BundleError` | Subclass of `ValueError`. |
| `BUNDLE_FORMAT`, `BUNDLE_VERSION`, `BUNDLE_SUFFIX`, `RUNNER_SUFFIX`, `PACKAGE_ROOT` | `"timewarp-run"`, `1`, `".twrun"`, `".pyz"`, the repository root |

`core/runner.py`:

| Name | Notes |
|------|-------|
| `run_source(program, language, stream=None)` | Runs *program* in a fresh interpreter and returns `EXIT_OK` or `EXIT_PROGRAM_ERROR`. Output is printed to stdout, or to *stream* when one is given. |
| `EXIT_OK`, `EXIT_PROGRAM_ERROR` | `0`, `1` |

Making a bundle and a runner from a source file (run from the repository
root):

```python
from pathlib import Path

from core.export import RunBundle, build_standalone_runner, read_bundle, write_bundle

source = Path("hello.bas").read_text(encoding="utf-8")
bundle = RunBundle(language="basic", program=source, name="hello")
write_bundle(bundle, "hello.twrun")
print(read_bundle("hello.twrun") == bundle)      # True
build_standalone_runner(bundle, "hello.pyz")
```

Capturing output in-process:

```python
import io

from core.runner import run_source

out = io.StringIO()
code = run_source('T:Hello from PILOT\nE:', "pilot", stream=out)
print(code, out.getvalue())     # 0 Hello from PILOT
```

See [TECHNICAL_REFERENCE.md](TECHNICAL_REFERENCE.md#headless-runner-and-cli-corerunnerpy-time_warppy)
for how the runner configures the interpreter.
