# Language Tutorials

A short, hands-on tour of all nine languages in Time Warp Classic 1.6.0.
Each section starts with a first program, works through the core ideas
with small examples, and ends with an exercise and pointers to the full
reference.

Every example for the six built-in languages (BASIC, PILOT, Logo, Forth,
Pascal, Prolog) was run through Time Warp's own interpreters, and the
output shown is what they print, trace lines included. These interpreters
implement a practical subset of each language, not the whole standard;
each section ends with a "Limits in 1.6.0" note so that the gaps do not
surprise you.

Python, JavaScript and Perl are different: Time Warp runs them with the
real `python3`, `node` and `perl` programs. Their sections are short and
point to pages that explain how those runtimes behave inside the IDE.

## Contents

Built-in languages:

1. [BASIC](#basic)
2. [PILOT](#pilot)
3. [Logo](#logo)
4. [Forth](#forth)
5. [Pascal](#pascal)
6. [Prolog](#prolog)

Host runtimes:

7. [Python](#python)
8. [JavaScript](#javascript)
9. [Perl](#perl)

Then: [Where to go next](#where-to-go-next)

## How to follow along

1. Pick the language from the language menu.
2. Paste the example into the editor and press Run (F5 on the desktop).
3. Compare the console with the output shown here.

When a program asks for input, type into the console bar under the output
and press Enter. Your answer is echoed in the console, as shown in the
examples.

---

## BASIC

The language of 1970s and 80s home computers: numbered lines, `GOTO`,
`GOSUB`, and instant results. Good for learning how programs flow.

### First program

```basic
10 PRINT "HELLO, WORLD!"
20 PRINT "WELCOME TO TIME WARP."
30 END
```

```text
HELLO, WORLD!
WELCOME TO TIME WARP.
```

Line numbers are optional. They set the order of the program and give
`GOTO` and `GOSUB` somewhere to jump.

### Variables and arithmetic

Numeric variables are plain names; string variables end in `$`. `LET` is
optional. Use `;` in `PRINT` to join items.

```basic
10 LET N$ = "ALICE"
20 LET A = 25
30 X = 10
40 Y = 3
50 PRINT N$; " IS "; A
60 PRINT X + Y; " "; X - Y; " "; X * Y; " "; X / Y
70 PRINT X MOD Y; " "; X ^ 2; " "; INT(X / Y)
80 PRINT LEN(N$); " "; LEFT$(N$, 3); " "; MID$(N$, 2, 3); " "; RIGHT$(N$, 2)
```

```text
ALICE IS 25
13 7 30 3.3333333333333335
1 100 3
5 ALI LIC CE
```

`/` is floating-point division; use `INT()` to drop the fraction.

### Loops

```basic
10 FOR I = 1 TO 3
20 PRINT I
30 NEXT I
40 FOR J = 10 TO 1 STEP -3
50 PRINT J
60 NEXT J
70 C = 1
80 WHILE C <= 3
90 PRINT "PASS "; C
100 C = C + 1
110 WEND
```

```text
1
2
3
10
7
4
1
PASS 1
PASS 2
PASS 3
```

### Decisions and GOTO

```basic
10 S = 85
20 IF S >= 90 THEN PRINT "GRADE A"
30 IF S >= 80 AND S < 90 THEN PRINT "GRADE B"
40 IF S < 80 THEN GOTO 70
50 PRINT "PASSED"
60 END
70 PRINT "TRY AGAIN"
```

```text
GRADE B
PASSED
```

Multi-line blocks also work: `IF ... THEN` on its own line, then
`ELSE` and `END IF`.

### Arrays and subroutines

```basic
10 DIM A(5)
20 FOR I = 1 TO 5
30 A(I) = I * I
40 NEXT I
50 PRINT A(3); " "; A(5)
60 GOSUB 100
70 PRINT "BACK IN MAIN"
80 END
100 PRINT "IN THE SUBROUTINE"
110 RETURN
```

```text
Array A declared with dimensions [5]
9 25
IN THE SUBROUTINE
BACK IN MAIN
```

The first line is the interpreter reporting the `DIM`.

### Input

`INPUT` shows its prompt and waits for a line from the console bar. The
clock pauses while it waits.

```basic
10 INPUT "ENTER A NUMBER"; N
20 F = 1
30 FOR I = 1 TO N
40 F = F * I
50 NEXT I
60 PRINT N; "! = "; F
```

Typing `5`:

```text
ENTER A NUMBER 
5
5! = 120
```

### Exercise: guess the number

```basic
10 S = INT(RND(1) * 100) + 1
20 T = 0
30 INPUT "YOUR GUESS"; G
40 T = T + 1
50 IF G < S THEN PRINT "TOO LOW"
60 IF G > S THEN PRINT "TOO HIGH"
70 IF G <> S THEN GOTO 30
80 PRINT "GOT IT IN "; T; " TRIES"
```

`RND(1)` returns a number from 0 up to (not including) 1. Try adding a
limit of seven guesses.

### Limits in 1.6.0

- One statement per line: no `:` separators, and no `REM` after a
  statement. Put comments on their own `REM` line.
- `PRINT` joins items with `;` or `,` without adding spaces, and a
  trailing `;` does not suppress the newline. Add `" "` yourself.
- `GOTO`/`GOSUB` to a line that does not exist (or to a label) is
  silently skipped.
- The square root function is `SQRT`, not `SQR`. `SIN` and `COS` take
  degrees.
- `?ERROR IN n` gives the editor line, not the BASIC line number.

More: [BASIC reference](../languages/BASIC_REFERENCE.md),
[examples/basic/](../../examples/basic/).

---

## PILOT

PILOT (1968) was built for writing lessons and quizzes: Type text, Accept
an answer, Match it, and branch on the result. Each line starts with a
command letter and a colon.

### First program

```pilot
T:Hello, World!
T:What is your name?
A:[name]
T:Nice to meet you, [name]!
```

Typing `Ada`:

```text
Hello, World!
What is your name?
Awaiting input: Enter value for name: 
Ada
Nice to meet you, Ada!
```

`A:[name]` stores the answer in `name`; `[name]` in a `T:` line inserts
it.

### Computing

`C:` assigns. `[var]` inserts a variable and `*expr*` inserts the result
of an expression.

```pilot
C:x = 10 + 5
C:y = x * 2
T:x is [x], y is *y*, sum is *x+y*
```

```text
x is 15, y is 30, sum is 45
```

### Matching and branching

`M:` compares the last answer with a list of words (case does not
matter). `Y:` and `N:` prefix a command that runs only if the match
succeeded or failed. `J:` jumps to an `L:` label, and `J(condition):`
jumps only when the condition is true. `U:` calls a subroutine that ends
with `E:`; an `E:` outside a subroutine ends the program.

```pilot
T:Do you like programming? (Y/N)
A:
M:Y,YES
Y:T:Good. Carry on.
N:T:Give it time.
T:Pick 1 or 2:
A:[choice]
J(choice = 1):one
J(choice = 2):two
T:Not a valid choice.
J:done
L:one
T:You chose one.
J:done
L:two
T:You chose two.
L:done
U:greet
T:Back in main.
E:
L:greet
T:Hello from the subroutine.
E:
```

Typing `yes`, then `2`:

```text
Do you like programming? (Y/N)
Awaiting input: Input: 
yes
Good. Carry on.
Pick 1 or 2:
Awaiting input: Enter value for choice: 
2
You chose two.
Hello from the subroutine.
Back in main.
```

### Exercise: a two-question quiz

```pilot
T:=== Quick Quiz ===
C:score = 0
T:Q1: What is 7 * 8?
A:[ans]
J(ans = 56):q1right
T:Wrong. The answer is 56.
J:q2
L:q1right
T:Correct!
C:score = score + 1
L:q2
T:Q2: Which planet is closest to the sun?
A:
M:MERCURY
Y:T:Correct!
Y:C:score = score + 1
N:T:Wrong. It is Mercury.
T:Your score: [score] out of 2
```

Typing `56`, then `mercury`:

```text
=== Quick Quiz ===
Q1: What is 7 * 8?
Awaiting input: Enter value for ans: 
56
Correct!
Q2: Which planet is closest to the sun?
Awaiting input: Input: 
mercury
Correct!
Your score: 2 out of 2
```

Add a third question, then print a different message for a perfect score.

### Limits in 1.6.0

- Assign with `C:name = expression`. The bracket form `C:[x]=[...]` stores
  a list (`[12]`), not a number.
- Conditional jumps are written `J(condition):label`; `J:[condition]:label`
  is not supported.
- `M:` matches substrings, so `M:Y` also matches "maybe".

More: [PILOT reference](../languages/PILOT_REFERENCE.md),
[examples/pilot/](../../examples/pilot/).

---

## Logo

Logo (1967) teaches programming through a turtle that draws as it moves.
The drawing appears on the canvas; the console shows only text output.

### First program

```logo
REPEAT 4 [FD 100 RT 90]
```

Draws a 100-step square. `FD` moves forward, `RT` turns right by degrees.
`BK`, `LT`, `PU` (pen up), `PD` (pen down), `HOME` and `CS` (clear
screen) do what you would expect.

### Procedures

`TO name :param ... END` defines a new command.

```logo
TO SQUARE :size
  REPEAT 4 [FD :size RT 90]
END

SQUARE 50
SQUARE 100
```

Draws two nested squares. The console shows the definition:

```text
📝 Defined procedure SQUARE[':size']
```

### Nested REPEAT

`REPEAT` blocks can span lines and contain other `REPEAT`s.

```logo
REPEAT 12 [
  REPEAT 4 [FD 60 RT 90]
  RT 30
]
```

Draws a flower of twelve squares (48 lines).

### Variables and recursion

`MAKE "name value` sets a variable and `:name` reads it. `IF condition
[STOP]` ends a procedure. Work out the next value with `MAKE` before the
recursive call:

```logo
TO SPIRAL :size
  IF :size > 100 [STOP]
  FD :size
  RT 90
  MAKE "next :size + 5
  SPIRAL :next
END

SPIRAL 5
```

Draws a square spiral of 20 segments.

### Colour and position

```logo
SETPENCOLOR red
SETPENSIZE 3
CIRCLE 40
PU
SETXY 120 0
PD
SETPENCOLOR [0 128 255]
REPEAT 5 [FD 80 RT 144]
HOME
PRINT [Done drawing]
```

A thick red circle, then a blue five-pointed star to its right.

```text
Done drawing
```

`SETPENCOLOR` takes a colour name or an `[r g b]` list. `CIRCLE radius`
draws around the turtle's position.

### Exercise: any polygon

```logo
TO POLY :sides :len
  MAKE "turn 360 / :sides
  REPEAT 6 [FD :len RT :turn]
END
POLY 6 50
```

This draws a hexagon. Change `POLY` so it draws a triangle or an octagon
(for now, the `REPEAT` count has to be written as a number; see below).

### Limits in 1.6.0

- Movement commands and `REPEAT` take a number or a plain `:var`, not an
  expression: `FD :n * 10` ignores the `* 10`, and `REPEAT :n [...]` is
  rejected. Use `MAKE` to compute values first.
- Procedure arguments are not evaluated either: write `MAKE "next :size + 5`
  then `SPIRAL :next`, not `SPIRAL :size + 5` (which recurses forever).
- One command per line outside `REPEAT` brackets.
- `PRINT [text]` prints words; `PRINT :x` prints `:x` literally. `SHOW`,
  `TYPE`, `IFELSE` and `LABEL` are not available.
- `SETPENCOLOR` with a number (`SETPENCOLOR 2`) gives no valid colour. Use
  a name or an RGB list.
- `CS` clears the canvas but leaves the turtle where it is. Add `HOME`.

More: [Logo reference](../languages/LOGO_REFERENCE.md),
[examples/logo/](../../examples/logo/).

---

## Forth

Forth (1970) works on a stack: numbers are pushed, words pop their inputs
and push results. Programs are built by defining new words.

### First program

```forth
." Hello, World!" CR
```

```text
 Hello, World!

```

The space after `."` separates the word from the text; in 1.6.0 it shows
up in the output. `CR` prints an empty line.

### The stack and arithmetic

`.` pops and prints the top of the stack. Operators come after their
operands.

```forth
2 3 + .
10 4 - .
6 7 * .
20 4 / .
17 5 MOD .
```

```text
5
6
42
5
2
```

`.S` shows the stack without changing it (depth first):

```forth
5 DUP .S
* .
1 2 SWAP .S
DROP DROP
1 2 OVER .S
```

```text
<2> 5 5
25
<2> 2 1
<3> 1 2 1
```

Other stack words: `ROT`, `2DROP`, `NEGATE`, `ABS`, `MAX`, `MIN`, `1+`.

### Defining words

`: NAME ... ;` defines a word. The `( before -- after )` comment is a
convention describing what it does to the stack.

```forth
: SQUARE ( n -- n*n ) DUP * ;
: CUBE ( n -- n^3 ) DUP SQUARE * ;
5 SQUARE .
3 CUBE .
```

```text
Defined word: SQUARE
Defined word: CUBE
25
27
```

### Variables and constants

```forth
VARIABLE COUNT
0 COUNT !
COUNT @ 5 + COUNT !
COUNT @ .
42 CONSTANT ANSWER
ANSWER .
```

```text
Variable declared: COUNT
5
Constant declared: ANSWER
42
```

`!` stores, `@` fetches.

### Loops and decisions

`limit start DO ... LOOP` counts from start to limit - 1, with the index
in `I`. `BEGIN ... UNTIL` repeats until the flag on the stack is true.
`IF ... ELSE ... THEN` tests the top of the stack.

```forth
: TABLE ( -- ) 6 1 DO I 7 * . LOOP ;
TABLE
: COUNT-TO ( n -- ) 1 BEGIN DUP . 1+ 2DUP < UNTIL 2DROP ;
3 COUNT-TO
: SIGN ( n -- ) DUP 0 < IF ." negative" ELSE ." not negative" THEN DROP CR ;
-5 SIGN
```

```text
Defined word: TABLE
7
14
21
28
35
Defined word: COUNT-TO
1
2
3
Defined word: SIGN
 negative

```

### Exercise: factorial

```forth
: FACTORIAL ( n -- n! ) 1 SWAP 1+ 1 DO I * LOOP ;
5 FACTORIAL .
10 FACTORIAL .
```

```text
Defined word: FACTORIAL
120
3628800
```

Write `SUM-TO ( n -- sum )` that adds 1 to n the same way.

### Limits in 1.6.0

- Every `.` and `EMIT` prints on its own line.
- Errors (`Unknown word: FOO`, `Stack underflow in .`) stop the program
  with a plain message, not a `?ERROR` line.
- `/MOD` and `CLEARSTACK` are not available.

More: [Forth reference](../languages/FORTH_REFERENCE.md),
[examples/forth/](../../examples/forth/).

---

## Pascal

Pascal (1970) was designed for teaching structured programming: declared
variables, `BEGIN ... END` blocks, and clear control flow. Time Warp runs
a teaching subset.

### First program

```pascal
PROGRAM Hello;
BEGIN
  WriteLn('Hello from Pascal');
END.
```

```text
🚀 Starting program: Hello
Hello from Pascal
```

The first line is the interpreter announcing the program.

### Variables and arithmetic

```pascal
PROGRAM Basics;
VAR x, y: INTEGER;
BEGIN
  x := 17;
  y := 5;
  WriteLn('Sum: ', x + y);
  WriteLn('Quotient: ', x DIV y);
  WriteLn('Remainder: ', x MOD y);
  WriteLn('Real division: ', x / y);
END.
```

```text
🚀 Starting program: Basics
📝 Declared variables: x, y as INTEGER
✅ X := 17
✅ Y := 5
Sum: 22
Quotient: 3
Remainder: 2
Real division: 3.4
```

Assignment is `:=`. The interpreter traces each assignment with a `✅`
line; this is useful for seeing what a program does, and noisy in
loops. `WriteLn` prints its arguments with nothing in between.

### Loops

```pascal
PROGRAM Loops;
VAR i: INTEGER;
BEGIN
  FOR i := 1 TO 3 DO
  BEGIN
    WriteLn('Up ', i);
  END;
  FOR i := 3 DOWNTO 1 DO
  BEGIN
    WriteLn('Down ', i);
  END;
END.
```

```text
🚀 Starting program: Loops
📝 Declared variables: i as INTEGER
Up 1
Up 2
Up 3
Down 3
Down 2
Down 1
```

`WHILE condition DO BEGIN ... END;` and `REPEAT ... UNTIL condition;`
work too.

### Decisions

Wrap each branch of a multi-line `IF` in `BEGIN ... END`:

```pascal
PROGRAM Grade;
VAR score: INTEGER;
BEGIN
  score := 85;
  IF score >= 90 THEN
  BEGIN
    WriteLn('Grade A');
  END
  ELSE
  BEGIN
    WriteLn('Not an A');
  END;
END.
```

```text
🚀 Starting program: Grade
📝 Declared variables: score as INTEGER
✅ SCORE := 85
Not an A
```

A one-line form is fine for short cases:
`IF n MOD 2 = 0 THEN n := n DIV 2 ELSE n := 3 * n + 1;`

### Input

```pascal
PROGRAM Greet;
VAR name: STRING;
BEGIN
  WriteLn('What is your name?');
  ReadLn(name);
  WriteLn('Hello ', name);
END.
```

Typing `Ada`:

```text
🚀 Starting program: Greet
📝 Declared variables: name as STRING
What is your name?
Ada
Hello Ada
```

### Exercise: Collatz steps

```pascal
PROGRAM Collatz;
VAR n, steps: INTEGER;
BEGIN
  n := 6;
  steps := 0;
  WHILE n <> 1 DO
  BEGIN
    IF n MOD 2 = 0 THEN n := n DIV 2 ELSE n := 3 * n + 1;
    steps := steps + 1;
  END;
  WriteLn('Steps: ', steps);
END.
```

The last line printed is `Steps: 8`, after the trace of every
assignment. Try `n := 27` (111 steps, and a long trace).

### Limits in 1.6.0

- One statement per line, and keep the `VAR` section on one line.
- Avoid commas and `=` inside string literals: `'Hello, World!'` is
  split at the comma and `'a = b'` prints as `a == b`.
- Always use `BEGIN ... END` for multi-line `IF`, `ELSE` and `WHILE`
  bodies; without them both branches, or only the first pass, run.
- `FUNCTION` and `PROCEDURE` are not really supported (calls return 0),
  nor are `CASE`, arrays, `TRUE`/`FALSE`, `Sqrt`, `Abs` and `Length`.
- `Write` ends the line like `WriteLn`.

More: [Pascal reference](../languages/PASCAL_REFERENCE.md),
[examples/pascal/](../../examples/pascal/).

---

## Prolog

Prolog (1972) is logic programming: you state facts and rules, then ask
questions, and Prolog finds the answers.

### Facts and queries

```prolog
parent(tom, bob).
parent(tom, liz).
parent(bob, ann).
parent(bob, pat).
?- parent(tom, bob).
?- parent(tom, X).
?- parent(liz, X).
```

```text
📚 Fact added: parent(tom, bob)
📚 Fact added: parent(tom, liz)
📚 Fact added: parent(bob, ann)
📚 Fact added: parent(bob, pat)
✅ Query succeeded
   yes
✅ Query succeeded
   X = bob
   X = liz
❌ Query failed - no solutions found
```

Names starting with a lower-case letter are constants (atoms); names
starting with an upper-case letter are variables. A query with a variable
lists every value that makes it true.

### Rules

`head :- body.` means "head is true if body is true". A comma means "and".

```prolog
parent(tom, bob).
parent(bob, ann).
parent(bob, pat).
grandparent(X, Z) :- parent(X, Y), parent(Y, Z).
?- grandparent(tom, Who).
```

```text
📚 Fact added: parent(tom, bob)
📚 Fact added: parent(bob, ann)
📚 Fact added: parent(bob, pat)
📋 Rule added: grandparent(X, Z) :- parent(X, Y), parent(Y, Z)
✅ Query succeeded
   Who = ann
   Who = pat
```

### Comparisons

```prolog
age(alice, 30).
age(bob, 15).
age(carol, 70).
adult(P) :- age(P, A), A >= 18.
?- adult(Who).
```

```text
📚 Fact added: age(alice, 30)
📚 Fact added: age(bob, 15)
📚 Fact added: age(carol, 70)
📋 Rule added: adult(P) :- age(P, A), A >= 18
✅ Query succeeded
   Who = alice
   Who = carol
```

Put spaces around comparison operators (`A >= 18`).

### Lists and conjunctions

```prolog
likes(mary, wine).
likes(john, wine).
likes(john, mary).
?- likes(mary, X), likes(john, X).
?- member(X, [red, green]).
```

```text
📚 Fact added: likes(mary, wine)
📚 Fact added: likes(john, wine)
📚 Fact added: likes(john, mary)
✅ Query succeeded
   X = wine
✅ Query succeeded
   X = red
   X = green
```

### Exercise

Add `parent(liz, joe).` to the family above and write
`sibling(X, Y) :- parent(P, X), parent(P, Y).` Query `?- sibling(ann, S).`
Notice that `ann` is her own sibling: real Prolog would add `X \= Y`,
which this interpreter does not support yet.

### Limits in 1.6.0

- Recursive rules (such as `ancestor`) find only the first level of
  answers.
- `is`, `=`, `\=`, `append` and `length` are not available; `member`,
  `not(...)` and `write(...)` are.
- Rules need at least one argument: `hello :- write(hi).` is not added.
- Querying a rule with no variables (`?- adult(bob).`) can print the
  rule's internal bindings instead of `yes`.

More: [Prolog reference](../languages/PROLOG_REFERENCE.md),
[examples/prolog/](../../examples/prolog/).

---

## Python

Time Warp runs Python programs with a real Python 3 (the one Time Warp
itself runs on), so the whole language and standard library are
available. Programs run in a separate process with a time limit; there is
no turtle canvas.

```python
def fahrenheit(c):
    return c * 9 / 5 + 32

for c in range(0, 101, 25):
    print(f"{c:>4} C = {fahrenheit(c):5.1f} F")
```

```text
   0 C =  32.0 F
  25 C =  77.0 F
  50 C = 122.0 F
  75 C = 167.0 F
 100 C = 212.0 F
```

Read input with `print("Question?")` followed by `input()`, and keep
prompts on their own line. Lines typed in the console while no program is
running are each run as a separate one-line program.

Learn the language from the [Python tutorial](https://docs.python.org/3/tutorial/).
How it behaves inside Time Warp: [Python in Time Warp](../languages/PYTHON_REFERENCE.md).
Examples: [examples/python/](../../examples/python/).

---

## JavaScript

Time Warp runs JavaScript with [Node.js](https://nodejs.org/), which you
install separately. It is Node, not a browser: `console.log` works,
`alert` and `document` do not.

```javascript
const words = "the quick brown fox jumps over the lazy dog".split(" ");
const longest = words.reduce((a, b) => (b.length > a.length ? b : a));
console.log(`${words.length} words, longest is "${longest}"`);
console.log(words.map(w => w[0].toUpperCase() + w.slice(1)).join(" "));
```

```text
9 words, longest is "quick"
The Quick Brown Fox Jumps Over The Lazy Dog
```

Reading input needs a small `readline` helper, shown in the reference
page.

Learn the language from the [MDN JavaScript Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide).
How it behaves inside Time Warp: [JavaScript in Time Warp](../languages/JAVASCRIPT_REFERENCE.md).
Examples: [examples/javascript/](../../examples/javascript/).

---

## Perl

Time Warp runs Perl programs with the system `perl`. Perl's strengths are
text, regular expressions and hashes.

```perl
use strict;
use warnings;

my @log = ("ERROR disk full", "INFO started", "ERROR no route", "WARN slow");
my %count;
for my $line (@log) {
    $count{$1}++ if $line =~ /^(\w+)/;
}
printf "%-5s %d\n", $_, $count{$_} for sort keys %count;
```

```text
ERROR 2
INFO  1
WARN  1
```

Read input with `chomp(my $answer = <STDIN>);` after printing a prompt
that ends in `\n`.

Learn the language from [perlintro](https://perldoc.perl.org/perlintro).
How it behaves inside Time Warp: [Perl in Time Warp](../languages/PERL_REFERENCE.md).
Examples: [examples/perl/](../../examples/perl/).

---

## Where to go next

Some routes through the languages, roughly in historical order within
each:

- **First steps:** BASIC for flow and variables, then Logo for procedures
  and recursion you can see, then Python.
- **Structure and types:** BASIC, then Pascal, then Python or
  JavaScript.
- **Other ways of thinking:** Forth (the stack), Prolog (logic), PILOT
  (lessons as programs), Perl (text and patterns).

Further reading:

- Language references: [docs/languages/](../languages/)
- Example programs: [examples/](../../examples/)
- Documentation index: [docs/README.md](../README.md)
