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
- A central interpreter engine parses and executes code
- Language-specific modules handle syntax and semantics
- A tkinter GUI provides the IDE interface
- Utility modules handle optimization, highlighting, and templates

### Design Philosophy

1. **Language Modularity:** Each language is independent, can be added/removed
2. **Clean Separation:** UI, interpreter logic, and languages are separate layers
3. **Extensibility:** Adding new languages requires only a new module
4. **Performance:** Built-in optimization and caching mechanisms

### Component Relationships

```
┌─────────────────────────────────────────────┐
│           GUI Frontend (tkinter)            │
├─────────────────────────────────────────────┤
│              IDE Features                    │
│  - Editor  - Output - Buttons - Menu        │
├─────────────────────────────────────────────┤
│          Core Interpreter Engine             │
│  - Parse code - Detect language - Execute   │
├─────────────────────────────────────────────┤
│    Language Modules (9 languages)           │
│  - Parser - Validator - Executor            │
├─────────────────────────────────────────────┤
│         Support Modules                      │
│  - Syntax Highlighting - Templates - Utils  │
└─────────────────────────────────────────────┘
```

---

## Module Structure

### Directory Organization

```
Time_Warp_Classic/
├── Time_Warp.py              # Main entry point
├── core/                     # Core interpreter
│   ├── __init__.py
│   ├── interpreter.py        # Main interpreter class
│   ├── features/             # IDE features
│   │   ├── code_templates.py
│   │   └── syntax_highlighting.py
│   ├── languages/            # Language implementations
│   │   ├── __init__.py
│   │   ├── basic.py
│   │   ├── python_executor.py
│   │   ├── python.py
│   │   ├── javascript.py
│   │   ├── javascript_executor.py
│   │   ├── pascal.py
│   │   ├── prolog.py
│   │   ├── forth.py
│   │   ├── perl.py
│   │   ├── logo.py
│   │   └── pilot.py
│   └── optimizations/        # Performance optimization
│       ├── __init__.py
│       ├── performance_optimizer.py
│       ├── memory_manager.py
│       └── gui_optimizer.py
└── docs/                     # Documentation
```

### Core Module Descriptions

#### interpreter.py
Central interpreter engine

**Key Classes:**
- `Interpreter` - Main interpreter class
- Handles code execution, language detection, error handling

**Key Methods:**
- `execute()` - Run code, return output
- `detect_language()` - Identify language from syntax
- `format_output()` - Process execution results
- `register_language()` - Add new language support

#### Language Modules (basic.py, python.py, javascript.py, etc.)

**Pattern:** Each language has:
- `[Language]Executor` class - Main execution engine
- `validate()` - Syntax validation
- `execute()` - Code execution
- Language-specific parsing and validation logic

**Example Structure:**
```python
class BASICExecutor:
    def validate(self, code):
        """Validate BASIC syntax"""
        
    def execute(self, code):
        """Execute BASIC code"""
        
    def _parse_line(self, line):
        """Parse a line of BASIC code"""
```

#### features/syntax_highlighting.py
Syntax highlighting and styling

**Key Classes:**
- `SyntaxHighlighter` - Text coloring based on syntax
- Language-specific highlighting patterns

#### features/code_templates.py
Code templates and snippets

**Key Functions:**
- `get_template(language)` - Get starter template for language
- Pre-built templates for each language

#### optimizations/performance_optimizer.py
Performance optimization

**Optimizations:**
- Code caching
- Compiled code reuse
- Statement optimization

#### optimizations/memory_manager.py
Memory and resource management

**Features:**
- Variable scope management
- Garbage collection tracking
- Memory limit enforcement

#### optimizations/gui_optimizer.py
GUI performance optimization

**Features:**
- Output buffering
- Refresh rate optimization
- Widget optimization

---

## Core Interpreter

### Interpreter Class Overview

