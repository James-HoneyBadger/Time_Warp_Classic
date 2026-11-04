# Logo Language Reference

Logo was designed in 1967 by Wally Feurzeig, Seymour Papert and Cynthia
Solomon at BBN. It is a Lisp dialect, but most people remember it for turtle
graphics: a cursor with a position and a heading that draws as it moves.
UCBLogo (Brian Harvey, Berkeley) is the usual modern reference dialect.

Time Warp Classic has its own interpreter in `core/languages/logo.py`. It
handles turtle graphics well and procedures reasonably well, but it is a
**command interpreter, not a full Logo**. There are no reporters (functions
that return values), so you can't nest expressions like `FD SUM 10 :X` or
`PRINT :X`. Read the [Differences](#differences-from-classic-logo) section
before porting UCBLogo code. Everything below was checked by running it.

## Contents

- [Program Structure](#program-structure)
- [Turtle and Canvas](#turtle-and-canvas)
- [Command Reference](#command-reference)
- [Variables and Arguments](#variables-and-arguments)
- [Procedures](#procedures)
- [Control Flow](#control-flow)
- [Extras](#extras)
- [Examples](#examples)
- [Differences from Classic Logo](#differences-from-classic-logo)
- [See Also](#see-also)

## Program Structure

```logo
; Draw a square
TO SQUARE :size
    REPEAT 4 [
        FORWARD :size
        RIGHT 90
    ]
END

SQUARE 100
```

- One command per line at the top level. Commands are case-insensitive.
- `;` starts a comment line. `{ … }` comments are removed anywhere on a line.
  Lines starting with `#` are also skipped.
- `TO … END` definitions are collected before the program runs, so you can
  call a procedure above its definition.
- A `REPEAT` block may span several lines. `IF` blocks must stay on one line
  (see [Control Flow](#control-flow)).
- Unknown commands print `Unknown Logo command: X` and execution continues.

## Turtle and Canvas

- The turtle starts at `(0, 0)` in the centre of the canvas, facing up
  (heading 0), pen down, black, size 2.
- Headings are compass-style: 0 is up, 90 is right, and `RIGHT` turns
  clockwise. `FD 100` then `RT 90` then `FD 50` leaves the turtle at
  `(50, 100)`, heading 90.
- The y axis points up, as in classic Logo.

## Command Reference

### Movement

| Command | Alias | Example | Notes |
|---------|-------|---------|-------|
| `FORWARD n` | `FD` | `FD 100` | Negative values move backwards |
| `BACK n` | `BK`, `BACKWARD` | `BK 50` | |
| `RIGHT deg` | `RT` | `RT 90` | Clockwise |
| `LEFT deg` | `LT` | `LT 45` | |
| `HOME` | | `HOME` | Back to `(0, 0)`, heading 0. Draws no line |
| `SETXY x y` | | `SETXY 100 -50` | Jumps without drawing. Literal numbers only |
| `SETHEADING deg` | | `SETHEADING 180` | Literal number only. No `SETH` alias |
| `TOWARDS x y` | | `TOWARDS 0 100` | Buggy: uses math angles, not compass headings (see below) |

### Pen and screen

| Command | Alias | Example | Notes |
|---------|-------|---------|-------|
| `PENUP` | `PU` | `PU` | |
| `PENDOWN` | `PD` | `PD` | Going from up to down **advances the pen colour** through a built-in palette (see below) |
| `SETPENCOLOR c` | `SETPC`, `SETCOLOR`, `SETCOLOUR`, `COLOR` | `SETPENCOLOR red` | Colour name, `#RRGGBB`, `[R G B]` or `R G B` |
| `SETPENSIZE n` | | `SETPENSIZE 3` | Integer width. There is no `PENSIZE` |
| `CLEARSCREEN` | `CS` | `CS` | Erases the drawing. The turtle stays where it is |
| `CLEARTEXT` | `CT` | `CT` | Clears the text output |
| `SHOWTURTLE` | `ST` | `ST` | |
| `HIDETURTLE` | `HT` | `HT` | |

Colours: `SETPENCOLOR 2` does **not** select a palette entry. The string
`"2"` is used as a colour name, so stick to names (`red`, `navy`), hex, or RGB
lists:

```logo
SETPENCOLOR [255 128 0]
SETPENCOLOR #3060c0
SETPENCOLOR 0 160 80
```

Because `PD` changes the colour, set the colour *after* `PD`:

```logo
PU
SETXY -100 0
PD
SETPENCOLOR blue
FD 50
```

### Shapes and text

These take literal numbers, not `:variables`.

| Command | Example | Effect |
|---------|---------|--------|
| `CIRCLE r` | `CIRCLE 50` | Circle centred on the turtle. Drawn only if the pen is down |
| `DOT [size]` | `DOT 8` | Filled dot (default size 5) |
| `RECT w h` | `RECT 100 60` | Rectangle at the turtle position |
| `ARC radius angle [steps]` | `ARC 50 90` | Walks the turtle along an arc. Note the argument order. Top-level lines only |
| `POLYGON sides len [angle]` | `POLYGON 6 40` | Regular polygon; the turtle ends where it started. Top-level lines only |
| `TEXT words` | `TEXT Hello there` | Draws text on the canvas at the turtle |
| `STAMP` | `STAMP` | Stamps the turtle shape |
| `FILL` | `FILL` | Flood-fills at the turtle with the pen colour |
| `CLONE` | `CLONE` | Records a turtle clone (diagnostic only) |

### Information

These print a line of text. They do not return values.

| Command | Output |
|---------|--------|
| `HEADING` | `Turtle heading: 90.0 degrees` |
| `POSITION` | `Turtle position: (50.0, 100.0)` |
| `PRINT text` | Prints the rest of the line literally; `[ ]` around it are removed |

```logo
PRINT Hello, world
PRINT [Logo says hi]
```

```text
Hello, world
Logo says hi
```

`PRINT` does not evaluate anything. `PRINT :x` prints `:x`, and
`PRINT "hello` prints `"hello`, quote included.

## Variables and Arguments

```logo
MAKE "size 50
MAKE "size :size + 10
FD :size
```

- `MAKE "name expr` evaluates the rest of the line and stores the result.
  Names are case-insensitive. Numbers are stored as floats.
- `:name` reads a variable. Unknown variables read as `0`.
- Movement commands (`FD`, `BK`, `LT`, `RT`) evaluate **one token**, so
  expressions must have no spaces: `FD :size*2` and `RT 360/6` work;
  `FD :size * 2` moves `:size` and ignores the rest.
- Arithmetic uses `+ - * / %` and parentheses (Python rules). Comparisons
  use `== != < > <= >=`. `=` and `<>` are syntax errors. Logic operators
  are **lower-case** `and`, `or`, `not`.

## Procedures

```logo
TO POLY :sides :len
    REPEAT 6 [FD :len RT 60]
END

POLY 6 50
```

- `TO name :p1 :p2 … END` defines a procedure. Loading prints
  `📝 Defined procedure POLY[':sides', ':len']`.
- Arguments: plain numbers (`10`), a single variable (`:q`), or a
  parenthesised expression **without spaces**: `(:n-1)`, `(:size/2)`.
  `:n-1` (no parentheses) evaluates to 0, and `(:n - 1)` with spaces
  breaks argument parsing.
- Parameters are global variables that are saved and restored when the
  call returns normally.
- `STOP` leaves the procedure. Because of a bug, it also leaves every
  procedure that called it (see [Differences](#differences-from-classic-logo)).
  Tail recursion (`SPIRAL` below) works; branching recursion (a binary
  tree) does not.
- Inside a `REPEAT [ … ]` block, a procedure call that takes arguments
  is split from its arguments and runs with none. The same happens to
  `ARC`, `POLYGON` and most non-turtle commands. Only the core turtle
  commands (`FD`, `RT`, `PU`, `SETPENCOLOR`, `CIRCLE`, `MAKE`, `PRINT`,
  `REPEAT`, `IF` …) keep their arguments there. Put other calls on their
  own line in a procedure instead (see the flower example).

## Control Flow

| Form | Example | Notes |
|------|---------|-------|
| `REPEAT n [cmds]` | `REPEAT 4 [FD 100 RT 90]` | `n` must be a literal integer. Blocks may span lines and nest. Each `REPEAT` stops after 5000 commands (`REPEAT aborted: expansion too large`) |
| `IF cond [cmd]` | `IF :x > 3 [STOP]` | One line only. Only the first command in the block runs |
| `WHILE [cond] [cmds]` | `WHILE [:n < 3] [MAKE "n :n + 1 FD 10]` | Limit 10000 iterations |
| `UNTIL [cond] [cmds]` | `UNTIL [:n >= 3] [MAKE "n :n + 1 FD 1]` | |
| `DO.WHILE [cmds] [cond]` | `DO.WHILE [MAKE "n :n - 1 FD 1] [:n > 0]` | Body runs at least once |
| `DO.UNTIL [cmds] [cond]` | `DO.UNTIL [MAKE "n :n + 1 FD 1] [:n == 2]` | |
| `COND [[cond] [cmds]] …` | `COND [[:x > 1] [FD 5]] [[:x < 1] [FD 6]]` | First true clause runs |
| `CASE value [match cmds] …` | `CASE :x [ELSE FD 3]` | Numeric matches never succeed (see below) |
| `STOP` | `STOP` | Leaves a procedure. Ignored at top level |

In `WHILE`/`UNTIL`/`DO.*`/`COND` bodies a new command starts at a turtle
command keyword (`FD`, `RT`, `PU`, `REPEAT`, `IF` …). `MAKE "n :n + 1 FD 10`
therefore splits correctly into two commands, but a body containing only
`PRINT` or a user procedure call may not.

Not available: `IFELSE`, `REPCOUNT`, `REPEAT :n`, and a working `FOR`.
`FOR` is a stub that only logs the loop variable and ignores the body.

## Extras

These exist mainly for experiments. Most print diagnostic messages rather
than returning values.

| Group | Commands | Behaviour |
|-------|----------|-----------|
| Macros | `DEFINE name [cmds]`, `CALL name` | Store and replay a command list. `DEFINE BOX [FD 10 RT 90 …]` |
| Procedure calls | `APPLY "proc [args]`, `INVOKE "proc args…` | Call a `TO` procedure indirectly |
| Maths | `SIN 30`, `COS`, `TAN`, `SQRT 16`, `POWER 2 10`, `LOG 100` | Prints `SIN 30.0° = 0.5000`; degrees; `LOG` is base 10 |
| Bitwise | `BITAND 12 10`, `BITOR`, `BITXOR`, `ASHIFT 1 4`, `LSHIFT` | Prints `12 BITAND 10 = 8`. `BITNOT` reports missing operands |
| Lists | `LIST 10 20 30`, `FIRST`, `LAST`, `BUTFIRST`, `BUTLAST`, `ITEM 2 LIST_0` | `LIST` creates an auto-named list (`LIST_0` …); the others act on the most recent list and print the result |
| Arrays | `ARRAY A 3`, `SETITEM A 0 10`, `ITEM 1 A` | `SETITEM` is 0-based but `ITEM` is 1-based |
| Properties | `PPROP "dog "legs 4`, `GPROP`, `PLIST`, `REMPROP` | Print results; the quote stays part of the name |
| Trace | `TRACE ON` / `TRACE OFF` | Logs position, heading and pen after each move |
| Profile | `PROFILE ON` / `OFF` / `REPORT` | Command timing |
| State files | `SAVE "file` | Writes the turtle state as JSON to `file` in the working directory. `LOAD` is routed to the audio handler and does not restore it |
| Stubs | `EXPORT`, `SCRUNCH`, `ERRACT`, `ERROR`, `CUBE`, `SPHERE`, `CYLINDER`, `PYRAMID`, `PLAYNOTE`, `PLAYTUNE`, `SETSOUND`, `.MACRO`, `.DEFMACRO`, `FOREACH`, `CASCADE` | Print a message or do little else |

## Examples

### Squiral (tail recursion)

```logo
TO SPIRAL :size
    IF :size > 100 [STOP]
    FORWARD :size
    RIGHT 90
    SPIRAL (:size+10)
END

SPIRAL 10
PRINT finished
```

Draws ten segments of growing length, then prints `finished`.

### Star

```logo
TO STAR :size
    REPEAT 5 [
        FORWARD :size
        RIGHT 144
    ]
END

SETPENCOLOR gold
STAR 120
```

### Growing spiral with a variable

```logo
SETPENCOLOR [0 120 200]
MAKE "side 5
REPEAT 50 [
    FD :side
    RT 91
    MAKE "side :side + 3
]
```

### Flower (procedures calling procedures)

```logo
TO PETAL
    REPEAT 2 [REPEAT 15 [FD 4 RT 6] RT 90]
END

TO FLOWER
    PETAL
    RT 30
END

REPEAT 12 [FLOWER]
```

Calls without arguments are fine inside `REPEAT`. Each petal is two
quarter-circle arcs built from `FD`/`RT`, because `ARC 60 90` inside a
`REPEAT` block would lose its arguments.

### While loop

```logo
MAKE "n 0
WHILE [:n < 36] [MAKE "n :n + 1 FD 5 RT 10]
```

More complete programs: `examples/logo/mandala_art.logo` and
`examples/logo/spirograph_art.logo`.

## Differences from Classic Logo

Behaviour that differs from UCBLogo / LCSI Logo:

- **No reporters.** `PRINT`, `SUM`, `XCOR`, `YCOR`, `RANDOM`, `WORD`,
  `SENTENCE`, `OUTPUT`/`OP`, `SHOW` and `REPCOUNT` don't exist or don't
  return values. `PRINT` prints literal text.
- **Unsupported commands** (report `Unknown Logo command`): `IFELSE`,
  `SETPOS`, `SETPOSITION`, `SETH`, `XCOR`, `YCOR`, `PENSIZE`, `PENDOWNP`,
  `SETBG`/`SETBACKGROUND`, `LABEL` (use `TEXT`), `BOX` (use `RECT`), `SHOW`.
- `STOP` in a nested call unwinds all callers, so branching recursion (fractal
  trees) stops after the first leaf. `STOP` at top level is ignored.
- `IF` takes a single-line block and runs only its first command.
  A multi-line `IF … [` is reported as malformed, and the lines of its body
  then run **unconditionally**.
- `REPEAT` needs a literal count. `FOR` does nothing useful.
- Expressions use Python operators: `==` not `=`, `!=` not `<>`, lower-case
  `and`/`or`/`not`. Arguments to movement commands and procedures must not
  contain spaces.
- `SETXY` and `HOME` move without drawing. `CS` does not home the turtle.
- `PENDOWN` after `PENUP` cycles the pen through black, red, blue, green,
  purple, …. Set the colour after `PD` if it matters.
- `SETPENCOLOR n` with a number is not a palette lookup.
- `TOWARDS` computes a mathematical angle (0 = east, counter-clockwise),
  not a compass heading, so the turtle points the wrong way.
- `CASE` compares strings, and variables hold floats (`2.0`), so a numeric
  clause like `[2 FD 2]` never matches.
- No words, lists as data, or `RUN`. Quoted words keep their quote.

## See Also

- [Language Tutorials](../user/LANGUAGE_TUTORIALS.md)
- [Logo examples](../../examples/logo/)
- [PILOT Reference](PILOT_REFERENCE.md), whose `G:` turtle commands share
  the same canvas
