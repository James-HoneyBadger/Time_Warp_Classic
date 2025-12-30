#!/usr/bin/env python3
"""
Time Warp Classic - Complete Setup & Run Script (Cross-Platform)

This script:
1. Creates a Python virtual environment (if needed)
2. Installs all required Python dependencies
3. Launches the Time Warp Classic GUI

Usage:
    python3 run.py                 # Normal startup with dependency installation
    python3 run.py --clean         # Delete and recreate virtual environment
    python3 run.py --no-install    # Skip dependency installation
    python3 run.py --help          # Show this help message

Copyright © 2025 Honey Badger Universe
"""

import os
import sys
import subprocess
import argparse
import platform
from pathlib import Path

# Colors for console output
class Colors:
    """ANSI color codes for terminal output"""
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    END = '\033[0m'

    @staticmethod
    def disable_on_windows():
        """Disable colors on Windows if not supported"""
        if platform.system() == 'Windows':
            Colors.BLUE = Colors.GREEN = Colors.YELLOW = Colors.RED = Colors.END = ''


# Disable colors if needed
Colors.disable_on_windows()


def print_header(title):
    """Print a formatted header"""
    print(f"\n{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BLUE}{title:^60}{Colors.END}")
    print(f"{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_step(number, title):
    """Print a step header"""
    print(f"{Colors.YELLOW}[{number}/4]{Colors.END} {title}...")


def print_success(message):
    """Print a success message"""
    print(f"{Colors.GREEN}✓{Colors.END} {message}")


def print_warning(message):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.END}  {message}")


def print_error(message):
    """Print an error message"""
    print(f"{Colors.RED}✗{Colors.END} {message}")


def run_command(cmd, capture_output=False, check=True):
    """Run a shell command"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=capture_output,
            text=True,
            check=False
        )
        if check and result.returncode != 0:
            return False
        return result
    except Exception as e:
        print_error(f"Failed to run command: {e}")
        return False


def check_python():
    """Check Python version"""
    print_step(1, "Checking Python installation")

    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print_success(f"Python {version} found\n")

    if sys.version_info < (3, 9):
        print_error("Python 3.9 or higher is required")
        return False
    return True


def setup_venv(venv_path, clean=False):
    """Setup virtual environment"""
    print_step(2, "Setting up Virtual Environment")

    if clean and venv_path.exists():
        print("🗑️  Removing existing virtual environment...")
        import shutil
        shutil.rmtree(venv_path)

    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        result = run_command(f"{sys.executable} -m venv {venv_path}", check=True)
        if not result:
            print_error("Failed to create virtual environment")
            return False
        print_success("Virtual environment created")
    else:
        print_success("Virtual environment already exists")

    print()
    return True


def get_python_exe(venv_path):
    """Get the Python executable in the venv"""
    if platform.system() == 'Windows':
        return str(venv_path / 'Scripts' / 'python.exe')
    return str(venv_path / 'bin' / 'python')


def install_dependencies(venv_path, no_install=False):
    """Install Python dependencies"""
    if no_install:
        print_step(3, "Skipping dependency installation")
        print("(--no-install flag set)\n")
        return True

    print_step(3, "Installing Python dependencies")

    python_exe = get_python_exe(venv_path)

    # Check if requirements.txt exists
    req_file = Path('requirements.txt')
    if not req_file.exists():
        print_error("requirements.txt not found!")
        return False

    # Upgrade pip
    print("📥 Upgrading pip...")
    run_command(f"{python_exe} -m pip install --upgrade pip setuptools wheel")

    # Install requirements
    print("📚 Installing packages from requirements.txt...")
    result = run_command(f"{python_exe} -m pip install -r {req_file}")

    if result and result.returncode == 0:
        print_success("All dependencies installed successfully")
    else:
        print_warning("Some dependencies may have failed to install")
        print("    (This is often OK - many features work without optional dependencies)")

    print()
    return True


def verify_installation(venv_path):
    """Verify required and optional dependencies"""
    print_step(4, "Verifying installation")

    python_exe = get_python_exe(venv_path)

    # Check tkinter (required)
    result = run_command(f"{python_exe} -c 'import tkinter'", capture_output=True)
    if result.returncode == 0:
        print_success("tkinter available")
    else:
        print_error("tkinter not available!")
        print("  This is required. If missing after installation, try:")
        if platform.system() == 'Linux':
            print("    Ubuntu/Debian: sudo apt-get install python3-tk")
            print("    Fedora: sudo dnf install python3-tkinter")
        elif platform.system() == 'Darwin':
            print("    macOS: brew install python-tk")

    # Check optional packages
    packages = [
        ('pygame', 'pygame available (multimedia support)'),
        ('pygments', 'pygments available (syntax highlighting)'),
        ('PIL', 'PIL/Pillow available (image processing)'),
    ]

    for pkg, msg in packages:
        result = run_command(f"{python_exe} -c 'import {pkg}'", capture_output=True)
        if result.returncode == 0:
            print_success(msg)
        else:
            print_warning(f"{pkg} not available (optional feature)")

    print()
    return True


def launch_gui(venv_path):
    """Launch Time Warp Classic GUI"""
    print_header("🚀 Launching Time Warp Classic...")

    python_exe = get_python_exe(venv_path)

    # Check if Time_Warp.py exists
    if not Path('Time_Warp.py').exists():
        print_error("Time_Warp.py not found!")
        return False

    # Run the IDE
    try:
        subprocess.run([python_exe, 'Time_Warp.py'], check=False)
        return True
    except Exception as e:
        print_error(f"Failed to launch Time Warp: {e}")
        return False


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Time Warp Classic - Setup & Launch Script',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python3 run.py              # Normal startup
  python3 run.py --clean      # Recreate virtual environment
  python3 run.py --no-install # Skip dependency installation
        '''
    )
    parser.add_argument('--clean', action='store_true',
                        help='Delete and recreate the virtual environment')
    parser.add_argument('--no-install', action='store_true',
                        help='Skip dependency installation')

    args = parser.parse_args()

    # Get paths
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    venv_path = script_dir / 'venv'

    # Print header
    print(f"\n{Colors.BLUE}╔{'='*58}╗{Colors.END}")
    print(f"{Colors.BLUE}║ Time Warp Classic - Multi-Language IDE{' '*20}║{Colors.END}")
    print(f"{Colors.BLUE}║ Initialization & Setup Script{' '*28}║{Colors.END}")
    print(f"{Colors.BLUE}╚{'='*58}╝{Colors.END}")

    # Run steps
    if not check_python():
        return 1

    if not setup_venv(venv_path, clean=args.clean):
        return 1

    if not install_dependencies(venv_path, no_install=args.no_install):
        print_warning("Continuing despite installation issues...")

    if not verify_installation(venv_path):
        print_warning("Continuing despite verification issues...")

    # Launch GUI
    if not launch_gui(venv_path):
        return 1

    print(f"\n{Colors.BLUE}Goodbye from Time Warp Classic!{Colors.END}\n")
    return 0


if __name__ == '__main__':
    sys.exit(main())
