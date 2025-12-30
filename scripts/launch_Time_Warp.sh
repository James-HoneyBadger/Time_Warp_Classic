#!/bin/bash
# Time Warp Classic Launch Script
# This script launches Time Warp Classic GUI
# Copyright © 2025 Honey Badger Universe

echo "🚀 Launching Time Warp Classic..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the project root directory (parent of scripts)
cd "$SCRIPT_DIR/.."

# Check if Python 3 is available
if command -v python3 >/dev/null 2>&1; then
    echo "✅ Found Python 3"
    python3 Time_Warp.py
elif command -v python >/dev/null 2>&1; then
    echo "✅ Found Python"
    python Time_Warp.py
else
    echo "❌ Python not found. Please install Python 3.9 or higher."
    exit 1
fi

echo "👋 Time Warp Classic session ended."