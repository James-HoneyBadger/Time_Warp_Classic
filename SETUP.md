# Time Warp Classic - Setup & Launch Guide

## Quick Start

### Option 1: Python Script (Cross-Platform Recommended)
The easiest way to set up and launch Time Warp Classic on any operating system:

```bash
python3 run.py
```

This will:
1. Create a Python virtual environment (if needed) and bootstrap `pip` inside it
2. Offer to install a missing system package (for example `tkinter`), then
   install the Python dependencies
3. Verify the installation
4. Launch the GUI

### Option 2: Bash Script (Linux/macOS)
```bash
./run.sh
```

### Option 3: Batch Script (Windows)
```cmd
run.bat
```

---

## Prerequisites

- **Python 3.9 or higher** (required)
- **tkinter** (usually included with Python)
- Internet connection (for initial dependency installation)

### Checking Your Python Version

```bash
python3 --version
```

If you have Python 3.8 or lower, you'll need to upgrade. Visit [python.org](https://www.python.org) to download Python 3.9+.

---

## Installation Methods

### Method 1: Python Script (Recommended)

The `run.py` script is the most portable and user-friendly option:

```bash
# Standard startup (creates venv, installs dependencies, launches GUI)
python3 run.py

# Recreate the virtual environment from scratch
python3 run.py --clean

# Skip dependency installation (for faster startup on subsequent runs)
python3 run.py --no-install

# Show help information
python3 run.py --help
```

**Advantages:**
- Works on Windows, macOS, and Linux
- Automatic Python 3.9+ checking
- Clear colored output with progress indicators
- Bootstraps `pip` when a virtual environment was created without it
- Offers to install the OS `tkinter` package when it is missing (`apt-get`,
  `dnf`, `yum`, `zypper`, `pacman`, `apk`, or Homebrew) — it always asks
  first, and prompts for `sudo` credentials only when required
- Warns early when no graphical display is available
- Handles both tkinter checks and optional dependencies
- Self-contained - no external shell required

**What it does:**
1. Verifies Python 3.9+ is installed
2. Creates `venv/` directory with isolated Python environment
3. Bootstraps `pip` inside the venv if it is missing
4. Offers to install the system `tkinter` package when the interpreter lacks it
5. Upgrades pip, setuptools, and wheel
6. Installs all dependencies from `requirements.txt`
7. Verifies tkinter (required) and optional packages
8. Launches `Time_Warp.py`

### Method 2: Bash Script (Linux/macOS)

The `run.sh` script is optimized for Unix-like systems:

```bash
# Standard startup
./run.sh

# Recreate virtual environment
./run.sh --clean

# Skip installation
./run.sh --no-install
```

**Advantages:**
- Pure shell script, no Python bootstrapping needed
- Integrated with Unix development tools
- Minimal resource usage

### Method 3: Batch Script (Windows)

The `run.bat` script is native Windows batch:

```cmd
REM Standard startup
run.bat

REM Recreate virtual environment
run.bat --clean

REM Skip installation
run.bat --no-install
```

**Advantages:**
- Native Windows batch file
- No WSL or external tools required
- Works with Windows Command Prompt and PowerShell

### Method 4: Manual Setup

If you prefer manual control:

```bash
# Create and activate virtual environment
python3 -m venv venv

# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Launch the application
python3 Time_Warp.py
```

---

## Troubleshooting

### Python Not Found

**Error:** `python3: command not found` or `'python' is not recognized`

**Solution:** 
- Ensure Python 3.9+ is installed and in your PATH
- Try using `python` instead of `python3` on Windows
- On Windows, add Python to PATH during installation

### tkinter Not Available

**Error:** `No module named '_tkinter'`

**Solution:**

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-tkinter
```

**macOS:**
```bash
brew install python-tk
```

**Windows:**
Tkinter is included with Python. If missing, reinstall Python and ensure "tcl/tk and IDLE" is selected.

### Virtual Environment Issues

**Error:** `venv activation failed` or permission errors

**Solution:**
```bash
# Remove the corrupted venv
rm -rf venv/

# Or on Windows:
rmdir /s venv

# Then create a fresh one
python3 run.py --clean
```

### Dependency Installation Fails

Some dependencies may fail to install if development headers are missing:

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-dev python3-pip
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-devel python3-pip
```

**macOS:**
```bash
xcode-select --install
```

After installing system dependencies, run:
```bash
python3 run.py --clean
```

### GUI Doesn't Start

**Check the console output** - the launch scripts provide detailed error messages.

Common issues:
1. **Missing tkinter** - See "tkinter Not Available" above
2. **Port conflicts** - Ensure no other application is using the GUI port
3. **Display issues on headless systems** - Set display:
   ```bash
   export DISPLAY=:0
   python3 run.py
   ```

---

## Virtual Environment Management

The scripts automatically create and manage a `venv/` directory in the Time Warp Classic folder.

### Deleting the Virtual Environment

```bash
# Using the script
python3 run.py --clean

# Or manually
rm -rf venv/
```

### Using the Virtual Environment Outside the Scripts

Activate the virtual environment:

