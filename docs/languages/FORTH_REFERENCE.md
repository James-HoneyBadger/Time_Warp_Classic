# Forth Language Reference

Complete reference for Forth syntax in Time Warp Classic.

## Stack-Based Programming

Forth uses a **stack** for computation:
- Values are pushed onto stack
- Operations consume values from stack
- Results are pushed back on stack

```
Stack Operations:

2 3 +      Stack: [2, 3] -> [5]
```

## Basic Syntax

```forth
: SQUARE   ( n -- n^2 )
    DUP * ;

5 SQUARE   \ Stack: [25]
```

## Stack Manipulation

### Core Stack Operations

```forth
DUP         Duplicate top of stack
DROP        Remove top of stack
SWAP        Swap top two values
ROT         Rotate top 3 values
OVER        Copy second value to top
DEPTH       Return stack depth
```

### Examples

```forth
5 DUP +     \ Stack: [5, 5] -> [10]
5 3 SWAP    \ Stack: [5, 3] -> [3, 5]
1 2 3 ROT   \ Stack: [1, 2, 3] -> [2, 3, 1]
```

## Arithmetic

### Basic Operations

```forth
+           Addition
-           Subtraction
*           Multiplication
/           Division
MOD         Modulo
```

### Examples

```forth
5 3 +       \ 8
5 3 -       \ 2
5 3 *       \ 15
6 2 /       \ 3
7 3 MOD     \ 1
```

## Comparison

```forth
=           Equal
<>          Not equal
<           Less than
>           Greater than
<=          Less or equal
>=          Greater or equal
```

### Results

```forth
5 3 >       \ 1 (true)
5 3 <       \ 0 (false)
```

## Variables

### Variable Declaration

```forth
VARIABLE x
VARIABLE count

5 x !       \ Store 5 in variable x
x @         \ Retrieve value from x (5)
```

### Constants

```forth
10 CONSTANT TEN
20 CONSTANT TWENTY

TEN TWENTY + \ 30
```

## Word Definitions

### Define Custom Words

```forth
: SQUARE    ( n -- n^2 )
    DUP * ;

: CUBE      ( n -- n^3 )
    DUP DUP * * ;

5 SQUARE    \ 25
3 CUBE      \ 27
```

### Word Stack Notation

```forth
( inputs -- outputs )

: ADD       ( n1 n2 -- n3 )
    + ;

: DOUBLE    ( n -- n*2 )
    2 * ;
```

## Control Structures

### Conditional (IF/THEN)

```forth
: ABS       ( n -- |n| )
    DUP 0 < IF
        NEGATE
    THEN ;

-5 ABS      \ 5
```

### If/Else

```forth
: MAX       ( n1 n2 -- max )
    2DUP < IF
        SWAP THEN
    DROP ;

5 3 MAX     \ 5
```

### Loops

#### DO/LOOP

```forth
: PRINT-NUMBERS   ( n -- )
    1 ?DO
        I .
    LOOP ;

10 PRINT-NUMBERS  \ Prints 1 2 3 4 5 6 7 8 9
```

#### DO/+LOOP

```forth
: COUNT-UP ( n -- )
    1 ?DO
        I .
    2 +LOOP ;

10 COUNT-UP   \ Prints 1 3 5 7 9
```

#### BEGIN/UNTIL

```forth
: COUNTDOWN ( n -- )
    BEGIN
        DUP .
        DUP 0 =
    UNTIL
    DROP ;

5 COUNTDOWN   \ Prints 5 4 3 2 1 0
```

## Arrays (Forth Arrays)

### CREATE and ALLOT

```forth
CREATE NUMBERS 10 ALLOT

1 NUMBERS !
2 NUMBERS 1 CELLS + !
3 NUMBERS 2 CELLS + !

NUMBERS @       \ 1
NUMBERS 1 CELLS + @  \ 2
```

## Input/Output

### Output

```forth
.           Emit number from stack
."          Emit string
EMIT        Emit character
CR          Carriage return (newline)
SPACE       Space
SPACES      Multiple spaces
```

### Examples

```forth
42 .        \ 42
." Hello"   \ Hello
CR          \ Newline
65 EMIT     \ A (ASCII 65)
```

### Input

```forth
ACCEPT      Get user input (string)
```

## Comments

```forth
\ This is a line comment

( This is a block comment
  spanning multiple lines )
```

## Memory Operations

```forth
@           Fetch (read from address)
!           Store (write to address)
+!          Add to memory location
```

## Stack Inspection

```forth
.S          Show entire stack
.           Pop and print top
```

## Complete Examples

### Factorial

```forth
: FACTORIAL ( n -- n! )
    1 SWAP
    1 ?DO
        I *
    LOOP ;

5 FACTORIAL  \ 120
```

### Fibonacci

```forth
: FIB ( n -- fib(n) )
    DUP 2 < IF
        EXIT
    THEN
    DUP 1 - RECURSE
    SWAP 2 - RECURSE + ;

6 FIB       \ 8
```

### Sum 1 to N

```forth
: SUMTO ( n -- sum )
    0 SWAP
    1 ?DO
        SWAP I +
        SWAP
    LOOP
    DROP ;

10 SUMTO    \ 55
```

## Recursion

```forth
: COUNTDOWN ( n -- )
    DUP 0 > IF
        DUP .
        1 - RECURSE
    THEN ;

5 COUNTDOWN  \ Prints 5 4 3 2 1
```

## Advanced: User-Defined Words

```forth
: SQUARE-SUM ( n1 n2 -- sum )
    DUP * SWAP DUP * + ;

3 4 SQUARE-SUM  \ 25 (3^2 + 4^2)

: HYPOTENUSE ( a b -- c )
    SQUARE-SUM SQRT ;

3 4 HYPOTENUSE  \ ~5.0
```

## Debugging

```forth
.S              Show entire stack
DEPTH           Stack depth
TRACE           Enable tracing
NOTRACE         Disable tracing
```

## Tips & Best Practices

1. **Use stack diagrams** in comments
2. **Keep words small** and composable
3. **Test incrementally** at console
4. **Document thoroughly** with notation
5. **Use meaningful names** for clarity
6. **Avoid deep stacks** (more than 3-4 values)

## Common Patterns

### Temporary Storage
```forth
: TEMP-STORE VARIABLE temp ;
x temp !  \ Save x
temp @    \ Retrieve x
```

### Word Composition
```forth
: QUAD SQUARE SQUARE ;   \ Fourth power
5 QUAD    \ 625
```

## See Also

- [LANGUAGE_TUTORIALS.md](../user/LANGUAGE_TUTORIALS.md)
- [examples/forth/](../../examples/forth/)

---

**Last Updated:** 2024
