#!/usr/bin/env python3
"""
COMPREHENSIVE PYTHON DEMO - Time Warp Classic IDE
Demonstrates all major Python language features
"""

print("=" * 50)
print("COMPREHENSIVE PYTHON DEMO")
print("=" * 50)
print()

# --- VARIABLES AND DATA TYPES ---
print("=== VARIABLES AND DATA TYPES ===")
integer_var = 42
float_var = 3.14159
string_var = "Time Warp"
bool_var = True

print(f"Integer: {integer_var}")
print(f"Float: {float_var}")
print(f"String: {string_var}")
print(f"Boolean: {bool_var}")
print()

# --- ARITHMETIC OPERATIONS ---
print("=== ARITHMETIC OPERATIONS ===")
a, b = 10, 3
print(f"Addition: {a + b}")
print(f"Subtraction: {a - b}")
print(f"Multiplication: {a * b}")
print(f"Division: {a / b}")
print(f"Floor Division: {a // b}")
print(f"Modulo: {a % b}")
print(f"Exponentiation: {a ** 2}")
print()

# --- STRING OPERATIONS ---
print("=== STRING OPERATIONS ===")
msg = "Python Programming"
print(f"Original: {msg}")
print(f"Length: {len(msg)}")
print(f"Uppercase: {msg.upper()}")
print(f"Lowercase: {msg.lower()}")
print(f"Replace: {msg.replace('Python', 'Time Warp')}")
print(f"Slice [0:6]: {msg[0:6]}")
print(f"Contains 'Pro': {'Pro' in msg}")
print(f"Split: {msg.split()}")
print()

# --- LISTS ---
print("=== LISTS ===")
numbers = [10, 20, 30, 40, 50]
print(f"List: {numbers}")
print(f"First element: {numbers[0]}")
print(f"Last element: {numbers[-1]}")
print(f"Length: {len(numbers)}")
print(f"Sum: {sum(numbers)}")
print(f"Min: {min(numbers)}")
print(f"Max: {max(numbers)}")
numbers.append(60)
print(f"After append: {numbers}")
numbers.sort(reverse=True)
print(f"Sorted (reverse): {numbers}")
print()

# --- DICTIONARIES ---
print("=== DICTIONARIES ===")
person = {
    "name": "Alice",
    "age": 30,
    "city": "New York",
    "occupation": "Developer"
}
print(f"Dictionary: {person}")
print(f"Name: {person['name']}")
print(f"Age: {person['age']}")
print(f"Keys: {list(person.keys())}")
print(f"Values: {list(person.values())}")
print(f"'name' in dict: {'name' in person}")
print()

# --- TUPLES ---
print("=== TUPLES ===")
coordinates = (10, 20, 30)
print("Tuple: " + str(coordinates))
print(f"First element: {coordinates[0]}")
print(f"Length: {len(coordinates)}")
print("Is immutable (cannot modify)")
print()

# --- SETS ---
print("=== SETS ===")
colors = {"red", "green", "blue"}
print(f"Set (duplicates removed): {colors}")
print(f"'red' in set: {'red' in colors}")
colors.add("yellow")
print(f"After add: {colors}")
colors.remove("blue")
print(f"After remove: {colors}")
print()

# --- CONDITIONAL STATEMENTS ---
print("=== IF/ELIF/ELSE STATEMENTS ===")
age = 25
if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")

score = 85
if score >= 90:
    print("Grade: A")
elif score >= 80:
    print("Grade: B")
elif score >= 70:
    print("Grade: C")
else:
    print("Grade: F")
print()

# --- LOOPS ---
print("=== FOR LOOPS ===")
print("Counting 1 to 5:")
for i in range(1, 6):
    print(f"  {i} squared = {i * i}")

print("\nIterating through list:")
for num in [2, 4, 6, 8]:
    print(f"  {num}")

print("\nEnumerate with index:")
for index, value in enumerate(["a", "b", "c"]):
    print(f"  Index {index}: {value}")
print()

# --- WHILE LOOPS ---
print("=== WHILE LOOPS ===")
counter = 1
while counter <= 3:
    print(f"  Counter: {counter}")
    counter += 1
print()

# --- FUNCTIONS ---
print("=== FUNCTIONS ===")


def greet(name):
    """Simple greeting function"""
    return f"Hello, {name}!"

def add_numbers(a, b):
    """Add two numbers"""
    return a + b

def factorial(n):
    """Calculate factorial recursively"""
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(greet("Alice"))
print(f"5 + 3 = {add_numbers(5, 3)}")
print(f"5! = {factorial(5)}")
print()

# --- LAMBDA FUNCTIONS ---
print("=== LAMBDA FUNCTIONS ===")
def square_val(x):
    return x ** 2
def add_vals(x, y):
    return x + y
print(f"Square of 5: {square_val(5)}")
print(f"Add 3 + 7: {add_vals(3, 7)}")
print()

# --- LIST COMPREHENSION ---
print("=== LIST COMPREHENSION ===")
squares = [x ** 2 for x in range(1, 6)]
print(f"Squares: {squares}")
evens = [x for x in range(10) if x % 2 == 0]
print(f"Even numbers: {evens}")
print()

# --- MATHEMATICAL OPERATIONS ---
print("=== MATHEMATICAL OPERATIONS ===")
import math
print(f"math.sqrt(16): {math.sqrt(16)}")
print(f"math.sin(0): {math.sin(0)}")
print(f"math.cos(0): {math.cos(0)}")
print(f"math.pi: {math.pi}")
print(f"math.e: {math.e}")
print()

# --- STRING FORMATTING ---
print("=== STRING FORMATTING ===")
name = "Bob"
score = 95.5
print(f"f-string: {name} scored {score}%")
print("format: {} scored {}%".format(name, score))
print("%s scored %.1f%%" % (name, score))
print()

# --- EXCEPTION HANDLING ---
print("=== EXCEPTION HANDLING ===")
try:
    result = 10 / 2
    print(f"10 / 2 = {result}")
    result = 10 / 0  # This will raise an error
except ZeroDivisionError:
    print("Cannot divide by zero!")
except Exception as e:
    print(f"Error: {e}")
else:
    print("No error occurred")
print()

# --- COMPARISON OPERATORS ---
print("=== COMPARISON OPERATORS ===")
x = 5
print(f"5 > 3: {x > 3}")
print(f"5 == 5: {x == 5}")
print(f"5 < 10: {x < 10}")
print(f"5 >= 5: {x >= 5}")
print(f"5 <= 10: {x <= 10}")
print(f"5 != 3: {x != 3}")
print()

# --- LOGICAL OPERATORS ---
print("=== LOGICAL OPERATORS ===")
if 5 > 3 and 10 > 5:
    print("AND: True")
if 5 > 3 or 10 < 5:
    print("OR: True")
if 5 >= 3:
    print("NOT: True")
print()

# --- FINAL MESSAGE ---
print("=" * 50)
print("PYTHON DEMO COMPLETE!")
print("All major Python features demonstrated successfully!")
print("=" * 50)
