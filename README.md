# Time Warp Classic

> **A Multi-Language Programming Environment for Vintage and Modern Languages**

Time_Warp Classic is a sophisticated educational IDE that bridges the past and present of programming, supporting 9 programming languages through an elegant graphical interface with integrated turtle graphics, inspired by the golden age of computing.

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/James-HoneyBadger/Time_Warp_Classic)
[![Python](https://img.shields.io/badge/python-3.9+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)

---

## 🌟 Features

### Multi-Language Support
Execute code in 9 different programming languages, each with full language-specific features:
- **PILOT** - Educational computer-assisted instruction
- **BASIC** - Classic line-numbered programming with turtle graphics
- **Logo** - Visual turtle graphics programming
- **Pascal** - Structured programming with strong typing
- **Prolog** - Logic programming with facts and rules
- **Forth** - Stack-based concatenative programming
- **Perl** - Text processing and pattern matching
- **Python** - Modern general-purpose programming
- **JavaScript** - Web scripting with ES6+ features

### Professional IDE Interface
- **Refined Menu System** - File, Edit, Program, Preferences, About
- **Integrated Editor** - Syntax-aware code editing with undo/redo
- **Real-time Output** - Immediate program execution feedback
- **Turtle Graphics Canvas** - Visual programming with integrated graphics display
- **Theme Support** - 9 color themes with persistence
- **Customizable Fonts** - 7 font sizes plus system monospace choices
- **Panel Management** - Resizable output and graphics panels

### Educational Focus
- Clear, descriptive error messages
- Example programs for every language
- Immediate execution feedback
- Visual programming support
- Interactive learning environment

---

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- tkinter (usually included with Python)
- pip package manager

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/James-HoneyBadger/Time_Warp_Classic.git
   cd Time_Warp_Classic
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or use a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Launch the IDE:**
   ```bash
   python Time_Warp.py
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
 - **[User Manual](docs/user/USER_MANUAL.md)** - Complete guide to using the IDE
 - **[Quick Start Guide](docs/user/QUICKSTART.md)** - Get up and running quickly
 - **[Example Programs](examples/README.md)** - Guided tour of example programs

### Technical Documentation
 - **[Technical Manual](docs/dev/TECHNICAL_MANUAL.md)** - Architecture and implementation details

### Additional References
- **[Documentation Index](docs/README.md)** - Doc suite overview

## 🎨 Supported Languages

### Vintage Languages

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

### Modern Languages

#### Perl (1987)
Powerful text processing and scripting.
```perl
my @numbers = (1, 2, 3, 4, 5);
my $sum = 0;
$sum += $_ for @numbers;
print "Sum: $sum\n";
```

#### Python (1991)
Clean, readable general-purpose programming.
```python
numbers = [1, 2, 3, 4, 5]
squares = [n**2 for n in numbers]
print(f"Squares: {squares}")
```

#### JavaScript (1995)
Modern web scripting with ES6+ features.
```javascript
const numbers = [1, 2, 3, 4, 5];
const squares = numbers.map(n => n ** 2);
console.log(`Squares: ${squares}`);
```

---

## 🗂️ Project Structure

```
Time_Warp_Classic/
├── Time_Warp.py              # Main application entry point
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Modern Python configuration
│
├── core/                    # Core interpreter engine
│   ├── interpreter.py       # Central execution engine
│   ├── languages/           # Language-specific executors
│   │   ├── pilot.py         # PILOT executor
│   │   ├── basic.py         # BASIC executor
│   │   ├── logo.py          # Logo executor
│   │   ├── pascal.py        # Pascal executor
│   │   ├── prolog.py        # Prolog executor
│   │   ├── forth.py         # Forth executor
│   │   ├── perl.py          # Perl executor
│   │   ├── python.py        # Python executor
│   │   └── javascript.py    # JavaScript executor
│   ├── features/            # Advanced features
│   └── utilities/           # Helper utilities
│
├── examples/                # Example programs (organized by language)
│   ├── README.md           # Examples documentation
│   ├── pilot/              # PILOT examples
│   ├── basic/              # BASIC examples
│   ├── logo/               # Logo examples
│   ├── pascal/             # Pascal examples
│   ├── prolog/             # Prolog examples
│   ├── forth/              # Forth examples
│   ├── perl/               # Perl examples
│   ├── python/             # Python examples
│   └── javascript/         # JavaScript examples
│
├── docs/                   # Comprehensive documentation
│   ├── README.md           # Documentation index
│   ├── user/               # User-facing guides
│   │   ├── USER_MANUAL.md  # Complete user guide
│   │   └── QUICKSTART.md   # Quick start guide
│   └── dev/                # Developer-facing docs
│       └── TECHNICAL_MANUAL.md # Technical architecture
│
└── scripts/                # Launcher scripts
    ├── launch.py           # Python launcher
    ├── launch_Time_Warp.sh # Shell launcher
    └── start.sh            # Simple launcher
```

---

## ⌨️ Keyboard Shortcuts

### Program Execution
- **F5** - Run current program

### File Operations
- **Ctrl+N** - New file
- **Ctrl+O** - Open file
- **Ctrl+S** - Save file
- **Ctrl+Q** - Exit application

### Editing
- **Ctrl+Z** - Undo
- **Ctrl+Y** - Redo
- **Ctrl+X** - Cut
- **Ctrl+C** - Copy
- **Ctrl+V** - Paste
- **Ctrl+A** - Select all

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
- **OS:** Windows 10+, macOS 11+, Ubuntu 20.04+
- **Python:** 3.11 or higher
- **RAM:** 2 GB
- **Display:** 1920x1080 or higher

### Required Python Packages
- **tkinter** - GUI framework (usually included with Python)
- **pygame** - Graphics support (installed automatically)
- **Pillow** - Image processing (installed automatically)

### Optional Packages
- **pygments** - Syntax highlighting (for advanced features)
- **pytest** - Testing framework (for development)
- **black** - Code formatting (for development)
- **flake8** - Linting (for development)

---

## 🤝 Contributing

Contributions are welcome! Please see **[DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)** for detailed information.

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

# Install dependencies including dev tools
pip install -r requirements.txt
pip install pytest black flake8 mypy

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

- **PILOT Language** - Inspired by John Amsden Starkweather's original 1968 design
- **BASIC** - Tribute to Kemeny and Kurtz's accessible programming vision
- **Logo** - Honoring Seymour Papert's educational computing legacy
- **Classic Computing Community** - For keeping vintage computing alive
- **Open Source Contributors** - Everyone who helps improve Time_Warp

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
Explore Pascal for structured programming, then try Prolog for logic programming.

### For Advanced Users
Compare implementations across all 9 languages, or extend the interpreter with new features.

---

## 🚧 Roadmap

- [ ] Code completion and IntelliSense
- [ ] Syntax highlighting in editor
- [ ] Debugger with breakpoints
- [ ] More example programs
- [ ] Language tutorials
- [ ] Plugin system for custom languages
- [ ] Export programs to standalone executables
- [ ] Web-based version

---

**Time_Warp Classic** - *Programming Through the Ages* 🕰️

© 2025 Honey Badger Universe | Educational Software
