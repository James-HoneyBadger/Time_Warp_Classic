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
│   ├── features/             # IDE features
│   │   └── syntax_highlighting.py
│   ├── languages/            # Language executor modules
│   │   ├── __init__.py       # Exports all executors
│   │   ├── base.py           # SubprocessExecutor base class
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
│       └── __init__.py
├── docs/                     # Documentation
├── examples/                 # Example programs (one dir per language)
├── scripts/                  # Launch and test scripts
└── tests/                    # Test suite
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

#### optimizations/
Performance optimization modules.

- `performance_optimizer.py` — Code caching, expression optimization, profiling
- `memory_manager.py` — Variable scope management, memory limits
- `gui_optimizer.py` — Output buffering, refresh rate optimization

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

All errors display:
- Error message with ❌ prefix
- Line number (if available)
- Timestamp (stored in `error_history`)
- Summary at end of execution (error count or success message)

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
- **File:** New, Open, Save, Save As, Recent Files, Examples, Exit
- **Edit:** Undo, Redo, Cut, Copy, Paste, Select All, Find, Replace
- **View:** Themes, Fonts, Font Sizes
- **Run:** Execute, Clear Output, Clear Canvas
- **Tools:** Performance Stats, Profiling, Optimization
- **Test:** Smoke Test, Full Test Suite
- **Help:** About, Documentation, FAQ

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

#### 3. GUI Optimization
- Output buffering via `core/optimizations/gui_optimizer.py`
- Refresh rate limiting

#### 4. Execution Optimization
- Lazy module loading
- Profiling infrastructure

### Benchmarking

Run comprehensive demo for each language:
```bash
python scripts/run_tests.py
```

### Profiling

Toggle profiling from the Tools menu, or programmatically:
```python
interpreter.profile_enabled = True
```

---

## Development Workflow

### Setting Up Development Environment

1. **Clone repository:**
```bash
git clone <repo>
cd Time_Warp_Classic
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run tests:**
```bash
python scripts/run_tests.py
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
