#!/usr/bin/env python3
"""
Time Warp Classic Launcher
Simple launcher script for Time Warp Classic

Copyright © 2025–2026 Honey Badger Universe
"""

import os
import sys
import subprocess


def main():
    """Launch Time Warp Classic GUI"""
    print("🚀 Time Warp Classic Launcher")
    print("=" * 50)

    # Get the directory where this launcher is located
    launcher_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one level to the project root
    project_root = os.path.dirname(launcher_dir)

    # Path to main Time_Warp.py
    main_script = os.path.join(project_root, "Time_Warp.py")

    if not os.path.exists(main_script):
        print(f"❌ Error: Cannot find Time_Warp.py at {main_script}")
        sys.exit(1)

    # Use venv python if available, otherwise fall back to current interpreter
    if sys.platform == "win32":
        venv_python = os.path.join(project_root, "venv", "Scripts", "python.exe")
    else:
        venv_python = os.path.join(project_root, "venv", "bin", "python")

    if os.path.exists(venv_python):
        python_exe = venv_python
        print("✅ Using virtual environment")
    else:
        python_exe = sys.executable
        print("⚠️  No virtual environment found. Run ./run.sh first for full setup.")

    # Launch the GUI
    try:
        os.chdir(project_root)
        subprocess.run([python_exe, "Time_Warp.py"], check=True)
    except Exception as e:
        print(f"❌ Failed to launch Time Warp Classic: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
