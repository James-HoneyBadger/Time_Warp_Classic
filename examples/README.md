# Time Warp Classic - Example Programs

This directory contains example programs for all supported languages in Time Warp Classic. These examples can be loaded directly in the GUI using the File → Open menu.

## Supported Languages

### 1. BASIC (`.bas`)
**File:** `hello_basic.bas`

Classic BASIC with line numbers, demonstrating:
- PRINT statements and string output
- FOR/NEXT loops
- Turtle graphics (FORWARD, RIGHT, PENDOWN, PENUP)
- Comments with REM

### 2. Logo (`.logo`)
**File:** `spiral_logo.logo`

Educational Logo with turtle graphics, demonstrating:
- REPEAT loops
- Turtle movement (FORWARD, RIGHT, LEFT)
- Pen control (PENUP, PENDOWN)
- Color commands (SETPENCOLOR)
- Position commands (HOME, SETXY)
- Screen control (CLEARSCREEN)

### 3. PILOT (`.pilot`)
**File:** `quiz_pilot.pilot`

Computer-assisted instruction language, demonstrating:
- Text output (T:)
- User input (A:)
- Pattern matching (M:)
- Conditional output (TY:, TN:)
- Labels and branching
- Interactive quiz creation

### 4. Pascal (`.pas`)
**File:** `hello_pascal.pas`

Structured programming language, demonstrating:
- Program structure
- Variable declarations (VAR)
- Functions and procedures
- FOR loops
- Writeln for output
- Comments { }

### 5. Prolog (`.pl`)
**File:** `facts_prolog.pl`

Logic programming language, demonstrating:
- Facts and rules
- Queries
- Logical inference
- Pattern matching
- Recursive rules (ancestor relationships)
- Comments %

### 6. Forth (`.fth`)
**File:** `stack_forth.fth`

Stack-based programming language, demonstrating:
- Word definitions (: word-name ... ;)
- Stack operations (DUP, DROP, etc.)
- Reverse Polish Notation (RPN)
- Loops (DO...LOOP, BEGIN...WHILE...REPEAT)
- String output (.")
- Comments \

### 7. Perl (`.pl`)
**File:** `patterns_perl.pl`

Text processing language, demonstrating:
- Arrays and hashes
- Pattern matching with regular expressions
- Subroutines
- String manipulation
- grep and map functions
- Comments #

### 8. Python (`.py`)
**File:** `modern_python.py`

Modern multi-paradigm language, demonstrating:
- List comprehensions
- Dictionaries
- Classes and objects
- Generators
- Lambda functions
- Decorators
- f-strings
- Comments """ """ and #

### 9. JavaScript (`.js`)
**File:** `interactive_javascript.js`

Modern web programming language, demonstrating:
- const/let declarations
- Arrow functions
- Array methods (map, filter, forEach)
- Objects and classes
- Template literals
- Promises and async/await
- Spread operator and destructuring
- Comments //

## Loading Examples in the GUI

1. Launch Time Warp Classic
2. Click **File → Open** (or press Ctrl+O)
3. Navigate to the `examples` directory
4. Select any example file
5. Click **Open**
6. Click **Run** to execute the program

## Running from Command Line

You can also run examples from the command line:

```bash
# BASIC
python scripts/timewarp-cli.py run examples/hello_basic.bas

# Logo
python scripts/timewarp-cli.py run examples/spiral_logo.logo

# Python
python scripts/timewarp-cli.py run examples/modern_python.py

# JavaScript
python scripts/timewarp-cli.py run examples/interactive_javascript.js
```

## Creating Your Own Programs

Use these examples as templates for your own programs. Each example demonstrates:
- Language syntax and structure
- Common operations and patterns
- Comments and documentation style
- Best practices for that language

## File Extensions

- `.bas` - BASIC
- `.logo` - Logo
- `.pilot` - PILOT
- `.pas` - Pascal
- `.pl` - Prolog
- `.fth` - Forth
- `.pl` - Perl (note: same as Prolog, detected by content)
- `.py` - Python
- `.js` - JavaScript

## Notes

- Some examples include turtle graphics commands that will draw on the canvas
- Interactive examples (like PILOT quiz) may require user input
- Prolog examples define facts and rules; queries can be entered at the prompt
- All examples are designed to run without external dependencies

Enjoy exploring the history of programming languages!
