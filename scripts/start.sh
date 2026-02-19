#!/bin/bash
# Time Warp Classic Simple Launcher
# Copyright © 2025–2026 Honey Badger Universe

echo "🚀 Starting Time Warp Classic..."

# Get script directory and change to project root
cd "$(dirname "$0")/.."

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
elif [ ! -d "venv" ]; then
    echo "⚠️  No virtual environment found. Run ./run.sh first for full setup."
fi

# Launch the GUI
if command -v python3 >/dev/null 2>&1; then
    python3 Time_Warp.py
elif command -v python >/dev/null 2>&1; then
    python Time_Warp.py
else
    echo "❌ Python not found. Please install Python 3.9 or higher."
    exit 1
fi