# PILOT Language Reference

Complete reference for PILOT (Programmed Instruction, Learning, Or Teaching) in Time Warp Classic.

## What is PILOT?

PILOT is an educational language designed for creating interactive instruction programs. It combines:
- Simple conditional logic
- Text output
- Variable assignment
- Mathematical operations
- Interactive branching

## Basic Structure

```
T:This is output text
A:This is an accept (input) statement
M:This is a message
```

## Output Statements

### T: (Type/Print Text)

```pilot
T:Hello, World!
T:Welcome to PILOT
T:The answer is 42
```

### Multiple Lines

```pilot
T:This is line 1
T:This is line 2
T:This is line 3
```

## Variable Operations

### Assigning Values

```pilot
A:Enter your name: [name]
M:[name]

T:Enter a number:
A:[x]

M:You entered: [x]
```

### Arithmetic

```pilot
C:[answer]=[10+5]       REM answer = 15
C:[result]=[x*2]        REM result = x * 2
C:[sum]=[a+b+c]         REM sum of three numbers
```

### Variable Display

```pilot
C:[total]=[10+20+30]
T:The total is: [total]
```

## Conditional Logic

### Simple If/Then

```pilot
T:Enter a number:
A:[x]
C:[check]=[x>10]
T:is $[check]
```

### IF Statement (Jump)

```pilot
T:Are you sure? (Y/N)
A:[answer]
J:[answer=Y]:yes
T:You said no
E:no
T:You said yes
```

### Comparison

```pilot
J:[x=5]:equal
J:[x>5]:greater
J:[x<5]:less
T:x equals 5
E:greater
T:x is greater than 5
E:less
T:x is less than 5
```

## Labels and Jumps

### Simple Jump

```pilot
T:This is the start
J:*:skip

T:This is skipped
E:skip
T:This appears after skipping
```

### Conditional Jump

```pilot
T:Enter 1 or 2:
A:[choice]
J:[choice=1]:option1
J:[choice=2]:option2

T:Invalid choice
J:*:end
E:option1
T:You chose option 1
J:*:end
E:option2
T:You chose option 2
E:end
T:Program complete
```

## Interactive Programs

### Question & Answer

```pilot
T:What is 2 + 3?
A:[answer]
J:[answer=5]:correct
T:Wrong, try again
J:*:start
E:correct
T:That's right!
```

### Menu Program

```pilot
T:
T:===== MENU =====
T:1. Add
T:2. Subtract
T:3. Quit
T:Enter choice:
A:[choice]

J:[choice=1]:add
J:[choice=2]:subtract
J:[choice=3]:quit
T:Invalid choice
J:*:start

E:add
T:Addition selected
J:*:start

E:subtract
T:Subtraction selected
J:*:start

E:quit
T:Goodbye!
```

## Arithmetic Operations

### Basic Math

```pilot
C:[sum]=[x+y]           REM Addition
C:[diff]=[x-y]          REM Subtraction
C:[prod]=[x*y]          REM Multiplication
C:[quot]=[x/y]          REM Division
C:[square]=[x*x]        REM x squared
```

### Complex Expressions

```pilot
C:[result]=[10+5*2]     REM 20
C:[average]=[a+b+c/3]   REM Average of three
```

## Loops

### REPEAT Loop

```pilot
M:looping 5 times
R:[i]=1,[i<=5],[i]+1
T:Iteration [i]

T:Done looping
```

### LOOP with Counter

```pilot
R:[count]=1,[count<=10],[count]+1
T:Number [count]
```

### Infinite Loop with Break

```pilot
T:Enter 0 to quit:
R:[x]=1,[x>0],[x]=1
A:[x]
T:You entered [x]
```

## Comments

```pilot
REM This is a comment
REM Program to calculate average
T:Starting program
```

## String Operations

### Concatenation

```pilot
C:[first]=Alice
C:[last]=Smith
T:[first] [last]
```

### Length & Substring (varies by implementation)

```pilot
T:Your name is [name]
```

## Complete Examples

### Guessing Game

```pilot
T:Think of a number between 1 and 10
T:I will try to guess it
T:
C:[guess]=5
T:Is your number [guess]?
A:[answer]

J:[answer=Y]:done
T:Is it higher?
A:[higher]
J:[higher=Y]:higher
J:[higher=N]:lower

E:higher
T:Then it must be 8
A:[answer2]
J:[answer2=Y]:done
T:Lucky guess!
J:*:restart

E:lower
T:Then it must be 3
A:[answer3]
J:[answer3=Y]:done
T:I got it!
J:*:restart

E:done
T:Great! I guessed correctly!
J:*:restart

E:restart
T:Play again? (Y/N)
A:[playagain]
J:[playagain=Y]:start
T:Thanks for playing!
```

### Quiz Program

