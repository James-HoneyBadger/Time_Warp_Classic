# This file marks the 'utilities' directory as a Python package.

"""
Time_Warp Utilities Module
==========================

Utility functions and helper classes for the Time_Warp IDE.

This module provides shared functionality used across different parts of the
Time_Warp system, including helper functions for string processing, math
operations, and common programming tasks.
"""

# Utility functions for string manipulation
def safe_str(value):
    """Convert a value to string safely"""
    try:
        return str(value)
    except Exception:
        return "<error>"

def truncate_string(text, max_length=100):
    """Truncate a string to a maximum length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

# Utility functions for math operations
def clamp(value, min_val, max_val):
    """Clamp a value between min and max"""
    return max(min_val, min(value, max_val))

def lerp(a, b, t):
    """Linear interpolation between a and b"""
    return a + (b - a) * t

# Add specific utility imports here as they are implemented
