# Technical Reference - Time Warp Architecture

Complete technical documentation for developers extending Time Warp Classic.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Module Structure](#module-structure)
3. [Core Interpreter](#core-interpreter)
4. [Language Implementations](#language-implementations)
5. [GUI System](#gui-system)
6. [Data Flow](#data-flow)
7. [Extension Points](#extension-points)
8. [Performance Optimization](#performance-optimization)

---

## Architecture Overview

### High-Level Design

Time Warp Classic uses a **modular interpreter architecture** where:
- A thin entry-point (`Time_Warp.py`) launches the application
- The `gui/` package provides the tkinter IDE interface
- A central interpreter engine (`core/interpreter.py`) routes code to language executors
- Language-specific modules in `core/languages/` handle syntax and semantics
- Utility modules handle syntax highlighting and performance optimization

### Design Philosophy

1. **Language Modularity:** Each language is an independent executor, can be added/removed
2. **Clean Separation:** GUI (`gui/`), interpreter logic (`core/`), and languages (`core/languages/`) are separate layers
3. **Extensibility:** Adding new languages requires only a new module and a one-line registration
4. **Performance:** Built-in optimization and caching via `core/optimizations/`

### Component Relationships

```
┌─────────────────────────────────────────────┐
│   Entry Point (Time_Warp.py — thin launcher)│
├─────────────────────────────────────────────┤
│         GUI Frontend  (gui/ package)        │
│  app.py  menus.py  dialogs.py  themes.py   │
├─────────────────────────────────────────────┤
│     Core Interpreter Engine (core/)         │
│  interpreter.py  stubs.py  optimizations/   │
├─────────────────────────────────────────────┤
│     Language Modules (core/languages/)      │
│  base.py  pilot  basic  logo  pascal        │
│  prolog  forth  perl  python  javascript    │
├─────────────────────────────────────────────┤
│         Support Modules                      │
│  Syntax Highlighting · Performance Optimizer │
└─────────────────────────────────────────────┘
```

---

## Module Structure

### Directory Organization

```
Time_Warp_Classic/
├── Time_Warp.py              # Thin entry-point (launches gui.app.TimeWarpApp)
├── run.py                    # Alternative launcher with venv/dependency handling
├── gui/                      # GUI package (tkinter IDE)
│   ├── __init__.py           # Exports TimeWarpApp
│   ├── app.py                # TimeWarpApp class — main IDE window
│   ├── menus.py              # Menu bar construction, language detection
│   ├── dialogs.py            # Find/Replace, Error History, About dialogs
│   └── themes.py             # Themes, fonts, EXT_TO_LANG mapping
├── core/                     # Core interpreter engine
│   ├── __init__.py
│   ├── interpreter.py        # Time_WarpInterpreter class
│   ├── stubs.py              # Placeholder classes for optional features
│   ├── export.py             # .twrun bundles and standalone .pyz runners
│   ├── plugins.py            # Manifest parsing and plugin registry
│   ├── languages/catalog.py  # Language names and extension maps
│   ├── runner.py             # Headless execution used by exports and --run
│   ├── features/             # IDE features
│   │   ├── completion.py     # Word-completion vocabulary and matching
│   │   └── syntax_highlighting.py
│   ├── languages/            # Language executor modules
│   │   ├── __init__.py       # Exports all executors
│   │   ├── base.py           # SubprocessExecutor base class
│   │   ├── basic_console.py  # BASIC direct mode (READY. console)
│   │   ├── pilot.py          # TwPilotExecutor
│   │   ├── basic.py          # TwBasicExecutor
│   │   ├── logo.py           # TwLogoExecutor
│   │   ├── pascal.py         # TwPascalExecutor
│   │   ├── prolog.py         # TwPrologExecutor
│   │   ├── forth.py          # TwForthExecutor
│   │   ├── perl.py           # PerlExecutor (SubprocessExecutor)
│   │   ├── python_executor.py # PythonExecutor (SubprocessExecutor)
│   │   └── javascript_executor.py # JavaScriptExecutor (SubprocessExecutor)
│   ├── optimizations/        # Performance optimization
│   │   ├── __init__.py
│   │   ├── performance_optimizer.py
│   │   ├── memory_manager.py
│   │   └── gui_optimizer.py
│   └── utilities/
│       ├── __init__.py
│       └── safe_eval.py      # AST-based safe expression evaluator
├── docs/                     # Documentation
├── examples/                 # Example programs (one dir per language)
└── scripts/                  # Launch scripts
```

### Core Module Descriptions

#### core/interpreter.py
Central interpreter engine.

**Key Class:**
- `Time_WarpInterpreter` — Main interpreter class

**Key Methods:**
- `execute_line(command)` — Execute a single line of code
- `run_program(code)` — Parse and execute a full program
- `step()` — Execute a single line and pause (debugger)
- `log_output(text)` — Send output to the IDE's output widget
- `log_error(msg, line_num)` — Log an error with formatting and history
- `get_current_time()` — Return ISO-8601 timestamp
- `init_turtle_graphics()` — Set up the turtle graphics system
- `resolve_variables(text)` — Resolve `*VAR*` and `%SYSVAR%` references

**Key Attributes:**
- `variables` — Global variable storage shared across all languages
- `program_lines` — Parsed program lines
- `current_line` — Current execution position
- `error_history` — List of logged errors with timestamps
- `running` — Whether a program is currently executing
- `debug_mode` — Whether debug output is enabled
- `turtle_graphics` — State of the turtle graphics system

#### core/stubs.py
Centralized placeholder classes for optional features (audio, games, hardware, IoT, networking).  These provide no-op implementations so the interpreter can run even without specialized packages like pygame, RPi.GPIO, etc.

**Classes:** `AudioEngine`, `GameManager`, `MultiplayerGameManager`, `CollaborationManager`, `ArduinoController`, `RPiController`, `RobotInterface`, `GameController`, `SensorVisualizer`, `IoTDeviceManager`, `SmartHomeHub`, `SensorNetwork`, `AdvancedRobotInterface`, `Mixer`, `Tween`, `Timer`, `Particle`

#### core/languages/base.py
Base class for language executors that run code via an external subprocess.

**Key Class:**
- `SubprocessExecutor` — Provides temp-file creation, subprocess execution, output capture, cleanup, and executable discovery.

**Subclass Configuration:**
```python
class YourExecutor(SubprocessExecutor):
    lang_name = "YourLang"
    file_suffix = ".ext"
    executable_candidates = ["yourexe", "yourexe2"]
```

#### Language Modules (pilot.py, basic.py, logo.py, etc.)

**Internal executors** (PILOT, BASIC, Logo, Pascal, Prolog, Forth) interpret code in-process. Each has:
- `execute_command(command)` — Execute a single command, return status string

**External executors** (Python, JavaScript, Perl) extend `SubprocessExecutor` and run code as a subprocess:
- `execute_command(command)` — Write to temp file, execute, capture output
- `execute_file(filepath)` — Run an existing source file
- `get_version()` — Return runtime version string

#### features/syntax_highlighting.py
Syntax highlighting and styling.

**Key Classes:**
- `SyntaxHighlighter` — Text coloring based on language-specific patterns

#### web/server.py
Browser front-end: a `ThreadingHTTPServer` serving `web/static/index.html` plus
a JSON/SSE API. `RunnerService` owns language metadata, examples and program
execution, and is usable without HTTP in tests. Every run gets a fresh
interpreter with `console_banner` and `turtle_console` off, a wall-clock
deadline and a concurrency cap. See [WEB.md](WEB.md).

#### export.py and runner.py
Headless execution and packaging. `Time_Warp.py --run` and every exported
runner go through `core.runner.run_source()`, which shares the full
interpreter but writes to stdout and turns reported errors into exit code 1.
`core.export` writes `.twrun` bundles and builds `.pyz` zipapps from a copy of
`core/` plus the embedded program. See [EXPORTING.md](EXPORTING.md).

#### plugins.py
Language plugins: JSON manifests that add an external-runtime language.

**Key API:**
- `parse_manifest(data)` — Validate a decoded manifest, raising `PluginError`
- `discover_plugins(directories)` — `(specs, problems)` from
  `~/.timewarp/plugins` plus `TIMEWARP_PLUGIN_PATH`
- `PluginRegistry.load()` / `.get(name)` / `.executor(interpreter, name)` —
  lookups and cached executors
- `PluginSpec` — the normalised manifest (name, executable, extension, args,
  syntax, comment, keywords, timeout)

Each plugin runs through `core/languages/plugin_executor.py`, a
`SubprocessExecutor` configured from its spec, so it gets streaming output,
stdin routing, the Stop control and clickable error lines for free. See
[PLUGINS.md](PLUGINS.md) for the manifest format.

#### features/completion.py
Word completion for the editor, kept free of Tk so it runs headless.

**Key API:**
- `CompletionEngine.suggestions(language, prefix)` — Words starting with
  *prefix*, exact-case matches first
- `CompletionEngine.completion_at(language, text, cursor, forced=False)` —
  `(start, items)` for the caret, or `None` in comments/strings
- `VOCABULARIES` — Per-language words taken from what each interpreter accepts

The popup itself lives in `gui/completion_popup.py`; the editor binding is
`TimeWarpApp._init_completion()`. Typing two or more word characters opens the
list, Ctrl+Space opens it anywhere, Enter/Tab accept and Escape dismisses it.

#### optimizations/
Performance optimization modules.

- `performance_optimizer.py` — Code caching, expression optimization, profiling
- `memory_manager.py` — Variable scope management, memory limits
- `gui_optimizer.py` — Optional batched-draw/text-refresh helpers

#### utilities/safe_eval.py
AST-based safe expression evaluator that replaces Python's `eval()` throughout the codebase.

**Key Function:**
- `safe_eval(expr, variables, allowed_functions)` — Evaluate a mathematical expression safely

**Safety Model:**
- Parses expressions into an AST (Abstract Syntax Tree) before evaluation
- Only allows: numeric literals, strings, arithmetic operators, comparisons, boolean operators
- Supports whitelisted function calls (e.g., `ABS`, `INT`, `SIN`, `COS`, `SQR`, `RND`)
- Supports variable references, subscripts, and string attribute access
- Rejects any node type not explicitly permitted (no imports, no exec, no file access)

**Used By:** BASIC, Logo, Pascal, and Prolog interpreters for evaluating user expressions safely.

---

## Security Architecture

### Expression Evaluation

All user-provided expressions are evaluated through `core/utilities/safe_eval.py` instead of Python's built-in `eval()`. This prevents arbitrary code execution from user programs.

### Subprocess Isolation

External language executors (Python, JavaScript, Perl) run user code in isolated subprocesses with:
- **30-second timeout** — prevents infinite loops and resource exhaustion
- **Temporary file execution** — code written to temp file, executed, file cleaned up
- **Streamed output** — merged stdout/stderr is forwarded line-by-line as it is produced
  (`stdbuf` forces line buffering; Python runs with `-u`, Perl gets `$| = 1;`)
- **Console input** — lines typed in the IDE console are written to the script's stdin,
  so `input()`, `<>` and `readline` work
- **Error line mapping** — the script line named by the runtime's traceback is reported as
  `?ERROR IN <line>: <message>`, which the IDE makes clickable
- **Stop support** — the IDE's Stop control kills the process immediately
- **No shell=True** — subprocess calls use argument lists, not shell interpretation

### Input Validation

- File paths are validated before use
- Variable names are sanitized
- Expression parsing rejects dangerous constructs at the AST level

---

## Core Interpreter

### Time_WarpInterpreter Class

```python
class Time_WarpInterpreter:
    def __init__(self, output_widget=None):
        self.variables = {}        # Global variable storage
        self.program_lines = []    # Parsed program lines
        self.current_line = 0      # Current execution position
        self.error_history = []    # Error tracking
        self.running = False       # Execution state
        self.debug_mode = False    # Debug output toggle
        self.turtle_graphics = None # Lazy-initialized graphics

        # Language executors (one per language)
        self.pilot_executor = TwPilotExecutor(self)
        self.basic_executor = TwBasicExecutor(self)
        self.logo_executor = TwLogoExecutor(self)
        self.pascal_executor = TwPascalExecutor(self)
        self.prolog_executor = TwPrologExecutor(self)
        self.forth_executor = TwForthExecutor(self)
        self.perl_executor = PerlExecutor(self)
        self.python_executor = PythonExecutor(self)
        self.javascript_executor = JavaScriptExecutor(self)
```

### Execution Flow

1. **Code Input:** User submits code via the GUI editor
2. **Parsing:** `run_program()` splits code into lines
3. **Language Detection:** Each line is routed based on syntax patterns or explicit language mode
4. **Execution:** The appropriate language executor's `execute_command()` is called
5. **Output Capture:** Results routed through `log_output()` to the IDE output widget
6. **Error Handling:** Errors logged via `log_error()` with line numbers and timestamps

While the loop runs it calls `interpreter.pump()` before every line. The host
hooks it relies on are:

| Hook | Purpose |
|------|---------|
| `pump_callback` | Lets the GUI process events so the window stays responsive |
| `stop_requested` | Set by Stop (button or Ctrl+.), ends the run at the next line |
| `input_provider` | Supplies a console line for `INPUT` instead of a modal dialog |
| `max_iterations` | Safety cap for unattended runs; the IDE sets it to `None` |

`run_program()` resets `stop_requested`/`interrupted` per run, and `reset()`
(used by the IDE before each RUN) clears variables and loop stacks so a new
run starts clean.

### Language Detection Strategy

Detects language by looking for:
- Keywords specific to each language (e.g., `T:` for PILOT, `FORWARD` for Logo)
- Line number prefixes (BASIC)
- Stack notation (Forth)
- User selection via language dropdown (highest priority)

**Priority Order:** User selection > Explicit mode > Syntax detection > Default (BASIC)

### Error Handling

- **Syntax Errors:** Invalid syntax, caught during parsing
- **Runtime Errors:** Execution errors, caught per-line with `try/except`
- **Timeout Errors:** External scripts that exceed the 30-second timeout

All errors display in classic form:
- `?ERROR IN <line>: message` (no line number when it is unknown)
- Timestamp (stored in `error_history`)
- `READY.` when execution finishes, or `BREAK IN <line>` when the user stops it

---

## Language Implementations

### Adding a New Language

#### For External-Process Languages (recommended for existing runtimes)

1. **Create language module:** `core/languages/your_lang.py`

2. **Extend `SubprocessExecutor`:**
```python
from .base import SubprocessExecutor

class YourLangExecutor(SubprocessExecutor):
    lang_name = "YourLang"
    file_suffix = ".yl"
    executable_candidates = ["yourlang", "yl"]
```

3. **Register in `core/languages/__init__.py`:**
```python
from .your_lang import YourLangExecutor
# Add to __all__ list
```

4. **Add executor in `core/interpreter.py` `__init__`:**
```python
self.yourlang_executor = YourLangExecutor(self)
```

#### For In-Process Interpreters

1. **Create module** with an executor class accepting `interpreter` reference
2. **Implement `execute_command(command)`** returning `"continue"`, `"error"`, or `"end"`
3. **Register** as above

### Language Architecture Patterns

**Internal executors** (interpret in-process):
```python
class TwYourLangExecutor:
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def execute_command(self, command):
        """Execute a single command. Returns status string."""
        # Parse and execute
        self.interpreter.log_output("result")
        return "continue"
```

**External executors** (delegate to subprocess via `SubprocessExecutor`):
```python
class YourLangExecutor(SubprocessExecutor):
    lang_name = "YourLang"
    file_suffix = ".yl"
    executable_candidates = ["yourlang"]

    def execute_command(self, command):
        # Optional: preprocess before execution
        return super().execute_command(command)
```

### Current Language Implementations

| Language   | File | Executor Class | Type | Features |
|-----------|------|----------------|------|----------|
| PILOT | pilot.py | TwPilotExecutor | Internal | Conditional logic, pattern matching |
| BASIC | basic.py | TwBasicExecutor | Internal | Variables, loops, arrays, subroutines |
| Logo | logo.py | TwLogoExecutor | Internal | Turtle graphics, procedures |
| Pascal | pascal.py | TwPascalExecutor | Internal | Types, procedures, functions |
| Prolog | prolog.py | TwPrologExecutor | Internal | Facts, rules, unification |
| Forth | forth.py | TwForthExecutor | Internal | Stack operations, word definitions |
| Python | python_executor.py | PythonExecutor | External | Full Python 3 via subprocess |
| JavaScript | javascript_executor.py | JavaScriptExecutor | External | Node.js via subprocess |
| Perl | perl.py | PerlExecutor | External | Full Perl via subprocess |

---

## GUI System

### Package Structure

The GUI is organized in the `gui/` package:

```
gui/
├── __init__.py     # Exports TimeWarpApp
├── app.py          # TimeWarpApp — main IDE window and logic
├── menus.py        # build_menu_bar(), detect_language_from_extension()
├── dialogs.py      # FindDialog, ReplaceDialog, show_error_history(), show_about()
└── themes.py       # THEMES, FONT_SIZES, EXT_TO_LANG, SUPPORTED_LANGUAGES
```

### TimeWarpApp (gui/app.py)

The main application class owns the `tk.Tk` root window and orchestrates:
- Editor widget with line numbers and syntax highlighting
- Output display area
- Turtle graphics canvas
- Language selector dropdown
- Settings persistence (recent files, theme, font)

### Menu Bar (gui/menus.py)

`build_menu_bar(app)` constructs all menus:
- **File:** New, Open, Save, Save As, Load Example, Exit
- **Edit:** Undo, Redo, Cut, Copy, Paste, Select All, Find, Replace
- **Program:** Run Program, Load Example
- **Debug:** Debug Mode, Toggle Breakpoint at Cursor (F9), Clear All Breakpoints, Error History
- **Test:** Smoke Test, Full Test Suite
- **Performance:** Show Statistics, Optimize Performance, Toggle Profiling
- **Preferences:** Themes, Font Family, Font Size
- **About:** Version and credits

### Dialogs (gui/dialogs.py)

- `FindDialog` — Ctrl+F search with Next/Previous navigation
- `ReplaceDialog` — Ctrl+H search and replace
- `show_error_history()` — Display logged errors from interpreter
- `show_about()` — Version and credits dialog

### Themes & Configuration (gui/themes.py)

Single source of truth for:
- `THEMES` — 9 color themes (Light, Dark, Solarized, Monokai, etc.)
- `FONT_SIZES` — Named size presets (Small, Medium, Large, Extra Large)
- `EXT_TO_LANG` — File extension to language mapping (unified, no duplicates)
- `SUPPORTED_LANGUAGES` — Ordered list of all supported languages
- `LINE_NUMBER_BG` — Per-theme line number background colors

---

## Data Flow

### Execution Pipeline

```
User Code (editor)
    ↓
gui/app.py  TimeWarpApp.run_code()
    ↓
core/interpreter.py  Time_WarpInterpreter.run_program()
    ↓
Parse into program_lines
    ↓
For each line:  execute_line(command)
    ↓
Route to language executor  (e.g. basic_executor.execute_command())
    ↓
Internal: interpret in-process
External: write temp file → subprocess.run() → capture stdout/stderr
    ↓
log_output() → output widget
    ↓
Display result in GUI
```

### Variable Scope

```
Global Scope  (interpreter.variables)
├── Shared across all languages
├── PILOT system variables
├── BASIC arrays and variables
└── Logo procedures and turtle state
```

Each language executor accesses shared state via `self.interpreter.variables`.

---

## Extension Points

### Adding Features

#### New Language Support

1. Create `core/languages/[lang].py`
2. Implement executor class (extend `SubprocessExecutor` for external runtimes)
3. Register in `core/languages/__init__.py`
4. Add executor instance in `core/interpreter.py` `__init__`
5. Add syntax highlighting patterns (optional)

#### New IDE Features

1. Add feature module to `core/features/`
2. Integrate in `gui/app.py` (for UI) or `core/interpreter.py` (for execution)
3. Add menu items in `gui/menus.py`
4. Implement event handlers

#### New Optimization

1. Create module in `core/optimizations/`
2. Integrate in interpreter initialization
3. Hook into execution pipeline
4. Benchmark improvements

---

## Performance Optimization

### Built-in Optimizations

#### 1. Expression Caching
The interpreter caches evaluated expressions to avoid redundant computation.

#### 2. Memory Management
- Track variable memory usage via `core/optimizations/memory_manager.py`
- Cleanup unused variables
- Limit memory per execution

#### 3. GUI Responsiveness
- The run loop pumps Tk events (`pump_callback`) so the window stays live
- **Performance → Show Statistics** reports measured figures: event pumps/sec,
  pending input lines, scheduled callbacks and output size
- `core/optimizations/gui_optimizer.py` ships batched-draw helpers
  (`OptimizedCanvas`, `AsyncTextUpdate`, `EventBatcher`) for embedders; the IDE
  itself writes directly to its widgets
- Refresh rate limiting

#### 4. Execution Optimization
- Lazy module loading
- Profiling infrastructure

### Benchmarking

Run examples for each language using the IDE's **File → Open Examples** menu, or use the **Test → Run Smoke Test** menu to verify all interpreters.

### Breakpoints

Breakpoints are keyed by the 1-based line number shown in the editor:

```python
interpreter.toggle_breakpoint(20)   # set or clear line 20
interpreter.is_breakpoint(20)       # -> True
interpreter.clear_breakpoints()
```

A run stops before the breakpoint line executes and reports `BREAK IN n`.

### Profiling

Toggle profiling from the **Performance → Toggle Profiling** menu, or
programmatically:
```python
interpreter.set_profiling(True)   # sets both the interpreter and optimizer flags
```

Timings then appear under **Performance → Show Statistics** (`Profiler:`).

---

## Development Workflow

### Setting Up Development Environment

1. **Clone repository:**
```bash
git clone <repo>
cd Time_Warp_Classic
```

2. **Install dependencies** (runtime + dev tools):
```bash
pip install -r requirements-dev.txt
```

3. **Run smoke test:**
```bash
python Time_Warp.py
# Then use Test → Run Smoke Test from the menu
```

4. **Start development:**
```bash
python Time_Warp.py
```

### Code Standards

- Python 3.9+ compatibility
- Type hints where practical
- Docstring documentation
- PEP 8 style guide
- Meaningful variable names

---

**For questions, see:** [../../README.md](../../README.md)
