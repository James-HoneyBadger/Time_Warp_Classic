# BASIC Language Reference

Complete reference for BASIC syntax and features in Time Warp Classic.

## Quick Reference

| Feature | Syntax | Example |
|---------|--------|---------|
| Variables | `LET var = value` | `LET x = 10` |
| Print | `PRINT expr` | `PRINT "Hello"` |
| Input | `INPUT prompt; var` | `INPUT "Name: "; name` |
| If/Then | `IF cond THEN ... END IF` | `IF x > 5 THEN PRINT "Big"` |
| For Loop | `FOR var = start TO end ... NEXT` | `FOR i = 1 TO 10 NEXT i` |
| While Loop | `WHILE cond ... END WHILE` | `WHILE x < 100 WEND` |
| Function | `FUNCTION name(args)` | `FUNCTION ABS(x)` |
| Array | `DIM array(size)` | `DIM nums(10)` |

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
```

### Math Functions

```basic
ABS(x)              Absolute value
SQRT(x)             Square root
INT(x)              Integer part
RND(n)              Random 0 to n
SIN(x)              Sine (radians)
COS(x)              Cosine (radians)
TAN(x)              Tangent (radians)
```

### Array Functions

```basic
SUM(array)          Sum of all elements
AVG(array)          Average of elements
MAX(array)          Maximum value
MIN(array)          Minimum value
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

### Subroutine Definition & Call

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

### Basic Graphics

```basic
PLOT x, y           Draw point at (x, y)
LINE x1, y1, x2, y2 Draw line
BOX x1, y1, x2, y2  Draw filled box
CIRCLE x, y, r      Draw circle
```

### Example

```basic
PLOT 50, 50
LINE 0, 0, 100, 100
BOX 10, 10, 90, 90
CIRCLE 50, 50, 25
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

**Last Updated:** 2024
