# Pascal Language Reference

Complete reference for Pascal syntax in Time Warp Classic.

## Program Structure

```pascal
PROGRAM ProgramName;

VAR
    { Variable declarations }

FUNCTION FunctionName(params) : ReturnType;
BEGIN
    { Function body }
END;

PROCEDURE ProcedureName(params);
BEGIN
    { Procedure body }
END;

BEGIN
    { Main program body }
END.
```

## Variables & Types

### Variable Declaration

```pascal
VAR
    count : INTEGER;
    name : STRING;
    height : REAL;
    isActive : BOOLEAN;
    numbers : ARRAY[1..10] OF INTEGER;
```

### Data Types

- **INTEGER** - Whole numbers
- **REAL** - Decimal numbers
- **STRING** - Text
- **BOOLEAN** - TRUE or FALSE
- **CHAR** - Single character

## Operators

### Arithmetic

```pascal
+       Addition
-       Subtraction
*       Multiplication
/       Division
DIV     Integer division
MOD     Modulo
```

### Comparison

```pascal
=       Equal
<>      Not equal
<       Less than
>       Greater than
<=      Less or equal
>=      Greater or equal
```

### Logical

```pascal
AND     Logical AND
OR      Logical OR
NOT     Logical NOT
```

## Control Structures

### If/Then/Else

```pascal
IF condition THEN
    statements
ELSE
    statements;
```

### Case Statement

```pascal
CASE variable OF
    1: WriteLn('One');
    2: WriteLn('Two');
    3: WriteLn('Three');
    ELSE WriteLn('Other');
END;
```

### For Loop

```pascal
FOR i := 1 TO 10 DO
    WriteLn(i);

FOR j := 10 DOWNTO 1 DO
    WriteLn(j);
```

### While Loop

```pascal
WHILE condition DO
BEGIN
    statements;
END;
```

### Repeat Until

```pascal
REPEAT
    statements;
UNTIL condition;
```

## Functions & Procedures

### Function

```pascal
FUNCTION Double(x : INTEGER) : INTEGER;
BEGIN
    Double := x * 2;
END;

VAR result : INTEGER;
BEGIN
    result := Double(5);
    WriteLn(result);
END.
```

### Procedure

```pascal
PROCEDURE PrintMessage(msg : STRING);
BEGIN
    WriteLn(msg);
END;

BEGIN
    PrintMessage('Hello');
END.
```

### Recursion

```pascal
FUNCTION Factorial(n : INTEGER) : INTEGER;
BEGIN
    IF n <= 1 THEN
        Factorial := 1
    ELSE
        Factorial := n * Factorial(n - 1);
END;
```

## Input/Output

### Writing Output

```pascal
WriteLn('Hello');           { With newline }
Write('Hello');             { Without newline }
WriteLn('Value: ', x);      { Multiple values }
```

### Reading Input

```pascal
ReadLn(name);               { Read string }
ReadLn(age);                { Read number }
```

## Arrays

### Array Declaration

```pascal
VAR
    numbers : ARRAY[1..10] OF INTEGER;
    matrix : ARRAY[1..5, 1..5] OF REAL;
```

### Array Operations

```pascal
numbers[1] := 10;
numbers[2] := 20;
WriteLn(numbers[1]);
```

## Complete Examples

### Fibonacci

```pascal
PROGRAM Fibonacci;
VAR i : INTEGER;

FUNCTION Fib(n : INTEGER) : INTEGER;
BEGIN
    IF n <= 1 THEN
        Fib := n
    ELSE
        Fib := Fib(n-1) + Fib(n-2);
END;

BEGIN
    FOR i := 0 TO 10 DO
        WriteLn(Fib(i));
END.
```

### Sum of Numbers

```pascal
PROGRAM Sum;
VAR
    i, total : INTEGER;
BEGIN
    total := 0;
    FOR i := 1 TO 10 DO
        total := total + i;
    WriteLn('Sum: ', total);
END.
```

## See Also

- [LANGUAGE_TUTORIALS.md](../user/LANGUAGE_TUTORIALS.md)
- [examples/pascal/](../../examples/pascal/)

---

**Last Updated:** 2024
