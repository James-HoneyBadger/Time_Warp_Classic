#!/usr/bin/env python3
"""
Test configuration and shared fixtures for Time_Warp_Classic tests.
"""

import pytest
import tkinter as tk
from unittest.mock import Mock
from core.interpreter import Time_WarpInterpreter


@pytest.fixture
def interpreter():
    """Create a fresh interpreter instance for testing."""
    interp = Time_WarpInterpreter()
    # Mock the output widget to avoid GUI dependencies
    interp.output_widget = Mock()
    return interp


@pytest.fixture
def root():
    """Create a tkinter root window for GUI tests."""
    root = tk.Tk()
    root.withdraw()  # Hide the window during tests
    yield root
    root.destroy()


@pytest.fixture
def sample_programs():
    """Sample programs for different languages."""
    return {
        "basic": """10 PRINT "Hello, BASIC!"
20 LET X = 42
30 PRINT "X = "; X
40 END""",

        "pilot": """T: Hello World Program
A: Welcome to PILOT!
T: Variables
A: Let's work with variables
C: X=10
T: Result
A: X is *X*
J: 1""",

        "logo": """FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100""",

        "python": """print("Hello from Python!")
x = 42
print(f"x = {x}")
for i in range(3):
    print(f"Count: {i}")""",

        "javascript": """console.log("Hello from JavaScript!");
let x = 42;
console.log(`x = ${x}`);
for (let i = 0; i < 3; i++) {
    console.log(`Count: ${i}`);
}"""
    }