```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Once activated, run Python code with installed dependencies:

```bash
python3 Time_Warp.py
```

Deactivate when done:

```bash
deactivate
```

---

## Dependencies

Time Warp Classic requires:

**Required:**
- `tkinter` - GUI framework (usually bundled with Python)

**Recommended:**
- `pygame-ce>=2.0.0` - Multimedia and graphics (community edition; or `pygame`)
- `pygments>=2.10.0` - Syntax highlighting
- `Pillow>=8.0.0` - Image processing

**Development (optional):**
- `pytest>=7.0` - Unit testing
- `black>=22.0` - Code formatting
- `flake8>=4.0` - Code linting

---

## Supported Languages

Time Warp Classic includes interpreters for:

1. **PILOT** - Computer-Aided Instruction language
2. **BASIC** - Beginner's All-Purpose Symbolic Instruction Code
3. **Logo** - Turtle graphics and education language
4. **Pascal** - Structured programming language
5. **Prolog** - Logic programming language
6. **Forth** - Stack-based language
7. **Perl** - Text processing language
8. **Python** - Python subset execution
9. **JavaScript** - JavaScript ES5 execution

---

## Features

### Editor
- **Multi-language support** - Switch languages with dropdown
- **Syntax highlighting** - Color-coded tokens (when pygments available)
- **Line numbers** - Easy code navigation
- **Find & Replace** - Search and modify code
- **Auto-indentation** - Intelligent formatting

### Execution
- **Run code** - Execute in selected language
- **Input entry** - Provide input to running programs
- **Output panel** - View program output
- **Debug mode** - Step through code execution

### Graphics
- **Turtle graphics canvas** - Visualize Logo programs
- **Graphics output** - See draw commands rendered

### Themes
- **9 color schemes** - Light, dark, and high-contrast themes
- **Font customization** - 7 font sizes for comfortable coding

### Tools
- **Code examples** - Learn from built-in examples
- **Performance monitor** - Check execution metrics
- **Test runner** - Execute unit tests
- **Settings persistence** - Save preferences

---

## File Structure

```
Time_Warp_Classic/
├── Time_Warp.py              # Entry point (launches GUI)
├── run.py                    # Python launcher (cross-platform)
├── run.sh                    # Bash launcher (Linux/macOS)
├── run.bat                   # Batch launcher (Windows)
├── requirements.txt          # Python dependencies
├── venv/                     # Virtual environment (created by scripts)
├── gui/                      # GUI package
│   ├── __init__.py
│   ├── app.py                # Main TimeWarpApp class
│   ├── menus.py              # Menu bar construction
│   ├── dialogs.py            # Find/Replace dialogs
│   └── themes.py             # Themes, languages, config
├── core/                     # Core interpreter code
│   ├── interpreter.py        # Multi-language interpreter
│   ├── stubs.py              # Placeholder classes for optional modules
│   └── languages/            # Language executors
│       ├── base.py           # SubprocessExecutor base class
│       ├── basic.py
│       ├── forth.py
│       ├── javascript_executor.py
│       ├── logo.py
│       ├── pascal.py
│       ├── perl.py
│       ├── pilot.py
│       ├── prolog.py
│       └── python_executor.py
├── docs/                     # Documentation
├── examples/                 # Code examples for each language
└── scripts/                  # Helper scripts
```

---

## Running from IDE/Editor

### VS Code
1. Create a terminal in VS Code (Ctrl+`)
2. Run: `python3 run.py`

### PyCharm
1. Open terminal in PyCharm
2. Run: `python3 run.py`

### Command Line
```bash
cd /path/to/Time_Warp_Classic
python3 run.py
```

---

## Advanced Usage

### Creating a Desktop Shortcut (Linux)

Create `~/.local/share/applications/Time_Warp.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=Time Warp Classic
Comment=Multi-language retro IDE
Exec=/home/username/Time_Warp_Classic/run.py
Icon=python
Terminal=false
Categories=Development;IDE;Education;
```

Then:
```bash
chmod +x ~/.local/share/applications/Time_Warp.desktop
```

### Environment Variables

Set custom settings via environment variables:

```bash
# Set default theme
export TIME_WARP_THEME=dark

# Set font size (1-7)
export TIME_WARP_FONT_SIZE=4

# Enable verbose output
export TIME_WARP_VERBOSE=1

python3 run.py
```

### Development Mode

For contributors working on Time Warp Classic:

```bash
# Activate the venv
source venv/bin/activate  # or on Windows: venv\Scripts\activate

# Install in editable mode
pip install -e .

# Run tests
pytest

# Run tests with a coverage report (needs the "test" extra: pip install -e .[test])
pytest --cov

# Check code quality
black . --check
flake8 .

# Run the IDE
python3 Time_Warp.py
```

---

## Getting Help

### Built-in Help
- Use the **Help** menu in the Time Warp Classic GUI
- Check code **examples/** directory for sample programs

### Online Resources
- Documentation: See `docs/` directory
- Issues: Report problems on the project page
- Examples: Browse `examples/` for language samples

---

## License

Time Warp Classic - Multi-language IDE  
Copyright © 2025–2026 Honey Badger Universe

See `License.md` for full license information.

---

## Quick Reference

| Task | Command |
|------|---------|
| Start normally | `python3 run.py` |
| Recreate venv | `python3 run.py --clean` |
| Skip install | `python3 run.py --no-install` |
| Manual venv activate (Linux/macOS) | `source venv/bin/activate` |
| Manual venv activate (Windows) | `venv\Scripts\activate` |
| Manual venv deactivate | `deactivate` |
| Run tests | `python3 -m pytest tests/` |
| Run tests with coverage | `python3 -m pytest --cov tests/` |
| Format code | `black .` |
| Check code | `flake8 .` |

---

**Enjoy coding in Time Warp Classic!** 🚀