```pilot
T:===== QUIZ =====
T:
T:Q1: What is 2+2?
A:[ans1]
C:[score]=0
J:[ans1=4]:q1right
T:Incorrect, answer is 4
J:*:q2
E:q1right
T:Correct!
C:[score]=[score+1]

E:q2
T:
T:Q2: What is the capital of France?
A:[ans2]
J:[ans2=Paris]:q2right
T:Incorrect, answer is Paris
J:*:results
E:q2right
T:Correct!
C:[score]=[score+1]

E:results
T:
T:Your score: [score] out of 2
```

### Calculator

```pilot
T:===== SIMPLE CALCULATOR =====
T:Enter first number:
A:[x]
T:Enter second number:
A:[y]

T:Choose operation:
T:1. Add
T:2. Subtract
T:3. Multiply
T:4. Divide
A:[op]

J:[op=1]:add
J:[op=2]:sub
J:[op=3]:mult
J:[op=4]:div

T:Invalid operation
J:*:end

E:add
C:[result]=[x+y]
T:[x] + [y] = [result]
J:*:end

E:sub
C:[result]=[x-y]
T:[x] - [y] = [result]
J:*:end

E:mult
C:[result]=[x*y]
T:[x] * [y] = [result]
J:*:end

E:div
C:[result]=[x/y]
T:[x] / [y] = [result]

E:end
T:Thanks for using calculator!
```

## Debugging

### Output Variables

```pilot
T:Debug: x = [x]
T:Debug: answer = [answer]
```

### Trace Logic

```pilot
T:At checkpoint 1
A:[input]
T:You entered: [input]
T:At checkpoint 2
```

## Tips & Best Practices

1. **Use clear labels** for jumps
2. **Test all paths** in conditional logic
3. **Display prompts clearly** before input
4. **Validate user input** when needed
5. **Use meaningful variables** names
6. **Comment complex logic** sections
7. **Format output nicely** with spacing

## Common Patterns

### Simple Decision Tree
```pilot
T:Choose A or B:
A:[choice]
J:[choice=A]:chosenA
T:You chose B
J:*:end
E:chosenA
T:You chose A
E:end
T:Done
```

### Input Validation
```pilot
T:Enter a number (1-10):
A:[num]
J:[num>=1]:checkmax
T:Too low, try again
J:*:start
E:checkmax
J:[num<=10]:valid
T:Too high, try again
J:*:start
E:valid
T:Valid number: [num]
```

## Yes/No Conditionals

### Y: (Yes Condition)

Execute the following command only if the last match or input was affirmative:

```pilot
T:Do you like programming? (Y/N)
A:[answer]
M:Y
Y:T:Great! Programming is fun!
```

### N: (No Condition)

Execute the following command only if the last match was negative:

```pilot
T:Ready to continue? (Y/N)
A:[answer]
M:Y
N:T:OK, take your time.
```

## TH: (Type Hang / Inline Output)

Output text without a trailing newline (inline output):

```pilot
TH:Enter your choice: 
A:[choice]
```

## MT: (Match Text)

Match the last input against a pattern and output the result:

```pilot
T:What is the capital of France?
A:[answer]
MT:Paris
Y:T:Correct!
N:T:Sorry, the answer is Paris.
```

## Subroutines (U: and E:)

### U: (Use Subroutine)

Call a labeled subroutine. The return address is saved on a stack:

```pilot
T:Main program
U:greet
T:Back in main

L:greet
T:Hello from subroutine!
E:
```

### E: (End / Return)

Return from a subroutine to the line after the U: call. If no subroutine is active, E: ends the program or acts as a label endpoint:

```pilot
L:calculate
C:[result]=[x*2]
T:Result: [result]
E:
```

### Nesting Subroutines

Subroutines can be nested up to 10 levels deep (configurable via `%maxuses`):

```pilot
U:outer
T:Done

L:outer
T:In outer
U:inner
T:Back in outer
E:

L:inner
T:In inner
E:
```

## Graphics Commands (G:)

PILOT supports turtle graphics through the G: command prefix:

### Drawing

```pilot
G:LINE,0,0,100,100        REM Draw line from (0,0) to (100,100)
G:CIRCLE,50,50,30          REM Draw circle at (50,50) radius 30
G:RECT,10,10,80,60         REM Draw rectangle at (10,10) 80x60
```

### Pen Control

```pilot
G:PENUP                    REM Lift pen (stop drawing)
G:PENDOWN                  REM Lower pen (start drawing)
G:COLOR,red                REM Set pen color
G:CLEAR                    REM Clear graphics screen
```

## Math Functions (MATH:)

Advanced mathematical operations that store results in the `MATH_RESULT` variable:

```pilot
MATH:SIN 45               REM sin(45°) → MATH_RESULT
MATH:COS 60               REM cos(60°) → MATH_RESULT
MATH:TAN 30               REM tan(30°) → MATH_RESULT
MATH:SQRT 144             REM √144 = 12 → MATH_RESULT
MATH:POWER 2,10           REM 2^10 = 1024 → MATH_RESULT
MATH:LOG 100              REM log₁₀(100) = 2 → MATH_RESULT
MATH:LN 2.718             REM ln(e) ≈ 1 → MATH_RESULT
MATH:ABS -42              REM |−42| = 42 → MATH_RESULT
MATH:ROUND 3.7            REM round(3.7) = 4 → MATH_RESULT
MATH:ROUND 3.456,2        REM round to 2 decimals → 3.46
MATH:RANDOM 1,100         REM Random number 1–100 → MATH_RESULT
```

