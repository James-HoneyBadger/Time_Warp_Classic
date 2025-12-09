#!/usr/bin/env python3
"""Run comprehensive Time_Warp language programs and verify outputs."""

# pylint: disable=import-error,wrong-import-position,broad-except,unspecified-encoding

import json
import sys
import tkinter as tk
from datetime import datetime
from pathlib import Path

# Ensure repository root on path
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.interpreter import Time_WarpInterpreter

# Programs for each language: list of (command, expected_substring or None)
PROGRAMS = {
    "Logo": [
        ("CLEARSCREEN", "cleared"),
        ("SETCOLOR red", "color"),
        ("SETPENSIZE 4", "pen size"),
        ("SETXY 30 40", "setxy"),
        ("FORWARD 20", "turtle moved"),
        ("LEFT 90", "left"),
        ("FORWARD 10", "turtle moved"),
        ("PENUP", "pen up"),
        ("RIGHT 45", "right"),
        ("PENDOWN", "pen down"),
        ("CIRCLE 15", "circle"),
    ],
    "PILOT": [
        ("T:Hello world", "hello"),
        ("A:Enter name", "awaiting input"),
        ("Y:OK", None),
        ("N:OK", None),
        ("G:PENUP", "pen"),
        ("G:PENDOWN", "pen"),
        ("G:COLOR,blue", "color"),
        ("G:LINE,0,0,50,50", "line"),
        ("MATH:SIN 90", "1"),
    ],
    "BASIC": [
        ("PRINT [HELLO]", "hello"),
        ("LET A = 5", None),
        ("LET B = 3", None),
        ("IF A > B THEN PRINT [A greater]", "greater"),
        ("FOR I = 1 TO 3", None),
        ("PRINT [LOOP]", "loop"),
        ("NEXT I", None),
    ],
    "Python": [
        ("print('py start')", "py start"),
        ("x=5\nprint(x*2)", "10"),
        ("for i in range(3):\n    print(i)", "2"),
    ],
    "JavaScript": [
        ("console.log('js start')", "js start"),
        ("var a = 2; var b = 3; console.log(a + b);", "5"),
        ("if (true) { console.log('yes'); }", "yes"),
    ],
    "Forth": [
        ("5 DUP .", None),
        ("5 6 DROP", None),
        ("1 2 SWAP . .", None),
        ("5 3 + .", None),
        ("42 .", None),
    ],
    "Pascal": [
        ("writeln('Hello Pascal')", "hello"),
        ("write('test')", "test"),
        ("IF 1 = 1 THEN writeln('yes')", "yes"),
    ],
    "Perl": [
        ("print 'Hello Perl'", "hello"),
        ("print 4+6;", "10"),
    ],
    "Prolog": [
        ("parent(tom, bob).", None),
        ("?- parent(tom, bob).", "query succeeded"),
    ],
}


def run_program(interp, output, language, commands):
    """Run a sequence of commands for a language and verify outputs."""
    results = []
    interp.current_language_mode = language

    # Provide a default input function to avoid blocking
    interp.get_user_input = lambda prompt: "test"

    for command, expected in commands:
        output.delete("1.0", "end")
        try:
            interp.execute_line(command)
            text = output.get("1.0", "end").strip()
            passed = True if expected is None else expected.lower() in text.lower()
            results.append({
                "command": command,
                "expected": expected,
                "output": text,
                "passed": passed,
            })
        except Exception as exc:
            results.append({
                "command": command,
                "expected": expected,
                "output": "",
                "passed": False,
                "exception": str(exc),
            })
    return results


def main():
    root = tk.Tk()
    root.withdraw()
    output = tk.Text(root)
    interp = Time_WarpInterpreter(output)
    interp.init_turtle_graphics()

    summary = {"timestamp": datetime.now().isoformat(), "languages": {}}

    for language, commands in PROGRAMS.items():
        print("\n" + "=" * 70)
        print(f"Running program for {language}")
        print("=" * 70)
        results = run_program(interp, output, language, commands)
        passed = sum(1 for r in results if r.get("passed"))
        total = len(results)
        summary["languages"][language] = {
            "passed": passed,
            "total": total,
            "details": results,
        }
        for r in results:
            status = "PASS" if r.get("passed") else "FAIL"
            print(f"[{status}] {r['command']} -> {r.get('output', '')[:80]}")

    # Write summary
    out_path = Path("test_results_programs.json")
    out_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("\nSummary saved to", out_path)

    root.destroy()


if __name__ == "__main__":
    sys.exit(main())
