# BASIC Language Reference

Time Warp Classic's BASIC is its own dialect, implemented in Python in
`core/languages/basic.py` with expression evaluation in `core/interpreter.py`.
It borrows from 1970s line-numbered BASIC and from the structured BASICs of
the late 1980s (Turbo BASIC, QuickBASIC): `IF … END IF`, `DO … LOOP`,
`WHILE … WEND`, `SELECT CASE`. It is not a clone of any of them. This page
documents what the interpreter actually does, quirks included; every example
output below was produced by running it.

## Contents

- [Program Structure](#program-structure)
- [Direct Mode (the console bar)](#direct-mode-the-console-bar)
- [Statement Reference](#statement-reference)
- [Expressions and Operators](#expressions-and-operators)
- [Built-in Functions](#built-in-functions)
- [Arrays](#arrays)
- [Graphics](#graphics)
- [Sound](#sound)
- [File I/O](#file-io)
- [Examples](#examples)
- [Differences from Classic BASIC](#differences-from-classic-basic)
- [See Also](#see-also)

## Program Structure

```basic
10 REM Count to three
20 FOR I = 1 TO 3
30   PRINT "Line "; I
40 NEXT I
50 END
```

- **One statement per line.** There is no `:` statement separator.
- **Line numbers are optional** but are the only jump targets: `GOTO` and
  `GOSUB` take a number, not a label.
- **Lines run in the order they appear in the editor.** The Run button does
  not sort by line number; the console's `RUN` does (see below).
- **Keywords are case-insensitive. Variable names are case-sensitive**:
  `x` and `X` are different variables.
- `REM` starts a comment line. Trailing comments after a statement are not
  supported (`LET X = 5 REM note` is a syntax error).
- A `$` suffix is allowed (`N$`) but is just part of the name; any variable
  can hold a number or a string.

## Direct Mode (the console bar)

In both the desktop IDE and the web IDE, the **Console** bar under the
editor behaves like a home computer's prompt whenever BASIC is selected and
no program is running.

```text
>PRINT 2+2
4
>10 PRINT "HELLO"
OK
>LIST
10 PRINT "HELLO"
>RUN
HELLO
READY.
```

| Type this | What happens |
|-----------|--------------|
| `10 PRINT "HI"` | Stores (or replaces) line 10 in the editor, kept in line-number order |
| `10` | Deletes line 10 |
| `LIST` | Lists the program, sorted by line number |
| `RUN` | Runs the program in line-number order |
| `RUN 100` | Runs from line 100 (unnumbered lines are dropped) |
| `RENUMBER` | Renumbers 10, 20, 30 … and rewrites `GOTO`/`GOSUB`/`THEN` targets |
| `NEW` | Clears the program and variables |
| `TRON` / `TROFF` | Turns line tracing on / off |
| `HELP` | Lists the console commands |
| `PRINT 2+2`, `LET A=5`, `A=5` | Executes immediately |
| `INPUT A` | Waits for a value typed into the console bar |

Flow-control statements that only make sense in a stored program (`FOR`,
`NEXT`, `GOTO`, `GOSUB`, `IF`, `WHILE`, `DO`, …) answer `?ILLEGAL DIRECT`.
Unknown statements answer `?SYNTAX ERROR`; a stopped program reports
`BREAK IN <line>`. `RUN` starts from a clean slate, so a program never
inherits variables left over from the console.

`INPUT` is interactive in both IDEs, in direct mode and in running
programs: the program pauses and the next line typed into the console bar
becomes the value.

## Statement Reference

### Core statements

| Statement | Syntax | Notes |
|-----------|--------|-------|
| `LET` | `LET X = expr` or `X = expr` | `LET` is optional |
| `PRINT` | `PRINT item; item, …` | See [PRINT](#print) |
| `INPUT` | `INPUT var` / `INPUT "prompt"; var` | Numeric-looking input is stored as a number |
| `REM` | `REM text` | Whole-line comment |
| `GOTO` | `GOTO 100` | Line number only |
| `GOSUB` / `RETURN` | `GOSUB 1000` … `RETURN` | Line number only; nests |
| `END` | `END` | Stops the program |
| `DIM` | `DIM A(10)`, `DIM M(3,3)` | See [Arrays](#arrays) |

### PRINT

`PRINT` evaluates each item and joins the results **with no separator**:
`;` and `,` both just concatenate. Add spaces yourself.

```basic
10 X = 2
20 PRINT "X="; X, "done"
30 PRINT X; " is the answer"
```
```text
X=2done
2 is the answer
```

There are no print zones, `TAB()` or `SPC()`, and a trailing `;` does not
suppress the newline.

### INPUT

```basic
10 INPUT "Name: "; N$
20 INPUT A
30 PRINT "Hi "; N$; " "; A + 1
```

With no prompt, `INPUT A` shows `Enter value for A:`. Input containing a `.`
becomes a float, other numeric input an integer, anything else a string.

### Decisions

```basic
10 IF X > 5 THEN PRINT "big"
20 IF X > 5 THEN PRINT "big" ELSE PRINT "small"
30 IF X > 5 THEN GOTO 100
```

Block form (each keyword on its own line; `ELSE IF` is two words):

```basic
10 X = 7
20 IF X > 10 THEN
30   PRINT "Large"
40 ELSE IF X > 5 THEN
50   PRINT "Medium"
60 ELSE
70   PRINT "Small"
80 END IF
```
```text
Medium
```

`IF … THEN 100` (a bare line number after `THEN`) is **not** an implicit
`GOTO`; write `THEN GOTO 100`.

### SELECT CASE

```basic
10 N = 7
20 SELECT CASE N
30   CASE 1, 2, 3
40     PRINT "low"
50   CASE 4 TO 9
60     PRINT "mid"
70   CASE ELSE
80     PRINT "other"
90 END SELECT
```
```text
mid
```

`CASE` accepts single values, comma lists and `a TO b` ranges, and works
with strings (`CASE "A"`). `CASE IS > n` is not supported.

### Loops

| Form | Syntax |
|------|--------|
| Counted | `FOR I = a TO b [STEP s]` … `NEXT [I]` |
| Pre-test | `WHILE cond` … `WEND` (or `END WHILE`) |
| Pre-test | `DO WHILE cond` … `LOOP` |
| Post-test | `DO` … `LOOP WHILE cond` / `LOOP UNTIL cond` |
| Endless | `DO` … `LOOP` |

`STEP` may be negative or fractional (`FOR I = 0 TO 1 STEP 0.5` prints
`0`, `0.5`, `1.0`). `DO` must be closed by `LOOP`; `DO … WHILE cond` without
`LOOP` does not repeat.

```basic
10 X = 0
20 DO
30   X = X + 1
40 LOOP UNTIL X >= 3
50 PRINT X
```
```text
3
```

`EXIT FOR`, `EXIT WHILE` and `EXIT DO` exist but do **not** jump out
immediately: they discard the loop's bookkeeping and execution carries on
with the next line, so the rest of the loop body runs once more, and
`EXIT FOR` then prints `NEXT without FOR` at the `NEXT`. To leave a loop
early, `GOTO` the line after it:

```basic
10 FOR I = 1 TO 10
20   IF I > 3 THEN GOTO 50
30   PRINT I
40 NEXT I
50 PRINT "out"
```

### Extended statements

| Statement | Syntax | Effect |
|-----------|--------|--------|
| `INCR` / `DECR` | `INCR X` | Adds / subtracts 1. The `INCR X, n` form does not work (see Limitations) |
| `SWAP` | `SWAP A, B` | Exchanges two variables |
| `RANDOMIZE` | `RANDOMIZE [seed]` | Seeds the random generator |
| `DELAY` | `DELAY seconds` | Pauses; the argument is in **seconds** (`DELAY 0.5`) |
| `SORT` | `SORT A` | Sorts a 1-D array in place, ascending |

### Accepted but not implemented

These parse without error but only echo a note to the output (or do
nothing): `SUB … END SUB` (the body runs inline like ordinary lines),
`CALL`, `DEFFN`, `DRAW`, `PALETTE`, `CIRCLE`, `PSET`, `PRESET`, and the
`MP…`, `NET…` and `MUSIC…` commands. There are no user-defined functions:
`DEF FN`, `DEFFN` and `FUNCTION` are not available.

## Expressions and Operators

| Operator | Meaning | Example → result |
|----------|---------|------------------|
| `+ - *` | Arithmetic; `+` also joins strings | `2 + 3 * 4` → `14` |
| `/` | Division, always floating point | `6 / 2` → `3.0`, `10 / 3` → `3.3333333333333335` |
| `^` | Power | `2 ^ 3` → `8` |
| `MOD` | Remainder | `7 MOD 3` → `1` |
| `= <> < > <= >=` | Comparison | `5 <> 3` → `True` |
| `AND OR NOT` | Logical | `NOT 0` → `True` |

Comparisons yield Python booleans, so `PRINT 5 > 3` shows `True`. There is
no `\` integer-division operator and no `TRUE`/`FALSE` constants (use `1`
and `0`).

A variable that has never been assigned is not zero: an expression that
mentions one is printed back as text (`PRINT Y + 1` shows `Y + 1`).
Initialise variables before use.

## Built-in Functions

Function names are upper-case.

### Math

| Function | Result |
|----------|--------|
| `ABS(x)` | Absolute value |
| `INT(x)` | Truncates toward zero: `INT(-3.7)` → `-3` |
| `FIX(x)` | Truncates toward zero (same as `INT` here) |
| `CEIL(x)` | Rounds up |
| `SQRT(x)` | Square root, always a float: `SQRT(16)` → `4.0` |
| `SIN(x)` `COS(x)` `TAN(x)` | Trigonometry with the angle in **degrees**: `SIN(90)` → `1.0` |
| `EXP(x)` `EXP2(x)` `EXP10(x)` | e^x, 2^x, 10^x |
| `LOG(x)` `LOG2(x)` `LOG10(x)` | Logarithms; return `0` for x ≤ 0 |
| `RND(1)` | Float in [0, 1) |
| `RND(n)` | Float in [0, n) — not an integer; use `INT(RND(1) * n) + 1` for dice |

`ATN`, `SGN` and `TIMER` are not available.

### Strings

| Function | Result |
|----------|--------|
| `LEN(s)` | Length |
| `LEFT(s, n)` / `LEFT$(s, n)` | First n characters |
| `RIGHT(s, n)` / `RIGHT$(s, n)` | Last n characters |
| `MID(s, start, n)` / `MID$(s, start, n)` | n characters from 1-based `start` |
| `INSTR(s, sub)` | 1-based position, `0` if absent |
| `UCASE(s)` / `UPPER(s)` | Upper case |
| `LCASE(s)` / `LOWER(s)` | Lower case |
| `CHR$(n)` / `CHR(n)` | Character for a code |
| `ASC(s)` | Code of first character |
| `STR$(n)` | Number to string |
| `VAL(s)` | String to number |
| `BIN(n)` `OCT(n)` `HEX(n)` | Base conversion, no prefix: `HEX(255)` → `ff` |

### Array aggregates

`SUM(A)`, `AVG(A)`, `MIN(A)`, `MAX(A)` take an array name. Unassigned
elements count as `0`.

## Arrays

```basic
10 DIM S(5)
20 S(1) = 95
30 S(2) = 87
40 PRINT S(1)
50 PRINT SUM(S); " "; MAX(S)
```
```text
Array S declared with dimensions [5]
95
182 95
```

`DIM A(n)` creates elements `0` to `n`, all `0`. Any number of dimensions
is allowed (`DIM M(3,3)`; `M(1,2) = 9`). `DIM` prints the confirmation line
shown above. Assigning to an element of an array that was never
`DIM`ensioned creates it on the fly.

## Graphics

### Turtle

| Command | Aliases | Effect |
|---------|---------|--------|
| `FORWARD n` | `FD` | Move forward, drawing if the pen is down |
| `BACK n` | `BACKWARD`, `BK` | Move backward |
| `LEFT deg` / `RIGHT deg` | | Turn |
| `PENUP` / `PENDOWN` | `PU` / `PD` | Lift / lower the pen |

```basic
10 FOR I = 1 TO 4
20   FORWARD 100
30   RIGHT 90
40 NEXT I
```

### Shapes

Arguments are separated by **spaces**, not commas, and colours are names:

| Command | Syntax |
|---------|--------|
| `LINE` | `LINE (x1,y1)-(x2,y2) [color]` |
| `BOX` | `BOX (x,y) width height [true]` (`true` = filled) |
| `ELLIPSE` | `ELLIPSE (x,y) width height [true]` |
| `TRIANGLE` | `TRIANGLE (x1,y1)-(x2,y2)-(x3,y3) [true]` |
| `FILL` | `FILL (x,y) [color]` (draws a small filled dot, not a flood fill) |

Each prints a confirmation such as `Drew line from (0.0,0.0) to (100.0,100.0)`.

### GAME commands

These use commas and RGB colours:

| Command | Syntax |
|---------|--------|
| `GAMESCREEN` | `GAMESCREEN w, h [, title]` |
| `GAMEBG` / `GAMECOLOR` | `GAMEBG r, g, b` |
| `GAMEPOINT` | `GAMEPOINT x, y` |
| `GAMERECT` | `GAMERECT x, y, w, h, filled` |
| `GAMECIRCLE` | `GAMECIRCLE x, y, r [, filled]` |
| `GAMETEXT` | `GAMETEXT x, y, "text"` |
| `GAMECLEAR`, `GAMEUPDATE` | Clear / refresh |
| `GAMEDELAY` | `GAMEDELAY ms` |

## Sound

No audio is produced on most systems; each command logs what it would play.

| Command | Syntax |
|---------|--------|
| `BEEP` | `BEEP [freq [dur]]` |
| `PLAY` | `PLAY 440` or `PLAY "C4"` |
| `SOUND` | `SOUND freq dur [vol]` (space-separated) |
| `NOTE` | `NOTE C 4 [dur]` |

## File I/O

```basic
10 OPEN "out.txt" FOR OUTPUT AS #1
20 WRITE #1 , 42
30 CLOSE #1
40 OPEN "out.txt" FOR INPUT AS #2
50 READ #2 , A
60 CLOSE #2
70 PRINT A
```

Modes are `INPUT`, `OUTPUT` and `APPEND`. `WRITE` and `READ` need the comma
**surrounded by spaces** (`WRITE #1 , X`); `WRITE #1, X` is rejected with a
syntax message. `READ` reads one line and stores it as a float when it looks
numeric (`42.0` above). Every file command also prints a status line.
`READ` is file-only: there is no `DATA`/`READ`/`RESTORE`.

## Examples

### Temperature converter

```basic
10 INPUT "Celsius: "; C
20 F = C * 9 / 5 + 32
30 PRINT C; "C = "; F; "F"
```

Input `100` prints `100C = 212.0F`.

### Number guessing

```basic
10 S = INT(RND(1) * 100) + 1
20 T = 0
30 G = 0
40 WHILE G <> S
50   INPUT "Guess (1-100): "; G
60   T = T + 1
70   IF G > S THEN PRINT "Too high"
80   IF G < S THEN PRINT "Too low"
90 WEND
100 PRINT "Got it in "; T; " tries"
```

### Subroutine

```basic
10 GOSUB 100
20 PRINT "Main"
30 END
100 PRINT "Header"
110 RETURN
```
```text
Header
Main
```

## Differences from Classic BASIC

- No `:` multi-statement lines, no `DATA`/`READ`/`RESTORE`, no
  `ON … GOTO`/`GOSUB`, no `STOP` (it is ignored), no `CLS`, `TAB`, `SPC`,
  `ATN`, `SGN` or `TIMER`, no `\` operator.
- No user-defined functions or callable `SUB`s; `DEFFN`, `SUB` and `CALL`
  only print a note.
- Lines execute in file order; line numbers are labels, not a sort key
  (except for the console's `RUN`).
- Variable names are case-sensitive; unassigned variables are not `0`.
- `PRINT` separators concatenate; there are no print zones.
- `SIN`/`COS`/`TAN` use degrees; `/` is always floating point;
  comparisons print `True`/`False` rather than `-1`/`0`.
- `EXIT FOR`/`WHILE`/`DO` do not jump; use `GOTO`.
- Unknown statements in a running program are silently ignored, so a typo
  does nothing instead of raising `?SYNTAX ERROR`.
- Statement arguments are split on spaces, so several commands (`LINE`,
  `BOX`, `SOUND`, `WRITE #n , x`, `INCR X, n`) are fussy about commas.

## See Also

- [Language Tutorials](../user/LANGUAGE_TUTORIALS.md)
- [BASIC examples](../../examples/basic/)
- [Logo Reference](LOGO_REFERENCE.md) for the full turtle command set
