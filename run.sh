#!/bin/bash
################################################################################
# Time Warp Classic - Complete Setup & Run Script
# 
# This script:
# 1. Creates a Python virtual environment (if needed)
# 2. Installs all required Python dependencies
# 3. Launches the Time Warp Classic GUI
#
# Usage: ./run.sh [--clean] [--no-install]
#   --clean      Delete and recreate the virtual environment
#   --no-install Skip dependency installation
#
# Copyright © 2025 Honey Badger Universe
################################################################################

set -e  # Exit on any error

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse command line arguments
CLEAN=false
NO_INSTALL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --clean)
            CLEAN=true
            shift
            ;;
        --no-install)
            NO_INSTALL=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        Time Warp Classic - Multi-Language IDE              ║${NC}"
echo -e "${BLUE}║              Initialization & Setup Script                 ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ============================================================================
# Step 1: Check Python availability
# ============================================================================
echo -e "${YELLOW}[1/4]${NC} Checking Python installation..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 not found!${NC}"
    echo "Please install Python 3.9 or higher from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"
echo ""

# ============================================================================
# Step 2: Virtual Environment Setup
# ============================================================================
echo -e "${YELLOW}[2/4]${NC} Setting up Virtual Environment..."

if [ "$CLEAN" = true ]; then
    if [ -d "venv" ]; then
        echo "🗑️  Removing existing virtual environment..."
        rm -rf venv
    fi
fi

if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
fi

# ============================================================================
# Step 3: Activate Virtual Environment
# ============================================================================
echo "🔗 Activating virtual environment..."

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
    echo -e "${GREEN}✓${NC} Virtual environment activated"
else
    echo -e "${RED}❌ Failed to activate virtual environment${NC}"
    exit 1
fi
echo ""

# ============================================================================
# Step 4: Install Dependencies
# ============================================================================
if [ "$NO_INSTALL" = false ]; then
    echo -e "${YELLOW}[3/4]${NC} Installing Python dependencies..."
    
    # Upgrade pip first
    echo "📥 Upgrading pip..."
    pip install --upgrade pip setuptools wheel > /dev/null 2>&1
    
    # Check if requirements.txt exists
    if [ -f "requirements.txt" ]; then
        echo "📚 Installing packages from requirements.txt..."
        
        # Install with some resilience
        if pip install -r requirements.txt; then
            echo -e "${GREEN}✓${NC} All dependencies installed successfully"
        else
            echo -e "${YELLOW}⚠️  Some dependencies may have failed to install${NC}"
            echo "    (This is often OK - many features work without optional dependencies)"
        fi
    else
        echo -e "${RED}❌ requirements.txt not found!${NC}"
        exit 1
    fi
else
    echo -e "${YELLOW}[3/4]${NC} Skipping dependency installation (--no-install)"
fi
echo ""

# ============================================================================
# Step 5: Verify Installation
# ============================================================================
echo -e "${YELLOW}[4/4]${NC} Verifying installation..."

# Check for tkinter (required)
python3 -c "import tkinter; print('  ✓ tkinter available')" 2>/dev/null || {
    echo -e "${RED}  ❌ tkinter not available!${NC}"
    echo "  Note: tkinter usually comes with Python. If missing, try:"
    echo "    Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "    Fedora: sudo dnf install python3-tkinter"
    echo "    macOS: Usually included; brew install python-tk if needed"
}

# Check for pygame (recommended)
if python3 -c "import pygame" 2>/dev/null; then
    echo "  ✓ pygame available (multimedia support)"
else
    echo -e "${YELLOW}  ℹ${NC}  pygame not available (optional - some features limited)"
fi

# Check for pygments (recommended)
if python3 -c "import pygments" 2>/dev/null; then
    echo "  ✓ pygments available (syntax highlighting)"
else
    echo -e "${YELLOW}  ℹ${NC}  pygments not available (syntax highlighting disabled)"
fi

# Check for PIL/Pillow (optional)
if python3 -c "import PIL" 2>/dev/null; then
    echo "  ✓ PIL/Pillow available (image processing)"
else
    echo -e "${YELLOW}  ℹ${NC}  PIL/Pillow not available (image features limited)"
fi

echo ""

# ============================================================================
# Step 6: Launch Time Warp Classic
# ============================================================================
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     🚀 Launching Time Warp Classic...                     ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Verify Time_Warp.py exists
if [ ! -f "Time_Warp.py" ]; then
    echo -e "${RED}❌ Time_Warp.py not found!${NC}"
    exit 1
fi

# Run the IDE
python3 Time_Warp.py "$@"

# Deactivate venv on exit (optional)
deactivate 2>/dev/null || true

echo ""
echo -e "${BLUE}Goodbye from Time Warp Classic!${NC}"
