# Time Warp Classic - Code Examples

This directory contains comprehensive example programs demonstrating all features of the 9 supported programming languages in Time Warp Classic.

---

## Directory Structure

```
examples/
├── README.md                      # This file
├── basic/
│   └── comprehensive_demo.bas     # Complete BASIC feature demo
├── forth/
│   └── comprehensive_demo.fth     # Complete Forth feature demo
├── javascript/
│   └── comprehensive_demo.js      # Complete JavaScript feature demo
├── logo/
│   └── comprehensive_demo.logo    # Complete Logo feature demo
├── pascal/
│   └── comprehensive_demo.pas     # Complete Pascal feature demo
├── perl/
│   └── comprehensive_demo.pl      # Complete Perl feature demo
├── pilot/
│   └── comprehensive_demo.pilot   # Complete PILOT feature demo
├── prolog/
│   └── comprehensive_demo.pl      # Complete Prolog feature demo
└── python/
    └── comprehensive_demo.py      # Complete Python feature demo
```

---

## Comprehensive Demo Programs

Each language directory contains a **comprehensive_demo** file that thoroughly demonstrates all major features and commands of that language.

### 1. BASIC (`basic/comprehensive_demo.bas`)

**Features Demonstrated:**
- Variables and data types
- Arithmetic operations (+, -, *, /, MOD, ^)
- Mathematical functions (SIN, COS, SQRT, ABS, INT, RND)
- String operations (LEN, LEFT, RIGHT, MID, INSTR, UPPER, LOWER)
- Array operations (DIM, SORT, SUM, AVG, MIN, MAX)
- Conditional statements (IF/THEN/ELSE)
- Loop control (FOR/NEXT, WHILE loops)
- Subroutines (GOSUB/RETURN)
- Type conversion (VAL, STR$)

**Output:** Text-based demonstration of all language features

---

### 2. Python (`python/comprehensive_demo.py`)

**Features Demonstrated:**
- Variables and all data types (int, float, str, bool)
- Arithmetic and comparison operators
- String methods and operations
- Collections (lists, dictionaries, tuples, sets)
- Conditional statements (if/elif/else)
- Loop constructs (for, while, list comprehensions)
- Function definitions and recursion
- Lambda expressions
- Exception handling
- Mathematical operations
- String formatting (f-strings, format)

**Output:** Comprehensive showcase of Python language capabilities

---

### 3. JavaScript (`javascript/comprehensive_demo.js`)

**Features Demonstrated:**
- Variables (var declaration)
- All data types (number, string, boolean, null, undefined)
- Arithmetic operators and precedence
- String operations and methods
- Arrays (create, access, methods)
- Objects (properties, methods)
- Conditional statements (if/else, switch)
- Loop constructs (for, while, do-while)
- Functions and anonymous functions
- Mathematical functions (Math object)
- Type conversion
- Comparison and logical operators

**Output:** Interactive demonstration of JavaScript features

---

### 4. Pascal (`pascal/comprehensive_demo.pas`)

**Features Demonstrated:**
- Variables with explicit typing
- Constants and custom types
- Procedures and functions
- Formal parameters and return values
- Arithmetic operations
- String operations
- Array declarations and operations
- IF/THEN/ELSE and CASE statements
- FOR, WHILE, and REPEAT-UNTIL loops
- Function recursion
- Boolean logic and comparisons

**Output:** Structured showcase of Pascal programming concepts

---

### 5. Prolog (`prolog/comprehensive_demo.pl`)

**Features Demonstrated:**
- Facts and rules (predicates)
- Unification and pattern matching
- List operations (append, member, length, sum)
- Recursion (ancestors, factorial)
- Arithmetic evaluation (is, =:=, =\=)
- Comparison operators
- Logical operators (AND, OR, NOT)
- Backtracking and search
- Aggregation (findall, forall)
- Database operations (retract, consult)
- I/O predicates (readln, readchar, readint)

**Output:** Logic programming demonstrations and family relationship queries

---

### 6. Forth (`forth/comprehensive_demo.fth`)

**Features Demonstrated:**
- Stack manipulation (DUP, SWAP, ROT, OVER)
- Variables and memory operations
- Word definitions (colon definitions)
- Conditional logic (IF/ELSE)
- Loop constructs (DO...LOOP, ?DO)
- Array/table creation and access
- Recursion
- User-defined words
- Floating-point operations
- Mathematical functions

**Output:** Stack-based computation demonstrations

---

### 7. Perl (`perl/comprehensive_demo.pl`)

**Features Demonstrated:**
- Variables (scalars, arrays, hashes)
- Arithmetic and string operators
- String operations and methods
- Arrays (push, pop, shift, unshift, sort)
- Hashes (key-value pairs)
- Conditional statements (if/elsif/else, unless)
- All loop types (for, foreach, while, do-while)
- Subroutines with parameters
- Regular expressions (matching, substitution)
- References and dereferencing
- Map and grep operations
- String comparison
- Logical operators

**Output:** Text processing and data manipulation demonstrations

---

### 8. Logo (`logo/comprehensive_demo.logo`)

