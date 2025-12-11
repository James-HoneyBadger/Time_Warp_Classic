#!/usr/bin/env python3
"""
====================================
   Python Demo - Modern Programming
====================================
"""


def greet():
    """Display welcome message."""
    print("Welcome to Time Warp Python!")
    print("Python is a versatile, high-level programming language.")
    print()


def list_comprehension_demo():
    """Demonstrate list comprehensions."""
    print("=== List Comprehensions ===")

    # Generate squares
    squares = [x**2 for x in range(1, 11)]
    print(f"Squares: {squares}")

    # Filter even numbers
    evens = [x for x in range(1, 21) if x % 2 == 0]
    print(f"Even numbers 1-20: {evens}")

    # List of tuples
    coordinates = [(x, y) for x in range(3) for y in range(3)]
    print(f"3x3 grid coordinates: {coordinates}")
    print()


def dictionary_demo():
    """Demonstrate dictionary operations."""
    print("=== Dictionary Operations ===")

    languages = {
        "BASIC": 1964,
        "Logo": 1967,
        "Pascal": 1970,
        "Python": 1991,
        "JavaScript": 1995,
    }

    for lang, year in sorted(languages.items()):
        print(f"{lang} was created in {year}")

    # Dictionary comprehension
    vintage = {k: v for k, v in languages.items() if v < 1980}
    print(f"\nVintage languages (pre-1980): {list(vintage.keys())}")
    print()


def class_demo():
    """Demonstrate object-oriented programming."""
    print("=== Object-Oriented Programming ===")

    class Language:
        def __init__(self, name, year, paradigm):
            self.name = name
            self.year = year
            self.paradigm = paradigm

        def __str__(self):
            return f"{self.name} ({self.year}): {self.paradigm}"

        def is_vintage(self):
            return self.year < 1980

    # Create instances
    languages = [
        Language("Python", 1991, "Multi-paradigm"),
        Language("Logo", 1967, "Educational"),
        Language("Prolog", 1972, "Logic"),
    ]

    for lang in languages:
        vintage = "vintage" if lang.is_vintage() else "modern"
        print(f"{lang} - {vintage}")
    print()


def generator_demo():
    """Demonstrate generators."""
    print("=== Generators ===")

    def fibonacci(n):
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b

    fib_sequence = list(fibonacci(10))
    print(f"First 10 Fibonacci numbers: {fib_sequence}")
    print()


def lambda_demo():
    """Demonstrate lambda functions."""
    print("=== Lambda Functions ===")

    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Map
    squares = list(map(lambda x: x**2, numbers))
    print(f"Squares: {squares}")

    # Filter
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    print(f"Evens: {evens}")

    # Reduce
    from functools import reduce

    sum_all = reduce(lambda x, y: x + y, numbers)
    print(f"Sum: {sum_all}")
    print()


def main():
    """Main program."""
    greet()
    list_comprehension_demo()
    dictionary_demo()
    class_demo()
    generator_demo()
    lambda_demo()
    print("Python demo complete!")


if __name__ == "__main__":
    main()
