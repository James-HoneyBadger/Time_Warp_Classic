# PILOT Language Reference

PILOT (Programmed Inquiry, Learning, Or Teaching) was designed by John
Starkweather in 1968 for writing computer-assisted instruction: print a
question, accept an answer, match it, branch. PILOT-73 standardised the core
and later versions added graphics and more.

Time Warp Classic implements its own dialect in `core/languages/pilot.py`.
The core instructions (`T:` `A:` `M:` `Y:` `N:` `J:` `U:` `E:` `C:`) follow
PILOT tradition; many extensions (`MATH:`, `S:`, `BRANCH:`, `F:` …) are
specific to this implementation. Everything below was checked by running
it.

## Contents

- [Program Structure](#program-structure)
- [Core Instructions](#core-instructions)
- [Variables and Interpolation](#variables-and-interpolation)
- [Matching and Conditions](#matching-and-conditions)
- [Labels, Jumps and Subroutines](#labels-jumps-and-subroutines)
- [Extension Commands](#extension-commands)
- [Examples](#examples)
- [Differences from Classic PILOT](#differences-from-classic-pilot)
- [See Also](#see-also)

## Program Structure

```pilot
* Greeting program
T:What is your name?
A:NAME
T:Hello, *NAME*!
END
```

- One instruction per line: an **upper-case** instruction code, a colon,
  then the operand. Codes are case-sensitive: `t:hello` is silently ignored.
- Lines starting with `*`, `;`, `#` or `REM` are comments.
- `END` (or `E:` outside a subroutine) stops the program.
- Labels are defined with `L:name` on their own line.
- Lines without a colon are not PILOT. The IDE guesses a language for them
  from the first keyword, so `PRINT 5` in a PILOT program runs as BASIC.
  Don't rely on that.

## Core Instructions

| Instruction | Syntax | Effect |
|-------------|--------|--------|
| `T:` | `T:text` | Type a line of text (with interpolation) |
| `TH:` | `TH:text` | Same as `T:` here (no "hang"; a newline is still printed) |
| `A:` | `A:` or `A:VAR` | Accept a line of input, into `VAR` if given |
| `M:` | `M:pat1,pat2\|pat3` | Match the last answer against patterns; sets the match flag |
| `MT:` | `MT:text` | Type text only if the last match succeeded |
| `Y:` | `Y:instruction` or `Y:expr` | Run the instruction if the match flag is set (see below) |
| `N:` | `N:instruction` or `N:expr` | Run the instruction if the match flag is clear |
| `J:` | `J:label` | Jump to a label |
| `J(cond):` | `J(N > 3):label` | Jump if the expression is true |
| `L:` | `L:label` | Define a label |
| `U:` | `U:label` | Call a subroutine (nesting limit 10) |
| `E:` | `E:` | Return from a subroutine; ends the program if none is active |
| `C:` | `C:VAR = expr` | Compute: assign an expression to a variable |
| `C:` | `C:` (empty) | Return from a `GOSUB`-style call (rarely needed) |
| `R:` | `R:VERSION`, `R:HELP`, `R:TIME`, `R:DATE`, `R:PRINT VAR` | Runtime info |
| `PA:` | `PA:seconds` / `PA:` | Pause for n seconds, or wait for Enter |
| `END` | `END` | Stop |

### A: input

`A:` prints `Awaiting input: Enter value for NAME:` (or `Input:` with no
variable), then waits. In both the desktop and web IDE the program pauses
and the next line typed into the console bar is the answer. Integer-looking
answers are stored as integers, other numbers as floats, everything else as
text. The answer is always kept for `M:` even when stored in a variable.

## Variables and Interpolation

Assign with `C:` using an ordinary expression (the same evaluator as BASIC:
`+ - * / ^ MOD`, comparisons, `AND OR NOT`, functions such as `SQRT`,
`LEN`, `UCASE`). Strings use double quotes.

```pilot
C:X = 10 + 5
C:A = "x"
C:B = A + "y"
T:X is *X*, also {X} or [X]
T:B is *B*
T:Double: *X*2*
```
```text
X is 15, also 15 or 15
B is xy
Double: 152*
```

`T:`, `MT:` and `TH:` substitute `*VAR*`, `{VAR}` and `[VAR]`. A `*…*`
token that is not a variable but looks like an expression is evaluated
(`*7/2*`), but adjacent stars confuse it, as the last line shows; compute
into a variable first. Unknown variables are printed literally (`*Z*`).
Variable names are case-sensitive.

Don't use brackets on the right of `C:`: `C:[Y]=[X+1]` stores the list
`[16]`, not `16`.

## Matching and Conditions

```pilot
T:Capital of France?
A:
M:paris,par*
Y:T:Correct!
N:T:Sorry, it is Paris.
```

- `M:` compares the most recent `A:` answer with each alternative
  (separated by `,` or `|`). Matching is case-insensitive and finds the
  pattern **anywhere** in the answer; `*` matches any run of characters and
  `?` any single character.
- `A:` itself sets the match flag when the answer is `Y`, `YES`, `TRUE` or
  `1`, so a yes/no question needs no `M:`.
- `Y:` / `N:` followed by an instruction (`Y:T:…`, `Y:J:label`, `N:U:help`)
  run it conditionally.
- `Y:expr` / `N:expr` (no instruction) instead evaluate the expression,
  set the flag, and make the **next** `T:` or `J:` conditional:

```pilot
C:X = 7
Y:X > 5
T:printed, because X > 5
N:X > 5
T:not printed
T:always printed
```

The system variables `%answer`, `%matched`, `%left` and `%right` are
updated by `A:` and `M:` and are substituted in `T:` text.

## Labels, Jumps and Subroutines

```pilot
C:I = 1
L:loop
T:I=*I*
C:I = I + 1
J(I <= 3):loop
T:done
```
```text
I=1
I=2
I=3
done
```

`J:` takes a bare label name (`J:done`); the `J:*label` / `J:*:label`
forms of other PILOTs are not recognised and fall through. Write
conditions in `J(…):` without a space before the colon.

```pilot
T:Main
U:greet
T:Back
E:
L:greet
T:In sub
E:
```
```text
Main
In sub
Back
```

## Extension Commands

These are Time Warp additions. Arguments are separated by spaces unless
shown otherwise; quote text containing spaces.

### MATH: — result in `MATH_RESULT`, plus a log line

| Command | Example | Notes |
|---------|---------|-------|
| `SIN` `COS` `TAN` | `MATH:SIN 30` → `0.5` | Degrees |
| `SQRT` | `MATH:SQRT 144` → `12.0` | |
| `POWER` | `MATH:POWER 2,10` → `1024.0` | |
| `LOG` / `LN` | `MATH:LOG 100` → `2.0` | Base 10 / natural |
| `ABS` | `MATH:ABS -4` | |
| `ROUND` | `MATH:ROUND 3.456,2` → `3.46` | |
| `RANDOM` | `MATH:RANDOM 1,6` | A **float** between the bounds |

### S: — strings

| Command | Example | Result |
|---------|---------|--------|
| `LENGTH` | `S:LENGTH "Hello World" L` | `11` |
| `UPPER` / `LOWER` | `S:UPPER "hello" U` | `HELLO` |
| `FIND` | `S:FIND "Hello World" "World" P` | `6` (0-based; `-1` if absent) |
| `REPLACE` | `S:REPLACE "Hello World" "World" "PILOT" R` | `Hello PILOT` |
| `SUBSTRING` | `S:SUBSTRING "Hello World" 0 5 SUB` | `Hello` (0-based start) |
| `SPLIT` | `S:SPLIT "a,b,c" "," SP` | `a` (first piece only) |

Text arguments are interpolated, so `S:UPPER "*NAME*" U` works.

### BRANCH: — multi-way jumps

```pilot
BRANCH:CASE G, A:excellent, B:good, DEFAULT:other
BRANCH:RANGE S, 90-100:gradeA, 80-89:gradeB, 0-79:gradeC
BRANCH:MULTI X > 100:big, X > 50:medium, X > 0:small
```

The first matching entry wins; if none match, execution continues on the
next line. Labels fall through into each other as usual, so end each
branch with `J:`.

### Other commands

| Command | Syntax | Effect |
|---------|--------|--------|
| `G:` | `G:LINE,x1,y1,x2,y2` `G:CIRCLE,x,y,r` `G:RECT,x,y,w,h` `G:PENUP` `G:PENDOWN` `G:COLOR,red` `G:CLEAR` | Turtle-canvas drawing (comma-separated) |
| `F:` | `F:WRITE "file" "text"` `F:APPEND …` `F:READ "file" VAR` `F:EXISTS "file" VAR` `F:SIZE "file" VAR` `F:DELETE "file"` | Whole-file I/O; `EXISTS` gives `1`/`0` |
| `DT:` | `DT:NOW "YYYY-MM-DD" VAR`, `DT:NOW "HH:MM:SS" VAR`, `DT:TIMESTAMP VAR`, `DT:FORMAT ts "fmt" VAR` | Dates and times (format strings without spaces) |
| `W:` | `W:ENCODE "text" VAR`, `W:DECODE "text" VAR` | URL encoding only |
| `STORAGE:` | `SAVE "file"`, `LOAD "file"`, `LIST`, `COUNT`, `DELETE a, b`, `ARRAY name, size [,init]` | Variable persistence and listing |
| `GAME:` | `SCORE`, `SCORE n`, `LIVES`, `RESET` | Score keeping in `SCORE`/`LIVES` |
| `AUDIO:` | `BEEP`, `PLAY …`, `VOLUME n`, `STOP` | Logged; usually no real sound |
| `D:` | `D:OPEN …`, `D:QUERY …`, `D:INSERT …` | SQLite database access |
| `CH:` | `CH:` | "Clears" by printing 50 blank lines |
| `XS:` | `XS:echo hi` | Runs a program on the host (no shell), prints its stdout; 10 s limit |

`CA:`, `CL:`, `CE:`, `JM:` and `PR:` are accepted but have no visible
effect. `D:NAME(n)` creates an array that programs cannot read back;
`C:SCORES(1) = 9` creates a plain variable whose name happens to be
`SCORES(1)`.

`XS:` runs with the IDE's permissions (in the web IDE, the server's), so
treat PILOT programs from strangers like any other script.

## Examples

### Quiz with scoring

```pilot
C:SCORE = 0
T:Q1: What is 2+2?
A:
M:4,four
Y:C:SCORE = SCORE + 1
Y:T:Correct!
N:T:The answer is 4.
T:Q2: Capital of France?
A:
M:paris
Y:C:SCORE = SCORE + 1
Y:T:Correct!
N:T:It is Paris.
T:You scored *SCORE* out of 2.
END
```

With answers `four` and `Paris` this prints both `Correct!` lines and
`You scored 2 out of 2.`

### Menu with subroutines

```pilot
L:menu
T:1) Greet  2) Quit
A:CHOICE
J(CHOICE = 2):bye
U:greet
J:menu
L:greet
T:Hello there.
E:
L:bye
T:Goodbye.
END
```

## Differences from Classic PILOT

- No conditioners on instruction codes: `TY:`, `TN:`, `JY:`, `T(cond):`
  are ignored. Use `Y:T:…`, `N:J:…` and `J(cond):` instead.
- Labels are `L:name`, not `*name`; a line starting with `*` is a comment.
- `C:` uses BASIC-style expressions, not `#`/`$` variable sigils.
- `M:` is a substring match with wildcards; it does not set `%left`/`%right`
  reliably and there is no `JM:` match-number jump.
- `TH:` and `CA:` do not control the cursor; output is line-based.
- `%answer` and friends are system variables: `T:%answer` prints the last
  answer, `T:%matched` the last match.
- Instruction codes are case-sensitive and unknown codes are ignored
  silently, so check spelling when a line seems to do nothing.

## See Also

- [Language Tutorials](../user/LANGUAGE_TUTORIALS.md)
- [PILOT examples](../../examples/pilot/)
- [BASIC Reference](BASIC_REFERENCE.md) for the expression syntax used by `C:`
