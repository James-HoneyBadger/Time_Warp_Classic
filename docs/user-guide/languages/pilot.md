# PILOT Language Reference

## Overview

PILOT (Programmed Inquiry, Learning Or Teaching) is an educational programming language designed for interactive learning and computer-assisted instruction. Time_Warp implements a comprehensive PILOT dialect that is fully compatible with PILOT 73, the standardized version of PILOT developed in 1973, plus modern enhancements.

## PILOT 73 Compatibility

TW PILOT supports all core PILOT 73 commands and features:

- **Typed Variables**: String variables (`$NAME`) and numeric variables (`#SCORE`)
- **System Variables**: `%answer`, `%matched`, `%left`, `%right` for I/O operations
- **Arrays**: `D:SCORES(10)` for array declarations
- **Advanced Pattern Matching**: Wildcards (`?`, `*`) and alternatives (`|`, `,`)
- **Subroutines**: `U:*SUBROUTINE` and `E:` for structured programming
- **Screen Control**: `CH:`, `CA:`, `CL:`, `CE:` for cursor and screen management
- **System Integration**: `XS:` for shell commands, `PA:` for timing
- **Enhanced Control Flow**: `JM:` for computed jumps, `TH:` for no-newline output

## Program Structure

PILOT programs consist of statements that control the flow of a lesson or interactive program. Each statement begins with a command letter followed by a colon:

```
T:Welcome to PILOT!
A:What is your name?
T:Nice to meet you!
E:
```

## Commands

### T: Type
Display text to the user:
```
T:Hello, World!
T:This is a PILOT program.
T:Variable value: #SCORE
```

### A: Accept
Get input from the user:
```
A:Enter your name
A:What is 2 + 2?
A:#INPUT
```

### J: Jump
Unconditional jump to a label:
```
J:*START
J:(SCORE > 5)*HIGH_SCORE
```

### Y: Yes
Conditional jump if condition is true:
```
Y:(ANSWER = "YES")*CORRECT
Y:(SCORE >= 80)*PASS
```

### N: No
Conditional jump if condition is false:
```
N:(AGE < 18)*TOO_YOUNG
N:(CHOICE = "QUIT")*EXIT
```

### C: Compute
Perform calculations and assignments:
```
C:SCORE=0
C:TOTAL=PRICE * QUANTITY
C:NAME="John"
C:#COUNTER=#COUNTER + 1
```

### M: Match (PILOT 73 Enhanced)
Advanced pattern matching with wildcards and alternatives:
```
M:yes|yeah|y*CORRECT
M:quit|exit|q*GOODBYE
M:hello*?*GREETING
```

**PILOT 73 Pattern Features:**
- `?` : Matches any single character
- `*` : Matches any sequence of characters
- `|` : Separates alternative patterns
- `,` : Additional alternative separator

**System Variables Set:**
- `%matched` : The matched text
- `%left` : Text before the match
- `%right` : Text after the match

### U: Use (PILOT 73)
Call subroutines with proper stack management:
```
U:*CALCULATE_SCORE
U:*DISPLAY_RESULTS
```

**Features:**
- Supports subroutine nesting (up to `%maxuses` levels)
- Returns with `E:` command
- Maintains return address stack

### R: Remark
Comments (ignored during execution):
```
R:This is a comment
R:Program version 1.0
```

### E: End
Terminate the program or return from subroutine:
```
E:
```

## PILOT 73 Commands

### D: Dimension
Declare arrays:
```
D:SCORES(10)
D:#NUMBERS(5)
```

### PA: Pause
Pause execution for specified seconds or wait for user:
```
PA:2.5
PA:
```

### CH: Clear Home
Clear screen and move cursor to home position:
```
CH:
```

### CA: Cursor Address
Move cursor to specific position:
```
CA:10,5
```

### CL: Clear Line
Clear from cursor to end of line:
```
CL:
```

### CE: Clear End
Clear from cursor to end of screen:
```
CE:
```

### JM: Jump Match
Jump based on which pattern matched:
```
JM:*LABEL1,*LABEL2,*LABEL3
```

### TH: Type Hang
Display text without newline:
```
TH:Enter your name:
```

