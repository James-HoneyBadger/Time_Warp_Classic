# Python Language Reference

Complete reference for Python 3 syntax and features in Time Warp Classic.

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

## Tips & Best Practices

1. **Use f-strings** for string formatting
2. **List comprehensions** are more efficient than loops
3. **Type hints** improve code clarity (Python 3.5+)
4. **Error handling** prevents crashes
5. **Use meaningful names** for variables
6. **Avoid global variables** when possible
7. **Test your code** with various inputs

## See Also

- [USER_GUIDE.md](../user/USER_GUIDE.md)
- [LANGUAGE_TUTORIALS.md](../user/LANGUAGE_TUTORIALS.md)
- [examples/python/](../../examples/python/)

---

**Last Updated:** 2024
