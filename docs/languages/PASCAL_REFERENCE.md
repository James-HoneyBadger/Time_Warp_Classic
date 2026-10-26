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
- **LONGINT** - Large whole numbers
- **BYTE** - 0 to 255
- **WORD** - 0 to 65535
- **REAL** - Decimal numbers
- **DOUBLE** - Double-precision decimal numbers
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

WHILE condition DO BEGIN
    statements;
END;
```

`BEGIN` may open on the same line as the loop header; nested
`BEGIN ... END` blocks (including `IF ... THEN BEGIN`) are matched
correctly.

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

## Type Definitions

### TYPE Keyword

```pascal
TYPE
    TColor = (Red, Green, Blue, Yellow);
    TScoreArray = ARRAY[1..100] OF INTEGER;
    TMatrix = ARRAY[1..3, 1..3] OF REAL;
```

### Record Types

```pascal
TYPE
    TStudent = RECORD
        name : STRING;
        age : INTEGER;
        grade : REAL;
    END;

VAR
    student : TStudent;
BEGIN
    student.name := 'Alice';
    student.age := 20;
    student.grade := 3.8;
    WriteLn(student.name, ' age ', student.age);
END.
```

## String Operations

### Built-in String Functions

```pascal
Length(s)                { Returns length of string }
Copy(s, start, count)   { Returns substring }
Pos(substr, s)           { Find position of substring }
UpCase(ch)               { Uppercase a character }
Concat(s1, s2)           { Concatenate strings }

{ Examples }
VAR s : STRING;
BEGIN
    s := 'Hello World';
    WriteLn(Length(s));         { 11 }
    WriteLn(Copy(s, 1, 5));    { Hello }
    WriteLn(Pos('World', s));  { 7 }
END.
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

## Quick Reference

| Feature | Syntax | Example |
|---------|--------|---------|
| Variable | `VAR x : TYPE` | `VAR i : INTEGER` |
| Assign | `:=` | `x := 10` |
| Print | `WriteLn(expr)` | `WriteLn('Hi')` |
| Input | `ReadLn(var)` | `ReadLn(name)` |
| If/Then | `IF cond THEN ... ELSE` | `IF x > 5 THEN ...` |
| Case | `CASE var OF ... END` | `CASE x OF 1: ... END` |
| For Loop | `FOR i := a TO b DO` | `FOR i := 1 TO 10 DO` |
| While | `WHILE cond DO` | `WHILE x < 100 DO` |
| Repeat | `REPEAT ... UNTIL cond` | `REPEAT ... UNTIL done` |
| Function | `FUNCTION name : TYPE` | `FUNCTION Sqr(x) : INTEGER` |
| Procedure | `PROCEDURE name` | `PROCEDURE Print(msg)` |
| Array | `ARRAY[a..b] OF TYPE` | `ARRAY[1..10] OF INTEGER` |
| Record | `RECORD ... END` | `TPoint = RECORD x,y END` |
| Type | `TYPE name = ...` | `TYPE TColor = (R,G,B)` |

## See Also

- [LANGUAGE_TUTORIALS.md](../user/LANGUAGE_TUTORIALS.md)
- [examples/pascal/](../../examples/pascal/)

---

**Last Updated:** 2025
