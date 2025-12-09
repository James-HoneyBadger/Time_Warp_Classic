#!/usr/bin/env python3
"""Run a GUI test: open a Tk window, attach a real Canvas and run a demo program.

This script is intended to be used in environments with a display (or Xvfb).
It will load examples/PILOT/demo_graphics.pilot and execute it via the interpreter
using the real Tk Canvas so we can validate actual GUI drawing occurs.
"""
import sys
from pathlib import Path
import tkinter as tk

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.interpreter import Time_WarpInterpreter


def main():
    demo = ROOT / "examples" / "PILOT" / "demo_graphics.pilot"
    if not demo.exists():
        print(f"Demo not found: {demo}")
        sys.exit(2)

    code = demo.read_text(encoding="utf-8")

    root = tk.Tk()
    root.title("Time_Warp GUI Demo Test")

    output = tk.Text(root, height=10, width=80)
    output.pack(side=tk.BOTTOM, fill=tk.X)

    canvas = tk.Canvas(root, width=640, height=480, bg="white")
    canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    interp = Time_WarpInterpreter(output)
    # Attach the IDE canvas so interpreter will use it for drawing
    interp.ide_turtle_canvas = canvas
    interp.init_turtle_graphics()

    print("Starting demo run...")
    interp.run_program(code)

    # After running, gather some stats
    items = canvas.find_all()
    print(f"Canvas items: {len(items)}")

    # Output the text area content for debugging
    out_text = output.get("1.0", "end").strip()
    print("-- Output --")
    print(out_text)

    # Keep the window open briefly so a human can see it if connected
    root.after(2000, root.destroy)
    root.mainloop()


if __name__ == "__main__":
    main()
