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
- See: `examples/basic/comprehensive_demo.bas`
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
- See: `examples/python/comprehensive_demo.py`
- Reference: [PYTHON_REFERENCE.md](../languages/PYTHON_REFERENCE.md)

---

## JavaScript - Web Scripting

**Best for:** Understanding web programming, ES5 features

### What is JavaScript?

JavaScript is a dynamic language with flexible typing and functional programming capabilities.

### Your First Program

```javascript
console.log("Hello, World!");
console.log("Welcome to Time Warp!");
```

### Core Concepts

#### Variables & Data Types
```javascript
var name = "Alice";
var age = 25;
var height = 5.7;
var isStudent = true;

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
- See: `examples/javascript/comprehensive_demo.js`
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

### Learn More
- See: `examples/pascal/comprehensive_demo.pas`
- Reference: [PASCAL_REFERENCE.md](../languages/PASCAL_REFERENCE.md)

---

## Prolog - Logic Programming

**Best for:** Understanding logic programming, pattern matching

### Your First Prolog Program

```prolog
parent(tom, bob).
parent(bob, ann).

GRANDFATHER(X, Z) :- parent(X, Y), parent(Y, Z).
```

### Core Concepts

#### Facts & Rules
```prolog
% Facts
likes(alice, coffee).
likes(bob, tea).
likes(alice, tea).

% Rules
beverage(X) :- likes(alice, X).
```

### Learn More
- See: `examples/prolog/comprehensive_demo.pl`
- Reference: [PROLOG_REFERENCE.md](../languages/PROLOG_REFERENCE.md)

---

## Forth - Stack-Based

**Best for:** Understanding stack-based languages

### Your First Forth Program

```forth
: HELLO ." Hello, World!" CR ;
HELLO
```

### Learn More
- See: `examples/forth/comprehensive_demo.fth`
- Reference: [FORTH_REFERENCE.md](../languages/FORTH_REFERENCE.md)

---

## Perl - Text Processing

**Best for:** Text processing, regular expressions

### Your First Perl Program

```perl
#!/usr/bin/perl
use strict;
use warnings;

print "Hello, World!\n";
print "Welcome to Time Warp!\n";
```

### Learn More
- See: `examples/perl/comprehensive_demo.pl`
- Reference: [PERL_REFERENCE.md](../languages/PERL_REFERENCE.md)

---

## Logo - Graphics

**Best for:** Visual learning, turtle graphics

### Your First Logo Program

```logo
FORWARD 100
RIGHT 90
FORWARD 100
```

### Learn More
- See: `examples/logo/comprehensive_demo.logo`
- Reference: [LOGO_REFERENCE.md](../languages/LOGO_REFERENCE.md)

---

## PILOT - Education

**Best for:** Learning conditional logic, education

### Your First PILOT Program

```
T:Hello, World!
T:Welcome to PILOT!
```

### Learn More
- See: `examples/pilot/comprehensive_demo.pilot`
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
