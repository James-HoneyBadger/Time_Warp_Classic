# Forth Language Reference

Charles Moore developed Forth around 1970: a stack machine, a dictionary
of words, and an interpreter small enough to fit in a few kilobytes.
FORTH-79, FORTH-83 and ANS Forth (1994) standardised it; Gforth is the usual
modern implementation.

Time Warp Classic runs its own Forth in `core/languages/forth.py`, written in
Python. The core is solid: the data stack, arithmetic, colon definitions,
`IF`/`ELSE`/`THEN`, `DO`/`LOOP`, `BEGIN` loops, variables and constants.
Beyond that it isn't a real Forth. There's no memory model, no `HERE`, no
compile-time words, and output is line-based. Everything below was checked
by running it.

## Contents

- [Program Structure](#program-structure)
- [Output Model](#output-model)
- [Word Reference](#word-reference)
- [Defining Words](#defining-words)
- [Control Structures](#control-structures)
- [Variables, Constants and Arrays](#variables-constants-and-arrays)
- [Floating Point](#floating-point)
- [Examples](#examples)
- [Differences from Classic Forth](#differences-from-classic-forth)
- [See Also](#see-also)

## Program Structure

```forth
\ Square a number
: SQUARE ( n -- n*n ) DUP * ;
5 SQUARE .
```

```text
Defined word: SQUARE
25
```

- The program runs line by line, interpreting words left to right.
- **Built-in words are upper case.** `dup` is an unknown word. Your own
  words and variables are case-sensitive and match exactly as defined.
- `\` comments to end of line. `( … )` comments must open and close on the
  same line.
- A colon definition can span several lines; it ends at `;`.
- **Any error ends the program**: an unknown word, stack underflow or
  division by zero prints a message and stops the run.

## Output Model

Output is line-oriented, unlike a real Forth terminal:

| Word | Prints |
|------|--------|
| `.` | Pops and prints the top of stack on **its own line** |
| `." text"` | Prints `text` on its own line. The space after `."` is printed too, so `." Hi"` shows ` Hi` and `."Hi"` shows `Hi` |
| `CR` | An empty line |
| `EMIT` | The character on its own line (`65 EMIT` gives `A`) |
| `n SPACES` | A line of `n` spaces |
| `.S` | The stack, non-destructively: `<3> 1 2 3` |

So `1 . 2 .` prints two lines, `1` and `2`, not `1 2 `.

There is no input: `KEY`, `ACCEPT` and `EXPECT` don't exist.

## Word Reference

### Stack

| Word | Effect |
|------|--------|
| `DUP` | `( a -- a a )` |
| `DROP` | `( a -- )` |
| `SWAP` | `( a b -- b a )` |
| `OVER` | `( a b -- a b a )` |
| `ROT` | `( a b c -- b c a )` |
| `NIP` | `( a b -- b )` |
| `TUCK` | `( a b -- b a b )` |
| `2DUP` | `( a b -- a b a b )` |
| `2DROP` | `( a b -- )` |
| `PICK` | `( … n -- … x )`, `0 PICK` = `DUP` |
| `ROLL` | `( … n -- … )` moves the nth item to the top |
| `DEPTH` | Pushes the number of items on the stack |

### Arithmetic

| Word | Example | Result |
|------|---------|--------|
| `+` `-` `*` | `6 7 * .` | `42` |
| `/` | `7 2 / .` | `3` (integer, truncates toward zero: `-7 2 /` gives `-3`) |
| `MOD` | `17 5 MOD .` | `2` (Python-style: `-7 2 MOD` gives `1`) |
| `**` | `2 10 ** .` | `1024` (integer power, not standard Forth) |
| `NEGATE` `ABS` | `-5 ABS .` | `5` |
| `MIN` `MAX` | `3 7 MAX .` | `7` |
| `1+` `1-` `2+` `2-` `2*` `2/` | `9 2/ .` | `4` |

### Comparison and logic

True is `-1`, false is `0`, as in standard Forth.

| Word | Example | Result |
|------|---------|--------|
| `=` `<>` `<` `>` `<=` `>=` | `5 3 > .` | `-1` |
| `0=` `0<` `0>` | `0 0= .` | `-1` |
| `AND` `OR` `XOR` | `12 10 AND .` | `8` |
| `INVERT` | `0 INVERT .` | `-1` |
| `TRUE` `FALSE` | `TRUE .` | `-1` |

### Maths

| Word | Example | Result |
|------|---------|--------|
| `SIN` `COS` `TAN` | `30 SIN .` | `0.49999999999999994` (argument in **degrees**) |
| `SQRT` | `2 SQRT .` | `1.4142135623730951` |
| `LOG` | natural log | |
| `EXP` | `1 EXP .` | `2.718281828459045` |
| `PI` `E` | `PI .` | `3.141592653589793` |

These work on the integer stack and leave Python floats there.

## Defining Words

```forth
: SQUARE DUP * ;
: CUBE DUP SQUARE * ;
3 CUBE .
```

```text
Defined word: SQUARE
Defined word: CUBE
27
```

- `: name … ;` defines a word and logs `Defined word: name`.
- Redefining a word replaces it.
- `RECURSE` calls the word being defined:

```forth
: FACT DUP 1 > IF DUP 1- RECURSE * THEN ;
5 FACT .
```

```text
120
```

## Control Structures

Loops only loop **inside a colon definition**. At the top level, `DO … LOOP`
and `BEGIN … UNTIL` run their body once (`UNTIL` prints a warning saying so).
`IF … THEN` works at the top level.

| Structure | Example |
|-----------|---------|
| `IF … THEN` | `: POS? 0 > IF ." positive" THEN ;` |
| `IF … ELSE … THEN` | `: SIGN 0 < IF ." negative" ELSE ." non-negative" THEN ;` |
| `limit start DO … LOOP` | `: COUNT 10 0 DO I . LOOP ;` prints 0 to 9 |
| `limit start DO … n +LOOP` | `: EVENS 10 0 DO I . 2 +LOOP ;` prints 0 2 4 6 8 |
| `BEGIN … flag UNTIL` | `: CD 5 BEGIN DUP . 1- DUP 0= UNTIL DROP ;` prints 5 to 1 |
| `BEGIN … flag WHILE … REPEAT` | `: W 0 BEGIN DUP 5 < WHILE DUP . 1+ REPEAT DROP ;` prints 0 to 4 |

- `I` is the innermost loop index and `J` the next one out. Nested `DO`
  loops and nested `IF`s work.
- A negative `+LOOP` step counts down: `0 10 DO I . -2 +LOOP` prints
  10 down to 0.
- **`I` and `J` fail inside an `IF` branch** within a loop, and the run stops
  silently. Read the index before the `IF`:

```forth
\ Works: I is fetched before IF
: SHOW 3 0 DO I DUP 0= IF ." zero" DROP ELSE . THEN LOOP ;
SHOW
```

```text
 zero
1
2
```

Not available: `LEAVE`, `UNLOOP`, `?DO`, `EXIT`, `CASE … OF … ENDOF … ENDCASE`,
`AGAIN`.

## Variables, Constants and Arrays

```forth
VARIABLE X
42 X !
X @ .
X @ 1+ X !
X @ .
100 CONSTANT HUNDRED
HUNDRED .
```

```text
Variable declared: X
42
43
Constant declared: HUNDRED
100
```

| Word | Effect |
|------|--------|
| `VARIABLE name` | Creates a cell holding 0 |
| `n CONSTANT name` | Creates a word that pushes `n` |
| `!` `@` | Store and fetch |
| `n VALUE name` | Same as `CONSTANT`. `TO` is a stub, so values can't change |
| `CREATE name n CELLS ALLOT` | A simple array. `CELLS` is a no-op (one cell = one slot) |

Arrays use name-plus-offset references:

```forth
CREATE ARR 10 CELLS ALLOT
5 ARR 2 + !
ARR 2 + @ .
```

```text
5
```

Not available: `+!`, `HERE`, `,` (comma), `C@`/`C!`, `FILL`, `MOVE`.

## Floating Point

A number containing one `.` goes to a separate float stack. Float words:
`F+ F- F* F/ F. FDUP FDROP FSWAP F@ F!`.

```forth
5.0 2.0 F/ F.
1.5 2.3 F+ F.
```

```text
2.5
3.8
```

`1.5 .` fails with a stack underflow, because `.` reads the integer stack.
`FSIN` and other float maths words don't exist; use `SIN` on the integer
stack.

### Partial and stub words

These words exist but are simplified or do nothing useful:

- Double-cell words: `D+ D- D* D/ D. D@ D!`.
- Heap words: `ALLOCATE FREE RESIZE`. These return an id and a flag, but
  there is no way to address the memory.
- File words: `OPEN-FILE CLOSE-FILE READ-FILE WRITE-FILE FILE-POSITION
  REPOSITION-FILE` are simulated and print `… simulated (educational mode)`.
- String words: `COMPARE SEARCH SLITERAL` operate on placeholder strings.
- Exceptions: `TRY CATCH THROW` have no real effect; `THROW` prints
  `Exception thrown: n`.
- Structures and objects: `STRUCT FIELD END-STRUCT OBJECT METHOD END-OBJECT
  NEW SEND` only print a message.
- A quoted token like `"abc"` pushes a Python string, which `.` prints.

## Examples

### FizzBuzz

```forth
: FIZZ 16 1 DO
    I DUP 15 MOD 0= IF ." FizzBuzz" DROP ELSE
    DUP 3 MOD 0= IF ." Fizz" DROP ELSE
    DUP 5 MOD 0= IF ." Buzz" DROP ELSE
    . THEN THEN THEN
  LOOP ;
FIZZ
```

Prints 1, 2, ` Fizz`, 4, ` Buzz`, … ` FizzBuzz`, one item per line.

### Factorial with a loop

```forth
: FACT ( n -- n! ) 1 SWAP 1+ 1 DO I * LOOP ;
5 FACT .
10 FACT .
```

```text
Defined word: FACT
120
3628800
```

### Sum of squares with a variable

```forth
VARIABLE TOTAL
: SUMSQ ( n -- ) 0 TOTAL ! 1+ 1 DO I DUP * TOTAL @ + TOTAL ! LOOP ;
10 SUMSQ
TOTAL @ .
```

```text
Variable declared: TOTAL
Defined word: SUMSQ
385
```

Longer programs: `examples/forth/engineering_calc.fth` and
`examples/forth/number_theory.fth`.

## Differences from Classic Forth

- Output is one line per `.`, `."`, `EMIT` or `SPACES`. You can't build a
  line from several words, and `."` keeps the separating space.
- Built-in words are upper case only.
- Loops work only inside colon definitions.
- `I`/`J` inside an `IF` branch in a loop abort the run without a message.
- No `LEAVE`, `EXIT`, `?DO`, `CASE`, `+!`, `SPACE`, `HERE`, `,`, `KEY`,
  `ACCEPT`, `IMMEDIATE`, `POSTPONE`, `[']`, `EXECUTE`, `DOES>`, or number
  bases (`HEX`, `DECIMAL`).
- Values are Python numbers, not fixed-width cells: no overflow, and trig
  functions leave floats on the integer stack.
- `/` truncates toward zero but `MOD` follows Python's floored rule, so
  `/` and `MOD` disagree for negative operands.
- Multi-line `( … )` comments aren't supported, and `( … )` inside a `."`
  string is removed as a comment: `." Say (hi) there"` prints ` Say  there`.
- Any error ends the program; there is no interactive recovery. The run
  still reports exit status 0.

## See Also

- [Language Tutorials](../user/LANGUAGE_TUTORIALS.md)
- [Forth examples](../../examples/forth/)
