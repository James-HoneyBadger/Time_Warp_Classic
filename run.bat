@echo off
REM ============================================================================
REM Time Warp Classic - Complete Setup & Run Script (Windows)
REM 
REM This script:
REM 1. Creates a Python virtual environment (if needed)
REM 2. Installs all required Python dependencies
REM 3. Launches the Time Warp Classic GUI
REM
REM Usage: run.bat [--clean] [--no-install]
REM   --clean      Delete and recreate the virtual environment
REM   --no-install Skip dependency installation
REM
REM Copyright © 2025 Honey Badger Universe
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
echo [1/4] Checking Python installation...
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
echo [2/4] Setting up Virtual Environment...

if "%CLEAN%"=="true" (
    if exist "venv" (
        echo Removing existing virtual environment...
        rmdir /s /q venv
    )
)

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM ============================================================================
REM Step 3: Activate Virtual Environment
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
REM Step 4: Install Dependencies
REM ============================================================================
if "%NO_INSTALL%"=="false" (
    echo [3/4] Installing Python dependencies...
    
    REM Upgrade pip first
    echo Upgrading pip...
    python -m pip install --upgrade pip setuptools wheel >nul 2>&1
    
    REM Check if requirements.txt exists
    if exist "requirements.txt" (
        echo Installing packages from requirements.txt...
        pip install -r requirements.txt
        if errorlevel 0 (
            echo [OK] Dependencies installed
        ) else (
            echo [WARN] Some dependencies may have failed
            echo        (This is often OK - many features work without optional dependencies)
        )
    ) else (
        echo ERROR: requirements.txt not found!
        pause
        exit /b 1
    )
) else (
    echo [3/4] Skipping dependency installation (--no-install)
)
echo.

REM ============================================================================
REM Step 5: Verify Installation
REM ============================================================================
echo [4/4] Verifying installation...

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
REM Step 6: Launch Time Warp Classic
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

REM Run the IDE
python Time_Warp.py %*

echo.
echo Goodbye from Time Warp Classic!
pause