```python
class Interpreter:
    def __init__(self):
        self.languages = {}      # Registered language executors
        self.output = []         # Execution output
        self.variables = {}      # Global variables
        self.last_language = None # Cached language
        
    def execute(self, code, language=None):
        """Main execution method"""
        
    def detect_language(self, code):
        """Automatic language detection"""
        
    def register_language(self, name, executor):
        """Register new language support"""
```

### Execution Flow

1. **Code Input:** User submits code and optional language
2. **Language Detection:** If not specified, detect from syntax
3. **Validation:** Check syntax using language module
4. **Execution:** Run code in language-specific executor
5. **Output Processing:** Format and display results
6. **Error Handling:** Catch and display exceptions

### Language Detection Strategy

Detects language by looking for:
- Keywords specific to each language
- Syntax patterns
- File extensions (if applicable)
- User selection (if provided)

**Priority Order:** User selection > Detected > Default (BASIC)

### Error Handling

- **Syntax Errors:** Invalid syntax, caught during validation
- **Runtime Errors:** Execution errors, caught during execution
- **System Errors:** OS-level errors, wrapped with context

All errors display:
- Error message
- Line number (if available)
- Language context
- Suggestion for fix (where applicable)

---

## Language Implementations

### Adding a New Language

1. **Create language module:** `core/languages/[language].py`

2. **Implement executor class:**
```python
class YourLanguageExecutor:
    def validate(self, code):
        """Validate syntax, raise SyntaxError if invalid"""
        
    def execute(self, code):
        """Execute code, return output string"""
```

3. **Register in interpreter:**
```python
# In interpreter.py __init__
from core.languages.your_language import YourLanguageExecutor
self.languages['yourlang'] = YourLanguageExecutor()
```

4. **Add to language detection:**
```python
# In detect_language() method
if self._detect_yourlang(code):
    return 'yourlang'
```

5. **Add syntax highlighting (optional):**
```python
# In features/syntax_highlighting.py
'yourlang': {
    'keywords': [...],
    'patterns': {...}
}
```

### Language Architecture Pattern

Each language module follows this pattern:

```python
class [Language]Executor:
    def __init__(self):
        self.output = ""
        self.variables = {}
        self.state = {}
        
    def validate(self, code):
        """Check syntax validity"""
        
    def execute(self, code):
        """Execute and return output"""
        
    def _initialize(self):
        """Reset state before execution"""
        
    def _parse(self, code):
        """Parse code into statements"""
        
    def _execute_statement(self, statement):
        """Execute single statement"""
        
    def _print(self, value):
        """Handle output"""
```

### Current Language Implementations

| Language   | File | Executor | Features |
|-----------|------|----------|----------|
| BASIC | basic.py | BASICExecutor | Variables, loops, arrays, subroutines |
| Python | python_executor.py | PythonExecutor | Exec-based with safety |
| JavaScript | javascript_executor.py | JavaScriptExecutor | Node.js based |
| Pascal | pascal.py | PascalExecutor | Types, procedures, functions |
| Prolog | prolog.py | PrologExecutor | Facts, rules, unification |
| Forth | forth.py | ForthExecutor | Stack operations |
| Perl | perl.py | PerlExecutor | Regex, strings, arrays |
| Logo | logo.py | LogoExecutor | Turtle graphics |
| PILOT | pilot.py | PILOTExecutor | Conditional logic |

---

## GUI System

### Main Window Structure

```
Time_Warp.py
├── Root Window (tk.Tk)
├── Menu Bar
│   ├── File Menu
│   ├── Edit Menu
│   └── Help Menu
├── Control Panel (Frame)
│   ├── Language Dropdown
│   └── Execute Button
├── Editor (Text Widget)
│   ├── Text content
│   └── Line numbers
├── Output Area (Frame)
│   ├── Output Text
│   ├── Error Display
│   └── Clear Button
└── Status Bar
    ├── Line/Column
    └── Language indicator
```

