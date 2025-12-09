# Time_Warp

A command-line multi-language interpreter for educational programming, supporting 9 programming languages through a unified execution engine.

## Overview

Time_Warp is an educational tool that allows users to write and execute programs in 9 different programming languages using a command-line interface. It's designed for learning programming concepts across different paradigms with immediate execution feedback.

## Features

- **Multi-Language Support**: Execute code in PILOT, BASIC, Logo, Pascal, Prolog, Forth, Perl, Python, and JavaScript
- **Command-Line Interface**: Powerful CLI for running programs and displaying code with syntax highlighting
- **Turtle Graphics**: Text-based visual programming support for Logo and PILOT languages
- **Educational Focus**: Clear error messages and immediate execution feedback
- **Syntax Highlighting**: Display code with terminal-based syntax highlighting (requires pygments)

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

3. Run programs via CLI:

   ```bash
   python scripts/timewarp-cli.py run examples/basic/hello_world.bas
   ```

## Usage

### Command Line Interface

Time_Warp provides a comprehensive CLI for running and managing programs:

```bash
# Run a program
python scripts/timewarp-cli.py run examples/basic/hello_world.bas

# Display code with syntax highlighting
python scripts/timewarp-cli.py cat examples/basic/hello_world.bas

# List available example programs
python scripts/timewarp-cli.py list

# Get information about a language
python scripts/timewarp-cli.py info basic

# Show help
python scripts/timewarp-cli.py help
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
