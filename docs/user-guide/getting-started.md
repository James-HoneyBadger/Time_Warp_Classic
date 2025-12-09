# 🚀 Getting Started with Time_Warp

Welcome to Time_Warp! This guide will help you get up and running with this educational programming environment.

## 📋 Prerequisites

- **Python 3.9 or higher** - Required for running Time_Warp
- **Git** - For cloning the repository (optional)
- **Operating System** - Windows, macOS, or Linux

## 🛠️ Installation

### Option 1: Clone from GitHub (Recommended)

```bash
# Clone the repository
git clone https://github.com/James-HoneyBadger/Time_Warp_Classic.git
cd Time_Warp_Classic

# Install dependencies
pip install -r requirements.txt
```

### Option 2: Direct Download

1. Download the latest release from GitHub
2. Extract the archive
3. Install dependencies: `pip install -r requirements.txt`

### Option 3: Development Setup

For contributors or advanced users:

```bash
# Run the automated setup script
./scripts/setup_dev.sh

# Or manual setup
pip install -r requirements.txt
pip install -r tests/test_requirements.txt
```

## 🎯 Quick Start

### Run Time_Warp

```bash
# Run Time_Warp (CLI interface)
python Time_Warp.py
```

The Time_Warp CLI will start with:
- **Code Editor** (left panel) - Write your programs here
- **Output Panel** (right panel) - See execution results
- **Menu Bar** - Access file operations and help

### Your First Program

1. **Type this in the editor:**
   ```
   T:Hello, Time_Warp!
   ```

2. **Click "▶ Run Program"** or press **F5**

3. **See the result** in the output panel: "Hello, Time_Warp!"

### Try Different Languages

**PILOT (Beginner-friendly):**
```
T:Welcome to PILOT!
A:What is your name?
T:Hello *NAME*, nice to meet you!
```

**BASIC (Classic style):**
```
10 PRINT "Hello from BASIC!"
20 LET X = 42
30 PRINT "The answer is: "; X
```

**Logo (Turtle graphics):**
```
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
```

## 💻 Command Line Usage

Time_Warp also works from the command line:

```bash
# Run a program file
python Time_Warp.py --cli examples/pilot/hello.pilot

# Check dependencies only
python Time_Warp.py --check

# List all example programs
python scripts/timewarp-cli.py list

# Get information about a language
python scripts/timewarp-cli.py info pilot
```

## 🗂️ Project Structure

After installation, your project should look like this:

```
Time_Warp_Classic/
├── Time_Warp.py          # Unified entry point with dependency checking
├── core/                 # Interpreter system
├── examples/             # Sample programs
├── scripts/              # Development tools
├── docs/                 # Documentation
└── requirements.txt      # Dependencies
```

## 📚 Next Steps

- **Explore Examples**: Check the `examples/` directory for sample programs
- **Learn Languages**: See the [language guides](languages/) for syntax help
- **Try CLI**: Use the [command-line interface](cli.md) for batch processing
- **View Demos**: See [examples & demos](examples.md) for turtle graphics

## 🆘 Troubleshooting

### Common Issues

**"Module not found" errors:**
```bash
# Make sure dependencies are installed
pip install -r requirements.txt
```

**Time_Warp doesn't start:**
- Ensure you have Python 3.9+
- Try running: `python3 Time_Warp.py`

**Turtle graphics not working:**
- Some systems need additional graphics libraries
- The interpreter will work in "headless" mode

### Getting Help

- Check the [CLI documentation](cli.md) for command-line options
- Review [examples](examples.md) for working code samples
- See the [contributing guide](../developer-guide/contributing.md) for development help

## 🎉 You're Ready!

Time_Warp is now installed and ready to use. Start exploring different programming languages and enjoy the journey of learning to code!

*Happy coding! 🐢✨*