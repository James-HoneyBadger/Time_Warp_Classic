#!/usr/bin/env python3
"""
Test runner script for Time_Warp_Classic.

This script provides a simple way to run the test suite from the command line
or from within the application.
"""

import sys
import subprocess
from pathlib import Path


def run_tests(test_type="all", verbose=False, coverage=False):
    """
    Run the test suite.

    Args:
        test_type: Type of tests to run ("unit", "integration", "language", "all")
        verbose: Enable verbose output
        coverage: Generate coverage report
    """
    project_root = Path(__file__).parent

    # Build pytest command
    cmd = [sys.executable, "-m", "pytest"]

    if test_type == "unit":
        cmd.append("tests/unit/")
    elif test_type == "integration":
        cmd.append("tests/integration/")
    elif test_type == "language":
        cmd.append("tests/language/")
    else:  # all
        cmd.append("tests/")

    if verbose:
        cmd.append("-v")
    else:
        cmd.append("--tb=short")

    if coverage:
        cmd.extend([
            "--cov=time_warp",
            "--cov-report=term-missing",
            "--cov-report=html:htmlcov"
        ])

    # Run tests
    try:
        result = subprocess.run(cmd, cwd=project_root, check=False)
        return result.returncode == 0
    except FileNotFoundError:
        print("❌ pytest not found. Install with: pip install pytest")
        return False


def run_quick_test():
    """Run a quick smoke test to verify basic functionality."""
    print("🧪 Running quick smoke test...")

    try:
        # Import core modules
        from core.interpreter import Time_WarpInterpreter
        from core.languages.basic import TwBasicExecutor
        from core.languages.pilot import TwPilotExecutor

        # Create interpreter
        interpreter = Time_WarpInterpreter()

        # Create interpreter
        interpreter = Time_WarpInterpreter()

        # Test basic functionality
        result = interpreter.evaluate_expression("2 + 3")
        assert result == 5, f"Expected 5, got {result}"

        # Test variable assignment
        interpreter.variables['TEST'] = 42
        assert interpreter.variables['TEST'] == 42

        # Test basic program execution
        basic_program = 'PRINT "Hello, Test!"'
        interpreter.load_program(basic_program)

        print("✅ Smoke test passed!")
        return True

    except Exception as e:
        print(f"❌ Smoke test failed: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run Time_Warp_Classic tests")
    parser.add_argument(
        "test_type",
        nargs="?",
        choices=["unit", "integration", "language", "all", "smoke"],
        default="all",
        help="Type of tests to run"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "-c", "--coverage",
        action="store_true",
        help="Generate coverage report"
    )

    args = parser.parse_args()

    if args.test_type == "smoke":
        success = run_quick_test()
    else:
        success = run_tests(args.test_type, args.verbose, args.coverage)

    sys.exit(0 if success else 1)