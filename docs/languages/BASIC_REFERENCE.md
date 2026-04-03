# BASIC Language Reference

Complete reference for BASIC syntax and features in Time Warp Classic.

## Quick Reference

| Feature | Syntax | Example |
|---------|--------|---------|
| Variables | `LET var = value` | `LET x = 10` |
| Print | `PRINT expr` | `PRINT "Hello"` |
| Input | `INPUT prompt; var` | `INPUT "Name: "; name` |
| If/Then | `IF cond THEN ... END IF` | `IF x > 5 THEN PRINT "Big"` |
| Select Case | `SELECT CASE expr ... END SELECT` | `SELECT CASE x` |
| For Loop | `FOR var = start TO end ... NEXT` | `FOR i = 1 TO 10 NEXT i` |
| While Loop | `WHILE cond ... WEND` | `WHILE x < 100 WEND` |
| Do Loop | `DO ... WHILE cond` | `DO ... WHILE x > 0` |
| Subroutine | `GOSUB label ... RETURN` | `GOSUB PrintHeader` |
| Named Sub | `SUB name ... END SUB` | `SUB Greet(name)` |
| Function | `DEFFN name(args) = expr` | `DEFFN Square(x) = x*x` |
| Array | `DIM array(size)` | `DIM nums(10)` |
| Turtle | `FORWARD dist` | `FORWARD 100` |
| Sound | `BEEP` / `PLAY freq` | `PLAY 440` |

## Statements

### Variable Declaration & Assignment

```basic
LET variable = value
LET x = 5
LET name = "Alice"
LET pi = 3.14159
```

### Print Statement

```basic
PRINT expression
PRINT "Hello, World!"
PRINT 5 + 3
PRINT x; " is the answer"
```

### Input Statement

```basic
INPUT prompt; variable
INPUT "Enter name: "; name
INPUT "Age: "; age
```

### Comments

```basic
REM This is a comment
LET x = 5  REM Inline comment
```

## Control Structures

### If/Then/Else

```basic
IF condition THEN
    statements
ELSE
    statements
END IF

IF x > 5 THEN
    PRINT "Greater"
ELSE
    PRINT "Not greater"
END IF
```

### If/ElseIf/Else

```basic
IF x > 10 THEN
    PRINT "Large"
ELSE IF x > 5 THEN
    PRINT "Medium"
ELSE
    PRINT "Small"
END IF
```

### For Loop

```basic
FOR variable = start TO end [STEP increment]
    statements
NEXT variable

FOR i = 1 TO 10
    PRINT i
NEXT i

FOR j = 10 TO 1 STEP -1
    PRINT j
NEXT j
```

### While Loop

```basic
WHILE condition
    statements
END WHILE

LET x = 1
WHILE x <= 5
    PRINT x
    LET x = x + 1
END WHILE
```

### Do/While Loop

```basic
DO
    statements
WHILE condition

DO
    PRINT "Enter 0 to quit"
    INPUT x
WHILE x <> 0
```

### Select Case

```basic
SELECT CASE expression
    CASE value1
        statements
    CASE value2
        statements
    CASE ELSE
        statements
END SELECT

SELECT CASE grade
    CASE "A"
        PRINT "Excellent"
    CASE "B"
        PRINT "Good"
    CASE "C"
        PRINT "Average"
    CASE ELSE
        PRINT "Needs improvement"
END SELECT
```

### Loop Alternatives

`WEND` can be used as an alternative to `END WHILE`:

```basic
WHILE x < 10
    PRINT x
    LET x = x + 1
WEND
```

### Loop Control

```basic
EXIT FOR         Break out of current FOR loop
EXIT WHILE       Break out of current WHILE loop
EXIT DO          Break out of current DO loop
```

Example:
```basic
FOR i = 1 TO 100
    IF i > 10 THEN EXIT FOR
    PRINT i
NEXT i
```

## Data Types & Operators

### Data Types

