# Python Language Reference

Complete reference for Python 3 syntax and features in Time Warp Classic.

> **Note:** Python runs via subprocess with a 30-second timeout. Full Python 3 standard library is available.

## Quick Reference

| Feature | Syntax | Example |
|---------|--------|---------|
| Variables | `var = value` | `x = 10` |
| Print | `print(expr)` | `print("Hello")` |
| Input | `input(prompt)` | `name = input("Name: ")` |
| If/Elif/Else | `if cond: ... elif ... else:` | `if x > 5: print("Big")` |
| For Loop | `for var in iterable:` | `for i in range(10):` |
| While Loop | `while cond:` | `while x < 100:` |
| Function | `def name(args):` | `def add(a, b): return a + b` |
| List | `[value, value, ...]` | `[1, 2, 3]` |
| Dict | `{key: value, ...}` | `{"name": "Alice"}` |

## Variables & Data Types

### Variable Assignment

```python
x = 10                    # Integer
name = "Alice"            # String
height = 5.7              # Float
is_active = True          # Boolean
items = [1, 2, 3]         # List
```

### Data Types

```python
type(10)                  # <class 'int'>
type("hello")             # <class 'str'>
type(3.14)                # <class 'float'>
type(True)                # <class 'bool'>
type([1, 2])              # <class 'list'>
type({"a": 1})            # <class 'dict'>
```

### Type Conversion

```python
int("42")                 # 42
str(42)                   # "42"
float("3.14")             # 3.14
bool(1)                   # True
list("abc")               # ['a', 'b', 'c']
```

## Operators

### Arithmetic

```python
+       Addition         5 + 3 = 8
-       Subtraction      5 - 3 = 2
*       Multiplication   5 * 3 = 15
/       Division         6 / 2 = 3.0
//      Floor division   7 // 2 = 3
%       Modulo           7 % 3 = 1
**      Power            2 ** 3 = 8
```

### Comparison

```python
==      Equal            5 == 5
!=      Not equal        5 != 3
<       Less than        3 < 5
>       Greater than     5 > 3
<=      Less or equal    5 <= 5
>=      Greater or equal 5 >= 5
```

### Logical

```python
and     Logical AND      x > 5 and y < 10
or      Logical OR       x == 1 or x == 2
not     Logical NOT      not done
```

### Membership

```python
in      Membership       "a" in "abc"
not in  Not membership   "x" not in "abc"
```

## Control Structures

### If/Elif/Else

```python
if condition:
    statements
elif condition:
    statements
else:
    statements

# Example
if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teen")
else:
    print("Child")
```

### For Loop

```python
for variable in iterable:
    statements

# Examples
for i in range(5):
    print(i)                # 0, 1, 2, 3, 4

for name in ["Alice", "Bob"]:
    print(name)

for i in range(1, 11, 2):
    print(i)                # 1, 3, 5, 7, 9 (step by 2)
```

### While Loop

```python
while condition:
    statements

# Example
count = 0
while count < 5:
    print(count)
    count += 1
```

### Break & Continue

```python
for i in range(10):
    if i == 5:
        break               # Exit loop
    if i == 2:
        continue            # Skip to next iteration
    print(i)
```

## Collections

### Lists

```python
numbers = [1, 2, 3, 4, 5]

# Access
numbers[0]                # 1 (first element)
numbers[-1]               # 5 (last element)
numbers[1:3]              # [2, 3] (slice)

# Methods
numbers.append(6)         # Add element
numbers.pop()             # Remove and return last
numbers.pop(0)            # Remove and return first
numbers.insert(0, 0)      # Insert at position
numbers.remove(3)         # Remove value
numbers.sort()            # Sort in place
numbers.reverse()         # Reverse in place
numbers.clear()           # Remove all elements

# Functions
len(numbers)              # 5
sum(numbers)              # 15
max(numbers)              # 5
min(numbers)              # 1

# Iteration
for num in numbers:
    print(num)

# List comprehension
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]
```

### Tuples

```python
point = (10, 20)
colors = ("red", "green", "blue")

# Access (like lists, but immutable)
point[0]                  # 10
colors[1:3]               # ("green", "blue")

# Unpacking
x, y = point              # x=10, y=20
```

### Dictionaries

