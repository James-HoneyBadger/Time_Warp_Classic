@echo off
REM ============================================================================
REM Time Warp Classic - Complete Setup & Run Script (Windows)
REM
REM This script:
REM 1. Creates a Python virtual environment (if needed)
REM 2. Installs all required Python dependencies (individually for resilience)
REM 3. Launches the Time Warp Classic GUI
REM
REM Usage: run.bat [--clean] [--no-install]
REM   --clean      Delete and recreate the virtual environment
REM   --no-install Skip dependency installation
REM
REM Copyright © 2025–2026 Honey Badger Universe
REM ============================================================================

setlocal enabledelayedexpansion

REM Get script directory
cd /d "%~dp0"

REM Colors (using title for visual feedback on Windows)
setlocal
set "CLEAN=false"
set "NO_INSTALL=false"

REM Parse command line arguments
:parse_args
if "%1"=="" goto done_args
if "%1"=="--clean" set "CLEAN=true" && shift && goto parse_args
if "%1"=="--no-install" set "NO_INSTALL=true" && shift && goto parse_args
shift
goto parse_args

:done_args

cls
title Time Warp Classic - Setup & Launch
echo.
echo ============================================================================
echo.
echo         Time Warp Classic - Multi-Language IDE
echo            Initialization ^& Setup Script (Windows)
echo.
echo ============================================================================
echo.

REM ============================================================================
REM Step 1: Check Python availability
REM ============================================================================
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python 3 not found!
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found
echo.

REM ============================================================================
REM Step 2: Virtual Environment Setup
REM ============================================================================
echo [2/5] Setting up Virtual Environment...

if "%CLEAN%"=="true" (
    if exist "venv" (
        echo Removing existing virtual environment...
        rmdir /s /q venv
    )
)

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM ============================================================================
REM Activate Virtual Environment
REM ============================================================================
echo Activating virtual environment...

if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
) else (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo.

REM ============================================================================
REM Step 3: Install Dependencies (individually for resilience)
REM ============================================================================
if "%NO_INSTALL%"=="false" (
    echo [3/5] Installing Python dependencies...

    REM Upgrade pip first
    echo Upgrading pip...
    python -m pip install --upgrade pip setuptools wheel >nul 2>&1

    set "FAILED=0"

    echo   -- Required packages --

    REM pygame-ce (community edition with broad platform support)
    python -c "import pygame" >nul 2>&1
    if errorlevel 1 (
        echo   Installing pygame-ce...
        pip install "pygame-ce>=2.0.0" >nul 2>&1
        if errorlevel 1 (
            echo   [FAIL] pygame-ce failed to install
            set /a FAILED+=1
        ) else (
            echo   [OK] pygame-ce installed
        )
    ) else (
        echo   [OK] pygame already available
    )

    REM pygments
    echo   Installing pygments...
    pip install "pygments>=2.15.0" >nul 2>&1
    if errorlevel 1 (
        echo   [FAIL] pygments failed to install
        set /a FAILED+=1
    ) else (
        echo   [OK] pygments installed
    )

    REM Pillow
    echo   Installing Pillow...
    pip install "Pillow>=8.0.0" >nul 2>&1
    if errorlevel 1 (
        echo   [FAIL] Pillow failed to install
        set /a FAILED+=1
    ) else (
        echo   [OK] Pillow installed
    )

    echo   -- Development packages --

    REM pytest
    pip install "pytest>=7.0.0" >nul 2>&1
    if errorlevel 1 (
        echo   [INFO] pytest not installed (optional^)
    ) else (
        echo   [OK] pytest installed
    )

    REM black
    pip install "black>=22.0.0" >nul 2>&1
    if errorlevel 1 (
        echo   [INFO] black not installed (optional^)
    ) else (
        echo   [OK] black installed
    )

    REM flake8
    pip install "flake8>=4.0.0" >nul 2>&1
    if errorlevel 1 (
        echo   [INFO] flake8 not installed (optional^)
    ) else (
        echo   [OK] flake8 installed
    )

    echo.
    if "!FAILED!"=="0" (
        echo [OK] All runtime dependencies installed successfully
    ) else (
        echo [WARN] !FAILED! runtime package(s^) had issues (app may still work^)
    )
) else (
    echo [3/5] Skipping dependency installation (--no-install)
)
echo.

REM ============================================================================
REM Step 4: Verify Installation
REM ============================================================================
echo [4/5] Verifying installation...

python -c "import tkinter; print('  [OK] tkinter available')" 2>nul
if errorlevel 1 (
    echo   [FAIL] tkinter not available!
    echo   Note: tkinter comes with Python. Try reinstalling Python.
)

python -c "import pygame; print('  [OK] pygame available (multimedia support)')" 2>nul
if errorlevel 1 (
    echo   [INFO] pygame not available (optional - some features limited^)
)

python -c "import pygments; print('  [OK] pygments available (syntax highlighting)')" 2>nul
if errorlevel 1 (
    echo   [INFO] pygments not available (syntax highlighting disabled^)
)

python -c "import PIL; print('  [OK] PIL/Pillow available (image processing)')" 2>nul
if errorlevel 1 (
    echo   [INFO] PIL/Pillow not available (image features limited^)
)

echo.

REM ============================================================================
REM Step 5: Launch Time Warp Classic
REM ============================================================================
echo ============================================================================
echo.
echo                  [*] Launching Time Warp Classic...
echo.
echo ============================================================================
echo.

REM Verify Time_Warp.py exists
if not exist "Time_Warp.py" (
    echo ERROR: Time_Warp.py not found!
    pause
    exit /b 1
)

echo [5/5] Starting IDE...

REM Run the IDE
python Time_Warp.py %*

echo.
echo Goodbye from Time Warp Classic!
pause
