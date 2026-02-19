# Time Warp Classic

> **Back-to-basics Tkinter IDE for 9 vintage + modern languages with turtle graphics.**

Time Warp Classic is an educational multi-language IDE that bridges the past and present of programming, supporting 9 programming languages through an elegant graphical interface with integrated turtle graphics, inspired by the golden age of computing.

[![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)](https://github.com/James-HoneyBadger/Time_Warp_Classic)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![education](https://img.shields.io/badge/topic-education-lightgrey)](https://github.com/topics/education)
[![ide](https://img.shields.io/badge/topic-ide-lightgrey)](https://github.com/topics/ide)
[![tkinter](https://img.shields.io/badge/topic-tkinter-lightgrey)](https://github.com/topics/tkinter)
[![multi-language](https://img.shields.io/badge/topic-multi--language-lightgrey)](https://github.com/topics/multi-language)
[![turtle-graphics](https://img.shields.io/badge/topic-turtle--graphics-lightgrey)](https://github.com/topics/turtle-graphics)

---

## 🌟 Features

### Multi-Language Support
Execute code in 9 different programming languages — six with full built-in interpreters and three delegating to external runtimes:

**Built-in Interpreters:**
- **PILOT** (1968) — Educational computer-assisted instruction
- **BASIC** (1964) — Classic line-numbered programming with turtle graphics
- **Logo** (1967) — Visual turtle graphics programming
- **Pascal** (1970) — Structured programming with strong typing
- **Prolog** (1972) — Logic programming with facts, rules, and backtracking
- **Forth** (1970) — Stack-based concatenative programming

**External Runtime Executors:**
- **Perl** (1987) — Text processing and pattern matching (requires `perl`)
- **Python** (1991) — Modern general-purpose programming (uses host Python)
- **JavaScript** (1995) — Web scripting with ES6+ features (requires Node.js)

### Professional IDE Interface
- **Menu System** — File, Edit, Program, Debug, Test, Performance, Preferences, About
- **Syntax Highlighting** — Real-time syntax coloring via Pygments (with plain-text fallback)
- **Line Numbers** — Always-visible line numbering for easy navigation
- **Integrated Editor** — Code editing with undo/redo, find & replace (regex support)
- **Output Panel** — Immediate program execution feedback
- **Turtle Graphics Canvas** — Visual programming with integrated graphics display
- **Theme Support** — 9 color themes (Light, Dark, Classic, Solarized Dark/Light, Monokai, Dracula, Nord, High Contrast) with persistence
- **Customizable Fonts** — 7 font sizes (Tiny 8 pt to Giant 22 pt) plus system monospace families
- **Debug Tools** — Debug mode toggle, breakpoint management, error history tracking
- **Performance Tools** — Execution statistics, optimization, and profiling toggle
- **Settings Persistence** — Theme, font, and preferences saved to `~/.timewarp_settings.json`

### Educational Focus
- **Enhanced Error Messages** — Detailed error reporting with line numbers and context
- **Debug Tools** — Breakpoint support, debug mode, error history
- **Testing Framework** — Built-in smoke tests and full test suite via menu
- **Example Programs** — Comprehensive demos for every language
- **Immediate Feedback** — Run code with F5, see results instantly
- **Visual Programming** — Logo turtle graphics for immediate visual learning

---

## 📦 Installation

### Prerequisites
- **Python 3.9 or higher** (tested up to 3.14)
- **tkinter** (usually included with Python)
- **pip** package manager
- **Node.js** (optional — for JavaScript execution)
- **Perl** (optional — for Perl execution)

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/James-HoneyBadger/Time_Warp_Classic.git
   cd Time_Warp_Classic
   ```

2. **Launch with the setup script (recommended):**
   ```bash
   python3 run.py
   ```
   This automatically creates a virtual environment, installs dependencies, and launches the IDE.

   Or use the platform-specific scripts:
   ```bash
   ./run.sh          # Linux / macOS
   run.bat            # Windows
   ```

3. **Or install manually:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python Time_Warp.py
   ```

See [SETUP.md](SETUP.md) for detailed installation, troubleshooting, and advanced options.

## 🧪 Testing

Time_Warp_Classic includes a comprehensive test suite to ensure code quality and reliability.

### Running Tests

#### From Command Line
```bash
# Run all tests
python scripts/run_tests.py

# Run specific test types
python scripts/run_tests.py unit        # Unit tests only
python scripts/run_tests.py integration # Integration tests only
python scripts/run_tests.py smoke       # Quick smoke test

# Run with coverage
python scripts/run_tests.py --coverage
```

#### From Within the Application
Use the **Test** menu in the IDE:
- **Run Smoke Test** — Quick functionality check
- **Run Full Test Suite** — Complete test suite with verbose output

### Test Structure
```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_interpreter.py      # Core interpreter tests
├── test_basic.py            # BASIC language tests
├── test_logo.py             # Logo language tests
├── test_pilot.py            # PILOT language tests
├── test_pascal.py           # Pascal language tests
├── test_prolog.py           # Prolog language tests
├── test_forth.py            # Forth language tests
├── test_executors.py        # Subprocess executor tests
├── test_all_commands.py     # Cross-language command tests
├── test_gui.py              # GUI tests
├── test_stubs.py            # Stub class tests
└── test_languages_package.py # Language package tests
```

---

## 🚀 Getting Started

### Using the GUI

When you launch Time_Warp.py, you'll see the main IDE interface:

1. **Select Language** - Choose from the dropdown (PILOT, BASIC, Logo, etc.)
2. **Write Code** - Use the left editor panel
3. **Run Program** - Press **F5** or use **Program → Run Program**
4. **View Results** - See output in the right panel and graphics below

### Quick Example

Try this Logo program:
```logo
REPEAT 4 [
  FORWARD 100
  RIGHT 90
]
```

Or this BASIC program:
```basic
10 PRINT "Hello from the past!"
20 FOR I = 1 TO 5
30   PRINT "Count: "; I
40 NEXT I
50 END
```

### Loading Examples

**Via Menu:**
1. **Program → Load Example**
2. Select a language submenu
3. Choose an example program

**Via File Menu:**
1. **File → Open File...**
2. Navigate to `examples/[language]/`
3. Select an example file

---

## 📚 Documentation

### User Documentation
- **[Quick Start Guide](docs/QUICK_START.md)** — Get up and running in 5 minutes
- **[Language Tutorials](docs/user/LANGUAGE_TUTORIALS.md)** — Guided tutorials for all 9 languages
- **[Example Programs](examples/README.md)** — Guided tour of example programs

### Technical Documentation
- **[Technical Reference](docs/dev/TECHNICAL_REFERENCE.md)** — Architecture and implementation details

### Additional References
- **[Documentation Index](docs/README.md)** — Full doc suite overview
- **[FAQ](docs/FAQ.md)** — Frequently asked questions
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** — Common issues and solutions

### Language References
Individual reference docs for each language are in [`docs/languages/`](docs/languages/):
PILOT, BASIC, Logo, Pascal, Prolog, Forth, Perl, Python, JavaScript.

## 🎨 Supported Languages

### Vintage Languages (Built-in Interpreters)

#### PILOT (1968)
Computer-Assisted Instruction language designed for educational software.
```pilot
T:Welcome to PILOT programming!
A:What is your name?
T:Hello, *NAME*!
```

#### BASIC (1964)
The classic beginner's language with line numbers and turtle graphics.
```basic
10 PRINT "Drawing a square..."
20 FOR I = 1 TO 4
30   FORWARD 100
40   RIGHT 90
50 NEXT I
```

#### Logo (1967)
Educational language famous for turtle graphics.
```logo
REPEAT 36 [
  FORWARD 100
  RIGHT 10
]
```

#### Pascal (1970)
Structured programming language emphasizing clear code.
```pascal
program Hello;
begin
  WriteLn('Hello from Pascal!');
end.
```

#### Prolog (1972)
Logic programming with facts, rules, and queries.
```prolog
parent(john, mary).
parent(john, tom).
sibling(X, Y) :- parent(P, X), parent(P, Y), X \= Y.
```

#### Forth (1970)
Stack-based concatenative programming language.
```forth
: SQUARE DUP * ;
5 SQUARE .
```

### Modern Languages (External Runtime Executors)

#### Perl (1987)
Powerful text processing and scripting. Requires `perl` on PATH.
```perl
my @numbers = (1, 2, 3, 4, 5);
my $sum = 0;
$sum += $_ for @numbers;
print "Sum: $sum\n";
```

#### Python (1991)
Clean, readable general-purpose programming. Uses the host Python interpreter.
```python
numbers = [1, 2, 3, 4, 5]
squares = [n**2 for n in numbers]
print(f"Squares: {squares}")
```

#### JavaScript (1995)
Modern web scripting with ES6+ features. Requires Node.js on PATH.
```javascript
const numbers = [1, 2, 3, 4, 5];
const squares = numbers.map(n => n ** 2);
console.log(`Squares: ${squares}`);
```

---

## �️ Project Structure

```
Time_Warp_Classic/
├── Time_Warp.py              # Thin entry point (launches gui.app.TimeWarpApp)
├── run.py                    # Cross-platform launcher with venv/dependency setup
├── run.sh / run.bat          # Platform-specific launcher scripts
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── pyproject.toml            # Python project metadata and tool config
│
├── gui/                      # GUI package (tkinter IDE)
│   ├── app.py                # TimeWarpApp — main IDE window and layout
│   ├── menus.py              # Menu bar construction (8 menus)
│   ├── dialogs.py            # Find/Replace dialogs, About, error history
│   └── themes.py             # 9 themes, font sizes, extension mappings
│
├── core/                     # Core interpreter engine
│   ├── interpreter.py        # Time_WarpInterpreter — central execution engine
│   ├── stubs.py              # Placeholder classes (audio, games, hardware, IoT)
│   ├── languages/            # Language-specific executors
│   │   ├── base.py           # SubprocessExecutor base class
│   │   ├── pilot.py          # TwPilotExecutor (built-in)
│   │   ├── basic.py          # TwBasicExecutor (built-in)
│   │   ├── logo.py           # TwLogoExecutor (built-in)
│   │   ├── pascal.py         # TwPascalExecutor (built-in)
│   │   ├── prolog.py         # TwPrologExecutor (built-in)
│   │   ├── forth.py          # TwForthExecutor (built-in)
│   │   ├── perl.py           # PerlExecutor (subprocess → perl)
│   │   ├── python_executor.py # PythonExecutor (subprocess → python)
│   │   └── javascript_executor.py # JavaScriptExecutor (subprocess → node)
│   ├── features/
│   │   └── syntax_highlighting.py  # Pygments-based highlighting + line numbers
│   ├── optimizations/        # Performance optimizer, GUI optimizer, memory manager
│   └── utilities/            # Helper utilities
│
├── examples/                 # Example programs organized by language
│   ├── pilot/ basic/ logo/ pascal/ prolog/ forth/
│   ├── perl/ python/ javascript/
│   └── README.md             # Examples documentation
│
├── docs/                     # Comprehensive documentation
│   ├── README.md             # Documentation index
│   ├── INDEX.md              # Full doc suite navigation
│   ├── QUICK_START.md        # Quick start guide
│   ├── FAQ.md                # Frequently asked questions
│   ├── TROUBLESHOOTING.md    # Troubleshooting guide
│   ├── user/                 # User guides
│   │   └── LANGUAGE_TUTORIALS.md
│   ├── dev/                  # Developer docs
│   │   └── TECHNICAL_REFERENCE.md
│   └── languages/            # Per-language reference (9 files)
│
├── tests/                    # Test suite (pytest)
└── scripts/                  # Launcher and test-runner scripts
```

---

## ⌨️ Keyboard Shortcuts

### Program Execution
- **F5** — Run current program

### File Operations
- **Ctrl+N** — New file
- **Ctrl+O** — Open file
- **Ctrl+S** — Save file
- **Ctrl+Q** — Exit application

### Editing
- **Ctrl+Z** — Undo
- **Ctrl+Y** — Redo
- **Ctrl+X** — Cut
- **Ctrl+C** — Copy
- **Ctrl+V** — Paste
- **Ctrl+A** — Select all
- **Ctrl+F** — Find
- **Ctrl+H** — Find & Replace

---

## 🎯 Use Cases

### Education
- **Learn Programming Fundamentals** - Start with PILOT or BASIC
- **Explore Programming Paradigms** - Compare procedural, logic, and functional styles
- **Visual Learning** - Use Logo for immediate visual feedback
- **Historical Perspective** - Experience the evolution of programming languages

### Hobbyist Programming
- **Retro Computing** - Experience classic languages on modern hardware
- **Creative Coding** - Use turtle graphics for artistic expression
- **Language Exploration** - Try 9 languages without multiple installations
- **Quick Prototyping** - Test algorithms in different paradigms

### Teaching
- **Classroom Tool** - Teach multiple languages with one IDE
- **Interactive Lessons** - Use example programs as teaching aids
- **Comparative Learning** - Show same concepts across languages
- **Hands-on Practice** - Immediate execution and feedback

---

## 🔧 System Requirements

### Minimum Requirements
- **OS:** Windows 7+, macOS 10.12+, Linux (any modern distribution)
- **Python:** 3.9 or higher
- **RAM:** 512 MB
- **Display:** 1024x768 or higher

### Recommended Requirements
- **OS:** Windows 10+, macOS 11+, Fedora 40+, Ubuntu 22.04+
- **Python:** 3.11 or higher
- **RAM:** 2 GB
- **Display:** 1920x1080 or higher

### Required
- **tkinter** — GUI framework (usually included with Python)

### Recommended (Optional)
- **pygame-ce** — Graphics and multimedia support (community edition; or `pygame`)
- **Pillow** — Image processing features
- **Pygments** — Syntax highlighting in the editor

### Development Only
- **pytest** — Testing framework
- **black** — Code formatting
- **flake8** — Linting

> All optional packages degrade gracefully — the IDE works without them, with reduced features noted at startup.

---

## 🤝 Contributing

Contributions are welcome! Please see **[TECHNICAL_REFERENCE.md](docs/dev/TECHNICAL_REFERENCE.md)** for architecture details.

### Quick Contributing Guide

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Make your changes** and test thoroughly
4. **Commit your changes** (`git commit -m 'Add amazing feature'`)
5. **Push to the branch** (`git push origin feature/amazing-feature`)
6. **Open a Pull Request**

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/Time_Warp_Classic.git
cd Time_Warp_Classic

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install all dependencies (runtime + dev tools)
pip install -r requirements.txt

# Run tests
pytest

# Format code
black .

# Lint code
flake8
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **PILOT Language** — Inspired by John Amsden Starkweather's original 1968 design
- **BASIC** — Tribute to Kemeny and Kurtz's accessible programming vision
- **Logo** — Honoring Seymour Papert's educational computing legacy
- **Pascal** — Niklaus Wirth's vision of structured programming
- **Prolog** — Alain Colmerauer's logic programming breakthrough
- **Forth** — Charles H. Moore's elegantly minimal stack machine
- **Classic Computing Community** — For keeping vintage computing alive
- **Open Source Contributors** — Everyone who helps improve Time Warp

---

## 📞 Support

- **Documentation:** See the `docs/` directory
- **Issues:** Report bugs on [GitHub Issues](https://github.com/James-HoneyBadger/Time_Warp_Classic/issues)
- **Questions:** Check the [FAQ](docs/FAQ.md) first
- **Community:** Share your programs and experiences!

---

## 🎓 Learning Resources

### For Beginners
Start with PILOT or BASIC, then try Logo for visual programming.

### For Intermediate Programmers
Explore Pascal for structured programming, then try Prolog for logic programming or Forth for stack-based thinking.

### For Advanced Users
Compare implementations across all 9 languages, study the [Technical Reference](docs/dev/TECHNICAL_REFERENCE.md), or extend the interpreter with new features.

---

## 🚧 Roadmap

- [x] Syntax highlighting in editor (via Pygments)
- [x] Debug mode with breakpoints and error history
- [x] Comprehensive example programs for all 9 languages
- [x] Language tutorials and reference documentation
- [x] 9 color themes with persistence
- [x] Performance optimization system
- [ ] Code completion and IntelliSense
- [ ] Plugin system for custom languages
- [ ] Export programs to standalone executables
- [ ] Web-based version

---

**Time Warp Classic** — *Programming Through the Ages* 🕰️

© 2025–2026 Honey Badger Universe | Educational Software
