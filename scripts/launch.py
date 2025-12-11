#!/usr/bin/env python3
"""
Time Warp Classic Launcher
Simple launcher script for Time Warp Classic

Copyright © 2025 Honey Badger Universe
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
    
    # Launch the GUI
    try:
        os.chdir(project_root)
        subprocess.run([sys.executable, "Time_Warp.py"])
    except Exception as e:
        print(f"❌ Failed to launch Time Warp Classic: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
