# Language Tutorials - Learn All 9 Languages

Complete tutorials for mastering each programming language in Time Warp Classic.

## Table of Contents

1. [BASIC](#basic---classic-programming)
2. [Python](#python---modern-programming)
3. [JavaScript](#javascript---web-scripting)
4. [Pascal](#pascal---structured-programming)
5. [Prolog](#prolog---logic-programming)
6. [Forth](#forth---stack-based)
7. [Perl](#perl---text-processing)
8. [Logo](#logo---graphics)
9. [PILOT](#pilot---education)

---

## BASIC - Classic Programming

**Best for:** Beginners, learning fundamentals

### What is BASIC?

BASIC (Beginner's All-purpose Symbolic Instruction Code) is a simple, readable language perfect for learning programming fundamentals.

### Your First BASIC Program

```basic
PRINT "Hello, World!"
PRINT "Welcome to Time Warp!"
END
```

### Core Concepts

#### Variables & Assignment
```basic
LET name = "Alice"
LET age = 25
LET score = 95.5

PRINT name
PRINT age
PRINT score
```

#### Arithmetic
```basic
LET x = 10
LET y = 3

PRINT x + y    REM Addition
PRINT x - y    REM Subtraction
PRINT x * y    REM Multiplication
PRINT x / y    REM Division
PRINT x MOD y  REM Modulo (remainder)
PRINT x ^ 2    REM Power
```

#### String Operations
```basic
LET msg = "Hello"
PRINT LEN(msg)        REM Length
PRINT UPPER(msg)      REM Uppercase
PRINT LOWER(msg)      REM Lowercase
PRINT LEFT(msg, 3)    REM First 3 characters
PRINT MID(msg, 2, 3)  REM 3 chars starting at position 2
```

#### Conditional Statements
```basic
IF age >= 18 THEN
    PRINT "Adult"
ELSE
    PRINT "Minor"
END IF

IF score >= 90 THEN
    PRINT "Grade: A"
ELSE IF score >= 80 THEN
    PRINT "Grade: B"
ELSE
    PRINT "Grade: C"
END IF
```

#### Loops
```basic
REM For loop (count from 1 to 5)
FOR i = 1 TO 5
    PRINT i
NEXT i

REM For loop with step
FOR j = 10 TO 1 STEP -1
    PRINT j
NEXT j

REM While loop
LET count = 1
WHILE count <= 3
    PRINT count
    LET count = count + 1
END WHILE
```

#### Arrays
```basic
DIM numbers(5)
LET numbers(1) = 10
LET numbers(2) = 20
LET numbers(3) = 30

PRINT numbers(1)
PRINT SUM(numbers)
PRINT AVG(numbers)
PRINT MAX(numbers)
```

#### Subroutines
```basic
GOSUB PrintGreeting
PRINT "Main program continues"
GOTO SkipSub

PrintGreeting:
    PRINT "Hello from subroutine!"
    RETURN

SkipSub:
PRINT "Done"
END
```

### Practice Exercises

1. **Factorial Calculator**
```basic
INPUT "Enter number: "; n
LET result = 1
FOR i = 1 TO n
    LET result = result * i
NEXT i
PRINT "Factorial:"; result
END
```

2. **Guessing Game**
```basic
LET secret = RND(100)
LET guess = 0

WHILE guess <> secret
    INPUT "Guess a number: "; guess
    IF guess > secret THEN PRINT "Too high"
    IF guess < secret THEN PRINT "Too low"
WEND

PRINT "You got it!"
END
```

### Advanced Features
- Graphics with PLOT, LINE, BOX
- File I/O with OPEN, READ, WRITE
- User-defined functions

### Learn More
- See: `examples/basic/comprehensive_demo.bas` and `examples/basic/showcase_demo.bas`
- Reference: [BASIC_REFERENCE.md](../languages/BASIC_REFERENCE.md)

---

## Python - Modern Programming

**Best for:** Learning modern syntax, data structures, advanced features

### What is Python?

Python is a high-level, readable language with powerful data structures and functional programming features.

### Your First Python Program

```python
print("Hello, World!")
print("Welcome to Time Warp!")
```

### Core Concepts

#### Variables & Data Types
```python
name = "Alice"
age = 25
height = 5.7
is_student = True

print(name)
print(age)
print(height)
print(is_student)
```

#### Arithmetic & Math
```python
x = 10
y = 3

print(x + y)    # Addition
print(x - y)    # Subtraction
print(x * y)    # Multiplication
print(x / y)    # Division
print(x // y)   # Floor division
print(x % y)    # Modulo
print(x ** 2)   # Power

import math
print(math.sqrt(16))
print(math.sin(0))
```

#### Strings
```python
msg = "Hello, World!"

print(len(msg))           # Length
print(msg.upper())        # Uppercase
print(msg.lower())        # Lowercase
print(msg.replace("Hello", "Hi"))
print(msg[0:5])           # Slice: first 5 chars
print("Hello" in msg)     # Check if contains
```

#### Lists
```python
numbers = [1, 2, 3, 4, 5]

print(numbers[0])         # First element
print(len(numbers))       # Length
numbers.append(6)         # Add element
numbers.pop()             # Remove last
print(sum(numbers))       # Sum
print(max(numbers))       # Maximum

# List comprehension
squares = [x**2 for x in range(1, 6)]
```

#### Dictionaries
```python
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

print(person["name"])
person["email"] = "alice@example.com"
print(person.keys())
print(person.values())
```

#### Conditionals
```python
age = 25

if age >= 18:
    print("Adult")
else:
    print("Minor")

if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("C")
```

#### Loops
```python
# For loop
for i in range(1, 6):
    print(i)

# For loop with list
colors = ["red", "green", "blue"]
for color in colors:
    print(color)

# While loop
count = 1
while count <= 3:
    print(count)
    count += 1
```

#### Functions
```python
def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(greet("Alice"))
print(add(5, 3))
print(factorial(5))
```

### Practice Exercises

1. **Even/Odd Checker**
```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [n for n in numbers if n % 2 == 0]
print("Even numbers:", evens)
```

2. **Word Counter**
```python
text = "hello world hello python"
words = text.split()
word_count = {}
for word in words:
    word_count[word] = word_count.get(word, 0) + 1
print(word_count)
```

### Advanced Features
- Lambda functions
- List/dict comprehensions
- Classes and objects
- Exception handling
- Generators

### Learn More
- See: `examples/python/comprehensive_demo.py` and `examples/python/showcase_demo.py`
- Reference: [PYTHON_REFERENCE.md](../languages/PYTHON_REFERENCE.md)

---

## JavaScript - Web Scripting

**Best for:** Understanding web programming, modern ES6+ features

### What is JavaScript?

JavaScript is a dynamic language with flexible typing, functional programming, and modern class-based OOP.

### Your First Program

```javascript
console.log("Hello, World!");
console.log("Welcome to Time Warp!");
```

### Core Concepts

#### Variables & Data Types
```javascript
let name = "Alice";      // Block-scoped, reassignable
const age = 25;          // Block-scoped, constant
let height = 5.7;
const isStudent = true;

console.log(name);
console.log(age);
console.log(typeof name);
```

#### Operators
```javascript
var x = 10;
var y = 3;

console.log(x + y);    // Addition
console.log(x - y);    // Subtraction
console.log(x * y);    // Multiplication
console.log(x / y);    // Division
console.log(x % y);    // Modulo
console.log(Math.pow(x, 2));  // Power
```

#### Strings
```javascript
var msg = "Hello, World!";

console.log(msg.length);                    // Length
console.log(msg.toUpperCase());             // Uppercase
console.log(msg.toLowerCase());             // Lowercase
console.log(msg.substring(0, 5));           // Substring
console.log(msg.indexOf("World"));          // Find position
console.log(msg.replace("Hello", "Hi"));    // Replace
```

#### Arrays
```javascript
var numbers = [1, 2, 3, 4, 5];

console.log(numbers[0]);    // First element
console.log(numbers.length);  // Length
numbers.push(6);            // Add to end
var popped = numbers.pop(); // Remove from end
console.log(numbers.join(", "));  // Join with comma
```

#### Objects
```javascript
var person = {
    name: "Alice",
    age: 30,
    city: "New York"
};

console.log(person.name);
console.log(person["age"]);
person.email = "alice@example.com";
```

#### Conditionals
```javascript
var age = 25;

if (age >= 18) {
    console.log("Adult");
} else {
    console.log("Minor");
}

var score = 85;
if (score >= 90) {
    console.log("Grade: A");
} else if (score >= 80) {
    console.log("Grade: B");
} else {
    console.log("Grade: F");
}
```

#### Loops
```javascript
// For loop
for (var i = 1; i <= 5; i++) {
    console.log(i);
}

// While loop
var count = 1;
while (count <= 3) {
    console.log(count);
    count++;
}

// For..in loop (arrays)
var colors = ["red", "green", "blue"];
for (var i in colors) {
    console.log(colors[i]);
}
```

#### Functions
```javascript
function greet(name) {
    return "Hello, " + name + "!";
}

function add(a, b) {
    return a + b;
}

function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

console.log(greet("Alice"));
console.log(add(5, 3));
console.log(factorial(5));
```

### Learn More
- See: `examples/javascript/comprehensive_demo.js` and `examples/javascript/showcase_demo.js`
- Reference: [JAVASCRIPT_REFERENCE.md](../languages/JAVASCRIPT_REFERENCE.md)

---

## Pascal - Structured Programming

**Best for:** Learning structured programming, strong typing

### Your First Pascal Program

```pascal
PROGRAM HelloWorld;
BEGIN
    WriteLn('Hello, World!');
    WriteLn('Welcome to Time Warp!');
END.
```

### Core Concepts

#### Variables with Types
```pascal
VAR
    name : STRING;
    age : INTEGER;
    height : REAL;
    isStudent : BOOLEAN;
BEGIN
    name := 'Alice';
    age := 25;
    height := 5.7;
    isStudent := TRUE;
    
    WriteLn(name);
    WriteLn(age);
END.
```

#### Control Structures
```pascal
{ If/Then/Else }
IF age >= 18 THEN
    WriteLn('Adult')
ELSE
    WriteLn('Minor');

{ Case Statement }
CASE grade OF
    'A': WriteLn('Excellent');
    'B': WriteLn('Good');
    'C': WriteLn('Average');
END;

{ For Loop }
FOR i := 1 TO 10 DO
    WriteLn(i);

{ While Loop }
WHILE count < 10 DO
BEGIN
    WriteLn(count);
    count := count + 1;
END;
```

#### Functions & Procedures
```pascal
FUNCTION Add(a, b : INTEGER) : INTEGER;
BEGIN
    Add := a + b;
END;

PROCEDURE PrintGreeting;
BEGIN
    WriteLn('Hello!');
END;

BEGIN
    WriteLn(Add(5, 3));
    PrintGreeting;
END.
```

#### Arrays and Records
```pascal
VAR
    scores : ARRAY[1..5] OF INTEGER;

TYPE
    TStudent = RECORD
        name : STRING;
        grade : REAL;
    END;

VAR student : TStudent;
BEGIN
    student.name := 'Alice';
    student.grade := 3.8;
END.
```

### Practice Exercise
```pascal
PROGRAM Fibonacci;
VAR i : INTEGER;
FUNCTION Fib(n : INTEGER) : INTEGER;
BEGIN
    IF n <= 1 THEN Fib := n
    ELSE Fib := Fib(n-1) + Fib(n-2);
END;
BEGIN
    FOR i := 0 TO 10 DO
        WriteLn(Fib(i));
END.
```

### Learn More
- See: `examples/pascal/comprehensive_demo.pas` and `examples/pascal/showcase_demo.pas`
- Reference: [PASCAL_REFERENCE.md](../languages/PASCAL_REFERENCE.md)

---

## Prolog - Logic Programming

**Best for:** Understanding logic programming, pattern matching

### Your First Prolog Program

```prolog
parent(tom, bob).
parent(bob, ann).

grandparent(X, Z) :- parent(X, Y), parent(Y, Z).

?- grandparent(tom, ann).
```

### Core Concepts

#### Facts — Things That Are True
```prolog
likes(alice, coffee).
likes(bob, tea).
likes(alice, tea).
color(sky, blue).
color(grass, green).
```

#### Rules — How to Derive New Facts
```prolog
% X and Y are friends if they like the same thing
friends(X, Y) :- likes(X, Z), likes(Y, Z), X \= Y.

% Ancestor rule (recursive)
ancestor(X, Y) :- parent(X, Y).
ancestor(X, Y) :- parent(X, Z), ancestor(Z, Y).
```

#### Queries — Asking Questions
```prolog
?- likes(alice, coffee).        % yes
?- likes(Who, tea).             % Who = bob ; Who = alice
?- friends(alice, bob).         % yes (both like tea)
```

#### Lists
```prolog
% List operations
append([1,2], [3,4], Result).   % Result = [1,2,3,4]
member(3, [1,2,3,4]).           % yes
length([a,b,c], N).             % N = 3

% Head and Tail
[H|T] = [1,2,3].               % H = 1, T = [2,3]

% Sum a list
sum_list([], 0).
sum_list([H|T], Sum) :- sum_list(T, Rest), Sum is H + Rest.
```

#### Arithmetic
```prolog
?- X is 2 + 3.                 % X = 5
?- X is 10 mod 3.              % X = 1
?- X is sqrt(16).              % X = 4.0
```

### Practice Exercise
```prolog
% Family tree
parent(tom, bob).
parent(tom, liz).
parent(bob, ann).
parent(bob, pat).

sibling(X, Y) :- parent(Z, X), parent(Z, Y), X \= Y.

?- sibling(bob, liz).          % yes
?- sibling(ann, Who).          % Who = pat
```

### Learn More
- See: `examples/prolog/comprehensive_demo.pro` and `examples/prolog/showcase_demo.pro`
- Reference: [PROLOG_REFERENCE.md](../languages/PROLOG_REFERENCE.md)

---

## Forth - Stack-Based

**Best for:** Understanding stack-based computation, low-level thinking

### Your First Forth Program

```forth
." Hello, World!" CR
```

### Core Concepts

#### The Stack
Forth uses a stack to hold values. You push values, then operations consume them:

```forth
5 3 +           \ Push 5, push 3, add → stack: [8]
5 3 + .         \ Same, then print → prints: 8
10 2 / .        \ 10 divided by 2 → prints: 5
```

#### Stack Operations
```forth
5 DUP .S        \ Duplicate: stack [5, 5]
3 5 SWAP .S     \ Swap top two: stack [5, 3]
1 2 3 ROT .S    \ Rotate: stack [2, 3, 1]
7 DROP .S       \ Remove top: stack empty
3 5 OVER .S     \ Copy second: stack [3, 5, 3]
```

#### Defining Words (Functions)
```forth
: SQUARE ( n -- n^2 )  DUP * ;
: CUBE ( n -- n^3 )    DUP DUP * * ;

5 SQUARE .      \ 25
3 CUBE .        \ 27
```

#### Variables & Constants
```forth
VARIABLE count
10 count !      \ Store 10 in count
count @ .       \ Fetch and print: 10
count @ 1 + count !  \ Increment

42 CONSTANT ANSWER
ANSWER .        \ 42
```

#### Control Flow
```forth
\ If/Then
: CHECK ( n -- )  0 > IF ." Positive" THEN ;

\ If/Else
: SIGN ( n -- )  0 > IF ." +" ELSE ." -" THEN ;

\ Do Loop
: COUNTDOWN ( n -- )  0 DO I . LOOP ;
10 COUNTDOWN    \ 0 1 2 3 4 5 6 7 8 9

\ Begin/Until
: COUNT-TO ( n -- )
    1 BEGIN DUP . 1+ 2DUP > UNTIL DROP DROP ;
```

### Practice Exercise
```forth
: FACTORIAL ( n -- n! )
    1 SWAP 1+ 1 DO I * LOOP ;

5 FACTORIAL .   \ 120
10 FACTORIAL .  \ 3628800
```

### Learn More
- See: `examples/forth/comprehensive_demo.fth` and `examples/forth/showcase_demo.fth`
- Reference: [FORTH_REFERENCE.md](../languages/FORTH_REFERENCE.md)

---

## Perl - Text Processing

**Best for:** Text processing, regular expressions, scripting

### Your First Perl Program

```perl
#!/usr/bin/perl
use strict;
use warnings;

print "Hello, World!\n";
print "Welcome to Time Warp!\n";
```

### Core Concepts

#### Variables (Three Types)
```perl
# Scalar ($) — single value
my $name = "Alice";
my $age = 25;
my $pi = 3.14159;

# Array (@) — ordered list
my @colors = ("red", "green", "blue");
print $colors[0];        # red
push(@colors, "yellow"); # add to end

# Hash (%) — key-value pairs
my %person = (name => "Alice", age => 30);
print $person{name};     # Alice
```

#### String Interpolation
```perl
my $name = "Alice";
print "Hello, $name!\n";           # Interpolates variable
print 'Hello, $name!\n';           # Literal (no interpolation)
print "She is $person{age} years old\n";
```

#### Regular Expressions
```perl
my $text = "The quick brown fox";

# Match
if ($text =~ /quick/) {
    print "Found 'quick'!\n";
}

# Substitute
$text =~ s/fox/cat/;     # Replace fox with cat

# Extract
if ($text =~ /(\w+)\s+(\w+)/) {
    print "First two words: $1, $2\n";
}
```

#### Control Structures
```perl
# If/elsif/else
if ($age >= 18) {
    print "Adult\n";
} elsif ($age >= 13) {
    print "Teen\n";
} else {
    print "Child\n";
}

# Loops
for my $i (1..10) { print "$i "; }
foreach my $color (@colors) { print "$color\n"; }
while ($count < 10) { $count++; }
```

#### Subroutines
```perl
sub greet {
    my ($name) = @_;
    return "Hello, $name!";
}

print greet("Alice"), "\n";
```

### Practice Exercise
```perl
# Word frequency counter
my $text = "the cat sat on the mat the cat";
my %freq;
for my $word (split /\s+/, $text) {
    $freq{$word}++;
}
for my $word (sort keys %freq) {
    print "$word: $freq{$word}\n";
}
```

### Learn More
- See: `examples/perl/comprehensive_demo.pl` and `examples/perl/showcase_demo.pl`
- Reference: [PERL_REFERENCE.md](../languages/PERL_REFERENCE.md)

---

## Logo - Graphics

**Best for:** Visual learning, turtle graphics, creative coding

### Your First Logo Program

```logo
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
```
This draws a square! The turtle moves forward 100 units, turns right 90 degrees, and repeats.

### Core Concepts

#### Movement & Drawing
```logo
FORWARD 100     FD 100      Move forward
BACK 50         BK 50       Move backward
RIGHT 90        RT 90       Turn right
LEFT 45         LT 45       Turn left
PENUP           PU          Stop drawing
PENDOWN         PD          Start drawing
HOME                        Return to center
```

#### Repeat Loops — The Key to Patterns
```logo
REPEAT 4 [FD 100 RT 90]              Square
REPEAT 3 [FD 100 RT 120]             Triangle
REPEAT 6 [FD 60 RT 60]               Hexagon
REPEAT 360 [FD 1 RT 1]               Circle
```

#### Variables & Procedures
```logo
MAKE "size 50

TO SQUARE :size
    REPEAT 4 [FD :size RT 90]
END

SQUARE 100
SQUARE 50
```

#### Colors
```logo
SETPENCOLOR 2    Red
SETPENCOLOR 3    Green
SETPENCOLOR 4    Blue
SETPENCOLOR [255 128 0]   Orange (RGB)
```

#### Shapes
```logo
CIRCLE 50               Draw a circle
ARC 90 50               Draw a 90° arc
RECT 100 60             Draw a rectangle
POLYGON 5 40            Draw a pentagon
```

### Practice Exercise — Spiral
```logo
TO SPIRAL :size
    REPEAT 100 [
        FD :size
        RT 15
        MAKE "size :size + 2
    ]
END
SPIRAL 1
```

### Practice Exercise — Star
```logo
TO STAR :size
    REPEAT 5 [FD :size RT 144]
END
STAR 100
```

### Learn More
- See: `examples/logo/comprehensive_demo.logo` and `examples/logo/showcase_demo.logo`
- Reference: [LOGO_REFERENCE.md](../languages/LOGO_REFERENCE.md)

---

## PILOT - Education

**Best for:** Learning conditional logic, building quizzes and interactive lessons

### Your First PILOT Program

```pilot
T:Hello, World!
T:Welcome to PILOT!
T:What is your name?
A:[name]
T:Nice to meet you, [name]!
```

### Core Concepts

#### Output & Input
```pilot
T:This text is displayed          REM T: = Type (output)
A:[answer]                         REM A: = Accept (input)
T:You said: [answer]
```

#### Variables & Math
```pilot
C:[x]=[10+5]                      REM C: = Compute
C:[area]=[length*width]
T:The area is [area]
```

#### Conditional Logic with Matching
```pilot
T:Do you like programming? (Y/N)
A:[answer]
M:Y                                REM M: = Match
Y:T:Great! Let's continue!         REM Y: = If yes
N:T:Give it a try, you might like it! REM N: = If no
```

#### Labels & Jumps
```pilot
T:Choose 1 or 2:
A:[choice]
J:[choice=1]:option1               REM J: = Jump
J:[choice=2]:option2
T:Invalid choice
J:*:done

L:option1
T:You chose option 1
J:*:done
L:option2
T:You chose option 2
L:done
T:Program complete
```

#### Subroutines
```pilot
T:Main program
U:greet                            REM U: = Use subroutine
T:Back in main

L:greet
T:Hello from subroutine!
E:                                  REM E: = End/Return
```

#### Math Functions
```pilot
MATH:SQRT 144
T:Square root of 144 is [MATH_RESULT]

MATH:RANDOM 1,6
T:You rolled: [MATH_RESULT]
```

### Practice Exercise — Quiz
```pilot
T:=== Quick Quiz ===
C:[score]=[0]

T:Q1: What is 7 * 8?
A:[ans]
J:[ans=56]:q1right
T:Wrong! The answer is 56
J:*:q2
L:q1right
T:Correct!
C:[score]=[score+1]

L:q2
T:Q2: What planet is closest to the sun?
A:[ans]
M:Mercury
Y:T:Correct!
Y:C:[score]=[score+1]
N:T:Wrong! It's Mercury

T:Your score: [score] out of 2
```

### Learn More
- See: `examples/pilot/comprehensive_demo.pilot` and `examples/pilot/showcase_demo.pilot`
- Reference: [PILOT_REFERENCE.md](../languages/PILOT_REFERENCE.md)

---

## Learning Path Recommendations

### Path 1: Beginner (6 hours)
1. BASIC (2 hours) - fundamentals
2. Logo (1 hour) - visual feedback
3. Python (3 hours) - modern syntax

### Path 2: Intermediate (8 hours)
1. BASIC (1 hour) - review
2. Python (2 hours) - depth
3. JavaScript (2 hours) - different paradigm
4. Pascal (2 hours) - typing and structure
5. Prolog (1 hour) - logic programming

### Path 3: Advanced (10 hours)
All languages + deep dives

---

## Next Steps

- **Specific language reference:** [../languages/](../languages/) directory
- **Run examples:** [../../examples/](../../examples/)
- **User guide:** [USER_GUIDE.md](USER_GUIDE.md)

---

**Happy Learning! 🚀**
