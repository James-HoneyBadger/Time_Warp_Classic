# Time_Warp

A multi-language interpreter IDE for educational programming, supporting 9 programming languages through a unified execution engine with GUI and CLI interfaces.

## Overview

Time_Warp is an educational tool that allows users to write and execute programs in 9 different programming languages using either a graphical IDE or command-line interface. It's designed for learning programming concepts across different paradigms with immediate execution feedback.

## Features

- **Multi-Language Support**: Execute code in PILOT, BASIC, Logo, Pascal, Prolog, Forth, Perl, Python, and JavaScript
- **GUI IDE**: Interactive editor with syntax highlighting and real-time output display
- **Turtle Graphics**: Visual programming support for Logo and PILOT languages with graphical canvas
- **User Input**: Bottom input field for program input (no popup dialogs)
- **String Output**: PRINT commands with quoted text output directly to display
- **Educational Focus**: Clear error messages and immediate execution feedback
- **CLI Mode**: Command-line interface for running and managing programs

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/James-HoneyBadger/Time_Warp.git
   cd Time_Warp
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the IDE:

   ```bash
   python Time_Warp.py
   ```

## Usage

### GUI IDE Mode (Default)

When you run `python Time_Warp.py` without arguments, the graphical IDE launches:

1. **Code Editor**: Left panel for writing code in any supported language
2. **Output Display**: Right panel shows program output in real-time
3. **Graphics Canvas**: Bottom-right area for turtle graphics visualization
4. **Input Field**: Bottom input field for providing user input to programs
   - When a program executes an `INPUT` command, it waits for you to enter text in the bottom field and press Enter or Submit
   - The text is NOT entered via a popup dialog, but through the input field at the bottom of the window
5. **Control Buttons**: Run, Load, Save, Clear Output, Clear Editor

Example BASIC program with input:
```basic
10 PRINT "What is your name?"
20 INPUT NAME
30 PRINT "Hello, "; NAME
```

When you run this:
1. The program prints "What is your name?" to the output display
2. The interpreter waits for input from the bottom input field
3. You type your name and press Enter in the bottom field
4. Your input is displayed as ">> YourName" in the output
5. The program continues and prints the greeting

### Command Line Interface

For CLI execution, use the CLI scripts:

```bash
python scripts/timewarp-cli.py run program.bas
python scripts/launch.py program.logo
```

### Supported Languages

### TW PILOT (Educational Language)

```pilot
T:Hello World!
A:What is your name?
T:Nice to meet you, *NAME*!
U:X=10
T:X equals *X*
```

### TW BASIC (Classic Programming)

```basic
10 PRINT "Hello BASIC!"
20 LET X = 5
30 PRINT "X = "; X
40 END
```

### TW Logo (Turtle Graphics)

```logo
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
```

### Python

```python
print("Hello from Python!")
x = 42
print(f"x = {x}")
```

### JavaScript

```javascript
console.log("Hello from JavaScript!");
let x = 42;
console.log(`x = ${x}`);
```

### Perl

```perl
print "Hello from Perl!\n";
my $x = 42;
print "x = $x\n";
```

## Example Programs

The `examples/` directory contains ready-to-run example programs for all supported languages. These demonstrate language features and can be loaded directly in the GUI via **File → Open**.

### Available Examples

- **hello_basic.bas** - BASIC with turtle graphics (square drawing with pen control)
- **spiral_logo.logo** - Logo colorful spiral with SETPENCOLOR and loops
- **quiz_pilot.pilot** - PILOT interactive quiz demonstrating educational features
- **hello_pascal.pas** - Pascal structured program with functions
- **facts_prolog.pl** - Prolog logic programming with family relationships
- **stack_forth.fth** - Forth stack operations and RPN calculations
- **patterns_perl.pl** - Perl text processing with regex and functional programming
- **modern_python.py** - Modern Python features (comprehensions, classes, generators)
- **interactive_javascript.js** - JavaScript ES6+ features (async/await, classes, promises)

Each example includes comments explaining the code and demonstrates core language features. See `examples/README.md` for detailed documentation, or run `INDEX.bas` in the GUI for an interactive menu.

### Loading Examples

**GUI Mode:**
1. Launch Time Warp: `python Time_Warp.py`
2. Click **File → Open**
3. Navigate to `examples/`
4. Select any example file and click **Open**
5. Click **Run** to execute