```python
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York"
}

# Access
person["name"]            # "Alice"
person.get("age")         # 30
person.get("email", "N/A") # "N/A" (default)

# Modification
person["email"] = "alice@example.com"
del person["city"]

# Methods
person.keys()             # dict_keys(['name', 'age', 'email'])
person.values()           # dict_values(['Alice', 30, ...])
person.items()            # dict_items([('name', 'Alice'), ...])

# Iteration
for key in person:
    print(key, person[key])
```

### Sets

```python
unique = {1, 2, 3, 3, 4}  # {1, 2, 3, 4}

# Methods
unique.add(5)
unique.remove(3)
unique.discard(3)         # Remove if exists
unique.union({4, 5, 6})   # {1, 2, 4, 5, 6}
unique.intersection({3, 4})
```

## Functions

### Function Definition

```python
def greet(name):
    return f"Hello, {name}!"

def add(a, b):
    return a + b

def print_info(name, age=20):
    print(f"{name} is {age}")

# Calling
greet("Alice")
add(5, 3)
print_info("Bob", 25)
```

### Return Values

```python
def get_values():
    return 1, 2, 3        # Multiple returns (tuple)

a, b, c = get_values()
```

### *args and **kwargs

```python
def sum_all(*args):
    return sum(args)

def print_config(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

sum_all(1, 2, 3, 4)
print_config(host="localhost", port=8000)
```

### Lambda Functions

```python
square = lambda x: x ** 2
square(5)                 # 25

add = lambda x, y: x + y
add(3, 4)                 # 7
```

## String Operations

### String Basics

```python
msg = "Hello, World!"

# Length
len(msg)                  # 13

# Case conversion
msg.upper()               # "HELLO, WORLD!"
msg.lower()               # "hello, world!"
msg.capitalize()          # "Hello, world!"

# Finding
msg.find("World")         # 7
"World" in msg            # True
```

### String Slicing

```python
text = "Python"
text[0]                   # "P"
text[0:2]                 # "Py"
text[::2]                 # "Pto" (every 2nd char)
text[::-1]                # "nohtyP" (reversed)
```

### String Methods

```python
"  hello  ".strip()       # "hello"
"hello-world".split("-")  # ["hello", "world"]
",".join(["a", "b", "c"]) # "a,b,c"
"hello".replace("l", "L") # "heLLo"
"hello".startswith("he")  # True
"hello".endswith("lo")    # True
```

### String Formatting

```python
# f-strings
name = "Alice"
age = 30
f"{name} is {age}"        # "Alice is 30"

# format() method
"Hello, {}".format("Bob")
"{} + {} = {}".format(1, 2, 3)

# % formatting
"Hello, %s" % "Charlie"
```

## Comprehensions

### List Comprehension

```python
squares = [x**2 for x in range(5)]
# [0, 1, 4, 9, 16]

even = [x for x in range(10) if x % 2 == 0]
# [0, 2, 4, 6, 8]
```

### Dict Comprehension

```python
squares_dict = {x: x**2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}
```

### Set Comprehension

```python
unique_squares = {x**2 for x in [1, 2, 2, 3, 3, 3]}
# {1, 4, 9}
```

## Exception Handling

### Try/Except

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
except Exception as e:
    print(f"Error: {e}")
else:
    print("Success!")
finally:
    print("Cleanup code")
```

## Standard Library

### Math Module

```python
import math

math.sqrt(16)             # 4.0
math.sin(0)               # 0.0
math.cos(0)               # 1.0
math.pi                   # 3.14159...
math.floor(3.7)           # 3
math.ceil(3.2)            # 4
```

### Random Module

```python
import random

random.randint(1, 100)    # Random int 1-100
random.choice([1, 2, 3])  # Random from list
random.shuffle(list)      # Shuffle in place
```

## Complete Examples

### Even/Odd Checker

```python
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
evens = [n for n in numbers if n % 2 == 0]
odds = [n for n in numbers if n % 2 != 0]
print("Even:", evens)
print("Odd:", odds)
```

### Word Frequency Counter

```python
text = "hello world hello python hello"
words = text.split()
freq = {}
for word in words:
    freq[word] = freq.get(word, 0) + 1
print(freq)
# {'hello': 3, 'world': 1, 'python': 1}
```

### Fibonacci Generator

```python
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

