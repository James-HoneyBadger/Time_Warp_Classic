# Time_Warp Classic - Example Programs

This directory contains example programs for all 9 supported programming languages. Examples are organized by language and demonstrate key features of each language.

---

## Directory Structure

```
examples/
├── basic/          # BASIC programs
├── logo/           # Logo turtle graphics
├── pilot/          # PILOT educational programs
├── pascal/         # Pascal structured programming
├── prolog/         # Prolog logic programming
├── forth/          # Forth stack-based programming
├── perl/           # Perl text processing
├── python/         # Python modern programming
└── javascript/     # JavaScript ES6+ features
```

---

## Language Examples

### PILOT - Computer-Assisted Instruction

**File:** `pilot/quiz_pilot.pilot`

Demonstrates:
- Text output with `T:`
- User input with `A:`
- Pattern matching with `M:`
- Conditional output with `TY:` and `TN:`
- Variable substitution with `*VAR*`
- Labels and branching

**Try it:**
```bash
Program → Load Example → PILOT → Quiz Demo
```

---

### BASIC - Classic Line-Numbered Programming

**Files:**
- `basic/hello_basic.bas` - Hello world with turtle graphics
- `basic/INDEX.bas` - Interactive menu system

**hello_basic.bas** demonstrates:
- `PRINT` statements for output
- `LET` for variable assignment
- `FOR...NEXT` loops
- `REM` comments
- Turtle graphics (`FORWARD`, `RIGHT`, `PENDOWN`, `PENUP`)
- Drawing geometric shapes

**Try it:**
```bash
Program → Load Example → BASIC → Hello World + Turtle Graphics
```

---

### Logo - Turtle Graphics Programming

**File:** `logo/spiral_logo.logo`

Demonstrates:
- `REPEAT` loops
- Turtle movement commands (`FORWARD`, `RIGHT`)
- Color commands (`SETPENCOLOR`)
- Variable manipulation with `MAKE`
- Creating spirals and patterns
- Visual output on graphics canvas

**Try it:**
```bash
Program → Load Example → Logo → Colorful Spiral
```

**What it does:**
Draws a colorful expanding spiral by gradually increasing the forward distance and changing colors.

---

### Pascal - Structured Programming

**File:** `pascal/hello_pascal.pas`

Demonstrates:
- Program structure (`program`, `begin`, `end`)
- Variable declarations (`var`)
- Functions and procedures
- `FOR` loops
- `WriteLn` for output
- Comments with `{ }`
- Strong typing

**Try it:**
```bash
Program → Load Example → Pascal → Hello World + Functions
```

---

### Prolog - Logic Programming

**File:** `prolog/facts_prolog.pl`

Demonstrates:
- Facts (parent relationships)
- Rules (sibling, ancestor)
- Queries
- Pattern matching
- Logical inference
- Family tree relationships

**Try it:**
```bash
Program → Load Example → Prolog → Facts & Rules
```

**What it does:**
Defines family relationships and allows querying about ancestors, siblings, and family connections.

---

### Forth - Stack-Based Programming

**File:** `forth/stack_forth.fth`

Demonstrates:
- Stack operations (`DUP`, `SWAP`, `DROP`)
- Word definitions (`:` and `;`)
- Arithmetic operators
- RPN (Reverse Polish Notation)
- Stack manipulation
- Custom words

**Try it:**
```bash
Program → Load Example → Forth → Stack Operations
```

**What it does:**
Shows stack-based computation and custom word definitions.

---

### Perl - Text Processing

**File:** `perl/patterns_perl.pl`

Demonstrates:
- Regular expressions
- Array operations
- Hash (dictionary) usage
- Text pattern matching
- String manipulation
- `foreach` loops
- File-like operations

**Try it:**
```bash
Program → Load Example → Perl → Patterns & Text Processing
```

---

### Python - Modern Programming

**File:** `python/modern_python.py`

Demonstrates:
- List comprehensions
- Dictionary comprehensions
- Generator expressions
- Classes and objects
- Lambda functions
- f-strings for formatting
- Modern Python 3.9+ features

**Try it:**
```bash
Program → Load Example → Python → Modern Python Features
```

**What it does:**
Showcases modern Python syntax and functional programming features.

---

### JavaScript - ES6+ Web Scripting

**File:** `javascript/interactive_javascript.js`