**CLI Mode:**
```bash
python scripts/timewarp-cli.py run examples/hello_basic.bas
python scripts/launch.py examples/spiral_logo.logo
```

## Architecture

```
Time_Warp_Classic/                     # Root project directory
├── 📄 Time_Warp.py                    # Dependency checker and launcher
├── 📄 timewarp                        # CLI wrapper script
├── 📄 README.md                       # Main project documentation
├── 📄 requirements.txt                # Python dependencies
├── 📄 pyproject.toml                  # Modern Python configuration
│
├── 📁 core/                           # Core interpreter system
│   ├── 📄 __init__.py                 # Core module initialization
│   ├── 📄 interpreter.py              # Central execution engine
│   ├── 📁 languages/                  # Language-specific executors
│   │   ├── 📄 __init__.py
│   │   ├── 📄 basic.py                # BASIC language support
│   │   ├── 📄 forth.py                # Forth stack-based
│   │   ├── 📄 javascript.py           # JavaScript execution
│   │   ├── 📄 javascript_executor.py  # JS execution wrapper
│   │   ├── 📄 logo.py                 # Logo turtle graphics
│   │   ├── 📄 pascal.py               # Pascal structured
│   │   ├── 📄 perl.py                 # Perl text processing
│   │   ├── 📄 pilot.py                # PILOT educational
│   │   ├── 📄 prolog.py               # Prolog logic
│   │   ├── 📄 python.py               # Python execution
│   │   └── 📄 python_executor.py      # Python execution wrapper
│   ├── 📁 features/                   # Advanced features
│   │   └── 📄 code_templates.py       # Code template system
│   └── 📁 utilities/                  # Helper utilities
│       └── 📄 __init__.py
│
├── 📁 docs/                           # Documentation
│   ├── 📄 README.md                   # Documentation index
│   ├── 📄 CLI.md                      # CLI documentation
│   ├── 📄 *.md                        # Various guides and references
│   └── 📁 developer-guide/            # Developer documentation
│
├── 📁 examples/                       # Sample programs
│   ├── 📄 README.md                   # Examples documentation
│   ├── 📄 PROGRAMS_INDEX.md           # Program index
│   └── 📁 [language]/                 # Language-specific examples
│
├── 📁 scripts/                        # Development scripts
│   ├── 📄 README.md                   # Scripts documentation
│   ├── 📄 timewarp-cli.py             # CLI implementation
│   └── 📄 [other scripts]             # Various utility scripts
│
└── 📁 .github/                        # GitHub workflows
    └── 📁 workflows/                  # CI/CD automation
        └── 📄 ci.yml                  # Continuous integration
```

## Language Details

### TW PILOT

- **Purpose**: Educational programming with simple commands
- **Commands**: T: (text), A: (input), J: (jump), Y: (yes branch), N: (no branch), U: (update variable)
- **Features**: Variable interpolation with `*VAR*` syntax, turtle graphics integration

### TW BASIC

- **Purpose**: Classic line-numbered programming
- **Commands**: PRINT, LET, GOTO, IF...THEN, FOR...NEXT, INPUT
- **Features**: Traditional BASIC syntax with modern enhancements

### TW Logo

- **Purpose**: Educational turtle graphics programming
- **Commands**: FORWARD, BACK, LEFT, RIGHT, PENUP, PENDOWN, REPEAT
- **Features**: Visual programming with turtle graphics

### Modern Languages (Perl, Python, JavaScript)

- **Purpose**: Full scripting language support
- **Execution**: Direct execution with proper error handling
- **Features**: Access to standard libraries and modern language features

## Development

### Adding a New Language

1. Create executor class in `core/languages/newlang.py`
2. Implement `execute_command()` method
3. Add import to `core/languages/__init__.py`
4. Register in `interpreter.py` language mapping

### Code Style

- Use descriptive docstrings for all classes and methods
- Follow PEP 8 style guidelines
- Include type hints where helpful
- Write clear, educational error messages

## Requirements

- Python 3.8+
- pygments (optional, for syntax highlighting in CLI)

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions welcome! Please:

1. Test your changes manually
2. Update documentation
3. Follow existing code style
4. Add examples for new features