- **Numbers:** Integer or floating-point
- **Strings:** Text in quotes
- **Boolean:** TRUE or FALSE

```basic
LET x = 42         REM Integer
LET pi = 3.14159   REM Float
LET name = "Alice" REM String
LET active = TRUE  REM Boolean
```

### Arithmetic Operators

```basic
+       Addition         5 + 3 = 8
-       Subtraction      5 - 3 = 2
*       Multiplication   5 * 3 = 15
/       Division         6 / 2 = 3
MOD     Modulo           7 MOD 3 = 1
^       Power            2 ^ 3 = 8
```

### Comparison Operators

```basic
=       Equal            5 = 5
<>      Not equal        5 <> 3
<       Less than        3 < 5
>       Greater than     5 > 3
<=      Less or equal    5 <= 5
>=      Greater or equal 5 >= 5
```

### Logical Operators

```basic
AND     Logical AND      IF x > 5 AND y < 10
OR      Logical OR       IF x = 1 OR x = 2
NOT     Logical NOT      IF NOT done
```

## Functions

### String Functions

```basic
LEN(string)         Returns length
UPPER(string)       Convert to uppercase
LOWER(string)       Convert to lowercase
LEFT(string, n)     First n characters
RIGHT(string, n)    Last n characters
MID(string, start, n)  n characters starting at position
INSTR(string, sub)  Find position of substring (0 if not found)
CHR$(n)             Character from ASCII code
ASC(string)         ASCII code of first character
STR$(n)             Convert number to string
VAL(string)         Convert string to number
BIN(n)              Convert number to binary string
OCT(n)              Convert number to octal string
HEX(n)              Convert number to hexadecimal string
```

### Math Functions

```basic
ABS(x)              Absolute value
SQRT(x)             Square root
INT(x)              Integer part (truncate toward zero)
FIX(x)              Integer part (truncate toward zero, alias)
CEIL(x)             Ceiling (round up)
RND(n)              Random number 0 to n
SIN(x)              Sine (radians)
COS(x)              Cosine (radians)
TAN(x)              Tangent (radians)
ATN(x)              Arctangent (radians)
EXP(x)              e raised to x
EXP2(x)             2 raised to x
EXP10(x)            10 raised to x
LOG(x)              Natural logarithm (ln)
LOG2(x)             Base-2 logarithm
LOG10(x)            Base-10 logarithm
```

### Array Functions

```basic
SUM(array)          Sum of all elements
AVG(array)          Average of elements
MAX(array)          Maximum value
MIN(array)          Minimum value
SORT(array)         Sort array in ascending order
```

### Example Functions

```basic
FUNCTION ABS(x)
    IF x < 0 THEN
        ABS = -x
    ELSE
        ABS = x
    END IF
END FUNCTION

FUNCTION Factorial(n)
    IF n <= 1 THEN
        Factorial = 1
    ELSE
        Factorial = n * Factorial(n - 1)
    END IF
END FUNCTION

LET result = ABS(-5)
LET fact = Factorial(5)
```

## Arrays

### Array Declaration

```basic
DIM array(size)
DIM numbers(10)      REM 11 elements (0-10)
DIM matrix(5, 5)     REM 2D array
```

### Array Operations

```basic
DIM scores(5)
LET scores(1) = 95
LET scores(2) = 87
PRINT scores(1)
PRINT SUM(scores)
PRINT AVG(scores)
```

## Subroutines

### GOSUB/RETURN

```basic
GOSUB subroutine_name
statements
GOTO skip_label

subroutine_name:
    statements
    RETURN

skip_label:
    remaining code
```

### SUB/END SUB (Named Subroutines)

```basic
SUB PrintHeader
    PRINT "===== Report ====="
END SUB

SUB Greet(name)
    PRINT "Hello, "; name; "!"
END SUB

CALL PrintHeader
CALL Greet("Alice")
```

### DEFFN (User-Defined Functions)

