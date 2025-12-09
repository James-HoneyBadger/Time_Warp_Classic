# Development Scripts

This directory contains development utilities and setup scripts for Time_Warp IDE.

## 📝 Scripts

### Core CLI
- `timewarp-cli.py` - **Main CLI interface** for Time_Warp IDE

### Development Tools
- `install_dependencies.py` - Automatic dependency installer
- `integration_tests.py` - Full integration test suite
- `run_tests.py` - Standard test runner
- `run_tests_production.py` - Production-ready test runner
- `setup_dev.sh` - Development environment setup

### Launch Scripts
- `launch.py` - Python launcher for Time_Warp GUI
- `launch_Time_Warp.sh` - Shell launcher for Time_Warp GUI
- `start.sh` - Quick start script

## 🚀 Time_Warp CLI Usage

The Time_Warp CLI allows you to run programs from the command line without the GUI:

```bash
# Run a program
python scripts/timewarp-cli.py run examples/basic/hello_world.bas
./timewarp run examples/basic/hello_world.bas

# List available examples
python scripts/timewarp-cli.py list
./timewarp list

# Get language information
python scripts/timewarp-cli.py info basic
./timewarp info python

# Show help
python scripts/timewarp-cli.py help
./timewarp help
```

## 🛠️ Development Workflow

1. **Initial Setup**: Run `setup_dev.sh`
2. **Install Dependencies**: Run `install_dependencies.py`
3. **Development**: Make changes to code
4. **Testing**: Run `run_tests.py` for quick tests or use CLI to test programs
5. **Integration**: Run `integration_tests.py` for full testing
6. **Production**: Run `run_tests_production.py` before releases