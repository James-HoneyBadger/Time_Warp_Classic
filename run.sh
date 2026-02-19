#!/bin/bash
################################################################################
# Time Warp Classic - Complete Setup & Run Script
#
# This script:
# 1. Creates a Python virtual environment (if needed)
# 2. Installs all required Python dependencies (individually for resilience)
# 3. Launches the Time Warp Classic GUI
#
# Usage: ./run.sh [--clean] [--no-install]
#   --clean      Delete and recreate the virtual environment
#   --no-install Skip dependency installation
#
# Copyright © 2025–2026 Honey Badger Universe
################################################################################

# Get script directory (do NOT set -e; we handle errors per-step)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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
echo -e "${YELLOW}[1/5]${NC} Checking Python installation..."

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
echo -e "${YELLOW}[2/5]${NC} Setting up Virtual Environment..."

if [ "$CLEAN" = true ]; then
    if [ -d "venv" ]; then
        echo "🗑️  Removing existing virtual environment..."
        rm -rf venv
    fi
fi

if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    if ! python3 -m venv venv; then
        echo -e "${RED}❌ Failed to create virtual environment${NC}"
        echo "  Try: sudo dnf install python3-venv   (Fedora)"
        echo "       sudo apt install python3-venv   (Debian/Ubuntu)"
        exit 1
    fi
    echo -e "${GREEN}✓${NC} Virtual environment created"
else
    echo -e "${GREEN}✓${NC} Virtual environment already exists"
fi

# ============================================================================
# Activate Virtual Environment
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
# Step 3: Install Dependencies (individually for resilience)
# ============================================================================
if [ "$NO_INSTALL" = false ]; then
    echo -e "${YELLOW}[3/5]${NC} Installing Python dependencies..."

    # Upgrade pip first
    echo "📥 Upgrading pip..."
    pip install --upgrade pip setuptools wheel > /dev/null 2>&1

    # Helper: install a package, return 0 on success
    install_pkg() {
        local pkg="$1"
        local label="$2"
        if pip install "$pkg" > /dev/null 2>&1; then
            echo -e "  ${GREEN}✓${NC} $label installed"
            return 0
        else
            echo -e "  ${RED}✗${NC} $label failed to install"
            return 1
        fi
    }

    FAILED=0

    # --- Required runtime packages ---
    echo -e "${CYAN}  ── Required packages ──${NC}"

    # pygame-ce (community edition with pre-built wheels for more platforms)
    if python3 -c "import pygame" > /dev/null 2>&1; then
        echo -e "  ${GREEN}✓${NC} pygame already available"
    else
        install_pkg "pygame-ce>=2.0.0" "pygame-ce (multimedia)" || ((FAILED++))
    fi

    install_pkg "pygments>=2.15.0" "pygments (syntax highlighting)" || ((FAILED++))
    install_pkg "Pillow>=8.0.0" "Pillow (image processing)" || ((FAILED++))

    # --- Development packages (non-blocking) ---
    echo -e "${CYAN}  ── Development packages ──${NC}"
    install_pkg "pytest>=7.0.0" "pytest (testing)" || true
    install_pkg "black>=22.0.0" "black (formatting)" || true
    install_pkg "flake8>=4.0.0" "flake8 (linting)" || true

    echo ""
    if [ "$FAILED" -eq 0 ]; then
        echo -e "${GREEN}✓${NC} All runtime dependencies installed successfully"
    else
        echo -e "${YELLOW}⚠️  $FAILED runtime package(s) had issues (app may still work)${NC}"
    fi
else
    echo -e "${YELLOW}[3/5]${NC} Skipping dependency installation (--no-install)"
fi
echo ""

# ============================================================================
# Step 4: Verify Installation
# ============================================================================
echo -e "${YELLOW}[4/5]${NC} Verifying installation..."

VERIFY_OK=true

# Check for tkinter (required — provided by the OS, not pip)
if python3 -c "import tkinter" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} tkinter available"
else
    echo -e "${RED}  ❌ tkinter not available!${NC}"
    echo "  This is required. Install it with your system package manager:"
    echo "    Fedora:        sudo dnf install python3-tkinter"
    echo "    Ubuntu/Debian: sudo apt-get install python3-tk"
    echo "    macOS:         brew install python-tk"
    VERIFY_OK=false
fi

# Check for pygame (required for multimedia)
if python3 -c "import pygame" 2>/dev/null; then
    PYGAME_VER=$(python3 -c "import pygame; print(pygame.ver)" 2>/dev/null || echo "unknown")
    echo -e "  ${GREEN}✓${NC} pygame $PYGAME_VER available (multimedia support)"
else
    echo -e "${YELLOW}  ℹ  pygame not available (optional — some features limited)${NC}"
fi

# Check for pygments (syntax highlighting)
if python3 -c "import pygments" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} pygments available (syntax highlighting)"
else
    echo -e "${YELLOW}  ℹ  pygments not available (syntax highlighting disabled)${NC}"
fi

# Check for PIL/Pillow (image processing)
if python3 -c "import PIL" 2>/dev/null; then
    echo -e "  ${GREEN}✓${NC} PIL/Pillow available (image processing)"
else
    echo -e "${YELLOW}  ℹ  PIL/Pillow not available (image features limited)${NC}"
fi

if [ "$VERIFY_OK" = false ]; then
    echo ""
    echo -e "${RED}❌ Required dependency missing — see above.${NC}"
    exit 1
fi

echo ""

# ============================================================================
# Step 5: Launch Time Warp Classic
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

echo -e "${YELLOW}[5/5]${NC} Starting IDE..."

# Run the IDE
python3 Time_Warp.py "$@"

# Deactivate venv on exit (optional)
deactivate 2>/dev/null || true

echo ""
echo -e "${BLUE}Goodbye from Time Warp Classic!${NC}"
