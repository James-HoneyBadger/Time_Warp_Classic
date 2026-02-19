# Quick Start Guide - 5 Minute Setup

Get Time Warp Classic running and write your first program in 5 minutes!

## ⚡ Super Quick Start (90 Seconds)

### Step 1: Install (30 seconds)
```bash
cd /path/to/Time_Warp_Classic
python3 run.py
```
That's it! The script handles everything automatically.

### Step 2: Write Code (30 seconds)
```
1. Copy this code into the editor:

PRINT "Hello, Time Warp!"
PRINT "2 + 3 ="; 2 + 3
END

2. Select "BASIC" from the language dropdown
```

### Step 3: Run (30 seconds)
```
Click the "Run" button
→ See output appear!
```

## 📋 Full Quick Start

### Prerequisites
- Python 3.9 or higher
- About 2 minutes
- Internet connection (first run only)

### Installation

**Option 1: Python Launcher (Recommended)**
```bash
python3 run.py
```

**Option 2: Bash Script (Linux/macOS)**
```bash
./run.sh
```

**Option 3: Batch Script (Windows)**
```cmd
run.bat
```

All scripts will:
1. Create a virtual environment
2. Install dependencies
3. Verify installation
4. Launch the IDE

### First Program - Hello World in BASIC

```basic
PRINT "Welcome to Time Warp Classic!"
PRINT "Today is:"; DATE$
PRINT "Let's do math: 5 + 3 ="; 5 + 3
END
```

**Steps:**
1. Select **BASIC** from dropdown
2. Paste code into editor
3. Click **Run** button
4. See output in Output panel

### First Program - Hello World in Python

```python
print("Welcome to Time Warp Classic!")
print(f"10 + 20 = {10 + 20}")

for i in range(1, 4):
    print(f"Loop iteration {i}")

print("Done!")
```

**Steps:**
1. Select **Python** from dropdown
2. Paste code into editor
3. Click **Run** button
4. See output

### First Program - Graphics in Logo

```logo
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
RIGHT 90
FORWARD 100
```

**Steps:**
1. Select **Logo** from dropdown
2. Paste code
3. Click **Run**
4. See square drawn on canvas!

## 🎯 Next Steps

### Learn More Languages
- Check [LANGUAGE_TUTORIALS.md](user/LANGUAGE_TUTORIALS.md)
- Run examples in [../examples/](../examples/) directory
- Try each language: BASIC, Python, JavaScript, Pascal, Prolog, Forth, Perl, Logo, PILOT

### Master the IDE
- Read the [README](README.md) documentation index
- Explore [Language References](languages/) for each language
- Customize themes via the Preferences menu

### Run Examples
```bash
# Open any comprehensive demo
# Examples are in examples/[language]/comprehensive_demo.*

# E.g., for Python:
# Open examples/python/comprehensive_demo.py
```

### Troubleshooting
If something doesn't work:
1. See [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
2. Check [FAQ.md](FAQ.md)
3. Review full [SETUP.md](../SETUP.md)

## 🚀 IDE Overview

### Main Components

**Editor (Left Panel)**
- Write code here
- Syntax highlighting (via Pygments when available)
- Line numbers
- Find & Replace (Ctrl+F / Ctrl+H)

**Output (Top Right)**
- See program results
- Error messages
- Debug information

**Canvas (Bottom Right)**
- Turtle graphics display
- Visual output for Logo programs (also used by BASIC graphics)

**Bottom Bar**
- Input field for interactive programs
- Buttons: Run, Open, Save, Clear Editor, Clear Output, Clear Graphics

**Menu Bar**
- File, Edit, Program, Debug, Test, Performance, Preferences, About

### Your First Real Program

Let's calculate factorial in Python:

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

for i in range(1, 6):
    result = factorial(i)
    print(f"{i}! = {result}")
```

**Try it:**
1. Select Python
2. Paste code
3. Click Run
4. See results!

## 💡 Pro Tips

### Tip 1: Copy Examples
All comprehensive demo files are in `examples/[language]/`
```
examples/basic/comprehensive_demo.bas
examples/python/comprehensive_demo.py
examples/logo/comprehensive_demo.logo
... etc
```

### Tip 2: Use Keyboard Shortcuts
- Ctrl+Enter: Run program
- Ctrl+F: Find
- Ctrl+H: Find & Replace
- Ctrl+S: Save file

### Tip 3: Check Output Carefully
The output explains what each command does!

### Tip 4: Modify & Experiment
Don't just read examples - modify them!
Change numbers, add loops, try new things.

## ❓ Common First Questions

**Q: Which language should I start with?**
A: BASIC or Python - most familiar syntax

**Q: Where are the examples?**
A: In `examples/[language]/comprehensive_demo.*`

**Q: How do I save my code?**
A: File menu → Save, or Ctrl+S

**Q: Can I load from a file?**
A: Yes! File menu → Open File

**Q: Why no output?**
A: Check you're using PRINT/print/output commands

**Q: Can I use multiple languages?**
A: Yes! Just change language dropdown and paste new code

## 📞 Need More Help?

- **Full user guide:** [README.md](README.md)
- **Language tutorials:** [LANGUAGE_TUTORIALS.md](user/LANGUAGE_TUTORIALS.md)
- **Troubleshooting:** [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
- **FAQ:** [FAQ.md](FAQ.md)
- **Full documentation:** [INDEX.md](INDEX.md)

## 🎓 Learning Path

**5 minutes (now)**
→ You're reading this!

**15 minutes (next)**
→ Run your first program
→ Try another language
→ Modify an example

**30 minutes**
→ Read [README.md](README.md)
→ Learn IDE features
→ Customize your workspace

**1 hour**
→ Follow [LANGUAGE_TUTORIALS.md](user/LANGUAGE_TUTORIALS.md)
→ Write a small program
→ Combine language features

**Ongoing**
→ Explore all 9 languages
→ Build larger projects
→ Master advanced features

---

**You're ready! 🚀**

[Next: Try your first program →](#super-quick-start-90-seconds)

Or jump to:
- [Full Documentation Index](README.md)
- [Language Tutorials](user/LANGUAGE_TUTORIALS.md)
- [All Documentation](INDEX.md)