```basic
DEFFN Square(x) = x * x
DEFFN Cube(x) = x * x * x
DEFFN Avg2(a, b) = (a + b) / 2

PRINT Square(5)      REM 25
PRINT Cube(3)        REM 27
PRINT Avg2(10, 20)   REM 15
```

### INCR, DECR, and SWAP

```basic
LET x = 10
INCR x          REM x is now 11
DECR x          REM x is now 10

LET a = 5
LET b = 99
SWAP a, b       REM a is now 99, b is now 5
```

### Example

```basic
GOSUB PrintHeader
PRINT "Main program"
GOTO SkipPrint

PrintHeader:
    PRINT "===== Report ====="
    RETURN

SkipPrint:
PRINT "Done"
END
```

## Graphics

### Direct Graphics

```basic
PSET x, y            Plot a single point
LINE x1, y1, x2, y2  Draw line between two points
BOX x1, y1, x2, y2   Draw filled rectangle
CIRCLE x, y, r       Draw circle with center (x, y) and radius r
```

### Turtle Graphics

BASIC also supports turtle graphics commands:

```basic
FORWARD 100          Move turtle forward
BACKWARD 50          Move turtle backward
RIGHT 90             Turn right (degrees)
LEFT 45              Turn left (degrees)
PENUP                Lift pen (stop drawing)
PENDOWN              Lower pen (resume drawing)
```

Example — draw a square:
```basic
FOR i = 1 TO 4
    FORWARD 100
    RIGHT 90
NEXT i
END
```

## Sound

```basic
BEEP                 Produce a short beep
PLAY frequency       Play a tone at the given frequency (Hz)
SOUND freq, duration Play tone for specified duration
NOTE note_name       Play a named musical note (e.g., "C4")
```

## Timing

```basic
DELAY milliseconds   Pause execution for the given time
```

## Data Statements

```basic
DATA 10, 20, 30, 40, 50
READ x               Read next DATA value into x
RESTORE              Reset DATA pointer to the beginning
```

Example:
```basic
DATA 3, 1, 4, 1, 5
FOR i = 1 TO 5
    READ n
    PRINT n
NEXT i
END
```

## File I/O

### File Operations

```basic
OPEN file FOR mode AS file_num
CLOSE file_num
READ file_num, var
WRITE file_num, expr
```

## Complete Example Programs

### Hello World

```basic
PRINT "Hello, World!"
END
```

### Temperature Converter

```basic
INPUT "Enter Celsius: "; celsius
LET fahrenheit = (celsius * 9 / 5) + 32
PRINT celsius; "C ="; fahrenheit; "F"
END
```

### Fibonacci Sequence

```basic
FUNCTION Fib(n)
    IF n <= 1 THEN
        Fib = n
    ELSE
        Fib = Fib(n-1) + Fib(n-2)
    END IF
END FUNCTION

FOR i = 0 TO 10
    PRINT Fib(i)
NEXT i
END
```

### Number Guessing Game

```basic
LET secret = RND(100)
LET guess = 0
LET tries = 0

WHILE guess <> secret
    INPUT "Guess (0-100): "; guess
    LET tries = tries + 1
    
    IF guess > secret THEN
        PRINT "Too high"
    ELSE IF guess < secret THEN
        PRINT "Too low"
    ELSE
        PRINT "Correct! Tries:"; tries
    END IF
END WHILE
END
```

## Tips & Tricks

1. **Comments:** Use REM for clarity
2. **Variable Names:** Use descriptive names (score, total)
3. **Indentation:** Makes code more readable
4. **Testing:** Test with boundary values
5. **Debugging:** Use PRINT to trace execution

## See Also

- [USER_GUIDE.md](../user/USER_GUIDE.md)
- [LANGUAGE_TUTORIALS.md](../user/LANGUAGE_TUTORIALS.md)
- [examples/basic/](../../examples/basic/)

---

**Last Updated:** 2025