**Features Demonstrated:**
- Turtle movement (FORWARD, BACKWARD, RIGHT, LEFT)
- Pen control (PENUP, PENDOWN)
- Pen properties (SETPENCOLOR, SETPENSIZE)
- Drawing shapes (squares, circles, stars)
- REPEAT loops for patterns
- Nested structures
- Screen manipulation (CLEARSCREEN, HOME)
- Recursive drawing patterns

**Output:** Visual graphics on the turtle canvas

---

### 9. PILOT (`pilot/comprehensive_demo.pilot`)

**Features Demonstrated:**
- Text output (T:)
- Variable assignment (A:)
- Conditional branching (C:, Y, N)
- Arithmetic in variables
- Labels and jumping (M:, G:)
- Loop control
- Comparison operations
- String concatenation
- Multiple variables
- Nested conditionals

**Output:** Educational instruction program demonstrations

---

## How to Use the Demos

### Quick Start

1. **Launch Time Warp Classic:**
   ```bash
   python3 run.py
   ```

2. **Select a Language:**
   Use the dropdown menu to select from 9 languages

3. **Open a Demo:**
   Copy the comprehensive_demo file contents into the editor for your chosen language

4. **Run the Program:**
   Click "Run" button or press the Run button

5. **View Results:**
   Check the output panel for results and graphics

### Step-by-Step Example

```
1. Launch: python3 run.py
2. Select Language: Click dropdown → Choose "Python"
3. Open Demo: Copy contents of python/comprehensive_demo.py
4. Paste: Into the editor panel
5. Execute: Click Run button
6. Observe: Output shows all Python features
```

---

## Learning Recommendations

### By Skill Level

**Absolute Beginner:**
1. Start with **BASIC** - Familiar syntax, clear output
2. Try **Logo** - Visual feedback helps understanding
3. Explore **PILOT** - Instruction-oriented design

**Intermediate:**
1. Learn **Python** - Modern, readable syntax
2. Try **Pascal** - Structured, strongly typed
3. Explore **Perl** - Text processing power

**Advanced:**
1. Master **Prolog** - Logic programming paradigm
2. Study **Forth** - Stack-based thinking
3. Review **JavaScript** - Multiple paradigms

### By Learning Goal

**Goal: Learn Programming Fundamentals**
- BASIC → Pascal → Python

**Goal: Understand Different Paradigms**
- Procedural: BASIC, Pascal, Python
- Functional: JavaScript, Perl
- Logical: Prolog
- Stack-based: Forth

**Goal: Practice Pattern Matching & Logic**
- Prolog (pattern matching)
- Perl (regular expressions)
- Pascal (structured logic)

**Goal: Visual/Graphics Programming**
- Logo (turtle graphics)
- BASIC (with graphics extensions)

---

## Tips for Using These Examples

### Before Running

1. **Read the Comments** - Each demo has inline comments explaining features
2. **Understand the Structure** - Look at how the program is organized
3. **Identify Language Features** - Try to spot variables, loops, functions, etc.
4. **Predict Output** - Mentally run through the program

### While Running

1. **Watch the Output** - See exactly what each command produces
2. **Note the Order** - Output follows code execution order
3. **Check Section Headers** - Demos are organized into clear sections
4. **Read Carefully** - Output explains what each feature does

### After Running

1. **Modify Values** - Change numbers and re-run
2. **Add Comments** - Mark sections you want to understand better
3. **Create Variations** - Try adding new features
4. **Compare Languages** - Run demos in multiple languages to see differences

---

## Feature Reference Matrix

| Feature | BASIC | Python | JS | Pascal | Prolog | Forth | Perl | Logo | PILOT |
|---------|:-----:|:------:|:--:|:------:|:------:|:-----:|:----:|:----:|:-----:|
| Variables | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | ✅ |
| Arithmetic | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | ✅ |
| Strings | ✅ | ✅ | ✅ | ✅ | - | - | ✅ | - | ✅ |
| Arrays | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | - |
| If/Else | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | ✅ |
| Loops | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Functions | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | - |
| Recursion | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | - | - |
| Regular Expr | - | ✅ | ✅ | - | - | - | ✅ | - | - |
| Graphics | - | - | - | - | - | - | - | ✅ | - |

---

## Performance Notes

- **BASIC, Python, JavaScript, Pascal**: Fast execution ⚡
- **Prolog**: Slower due to backtracking; expected behavior
- **Forth**: Very fast; minimal overhead
- **Perl**: Good performance for text operations
- **Logo**: Graphics rendering adds minimal delay
- **PILOT**: Instant execution for education purposes

---

## Additional Resources

For more information:
- Check **SETUP.md** for installation and troubleshooting
- See **PROJECT_STATUS.md** for feature completeness status
- Review **README.md** in the root for project overview
- Browse **docs/** directory for detailed language documentation
- Check **INCOMPLETE_FEATURES.md** for known limitations

---

**Happy Learning! 🚀**

Master multiple programming languages from the 1970s-1990s era!

© 2025 Honey Badger Universe | Example Programs
