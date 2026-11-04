# Technical Reference

How Time Warp Classic 1.6.0 is put together, and what you can call from your
own code. Every name below exists in the source; when in doubt, the source
wins. Paths are relative to the repository root.

## Contents

1. [Architecture](#architecture)
2. [Repository layout](#repository-layout)
3. [The interpreter](#the-interpreter)
4. [Embedding the interpreter (host hooks)](#embedding-the-interpreter-host-hooks)
5. [Language executors](#language-executors)
6. [Hosts](#hosts)
7. [Support modules](#support-modules)
8. [Safety model](#safety-model)
9. [Adding a language](#adding-a-language)
10. [Development workflow](#development-workflow)

---

## Architecture

One interpreter, several hosts. `core.interpreter.Time_WarpInterpreter` owns
program state and routes each line (or the whole program) to a language
executor. The hosts differ only in where output goes, where input comes from
and how a run is stopped; they talk to the interpreter through a handful of
attributes described in [Embedding the interpreter](#embedding-the-interpreter-host-hooks).

```
            Time_Warp.py  (argparse: IDE, --run, --web, --version)
                 |                 |                    |
       gui/ (Tkinter IDE)   core/runner.py       web/server.py
       TimeWarpApp          run_source()         RunnerService + HTTP/SSE
                 \                 |                    /
                  core/interpreter.py  Time_WarpInterpreter
                  |                                    |
   built-in, in-process executors          subprocess executors
   core/languages/pilot.py  basic.py       core/languages/base.py
   logo.py  pascal.py  prolog.py           SubprocessExecutor
   forth.py                                  python_executor.py
                                             javascript_executor.py
                                             perl.py
                                             plugin_executor.py  <- core/plugins.py
```

- **Built-in languages** (PILOT, BASIC, Logo, Pascal, Prolog, Forth) are
  interpreted in-process, line by line, by the main run loop.
- **External languages** (Python, JavaScript, Perl and any plugin language)
  are run as one script in a child process by `SubprocessExecutor`.
- `core/` has no hard dependency on Tk: `core/interpreter.py` imports
  `tkinter` inside a `try`, so the web server and exported runners work on a
  Python without Tk. `gui/` requires Tk.

---

## Repository layout

```
Time_Warp_Classic/
├── Time_Warp.py              # CLI entry point: main(); `timewarp` console script
├── run.py                    # Setup helper: venv, dependencies, then the IDE
├── core/
│   ├── __init__.py           # __version__ = "1.6.0"; exports Time_WarpInterpreter
│   ├── interpreter.py        # Time_WarpInterpreter
│   ├── runner.py             # run_source(), EXIT_OK, EXIT_PROGRAM_ERROR
│   ├── export.py             # RunBundle, .twrun bundles, .pyz runners
│   ├── plugins.py            # PluginSpec, PluginRegistry, manifest parsing
│   ├── error_hints.py        # hint_for(): "?HINT:" lines
│   ├── stubs.py              # No-op stand-ins for audio/game/hardware/IoT
│   ├── languages/
│   │   ├── __init__.py       # Exports the nine executors + SubprocessExecutor
│   │   ├── base.py           # SubprocessExecutor
│   │   ├── catalog.py        # SUPPORTED_LANGUAGES, EXT_TO_LANG, runtime checks
│   │   ├── pilot.py          # TwPilotExecutor
│   │   ├── basic.py          # TwBasicExecutor
│   │   ├── basic_console.py  # BasicConsole (BASIC direct mode, "READY.")
│   │   ├── logo.py           # TwLogoExecutor
│   │   ├── pascal.py         # TwPascalExecutor
│   │   ├── prolog.py         # TwPrologExecutor
│   │   ├── forth.py          # TwForthExecutor
│   │   ├── python_executor.py      # PythonExecutor
│   │   ├── javascript_executor.py  # JavaScriptExecutor
│   │   ├── perl.py           # PerlExecutor
│   │   └── plugin_executor.py      # PluginExecutor
│   ├── features/
│   │   ├── completion.py     # CompletionEngine (Tk-free)
│   │   └── syntax_highlighting.py  # SyntaxHighlightingText, LineNumberedText (Tk)
│   ├── optimizations/
│   │   ├── performance_optimizer.py  # ExpressionCache, PerformanceProfiler, ...
│   │   ├── memory_manager.py         # ResourceManager, cleanup_all_resources()
│   │   └── gui_optimizer.py          # OptimizedCanvas, AsyncTextUpdate, EventBatcher
│   └── utilities/
│       └── safe_eval.py      # safe_eval(): AST-restricted expression evaluator
├── gui/
│   ├── __init__.py           # Exports TimeWarpApp
│   ├── app.py                # TimeWarpApp: the desktop IDE window
│   ├── menus.py              # build_menu_bar(), detect_language_from_extension()
│   ├── dialogs.py            # FindDialog, ReplaceDialog, show_error_history(), show_about()
│   ├── completion_popup.py   # CompletionPopup
│   └── themes.py             # THEMES, FONT_SIZES, LINE_NUMBER_BG (+ re-exports)
├── web/
│   ├── server.py             # RunnerService, create_server(), serve()
│   ├── canvas.py             # RasterCanvas, decode_rle()
│   ├── highlight.py          # highlight(): Pygments to HTML
│   └── static/index.html     # The browser IDE
├── examples/                 # Package: one folder per language, example_path()
├── scripts/                  # run_tests.py and launch scripts
├── tests/                    # pytest suite
└── docs/
```

---

## The interpreter

`Time_WarpInterpreter(output_widget=None)` in `core/interpreter.py`.

Constructing one creates all nine executors, the optimizer helpers and the
stub subsystems, then logs `Interpreter ready.` (see
[Output](#output) for how hosts keep that out of their console). Importing
the module prints a notice when Pillow is not installed.

### Running a program

```python
from core.interpreter import Time_WarpInterpreter

interp = Time_WarpInterpreter()
interp.run_program('10 PRINT "HELLO"\n20 END', language="basic")
```

`run_program(program_text, language=None)` does, in order:

1. Clears `error_history`, `stop_requested` and `interrupted`.
2. If *language* is given, stores it lower-cased in `current_language` and
   `current_language_mode`. Names are not validated here.
3. **Subprocess languages** (`python`, `javascript`, `perl`): the whole text
   goes to that executor's `execute_command()` in one call. A plugin language
   (looked up in `interp.plugins`) takes the same path. Afterwards it logs
   `READY.`, or `BREAK` if the user stopped it.
4. **Built-in languages**: Logo source is first passed through
   `_preprocess_logo_program()` (joins multi-line `REPEAT [...]` blocks), then
   `load_program()` splits the text into `program_lines` and collects PILOT
   `L:` labels. The run loop then, for each line:
   - stops after `max_iterations` lines with an error, if a cap is set;
   - calls `pump()` and breaks if a stop was requested;
   - stops at a breakpoint (only when `debug_mode` is on);
   - calls `execute_line()` and acts on the status it returns.
5. On exit it prints `READY.` (if `console_banner`) or `BREAK IN n` (if
   interrupted).

`run_program()` returns `True` in normal use. It keeps `variables` between
runs; call `reset()` first for a clean slate, which is what the IDE does
before each RUN.

### Executor status codes

`execute_line()` and every executor's `execute_command()` return a string the
run loop understands:

| Status | Meaning |
|--------|---------|
| `"continue"` | Go to the next line |
| `"end"` | Stop the program normally |
| `"jump:N"` | Continue at `program_lines[N]` (0-based index; `N == len(program_lines)` means "past the end") |
| `"error"` | Stop (in debug mode: log a notice and carry on) |
| `"stopped"` | Subprocess executors only: the user stopped the child process |

Anything else is treated as `"continue"`.

### Line dispatch and language detection

`execute_line(line)` strips a leading BASIC line number (only when the mode is
BASIC or unset), skips whole-line `;` and `#` comments (except in Forth, where
`;` ends a definition), then asks `determine_command_type(command,
language_mode)` which executor gets the line:

1. **Explicit mode wins.** If `current_language_mode` is one of the nine
   built-in names, that language is used for every line. PILOT mode is the
   exception: lines without a `:` (and not starting with `*`) fall through to
   the detection below.
2. Otherwise the first matching rule applies: second character `:` → PILOT;
   `?-`, `:-` or `LISTING`/`TRACE`/`NOTRACE` → Prolog; a BASIC keyword or
   `GAME*` → BASIC; a Forth word or leading `:` → Forth; a Pascal keyword or
   `:=` → Pascal; a Logo turtle command → Logo.
3. Default: **PILOT**.

`set_language_mode(mode)` sets the mode, accepting only the nine built-in
lower-case names (anything else logs `Invalid language mode: ...`).

### Interpreter attributes

State that executors share:

| Attribute | Purpose |
|-----------|---------|
| `variables` | Global variable dict shared by all built-in languages |
| `labels` | PILOT label name → program line index |
| `program_lines` | `[(line_number_or_None, command), ...]` from `load_program()` |
| `source_lines` | Editor line number for each parsed line (`source_line(i)` reads it) |
| `current_line` | 0-based index of the executing line |
| `stack`, `for_stack`, `do_stack`, `while_stack`, `select_stack` | BASIC control-flow stacks |
| `match_flag` | PILOT `Y:`/`N:` match result |
| `running` | True while the run loop is active |
| `current_language_mode`, `current_language` | Language set by `run_program()` / `set_language_mode()` |
| `error_history` | List of `{"message", "line", "hint", "timestamp"}` dicts, cleared per run |
| `breakpoints` | Set of **0-based** line indexes (use the 1-based methods below) |
| `debug_mode` | Enables breakpoints, debug trace lines and continue-after-error |
| `turtle_graphics` | Turtle state dict, `None` until `init_turtle_graphics()` |
| `logo_procedures`, `logo_arrays`, `property_lists` | Logo data |
| `pilot_executor`, `basic_executor`, `logo_executor`, `pascal_executor`, `prolog_executor`, `forth_executor`, `perl_executor`, `python_executor`, `javascript_executor` | The executor instances |

### Interpreter methods

| Method | Notes |
|--------|-------|
| `run_program(program_text, language=None)` | See above |
| `load_program(program_text)` | Parse into `program_lines`; keeps `variables`; returns `True` |
| `execute_line(line)` | Run one line, return a status code |
| `step()` | Execute `program_lines[current_line]` and advance (or jump). Needs `load_program()` first. Not bound to any menu in the IDE. |
| `reset()` | Clear variables, labels, program, `stack`/`for_stack`, PILOT match state and the stop flags |
| `stop_program()` | Set `stop_requested`, clear `running` |
| `pump()` | Call `pump_callback` (exceptions are swallowed); return `stop_requested` |
| `get_user_input(prompt="")` | See [Input](#input) |
| `log_output(text)` | See [Output](#output) |
| `log_error(error_msg, line_num=None)` | Format, record and print an error (see [Errors](#errors)) |
| `debug_output(text)` | `log_output()` only when `debug_mode` is on |
| `turtle_log(text)` | `log_output()` only when `turtle_console` is on |
| `evaluate_expression(expr)` | BASIC/PILOT expressions through `safe_eval`, cached when `enable_caching` |
| `resolve_variables(text)` | Replace `*VAR*` and `%sysvar%` (PILOT system variables) |
| `interpolate_text(text)` | Replace `*VAR*`, `{VAR}`, `[VAR]` and evaluate `*expr*` (PILOT `T:`) |
| `toggle_breakpoint(n)` / `is_breakpoint(n)` / `clear_breakpoints()` | `n` is the 1-based editor line |
| `set_debug_mode(enabled)` | Sets `debug_mode` |
| `set_profiling(enabled)` | Turns line timing on/off; returns `False` if the optimizer is unavailable |
| `source_line(index)` | Editor line for a `program_lines` index |
| `get_current_time()` | Static; ISO-8601 timestamp |
| `init_turtle_graphics()`, `turtle_forward()`, `turtle_turn()`, `turtle_setxy()`, `turtle_circle()`, ... | Turtle primitives used by Logo, BASIC and PILOT |

### Errors

`log_error(msg, line_num)` prints `?ERROR IN n: msg`, or `?ERROR: msg` when no
line is known. During a run a missing `line_num` defaults to the executing
editor line. If `error_hints` is on and a rule in `core/error_hints.py`
matches, a second line follows:

```
?ERROR IN 1: Division by zero in expression
?HINT: a value in the expression is 0 - check the divisor before dividing. See docs/languages/BASIC_REFERENCE.md.
```

The run ends with `READY.`, `BREAK IN n` (stopped mid-run or at a
breakpoint) or `BREAK` (subprocess language stopped). In the IDE, clicking an
output line containing `ERROR IN n` or `BREAK IN n` jumps to editor line n.

Subprocess executors map the runtime's own traceback to the script line:
the Python `File "...", line N`, Node `at ...:N:M` or Perl `... line N` that
names the temporary script file becomes `?ERROR IN N: <last error line>`.

### Breakpoints and debug mode

```python
interp.set_debug_mode(True)     # breakpoints are ignored without this
interp.toggle_breakpoint(2)     # 1-based editor line
interp.run_program('10 PRINT "A"\n20 PRINT "B"', language="basic")
# debug trace lines, A, then "BREAK IN 2"; interp.interrupted is True
```

In the IDE, **Debug → Enable Debug Mode** must be ticked for **F9**
breakpoints to stop a run. Debug mode also logs each line before it runs and
lets a run continue past `"error"` statuses.

### Turtle graphics

`init_turtle_graphics()` creates the `turtle_graphics` dict (position,
heading, pen state, colours, drawn items). It draws on `ide_turtle_canvas`
when the host sets one. Any object with the Tk canvas calls the turtle code
uses will do: the desktop passes a `tk.Canvas`, the web server a
`web.canvas.RasterCanvas` (`winfo_width/height`, `update_idletasks`, `bind`,
`create_line/polygon/oval/rectangle/text/image`, `delete`). With no canvas, a
headless stub records each drawing call in `turtle_graphics["canvas"].created`.

### Profiling and the expression cache

When `core/optimizations/performance_optimizer.py` imports (it always should),
the constructor attaches an `OptimizedInterpreterMixin` as `interp.optimizations`
and copies its helpers onto the interpreter: `expression_cache`, `profiler`,
`enable_caching` (default `True`), `enable_profiling` (default `False`),
`get_performance_stats()`, `optimize_for_production()`,
`cleanup_resources()`. Expressions containing `RND` are never cached. Use
`set_profiling(True)` rather than setting the flag yourself: the interpreter
and the optimizer each keep one. Timings appear under
**Performance → Show Statistics**.

---

## Embedding the interpreter (host hooks)

These attributes are how the desktop IDE, the web server and the headless
runner adapt the same interpreter. Set them after construction.

| Attribute | Default | Used for |
|-----------|---------|----------|
| `output_widget` | constructor arg | Object with `insert("end", text)` and `see("end")`; `None` prints to stdout |
| `log_output` | method | Replace it with your own callable to capture all output |
| `console_banner` | `True` | `False` drops `READY.` and `Language mode set to: ...` |
| `turtle_console` | `True` | `False` silences `turtle_log()` chatter (`Turtle moved`, `Pen up ...`) for hosts that show the canvas or have none |
| `error_hints` | `True` | `False` drops `?HINT:` lines |
| `pump_callback` | `None` | Called before every line and while a child process runs; keep the UI alive or enforce a deadline here |
| `stop_requested` | `False` | Set by `stop_program()`; checked by `pump()` |
| `interrupted` | `False` | True after a run ended through a stop or breakpoint |
| `input_provider` | `None` | `callable(prompt) -> str or None`; `None` cancels the run |
| `input_buffer` | `[]` | Lines queued for `INPUT`, and the stdin feed for child processes |
| `subprocess_stdin_pipe` | `True` | `False` lets child processes inherit the host's stdin (used by `--run`) instead of a pipe fed from `input_buffer` |
| `max_iterations` | `10000` | Line-execution cap for built-in languages; `None` removes it |
| `ide_turtle_canvas` | `None` | Canvas for turtle graphics |
| `plugins` | `None` | A `core.plugins.PluginRegistry`; without it plugin languages are unknown |

### Output

`log_output(text)` writes to `output_widget` if there is one, otherwise
`print()`s. Errors (`log_error`), debug lines and child-process output all go
through it, so replacing it captures everything:

```python
import contextlib
import io

from core.interpreter import Time_WarpInterpreter

with contextlib.redirect_stdout(io.StringIO()):  # hide "Interpreter ready."
    interp = Time_WarpInterpreter()

lines = []
interp.log_output = lambda text: lines.append(str(text))
interp.console_banner = False
interp.turtle_console = False
interp.max_iterations = None
answers = iter(["Ada"])
interp.input_provider = lambda prompt: next(answers, None)

interp.run_program('10 INPUT "NAME"; N$\n20 PRINT "HELLO "; N$', language="basic")
print(lines)                 # ['NAME ', 'HELLO Ada']
print(interp.error_history)  # []
```

The banner is logged inside the constructor, before you can configure
anything; the runner and the web server redirect stdout around the
constructor, the IDE's REPL passes a throw-away widget and swaps in the real
one afterwards.

### Input

`get_user_input(prompt)` (used by BASIC `INPUT`, PILOT `A:` and friends)
tries, in order:

1. `input_buffer` – pops the first queued line and echoes it;
2. `input_provider(prompt)` – a `None` result sets `stop_requested` and
   returns `""`, so the run ends with `BREAK`;
3. a Tk `simpledialog` if `output_widget` is set;
4. `input(prompt)` on the console.

Child processes (Python, JavaScript, Perl, plugins) do not use
`input_provider`: their stdin is a pipe fed from `input_buffer` while they
run. A host that wants `input()` in a Python program to work must append
lines to `interp.input_buffer`. A terminal host can set
`subprocess_stdin_pipe = False` so the child reads the real stdin, as
`core/runner.py` does.

### Stopping

Call `interp.stop_program()` from your pump callback, another thread or a UI
handler. Built-in languages stop at the next line (`BREAK IN n`); a child
process is killed at the next poll (every 50 ms) and the run ends with
`BREAK`. A wall-clock limit is a pump callback:

```python
import time

deadline = time.monotonic() + 0.5

def pump():
    if time.monotonic() > deadline:
        interp.stop_program()

interp.pump_callback = pump
interp.run_program("10 GOTO 10", language="basic")   # prints BREAK IN 1
```

---

## Language executors

### Built-in executors

`TwPilotExecutor`, `TwBasicExecutor`, `TwLogoExecutor`, `TwPascalExecutor`,
`TwPrologExecutor` and `TwForthExecutor` take the interpreter in
`__init__(self, interpreter)` and implement `execute_command(command)`,
returning a status code. They read and write shared state through
`self.interpreter` (`variables`, `log_output()`, `log_error()`,
`get_user_input()`, `evaluate_expression()`, the turtle methods). Some
languages keep extra state on the executor (Forth's stack and dictionary,
Prolog's database). Language syntax is documented in
[../languages/](../languages/).

| Language | Module | Class |
|----------|--------|-------|
| PILOT | `pilot.py` | `TwPilotExecutor` |
| BASIC | `basic.py` | `TwBasicExecutor` |
| Logo | `logo.py` | `TwLogoExecutor` |
| Pascal | `pascal.py` | `TwPascalExecutor` |
| Prolog | `prolog.py` | `TwPrologExecutor` |
| Forth | `forth.py` | `TwForthExecutor` |

### SubprocessExecutor (`core/languages/base.py`)

Base class for anything that runs in a child process. Subclasses set class
attributes and usually nothing else:

| Attribute | Default | Meaning |
|-----------|---------|---------|
| `lang_name` | `"Unknown"` | Used in messages (`?PERL NOT FOUND ...`) and hints |
| `file_suffix` | `".txt"` | Suffix of the temporary script file |
| `executable_candidates` | `[]` | Tried in order; the first that exits 0 on `--version` is used |
| `extra_args` | `()` | Inserted between the executable and the script path |
| `timeout` | `30` | Seconds before the child is killed and a timeout error logged |

| Method | Notes |
|--------|-------|
| `execute_command(command)` | Run the text as one script; returns `"continue"`, `"error"` or `"stopped"` |
| `execute_file(filepath)` | Run an existing file without streaming; returns `bool` |
| `get_version()` | First line of `--version` output, or `"<lang> not available"` |
| `missing_runtime_message()` | `?<LANG> NOT FOUND - install it ...` plus the catalog hint |
| `executable` | Resolved at construction; `None` if no candidate worked |

`_execute_script()` writes a temp file and runs
`[executable, *extra_args, path]` with `subprocess.Popen` (no shell), stdout
and stderr merged. On POSIX it prefixes `stdbuf -oL -eL` when available. A
reader thread feeds lines back; each is passed to `log_output()` as it
arrives, `input_buffer` is drained into stdin, and `interpreter.pump()` is
called between polls. Non-zero exit becomes a `log_error()` with the mapped
line. The temp file is deleted afterwards.

| Class | Module | Runtime | Specifics |
|-------|--------|---------|-----------|
| `PythonExecutor` | `python_executor.py` | `sys.executable`, then `python3`, `python` | `extra_args = ("-u",)` |
| `JavaScriptExecutor` | `javascript_executor.py` | `node`, `nodejs` | |
| `PerlExecutor` | `perl.py` | `perl`, `perl5` | Prepends `$| = 1; ` on line 1 so output streams and line numbers still match |
| `PluginExecutor` | `plugin_executor.py` | the manifest's `executable` | Configured per instance from a `PluginSpec`; finds the executable with `shutil.which()` or an existing path, no `--version` probe |

A missing runtime is reported with `log_output()`, not `log_error()`, so it
does not appear in `error_history`.

### Plugins (`core/plugins.py`)

JSON manifests add external-runtime languages without code. The manifest
format is in [PLUGINS.md](PLUGINS.md); the API:

| Name | Notes |
|------|-------|
| `parse_manifest(data, source=None)` | Validate a decoded manifest; returns `PluginSpec` or raises `PluginError` |
| `plugin_directories(directories=None)` | `[DEFAULT_PLUGIN_DIR, *TIMEWARP_PLUGIN_PATH entries]` unless given explicitly |
| `discover_plugins(directories=None)` | `(specs, problems)`; problems are strings |
| `PluginSpec` | Frozen dataclass: `name`, `executable`, `extension`, `args`, `syntax`, `comment`, `keywords`, `timeout`, `description`, `source`; `.language`, `.to_manifest()` |
| `PluginRegistry.load(directories=None)` | Discover and build a registry |
| `registry.names()`, `get(name)`, `extension_map()`, `problems`, `len()`, iteration | Lookups; names are case-insensitive |
| `registry.executor(interpreter, name)` | Cached `PluginExecutor`, or `None` |
| `PluginRegistry.write_example(directory=None)` | Writes `example-python.json` (does not overwrite) |
| `DEFAULT_PLUGIN_DIR`, `PLUGIN_PATH_ENV`, `RESERVED_LANGUAGES`, `DEFAULT_TIMEOUT` | Constants |

```python
from core.plugins import PluginRegistry

registry = PluginRegistry.load()          # ~/.timewarp/plugins + TIMEWARP_PLUGIN_PATH
interp.plugins = registry
interp.run_program('puts "hi"', language="Ruby")
```

`executor()` caches one `PluginExecutor` per language for the life of the
registry, bound to the interpreter that asked first. Later interpreters that
share the registry run the plugin through that first interpreter's
`log_output` and `pump()`. Give each long-lived interpreter its own
registry if that matters to your host.

### Language catalog (`core/languages/catalog.py`)

Tk-free metadata used by every host (`gui.themes` re-exports the first two):

| Name | Notes |
|------|-------|
| `SUPPORTED_LANGUAGES` | The nine display names, in selector order |
| `EXT_TO_LANG` | Extension → display name (`.pl` is Perl here; the IDE's `detect_language_from_extension()` can pick Prolog from content) |
| `LANGUAGE_EXTENSIONS` | Lower-case name → default Save As suffix |
| `language_extension(language)` / `extension_language(ext)` | Lookups with `.txt` / `None` fallbacks |
| `required_runtime(language)` | Commands needed (`("node", "nodejs")` for JavaScript, `("perl",)` for Perl, else `()`) |
| `runtime_available(language, executable=None)` | `PATH` check; *executable* is used for plugins |
| `missing_runtime_hint(language)` | Install suggestion, or `""` |

---

## Hosts

### Desktop IDE (`gui/`)

`TimeWarpApp()` builds the Tk root, layout, interpreter, completion and menus;
`run()` enters the main loop. Key wiring, from `_init_interpreter()`:

```python
self.interpreter = Time_WarpInterpreter(self.output_text)
self.interpreter.ide_turtle_canvas = self.turtle_canvas
self.interpreter.input_buffer = self.input_buffer      # shared with the console bar
self.interpreter.pump_callback = self._pump_events     # root.update() at most every 30 ms
self.interpreter.input_provider = self._request_input  # waits for the console bar
self.interpreter.max_iterations = None                 # Stop replaces the cap
self.interpreter.plugins = self.plugins
```

- **Run** (`run_code()`, F5): resets the interpreter (and the turtle for
  Logo), then calls `run_program()` on the Tk thread. **Stop** (button or
  Ctrl+.) calls `interpreter.stop_program()`.
- **Console bar** (`_submit_input()`): while a program runs, lines go to
  `input_buffer`. Otherwise BASIC lines go to
  `core.languages.basic_console.BasicConsole` (direct mode: `LIST`, `RUN`,
  `NEW`, `RENUMBER`, numbered-line editing, immediate statements); other
  languages go to a persistent REPL interpreter (`_repl_session()`) with a
  2-second per-line limit (`REPL_LINE_TIMEOUT`).
- **Plugins**: loaded at start-up into `self.plugins`; **Preferences →
  Plugins** offers *Reload Plugins*, *Create Example Plugin* and *Open Plugins
  Folder*.
- **Settings** persist to `~/.timewarp_settings.json` (theme, font size, font
  family, completion on/off).

Menus (`gui/menus.py`, `build_menu_bar(app)`):

| Menu | Entries |
|------|---------|
| File | New File, Open File..., Save, Save As..., Export Runner..., Exit |
| Edit | Undo, Redo, Cut, Copy, Paste, Select All, Find..., Replace..., Complete Word |
| Program | Run Program, Open Web IDE, Reset Console REPL, Load Example ▸ |
| Debug | Enable Debug Mode, Toggle Breakpoint at Cursor (F9), Clear All Breakpoints, Show Error History, Clear Error History |
| Test | Run Smoke Test, Run Full Test Suite (`scripts/run_tests.py`) |
| Performance | Show Statistics, Optimize Performance, Toggle Profiling |
| Preferences | Color Theme ▸, Font Family ▸, Font Size ▸, Auto-complete Words, Plugins ▸ |
| About | About Time Warp Classic |

`gui/themes.py` defines `THEMES` (nine: `light`, `dark`, `classic`,
`solarized_dark`, `solarized_light`, `monokai`, `dracula`, `nord`,
`high_contrast`), `LINE_NUMBER_BG` and `FONT_SIZES` (seven: `tiny` 8pt to
`xxxlarge` 22pt). `gui/dialogs.py` provides `FindDialog`, `ReplaceDialog`,
`show_error_history(parent, interpreter)` and `show_about(parent)`.

The editor widget is `SyntaxHighlightingText` from
`core/features/syntax_highlighting.py`: Pygments lexers for BASIC (Commodore
BASIC lexer), Pascal, Prolog, Forth, Perl, Python and JavaScript, small regex
rule sets for Logo and PILOT, and `get_lexer_by_name()` for plugin `syntax`
aliases (unknown aliases fall back to plain text).

### Headless runner and CLI (`core/runner.py`, `Time_Warp.py`)

`run_source(program, language, stream=None)` builds a fresh interpreter with
the banner suppressed, `max_iterations = None`, `console_banner = False` and
`turtle_console = False`, runs the program and returns `EXIT_OK` (0) or
`EXIT_PROGRAM_ERROR` (1, when `error_history` is non-empty or an exception
escaped). With *stream*, `log_output` writes there instead of stdout. It does
not set `plugins`, `input_provider` or `ide_turtle_canvas`.

`Time_Warp.py` (installed as `timewarp`):

| Flag | Effect |
|------|--------|
| *(none)* | Open the desktop IDE |
| `--run FILE`, `-r FILE` | Run a `.twrun` bundle or a source file headlessly |
| `--language LANG`, `-l LANG` | Language for a plain source file (required with one) |
| `--version`, `-V` | Print `Time Warp Classic 1.6.0` |
| `--web` | Serve the browser IDE |
| `--host HOST` | Address for `--web` (default `127.0.0.1`) |
| `--port PORT` | Port for `--web` (default `8000`, `0` picks a free one) |
| `--timeout SECONDS` | Per-run limit for `--web` (default `10`) |

Exit codes: `0` success, `1` program error (or the IDE failed to launch), `2`
bad invocation (`EXIT_USAGE`: missing file, missing `--language`, unreadable
bundle). Export formats and runner behaviour are in [EXPORTING.md](EXPORTING.md).

### Web IDE (`web/`)

`web/server.py` serves `web/static/index.html` and a JSON/Server-Sent-Events
API from a standard-library `ThreadingHTTPServer` (`TimeWarpWebServer`).
`RunnerService` holds the language list, examples, REPL sessions and
`run()`, and works without HTTP (the tests use it directly). Each run gets a
fresh interpreter with `console_banner` and `turtle_console` off, its own
`log_output` sink, a `RasterCanvas`, a wall-clock limit enforced from the
pump callback and an input provider fed by the browser. At most four runs
execute at once. `create_server(host, port, timeout, plugins, verbose)`
builds a server; `serve(...)` runs one until Ctrl+C or SIGTERM. Plugins are
available only when the desktop IDE starts the server (**Program → Open Web
IDE** passes its registry); `--web` starts with none.

`web/canvas.py` turns turtle drawing into palette-indexed, run-length-encoded
frames (`RasterCanvas.frame()`, `decode_rle()`); `web/highlight.py`
renders source to HTML with Pygments (`highlight(language, source,
alias=None)`), returning escaped plain text when Pygments is missing.

Endpoints, events and limits are documented in [WEB.md](WEB.md).

---

## Support modules

| Module | What it provides |
|--------|------------------|
| `core/error_hints.py` | `hint_for(message, language=None)`: first matching regex rule → one-line hint plus a pointer to `docs/languages/<LANG>_REFERENCE.md`, or `None` |
| `core/utilities/safe_eval.py` | `safe_eval(expr, names=None)`; see [Safety model](#safety-model) |
| `core/features/completion.py` | `CompletionEngine`: `suggestions(language, prefix, limit=12)`, `completion_at(language, text, cursor, limit=12, forced=False)` → `(start, items)` or `None`, `register(language, words, comment="")` for plugins, `vocabulary(language)`; module-level `VOCABULARIES` |
| `gui/completion_popup.py` | `CompletionPopup`, the Tk list shown by the editor |
| `core/stubs.py` | No-op `AudioEngine`, `GameManager`, `MultiplayerGameManager`, `CollaborationManager`, `ArduinoController`, `RPiController`, `RobotInterface`, `GameController`, `SensorVisualizer`, `IoTDeviceManager`, `SmartHomeHub`, `SensorNetwork`, `AdvancedRobotInterface`, `Mixer`, `Tween`, `Timer`, `Particle`, so commands that reach for them do not crash |
| `core/optimizations/performance_optimizer.py` | `ExpressionCache`, `LazyLoader`, `PerformanceProfiler`, `MemoryOptimizer`, `OptimizedInterpreterMixin` (attached to every interpreter) |
| `core/optimizations/memory_manager.py` | `MemoryPool`, `ResourceManager`, `MemoryMonitor`, `cleanup_all_resources()` (called by **Performance → Optimize Performance**); it does not limit program memory |
| `core/optimizations/gui_optimizer.py` | `OptimizedCanvas`, `AsyncTextUpdate`, `EventBatcher`, `GUIOptimizer` for embedders; the IDE writes to its widgets directly |

```python
from core.features.completion import CompletionEngine
from core.utilities.safe_eval import safe_eval

safe_eval("ABS(X) * 2 + 1", {"X": -4, "ABS": abs})            # 9
CompletionEngine().completion_at("basic", "10 PR", 5)         # (3, ['PRINT', 'PRESET'])
```

---

## Safety model

**Expressions.** User expressions in BASIC/PILOT (`evaluate_expression()`),
Logo, Pascal and Prolog go through `safe_eval()`, never `eval()`. It parses
with `ast` in `eval` mode and allows only literals, arithmetic, bitwise,
boolean and comparison operators, conditional expressions, subscripts, names
and calls present in the *names* dict, and a fixed list of string methods.
Everything else raises `ValueError`:

```python
safe_eval('__import__("os")')   # ValueError: Undefined name: '__import__'
```

**Child processes.** Python, JavaScript, Perl and plugin programs run in a
separate process with argument lists (no `shell=True`), a timeout (30 s by
default, per plugin otherwise) and a temp file that is removed afterwards.
They run with your user's permissions and full access to the file system and
network: the process boundary protects the IDE, not the machine.

**PILOT `XS:`** runs a host command (split with `shlex`, no shell, 10 s
limit). Bear that in mind before exposing the web server beyond loopback.

---

## Adding a language

**External runtime?** Write a plugin manifest ([PLUGINS.md](PLUGINS.md)). No
code changes, and it gets streaming output, stdin, Stop and clickable errors.

**Built-in language.** There is no single registration point; a new
language touches each place the existing nine are listed:

1. `core/languages/<lang>.py`: a class with `__init__(self, interpreter)` and
   `execute_command(self, command)` returning a status code. For an external
   runtime, subclass `SubprocessExecutor` and set `lang_name`,
   `file_suffix`, `executable_candidates` (and `extra_args` if needed).
2. `core/languages/__init__.py`: import it and add it to `__all__`.
3. `core/interpreter.py`:
   - create the instance in `__init__` (`self.<lang>_executor = ...`);
   - add the name to `valid_modes` in `set_language_mode()`;
   - add an explicit-mode branch in `determine_command_type()`;
   - add a dispatch branch in `_execute_line_original()`;
   - for a subprocess language, add it to `_SUBPROCESS_LANGUAGES` and to the
     table in `_run_subprocess_program()`.
4. `core/languages/catalog.py`: `SUPPORTED_LANGUAGES`, `EXT_TO_LANG`,
   `LANGUAGE_EXTENSIONS`, and `RUNTIME_COMMANDS`/`INSTALL_HINTS` if it needs
   a runtime.
5. `core/plugins.py`: add the lower-case name to `RESERVED_LANGUAGES`.
6. `core/export.py`: add it to `export_language_available()` if it runs
   without an external runtime.
7. Editor support: `VOCABULARIES` (and comment/string tables) in
   `core/features/completion.py`, the lexer map in
   `core/features/syntax_highlighting.py`, `lang_to_syntax` in
   `TimeWarpApp._on_language_change()`, `ALIASES` in `web/highlight.py`.
8. `core/error_hints.py`: `_LANGUAGE_DOCS`, plus a reference page in
   `docs/languages/`.
9. Optional: examples in `examples/<lang>/` and the `_EXAMPLES` list in
   `gui/menus.py`; graphics languages also go in
   `TimeWarpApp._GRAPHICS_LANGUAGES`.

Add tests next to `tests/test_languages_builtin.py` or
`tests/test_subprocess_features.py`.

```python
from core.languages.base import SubprocessExecutor


class RubyExecutor(SubprocessExecutor):
    lang_name = "Ruby"
    file_suffix = ".rb"
    executable_candidates = ["ruby"]
```

---

## Development workflow

```bash
git clone <repo> && cd Time_Warp_Classic
python3 -m pip install -r requirements-dev.txt   # runtime deps + pytest, black, flake8
python3 -m pytest                                 # whole suite
python3 -m pytest tests/test_plugins.py -q        # one file
python3 Time_Warp.py                              # the IDE
python3 Time_Warp.py --run examples/basic/INDEX.bas --language basic
```

- Python 3.9 or newer (`requires-python = ">=3.9"`).
- Tests marked `gui` need a display and Tk; the rest run headless.
- Coverage is opt-in: `python3 -m pytest --cov` (needs `pytest-cov`).
- Style: `black`, and `flake8` with the repository's `.flake8`
  (max line length 88).
- Runtime dependencies (`requirements.txt`): `pygments` for highlighting,
  `Pillow` for images, `pygame-ce`; all are optional at import time. `psutil`
  (extra `metrics`) adds real memory figures to **Show Statistics**.

See also: [../../README.md](../../README.md), [WEB.md](WEB.md),
[PLUGINS.md](PLUGINS.md), [EXPORTING.md](EXPORTING.md).