### XS: System
Execute shell command:
```
XS:dir
XS:echo "Hello World"
```

### PR: Problem
Mark problem sections (implementation dependent):
```
PR:Math Quiz Section
```

## Labels

Labels mark locations in the program for jumping:
```
*START
*CORRECT
*WRONG
*END
```

## Variables

### Variable Types (PILOT 73)
- **Numeric**: Store numbers (`#SCORE`, `#AGE`)
- **String**: Store text (`$NAME`, `$CITY`)
- **System**: Special variables (`%answer`, `%matched`)
- **Arrays**: Indexed collections (`SCORES(1)`, `#NUMBERS(5)`)

### Variable Names
- Start with a letter or appropriate prefix (`#`, `$`, `%`)
- Can contain letters, numbers, and underscores
- Case-insensitive for regular variables
- Maximum length: 32 characters

### System Variables (PILOT 73)
- `%answer` : Last input from A: command
- `%matched` : Text that matched in M: command
- `%left` : Text left of match in M: command
- `%right` : Text right of match in M: command
- `%status` : Status of last operation
- `%maxuses` : Maximum subroutine nesting level

### Legacy System Variables
- `#INPUT` : Last input from user
- `#TIME` : Current time
- `#DATE` : Current date
- `#RANDOM` : Random number

### Examples
```
C:SCORE=100
C:NAME="Alice"
C:#COUNTER=#COUNTER + 1
```

## Expressions

### Arithmetic
- `+` : Addition
- `-` : Subtraction
- `*` : Multiplication
- `/` : Division

### Comparison
- `=` : Equal
- `<>` : Not equal
- `<` : Less than
- `<=` : Less than or equal
- `>` : Greater than
- `>=` : Greater than or equal

### Logical
- `AND` : Logical AND
- `OR` : Logical OR
- `NOT` : Logical NOT

### Functions
- `#RANDOM(N)` : Random number 1 to N
- `#LEN(STRING)` : String length
- `#UPPER(STRING)` : Convert to uppercase
- `#LOWER(STRING)` : Convert to lowercase

## Variable Interpolation

Use `#VARNAME#` for regular variables and `%SYSTEMVAR%` for system variables:
```
C:$NAME="Alice"
T:Hello, %answer%! Welcome to the program.
T:Your score is #SCORE# out of 100.
T:You matched: %matched%
```

**Interpolation Syntax:**
- `#VARNAME#` : Regular variables
- `%systemvar%` : System variables (lowercase)
- `*VARNAME*` : Alternative syntax for regular variables

## Conditions

Conditions control program flow:
```
Y:(SCORE >= 70)*PASS
N:(ATTEMPTS >= 3)*TOO_MANY_TRIES
J:(CHOICE = "RESTART")*START
```

## Examples

### Simple Quiz
```
T:Math Quiz
C:SCORE=0

*QUESTION1
T:What is 2 + 2?
A:#INPUT
J:(#INPUT = 4)*CORRECT1
T:Sorry, wrong answer. The correct answer is 4.
J:*QUESTION2

*CORRECT1
T:Correct!
C:SCORE=SCORE+1
J:*QUESTION2

*QUESTION2
T:What is 10 * 5?
A:#INPUT
J:(#INPUT = 50)*CORRECT2
T:Sorry, wrong answer. The correct answer is 50.
J:*RESULTS

*CORRECT2
T:Correct!
C:SCORE=SCORE+1
J:*RESULTS

*RESULTS
T:Quiz complete!
T:You got #SCORE# out of 2 correct.
J:(SCORE = 2)*PERFECT
J:(SCORE = 1)*GOOD
T:Better luck next time!

*PERFECT
T:Perfect score! Excellent work!

*GOOD
T:Good job! You got one right.

E:
```

### Interactive Story
```
T:Choose Your Own Adventure
T:You are in a dark forest.
T:Do you go NORTH or SOUTH?

*CHOICE
A:Your choice (NORTH/SOUTH)
J:(#INPUT = "NORTH")*NORTH
J:(#INPUT = "SOUTH")*SOUTH
T:Please choose NORTH or SOUTH.
J:*CHOICE

*NORTH
T:You find a treasure chest!
T:Congratulations! You win!
E:

*SOUTH
T:You encounter a dragon!
T:The dragon eats you. Game over!
E:
```