### Key GUI Components

#### Editor Widget
- Text input with line numbers
- Syntax highlighting
- Find & Replace
- Keyboard shortcuts

#### Output Widget
- Scrollable text display
- Automatic scrolling
- Clear button
- Error highlighting

#### Language Selector
- Dropdown menu
- Auto-detection checkbox
- Current language display

### GUI Event Handlers

- **Execute Button:** Runs current code
- **Clear Button:** Clears output
- **File Operations:** Open, save, new
- **Edit Operations:** Undo, redo, cut, copy, paste
- **Find & Replace:** Search and modify text

### Customization

Users can customize:
- Font (size, family)
- Colors (theme)
- Window layout
- Keyboard shortcuts

---

## Data Flow

### Execution Pipeline

```
User Input Code
    ↓
[GUI] Text Widget
    ↓
Execute Button Pressed
    ↓
[Core] Interpreter.execute()
    ↓
Detect Language
    ↓
Language-Specific Executor
    ↓
Validate Syntax
    ↓
Execute Code
    ↓
Capture Output
    ↓
[Core] Format Output
    ↓
[GUI] Output Widget
    ↓
Display Result
```

### Variable Scope

```
Global Scope
├── Built-in functions
├── Standard library
└── User-defined globals
    │
    └── Function/Procedure Scope
        ├── Local variables
        ├── Parameters
        └── Function-local scope
```

### Output Capture

Each language captures output through:
1. **Print/Echo statements:** Direct output
2. **Return values:** Function results
3. **Graphics:** Visual output (Logo)
4. **Logging:** Debug output

All output consolidated into unified output stream.

---

## Extension Points

### Adding Features

#### New Language Support

1. Create `core/languages/[lang].py`
2. Implement executor class
3. Register in `core/__init__.py`
4. Add syntax highlighting

#### New IDE Features

1. Add feature module to `core/features/`
2. Integrate in GUI (`Time_Warp.py`)
3. Add menu items/buttons
4. Implement event handlers

#### New Optimization

1. Create module in `core/optimizations/`
2. Integrate in interpreter initialization
3. Hook into execution pipeline
4. Benchmark improvements

### Plugin Architecture

Consider for future:
- Plugin directory scanning
- Dynamic language loading
- Third-party extensions
- Community themes

---

## Performance Optimization

### Built-in Optimizations

#### 1. Code Caching
```python
# Interpreter caches compiled/parsed code
self.code_cache = {}
```

#### 2. Memory Management
- Track variable memory usage
- Cleanup unused variables
- Limit memory per execution

#### 3. GUI Optimization
- Output buffering
- Refresh rate limiting
- Lazy rendering

#### 4. Execution Optimization
- Statement compilation (where applicable)
- Function caching
- Lazy evaluation

### Performance Monitoring

Track:
- Execution time
- Memory usage
- Output size
- Cache hits

### Benchmarking

Run comprehensive demo for each language:
```bash
python scripts/run_tests.py
```

### Profiling

Identify bottlenecks:
```python
import cProfile
cProfile.run('interpreter.execute(code)')
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

### Testing

- **Unit tests:** Test individual components
- **Integration tests:** Test language implementations
- **GUI tests:** Verify UI functionality
- **Performance tests:** Benchmark optimizations

### Code Standards

- Python 3.9+ compatibility
- Type hints where practical
- Docstring documentation
- PEP 8 style guide
- Meaningful variable names

### Contribution Process

1. Create feature branch
2. Implement changes with tests
3. Run full test suite
4. Submit pull request
5. Code review
6. Merge to main

---

## API Reference

See [API_REFERENCE.md](API_REFERENCE.md) for detailed API documentation.

## Implementation Details

See [LANGUAGE_IMPLEMENTATIONS.md](LANGUAGE_IMPLEMENTATIONS.md) for how each language is implemented.

---

**For questions, see:** [../../README.md](../../README.md)