Demonstrates:
- Arrow functions
- `const` and `let` declarations
- Template literals
- Array methods (`map`, `filter`, `reduce`)
- Promises and async/await
- Classes
- Destructuring
- Spread operator

**Try it:**
```bash
Program → Load Example → JavaScript → Modern JavaScript (ES6+)
```

---

## Loading Examples

### Via GUI Menu

1. Click **Program → Load Example**
2. Select language submenu
3. Choose example program
4. Click **▶ Run** or press **F5**

### Via File Browser

1. Click **File → Open File...**
2. Navigate to `examples/[language]/`
3. Select `.bas`, `.logo`, `.pilot`, etc.
4. Click **▶ Run** or press **F5**

---

## Creating Your Own Examples

### Naming Conventions

- **PILOT:** `.pilot` extension
- **BASIC:** `.bas` extension
- **Logo:** `.logo` extension
- **Pascal:** `.pas` extension
- **Prolog:** `.pl` or `.pro` extension
- **Forth:** `.fth` or `.4th` extension
- **Perl:** `.pl` extension
- **Python:** `.py` extension
- **JavaScript:** `.js` extension

### Example Template

Create a new file following this structure:

```
[Language] - [Description]
Author: Your Name
Date: YYYY-MM-DD

Description:
  Brief description of what the program does

Features Demonstrated:
  - Feature 1
  - Feature 2
  - Feature 3

[Your code here]
```

### Contributing Examples

Want to share your examples?

1. Create your program in the appropriate language directory
2. Test it thoroughly in the IDE
3. Add comments explaining the code
4. Follow the language's style conventions
5. Submit a pull request on GitHub

---

## Tips for Learning

### For Beginners

1. **Start Simple** - Begin with `hello_basic.bas` or `quiz_pilot.pilot`
2. **Study the Code** - Read through examples before running them
3. **Experiment** - Modify values and see what changes
4. **Compare Languages** - See how different languages solve similar problems

### For Teachers

1. **Use as Templates** - Customize examples for your lessons
2. **Show Side-by-Side** - Compare implementations across languages
3. **Build Progressively** - Start simple, add complexity gradually
4. **Encourage Creativity** - Have students create their own versions

### For Programmers

1. **Language Tour** - Try one example from each language
2. **Paradigm Comparison** - Compare procedural vs functional vs logic programming
3. **Performance Analysis** - Time different implementations
4. **Extend Examples** - Add new features to existing programs

---

## Example Challenges

Try these exercises using the example programs as starting points:

### Beginner Challenges

1. **Modify the BASIC spiral** to draw a square instead
2. **Change colors** in the Logo spiral program
3. **Add new questions** to the PILOT quiz
4. **Create a new Pascal function** for multiplication
5. **Add more family members** to the Prolog facts

### Intermediate Challenges

1. **Draw a star** using Logo turtle graphics
2. **Create a calculator** in BASIC
3. **Build a word guessing game** in PILOT
4. **Implement factorial** in Forth
5. **Parse CSV data** in Perl

### Advanced Challenges

1. **Fractal tree** using recursive Logo
2. **Maze solver** in Prolog
3. **Text adventure game** in BASIC
4. **Mandelbrot set** in Python
5. **Sorting visualizer** in JavaScript

---

## Troubleshooting Examples

### Example Won't Run

- **Check language selection** - Dropdown must match file type
- **Check file extension** - Must be recognized extension
- **Check syntax** - Look for error messages in output
- **Check dependencies** - Ensure all packages installed

### Graphics Don't Appear

- **Verify Graphics Panel visible** - View → Graphics Panel
- **Check pen state** - Must use `PENDOWN` or `PD`
- **Verify movement commands** - Must call `FORWARD`, `BACK`, etc.
- **Check coordinates** - Must be within canvas bounds

### Wrong Output

- **Compare with expected** - Check example description
- **Read error messages** - They explain what went wrong
- **Check variable values** - May need to initialize variables
- **Verify logic** - Step through code mentally

---

## Additional Resources

- **[User Manual](../docs/USER_MANUAL.md)** - Complete IDE guide
- **[Language Reference](../docs/LANGUAGE_REFERENCE.md)** - Syntax for all languages
- **[Technical Manual](../docs/TECHNICAL_MANUAL.md)** - Implementation details

---

**Happy Coding Through the Ages!** 🕰️

© 2025 Time_Warp Project | Example Programs