### Calculator Program
```
T:PILOT Calculator
C:RUNNING=1

*MAIN_LOOP
J:(RUNNING = 0)*EXIT
T:Enter first number:
A:#NUM1
T:Enter operation (+, -, *, /):
A:#OP
T:Enter second number:
A:#NUM2

C:#RESULT=0
J:(#OP = "+")*ADD
J:(#OP = "-")*SUBTRACT
J:(#OP = "*")*MULTIPLY
J:(#OP = "/")*DIVIDE
T:Invalid operation.
J:*MAIN_LOOP

*ADD
C:#RESULT=#NUM1 + #NUM2
J:*DISPLAY

*SUBTRACT
C:#RESULT=#NUM1 - #NUM2
J:*DISPLAY

*MULTIPLY
C:#RESULT=#NUM1 * #NUM2
J:*DISPLAY

*DIVIDE
J:(#NUM2 = 0)*DIVIDE_ZERO
C:#RESULT=#NUM1 / #NUM2
J:*DISPLAY

*DIVIDE_ZERO
T:Cannot divide by zero!
J:*MAIN_LOOP

*DISPLAY
T:Result: #RESULT#
T:Calculate another? (YES/NO)
A:#CONTINUE
J:(#CONTINUE = "NO")*EXIT
J:*MAIN_LOOP

*EXIT
T:Goodbye!
E:
```

### Learning Program
```
T:Multiplication Tables Tutor
C:TABLE=5
C:CORRECT=0
C:QUESTIONS=0

*START
T:Let's practice multiplication tables!
T:We'll work with the #TABLE# times table.

*QUESTION
C:#A=#RANDOM(12)+1
C:#CORRECT_ANSWER=#A * TABLE
C:QUESTIONS=QUESTIONS+1

T:What is #A# × #TABLE#?
A:#ANSWER

J:(#ANSWER = CORRECT_ANSWER)*RIGHT
T:Sorry, that's not correct.
T:#A# × #TABLE# = #CORRECT_ANSWER#
J:*CONTINUE

*RIGHT
T:Correct! Well done.
C:CORRECT=CORRECT+1

*CONTINUE
J:(QUESTIONS < 10)*QUESTION

*RESULTS
T:Practice complete!
T:You got #CORRECT# out of #QUESTIONS# correct.
C:#PERCENT=CORRECT * 100 / QUESTIONS
T:That's #PERCENT#% correct.

J:(PERCENT >= 80)*EXCELLENT
J:(PERCENT >= 60)*GOOD
T:Keep practicing!

*EXCELLENT
T:Excellent work! You're a multiplication master!

*GOOD
T:Good job! You're getting better.

E:
```

## Best Practices

1. **Use clear labels** for program sections
2. **Validate user input** before processing
3. **Provide feedback** for correct/incorrect answers
4. **Use variables** for scores and counters
5. **Structure programs** with clear flow
6. **Test thoroughly** with different inputs

## Error Handling

PILOT programs handle errors gracefully:
- Invalid jumps display error messages
- Undefined variables use default values
- Division by zero is prevented
- Input validation prevents crashes

## Advanced Features

### Complex Conditions
```
Y:(SCORE >= 80 AND ATTEMPTS <= 3)*BONUS
N:(CHOICE <> "A" AND CHOICE <> "B" AND CHOICE <> "C")*INVALID
```

### String Operations
```
C:FULL_NAME=FIRST_NAME + " " + LAST_NAME
C:UPPER_NAME=#UPPER(FULL_NAME)
C:NAME_LENGTH=#LEN(FULL_NAME)
```

### Random Elements
```
C:DICE=#RANDOM(6)
C:CARD=#RANDOM(52)
```

## Compatibility

Time_Warp PILOT extends classic PILOT with:
- Enhanced variable interpolation
- More mathematical functions
- Better string handling
- Improved error messages
- Modern programming constructs

## See Also

- [PILOT Sample Programs](../../samples/pilot/)
- [Time_Warp User Guide](../user_guide.md)
- [Compiler Documentation](../compiler.md)