for num in fibonacci(8):
    print(num)
```

## Classes & Object-Oriented Programming

### Class Definition

```python
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}"

    def __str__(self):
        return f"Animal({self.name})"

dog = Animal("Rex", "Woof")
print(dog.speak())        # Rex says Woof
```

### Inheritance

```python
class Dog(Animal):
    def __init__(self, name):
        super().__init__(name, "Woof")
        self.tricks = []

    def learn(self, trick):
        self.tricks.append(trick)

    def show_tricks(self):
        return f"{self.name} knows: {', '.join(self.tricks)}"

rex = Dog("Rex")
rex.learn("sit")
rex.learn("shake")
print(rex.show_tricks())  # Rex knows: sit, shake
```

### Properties

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius must be non-negative")
        self._radius = value

    @property
    def area(self):
        import math
        return math.pi * self._radius ** 2
```

### Class Methods & Static Methods

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    @classmethod
    def from_string(cls, date_str):
        y, m, d = map(int, date_str.split("-"))
        return cls(y, m, d)

    @staticmethod
    def is_valid(year, month, day):
        return 1 <= month <= 12 and 1 <= day <= 31

d = Date.from_string("2025-06-15")
```

### Dataclasses

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

    def distance_to(self, other):
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5

p1 = Point(0, 0)
p2 = Point(3, 4)
print(p1.distance_to(p2))  # 5.0
```

## Decorators

```python
# Function decorator
def timer(func):
    import time
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    import time
    time.sleep(0.1)
    return "done"

# Decorator with parameters
def repeat(n):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say_hello():
    print("Hello!")
```

## Context Managers

```python
# Using with statement
with open("file.txt", "r") as f:
    content = f.read()

# Custom context manager
from contextlib import contextmanager

@contextmanager
def timer(label):
    import time
    start = time.time()
    yield
    elapsed = time.time() - start
    print(f"{label}: {elapsed:.4f}s")

with timer("Processing"):
    result = sum(range(1000000))
```

## Import System

```python
import math
from math import sqrt, pi
from collections import Counter, defaultdict
from itertools import chain, combinations
import json
import os
```

## Regular Expressions

```python
import re

text = "Hello World 123"

# Search
match = re.search(r'\d+', text)
if match:
    print(match.group())       # 123

# Find all
numbers = re.findall(r'\d+', "a1 b22 c333")
# ['1', '22', '333']

# Replace
result = re.sub(r'\d+', '#', text)
# "Hello World #"

# Split
parts = re.split(r'\s+', text)
# ['Hello', 'World', '123']

# Compile for reuse
pattern = re.compile(r'[A-Z][a-z]+')
words = pattern.findall(text)  # ['Hello', 'World']
```

## Generators & Itertools

```python
# Generator function
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Use generator
fib = fibonacci()
first_10 = [next(fib) for _ in range(10)]

# Generator expression
squares = (x**2 for x in range(100))

# Itertools
from itertools import count, cycle, chain, combinations

# Infinite counter
for i in count(1):
    if i > 5: break
    print(i)

# Combinations
list(combinations([1, 2, 3], 2))
# [(1, 2), (1, 3), (2, 3)]
```

## File I/O

```python
# Read file
with open("data.txt", "r") as f:
    content = f.read()           # Read all
    # lines = f.readlines()      # Read as list of lines

# Write file
with open("output.txt", "w") as f:
    f.write("Hello\n")
    f.write("World\n")

# JSON
import json
data = {"name": "Alice", "age": 30}
json_str = json.dumps(data)
parsed = json.loads(json_str)
```

## Tips & Best Practices

1. **Use f-strings** for string formatting
2. **List comprehensions** are more Pythonic than manual loops
3. **Use `with`** for resource management (files, connections)
4. **Use dataclasses** for simple data containers
5. **Use type hints** for clarity: `def add(a: int, b: int) -> int:`
6. **Handle errors** with try/except
7. **Use meaningful names** for variables and functions
8. **Execution timeout:** 30 seconds for all Python programs

## See Also

- [LANGUAGE_TUTORIALS.md](../user/LANGUAGE_TUTORIALS.md)
- [examples/python/](../../examples/python/)

---

**Last Updated:** 2025
