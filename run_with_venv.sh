#!/bin/bash
# Time Warp - Run with Virtual Environment
# This script activates the virtual environment and runs Time_Warp

cd "$(dirname "$0")"

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run Time_Warp
python Time_Warp.py "$@"
