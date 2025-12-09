# Time_Warp CLI Documentation

## Overview

The Time_Warp CLI (Command Line Interface) provides a powerful way to run Time_Warp programs directly from the terminal without launching the GUI. It's perfect for:

- Running programs in automated scripts
- Testing programs quickly
- Batch processing multiple programs
- Integration with other tools
- Server environments without GUI

## Installation

The CLI is included with Time_Warp. No additional installation required.

## Usage

### Basic Syntax
```bash
# Using Time_Warp.py with --cli flag:
python Time_Warp.py --cli <command> [arguments...]

# Or using the legacy wrapper script:
./timewarp <command> [arguments...]
```

### Available Commands

#### `run <file>`
Execute a Time_Warp program file.

```bash
python Time_Warp.py --cli examples/basic/hello_world.bas
python Time_Warp.py --cli examples/python/data_analysis.py
python Time_Warp.py --cli my_program.logo

# Legacy syntax still works:
./timewarp run examples/basic/hello_world.bas
```

**Supported file types:**
- `.bas`, `.basic` - BASIC programs
- `.logo` - Logo programs
- `.py` - Python programs
- `.js` - JavaScript programs
- `.pl` - Perl programs
- `.pas`, `.pp` - Pascal programs
- `.fs`, `.forth` - Forth programs
- `.pl`, `.prolog` - Prolog programs (note: `.pl` conflicts with Perl)
- `.pilot` - PILOT programs

#### `list`
Display all available example programs organized by language.

```bash
python Time_Warp.py --cli list
# or legacy:
./timewarp list
```

Shows a categorized list of all example programs with file counts.

#### `info <language>`
Show detailed information about a specific programming language.

```bash
python Time_Warp.py --cli info basic
python Time_Warp.py --cli info python
python Time_Warp.py --cli info logo

# or legacy:
./timewarp info basic
```

Displays:
- Full language name
- Description
- File extensions
- Key features
- Number of available examples

#### `help`
Show the help message with usage examples.

```bash
python Time_Warp.py --cli help
# or legacy:
./timewarp help
```

#### `version`
Show version information.

```bash
python Time_Warp.py --cli version
# or legacy:
./timewarp version
```

## Examples

### Running BASIC Programs
```bash
# Hello World
python Time_Warp.py --cli examples/basic/hello_world.bas

# Turbo BASIC features demo
python Time_Warp.py --cli examples/basic/turbo_features.bas

# Legacy syntax still works:
./timewarp run examples/basic/hello_world.bas
```

### Running Python Programs
```bash
# Data analysis demo
python Time_Warp.py --cli examples/python/data_analysis.py

# Interactive guessing game
python Time_Warp.py --cli examples/python/guessing_game.py
```

### Running Logo Programs
```bash
# Graphics demo
python Time_Warp.py --cli examples/logo/graphics_demo.logo

# Recursive patterns
python Time_Warp.py --cli examples/logo/recursive_graphics.logo
```

### Getting Language Information
```bash
# Learn about BASIC
python Time_Warp.py --cli info basic

# Learn about JavaScript
python Time_Warp.py --cli info javascript

# Learn about PILOT
python Time_Warp.py --cli info pilot
```

## Interactive Programs

Some programs (especially PILOT) are designed for interactive input. When running these through the CLI:

- The program will prompt for input in the terminal
- Enter values when prompted
- Some variable substitution may work differently than in interactive mode

## Error Handling

The CLI provides clear error messages:
- `❌ Error: File not found` - When the specified file doesn't exist
- `❌ Error: File is empty` - When the program file contains no code
- `❌ Unknown command` - When an invalid command is used
- `❌ Unknown language` - When requesting info for unsupported language

## Exit Codes

- `0` - Success
- `1` - Error occurred
- `130` - Interrupted by user (Ctrl+C)

## Integration

The CLI can be easily integrated into scripts and automation:

```bash
#!/bin/bash
# Run all BASIC examples
for file in examples/basic/*.bas; do
    echo "Running $file..."
    ./timewarp run "$file"
    echo "---"
done
```

## Troubleshooting

### Module Import Errors
If you get `ModuleNotFoundError`, ensure you're running the CLI from the Time_Warp root directory.

### File Path Issues
- Use relative paths from the Time_Warp root directory
- Or use absolute paths to program files

### Interactive Programs
- Some programs expect user input
- Press Enter after each response
- Use Ctrl+C to interrupt if needed

## Language Support

Time_Warp CLI supports all Time_Warp languages:

| Language | Extensions | Description |
|----------|------------|-------------|
| PILOT | `.pilot` | Educational programming |
| BASIC | `.bas`, `.basic` | Classic line-numbered programming |
| Logo | `.logo` | Turtle graphics |
| Python | `.py` | Modern scripting |
| JavaScript | `.js` | Web scripting |
| Perl | `.pl` | Text processing |
| Pascal | `.pas`, `.pp` | Structured programming |
| Forth | `.fs`, `.forth` | Stack-based |
| Prolog | `.pl`, `.prolog` | Logic programming |

## Tips

- Use `./timewarp list` to discover available programs
- Use `./timewarp info <lang>` to learn about language capabilities
- Programs run in the Time_Warp interpreter
- Output appears directly in the terminal
- Turtle graphics programs will show drawing commands (graphics window required for actual graphics)