### Using Math Results

```pilot
MATH:SQRT 25
T:The square root is [MATH_RESULT]

MATH:RANDOM 1,6
T:You rolled a [MATH_RESULT]
```

## String Operations (S:)

String processing commands:

```pilot
S:LENGTH "Hello World" result       REM result = 11
S:UPPER "hello" result              REM result = "HELLO"
S:LOWER "HELLO" result              REM result = "hello"
S:FIND "Hello World" "World" pos    REM pos = 6
S:REPLACE "Hello World" "World" "PILOT" result  REM result = "Hello PILOT"
S:SUBSTRING "Hello World" 0 5 result REM result = "Hello"
S:SPLIT "a,b,c" "," result         REM result = "a" (first part)
```

## Branching (BRANCH:)

Advanced branching beyond simple J: jumps:

### BRANCH:CASE

```pilot
T:Enter a grade (A/B/C):
A:[grade]
BRANCH:CASE [grade], A:excellent, B:good, C:average, DEFAULT:unknown

L:excellent
T:Outstanding work!
J:*:done
L:good
T:Good job!
J:*:done
L:average
T:Keep trying!
J:*:done
L:unknown
T:Invalid grade
L:done
```

### BRANCH:RANGE

```pilot
T:Enter your score (0-100):
A:[score]
BRANCH:RANGE [score], 90-100:gradeA, 80-89:gradeB, 70-79:gradeC, 0-69:gradeF

L:gradeA
T:Grade: A
J:*:end
L:gradeB
T:Grade: B
J:*:end
L:gradeC
T:Grade: C
J:*:end
L:gradeF
T:Grade: F
L:end
```

### BRANCH:MULTI

```pilot
BRANCH:MULTI [x>100]:big, [x>50]:medium, [x>0]:small
```

## Array Operations (D:)

Dimension and use arrays:

```pilot
D:scores(5)                REM Create array with 5 elements
```

## Screen Control

### CH: (Clear Home)

Clear the screen and return cursor to home position:

```pilot
CH:
T:Fresh screen!
```

### CA: (Cursor Address)

Move the cursor to a specific row and column:

```pilot
CA:5,10                    REM Move cursor to row 5, column 10
T:Positioned text
```

### PA: (Pause)

Pause execution for a specified duration (seconds):

```pilot
T:Wait for it...
PA:2
T:Here it is!
```

### CL: / CE: (Clear Line / Clear to End)

```pilot
CL:                        REM Clear current line
CE:                        REM Clear from cursor to end of line
```

## Date/Time (DT:)

```pilot
DT:NOW "YYYY-MM-DD" today        REM Get current date
DT:NOW "HH:MM:SS" time           REM Get current time
DT:TIMESTAMP ts                   REM Get Unix timestamp
T:Today is [today] at [time]
```

## System Variables

PILOT maintains special system variables accessible with `%`:

| Variable | Description |
|----------|-------------|
| `%answer` | Last input from A: command |
| `%matched` | Matched text from M: command |
| `%left` | Text to the left of match |
| `%right` | Text to the right of match |
| `%status` | Operation status code |
| `%maxuses` | Maximum subroutine nesting (default: 10) |

## Quick Reference

| Command | Description | Example |
|---------|-------------|---------|
| `T:` | Type/print text | `T:Hello World` |
| `TH:` | Type without newline | `TH:Enter: ` |
| `A:` | Accept input | `A:[name]` |
| `C:` | Compute/calculate | `C:[x]=[1+2]` |
| `J:` | Jump to label | `J:*:start` |
| `M:` | Match pattern | `M:yes` |
| `MT:` | Match and type result | `MT:Paris` |
| `Y:` | Yes conditional | `Y:T:Correct!` |
| `N:` | No conditional | `N:T:Wrong!` |
| `U:` | Use subroutine | `U:greet` |
| `E:` | End/return | `E:` |
| `L:` | Label definition | `L:start` |
| `R:` | Runtime command | `R:CLEAR` |
| `G:` | Graphics command | `G:LINE,0,0,100,100` |
| `S:` | String operation | `S:UPPER "hi" result` |
| `MATH:` | Math function | `MATH:SQRT 16` |
| `BRANCH:` | Advanced branching | `BRANCH:CASE ...` |
| `D:` | Dimension array | `D:arr(10)` |
| `CH:` | Clear home | `CH:` |
| `CA:` | Cursor address | `CA:5,10` |
| `PA:` | Pause | `PA:2` |
| `DT:` | Date/time | `DT:NOW "YYYY-MM-DD" var` |
| `REM` | Comment | `REM This is a comment` |

## See Also

- [LANGUAGE_TUTORIALS.md](../user/LANGUAGE_TUTORIALS.md)
- [examples/pilot/](../../examples/pilot/)

---

**Last Updated:** 2025
