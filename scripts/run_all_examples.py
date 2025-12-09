#!/usr/bin/env python3
"""Run all example files under examples/ through the interpreter and capture outputs.

This headless runner opens each example file, sets the corresponding language mode
(if applicable), runs line-by-line through the interpreter, and stores the output
snippet for inspection.
"""
# pylint: disable=import-error,wrong-import-position,unspecified-encoding
import sys
from pathlib import Path
import tkinter as tk
import json

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.interpreter import Time_WarpInterpreter

EXAMPLES_DIR = ROOT / "examples"

LANG_EXT_TO_MODE = {
    "pilot": "PILOT",
    "bas": "BASIC",
    "logo": "Logo",
    "py": "Python",
    "js": "JavaScript",
    "pas": "Pascal",
    "pl": "Perl",
    "prolog": "Prolog",
    "forth": "Forth",
}

OUTPUT = {}


def run_example_file(interp, output_widget, path, mode=None):
    """Run an example file through the interpreter line-by-line"""

    output_widget.delete("1.0", "end")
    interp.current_language_mode = mode
    text = path.read_text(encoding="utf-8")
    results = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            interp.execute_line(line)
            out_text = output_widget.get("1.0", "end").strip()
            results.append({"line": line, "output": out_text})
        except Exception as e:  # capture and store
            results.append({"line": line, "output": "", "error": str(e)})

    return results


def main():
    root = tk.Tk(); root.withdraw()
    output = tk.Text(root)
    interp = Time_WarpInterpreter(output)
    interp.init_turtle_graphics()

    for folder in EXAMPLES_DIR.iterdir():
        if not folder.is_dir():
            continue
        OUTPUT[str(folder.name)] = {}
        for file in folder.iterdir():
            if file.is_dir():
                continue
            mode = None
            ext = file.suffix.lower().strip('.')
            if ext in LANG_EXT_TO_MODE:
                mode = LANG_EXT_TO_MODE[ext]
            else:
                # infer by folder or filename
                # folders like PILOT contain .pilot file
                if folder.name.upper() in ["PILOT","LOGO","BASIC","PYTHON","JAVASCRIPT","PASCAL","PERL","PROLOG","FORTH"]:
                    mode = folder.name
            OUTPUT[str(folder.name)][file.name] = run_example_file(interp, output, file, mode=mode)

    out_path = ROOT / "test_results_examples.json"
    out_path.write_text(json.dumps(OUTPUT, indent=2), encoding="utf-8")

    print("Completed running examples. Results written to", out_path)
    root.destroy()


if __name__ == "__main__":
    main()
