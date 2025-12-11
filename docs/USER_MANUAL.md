# Time_Warp Classic - User Manual

**Version 1.3.0**

Welcome to the complete user manual for Time_Warp Classic IDE. This guide will help you master all features of the IDE and learn to program in 9 different languages.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [IDE Interface](#ide-interface)
4. [Working with Files](#working-with-files)
5. [Writing and Running Programs](#writing-and-running-programs)
6. [Using Turtle Graphics](#using-turtle-graphics)
7. [Customizing the IDE](#customizing-the-ide)
8. [Keyboard Shortcuts](#keyboard-shortcuts)
9. [Troubleshooting](#troubleshooting)

---

## Introduction

### What is Time_Warp Classic?

Time_Warp Classic is an educational multi-language programming environment that allows you to write, run, and debug programs in 9 different programming languages:

**Vintage Languages:**
- **PILOT** (1968) - Computer-Assisted Instruction
- **BASIC** (1964) - Classic Beginner's Programming
- **Logo** (1967) - Turtle Graphics Programming
- **Pascal** (1970) - Structured Programming
- **Prolog** (1972) - Logic Programming
- **Forth** (1970) - Stack-Based Programming

**Modern Languages:**
- **Perl** (1987) - Text Processing
- **Python** (1991) - General Purpose
- **JavaScript** (1995) - Web Scripting

### Who Should Use This?

- **Students** learning programming fundamentals
- **Teachers** demonstrating multiple programming paradigms
- **Hobbyists** exploring retro computing
- **Developers** comparing language features
- **Anyone** interested in the history of computing

---

## Getting Started

### Installation

1. **Install Python** (3.9 or higher)
   - Download from [python.org](https://www.python.org/)
   - Ensure "Add Python to PATH" is checked during installation

2. **Clone or Download Time_Warp Classic**
   ```bash
   git clone https://github.com/James-HoneyBadger/Time_Warp_Classic.git
   cd Time_Warp_Classic
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the IDE**
   ```bash
   python Time_Warp.py
   ```

### First Launch

When you first launch Time_Warp Classic:

1. The IDE automatically checks for required dependencies
2. Missing packages are installed automatically
3. The main IDE window opens with a welcome message
4. You're ready to start programming!

---

## IDE Interface

### Main Window Layout

The IDE is organized into four main areas:

```
┌─────────────────────────────────────────────────────────────┐
│ Menu Bar: File | Edit | Program | View | Preferences | Help │
├──────────────────┬──────────────────────────────────────────┤
│                  │                                          │
│   Code Editor    │         Output Panel                     │
│   (Left Panel)   │         (Top Right)                      │
│                  │                                          │
│  ┌─────────────┐ │ Program output appears here             │
│  │ Language:   │ │                                          │
│  │ [PILOT  ▼] │ │                                          │
│  └─────────────┘ │                                          │
│                  ├──────────────────────────────────────────┤
│                  │                                          │
│                  │    Turtle Graphics Canvas                │
│                  │    (Bottom Right)                        │
│                  │                                          │
│                  │    Visual graphics appear here           │
│                  │                                          │
├──────────────────┴──────────────────────────────────────────┤
│ Input: [________________________] [Submit]                  │
├─────────────────────────────────────────────────────────────┤
│ [▶ Run] [📂 Open] [💾 Save] [Clear Editor] [Clear Output]  │
└─────────────────────────────────────────────────────────────┘
```

### Menu Bar

#### File Menu
- **New File** (Ctrl+N) - Create a new program
- **Open File...** (Ctrl+O) - Load an existing file
- **Save File...** (Ctrl+S) - Save your program
- **Exit** (Ctrl+Q) - Close the IDE

#### Edit Menu
- **Undo** (Ctrl+Z) - Undo last change
- **Redo** (Ctrl+Y) - Redo undone change
- **Cut** (Ctrl+X) - Cut selected text
- **Copy** (Ctrl+C) - Copy selected text
- **Paste** (Ctrl+V) - Paste from clipboard
- **Select All** (Ctrl+A) - Select all text

#### Program Menu
- **Run Program** (F5) - Execute your code
- **Load Example** - Load example programs
  - PILOT, BASIC, Logo, Pascal, Prolog, Forth, Perl, Python, JavaScript

#### View Menu
- **Output Panel** - Toggle output visibility
- **Graphics Panel** - Toggle graphics visibility
- **Clear Canvas** - Clear turtle graphics
- **Clear Output** - Clear output text
- **Clear Editor** - Clear editor text

#### Preferences Menu
- **Color Theme** - Choose visual theme
  - Light Theme - Bright background
  - Dark Theme - Dark background (default)
  - Classic Theme - Retro look
- **Font Size** - Adjust text size
  - Small (9pt)
  - Medium (11pt) - default
  - Large (14pt)
  - Extra Large (16pt)

#### Help Menu
- **Getting Started** (F1) - Show help guide
- **About Time_Warp IDE** - Version and credits

---

## Working with Files

### Creating a New File

1. Click **File → New File** or press **Ctrl+N**
2. Confirm clearing the editor if prompted
3. Select your programming language from the dropdown
4. Start typing your code

### Opening an Existing File

1. Click **File → Open File...** or press **Ctrl+O**
2. Navigate to your file location
3. Select the file and click **Open**
4. The language is auto-detected from the file extension

### Saving Your Work

1. Click **File → Save File...** or press **Ctrl+S**
2. Choose a location and filename
3. Select the appropriate file extension:
   - `.pilot` for PILOT programs
   - `.bas` for BASIC programs
   - `.logo` for Logo programs
   - `.pas` for Pascal programs
   - `.pl` for Prolog programs
   - `.fth` or `.4th` for Forth programs
   - `.pl` for Perl scripts
   - `.py` for Python scripts
   - `.js` for JavaScript programs

### Loading Example Programs

1. Click **Program → Load Example**
2. Choose a language submenu
3. Select an example program
4. The example loads into the editor
5. Click **Run** to execute it

---

## Writing and Running Programs

### Basic Workflow

1. **Select Language** - Use the dropdown to choose your language
2. **Write Code** - Type your program in the left editor panel
3. **Run Program** - Press **F5** or click the **▶ Run** button
4. **View Output** - Results appear in the output panel
5. **See Graphics** - Visual output appears in the graphics canvas

### Language-Specific Notes

#### PILOT Programs
```pilot
T:Hello, World!
A:What is your name?
T:Nice to meet you, *NAME*!
```
- Use `T:` for text output
- Use `A:` for user input
- Use `*VARIABLE*` for variable substitution

#### BASIC Programs
```basic
10 PRINT "Hello, World!"
20 INPUT "Enter your name: ", NAME$
30 PRINT "Hello, "; NAME$
40 END
```
- All lines must have line numbers
- Use `PRINT` for output
- Use `INPUT` for user input
- End with `END` statement

#### Logo Programs
```logo
REPEAT 4 [
  FORWARD 100
  RIGHT 90
]
```
- Commands control turtle graphics
- Use `REPEAT` for loops
- Brackets `[ ]` group commands

### Handling User Input

When a program requests input:

1. The program pauses execution
2. Enter your input in the bottom input field
3. Press **Enter** or click **Submit**
4. Your input appears in the output as `>> YourInput`
5. The program continues with your input

**Example:**
```basic
10 INPUT "Enter a number: ", X
20 PRINT "You entered: "; X
```

When this runs:
1. "Enter a number:" appears in output
2. Type your number in the input field
3. Press Enter
4. Your number is displayed

---

## Using Turtle Graphics

### What is Turtle Graphics?

Turtle graphics is a visual programming system where you control a "turtle" that draws on the screen. The turtle has:
- A **position** (X, Y coordinates)
- A **heading** (direction it's facing)
- A **pen** (up or down for drawing)

### Turtle Commands

Available in **Logo** and **BASIC**:

#### Movement
- `FORWARD 100` - Move forward 100 units
- `BACK 50` - Move backward 50 units
- `LEFT 90` - Turn left 90 degrees
- `RIGHT 90` - Turn right 90 degrees

#### Pen Control
- `PENDOWN` or `PD` - Lower pen to draw
- `PENUP` or `PU` - Lift pen (move without drawing)

#### Position
- `HOME` - Return to center (0, 0)
- `SETXY 100 50` - Move to specific coordinates
- `SETHEADING 90` - Face specific direction (0° = North)

#### Appearance
- `SHOWTURTLE` or `ST` - Make turtle visible
- `HIDETURTLE` or `HT` - Hide turtle
- `SETPENCOLOR [255 0 0]` - Set pen color (RGB)

#### Screen
- `CLEARSCREEN` or `CS` - Clear canvas and reset turtle

### Coordinate System

```
        (0, 200) North (0°)
             │
             │
(-200, 0) ───┼─── (200, 0) East (90°)
             │
             │
        (0, -200) South (180°)
```

- Center is (0, 0)
- 0° points North (up)
- Angles increase clockwise
- Right is 90°, Down is 180°, Left is 270°

### Example: Drawing a Square

**Logo:**
```logo
REPEAT 4 [
  FORWARD 100
  RIGHT 90
]
```

**BASIC:**
```basic
10 PENDOWN
20 FOR I = 1 TO 4
30   FORWARD 100
40   RIGHT 90
50 NEXT I
60 PENUP
```

### Example: Colorful Spiral

```logo
REPEAT 36 [
  FORWARD :COUNT * 3
  RIGHT 10
  SETPENCOLOR [255 :COUNT * 7 100]
  MAKE "COUNT :COUNT + 1
]
```

---

## Customizing the IDE

### Changing Themes

**Preferences → Color Theme**

- **Light Theme** - White background, black text (good for bright rooms)
- **Dark Theme** - Dark background, light text (default, easy on eyes)
- **Classic Theme** - Gray background, retro computing feel

### Adjusting Font Size

**Preferences → Font Size**

- **Small (9pt)** - More code visible, harder to read
- **Medium (11pt)** - Default, balanced readability
- **Large (14pt)** - Easier to read, less code visible
- **Extra Large (16pt)** - Maximum readability, presentations

### Toggling Panels

**View Menu**

- **Output Panel** - Show/hide the output text panel
- **Graphics Panel** - Show/hide the turtle graphics canvas

Use these to maximize space for what you're working on.

### Clearing Displays

- **Clear Canvas** - Erase all graphics (turtle remains)
- **Clear Output** - Remove all output text
- **Clear Editor** - Delete all code in editor (confirms first)

---

## Keyboard Shortcuts

### Essential Shortcuts

| Action | Shortcut |
|--------|----------|
| Run Program | **F5** |
| Show Help | **F1** |
| New File | **Ctrl+N** |
| Open File | **Ctrl+O** |
| Save File | **Ctrl+S** |
| Exit IDE | **Ctrl+Q** |

### Editing Shortcuts

| Action | Shortcut |
|--------|----------|
| Undo | **Ctrl+Z** |
| Redo | **Ctrl+Y** |
| Cut | **Ctrl+X** |
| Copy | **Ctrl+C** |
| Paste | **Ctrl+V** |
| Select All | **Ctrl+A** |

### Pro Tips

1. **Press F5 frequently** - Test your code as you write it
2. **Use Ctrl+Z liberally** - Undo is your friend
3. **Ctrl+S often** - Save your work regularly
4. **F1 for help** - Quick access to documentation

---

## Troubleshooting

### Common Issues

#### "Python not found"
- **Solution:** Install Python 3.9+ from python.org
- Ensure "Add to PATH" was checked during installation

#### "Module not found" errors
- **Solution:** Run `pip install -r requirements.txt`
- Or let the IDE auto-install dependencies on first launch

#### Code doesn't run
- **Check:** Is the correct language selected?
- **Check:** Are there syntax errors?
- **Check:** Does output show error messages?

#### Turtle graphics don't appear
- **Check:** Is Graphics Panel visible? (View → Graphics Panel)
- **Check:** Is pen down? Use `PENDOWN` or `PD`
- **Check:** Did you use movement commands? (`FORWARD`, etc.)

#### Input doesn't work
- **Solution:** Type input in the bottom field, not in a popup
- Press **Enter** or click **Submit** after typing

### Getting Help

1. **Press F1** - Built-in help guide
2. **Check docs/** - Comprehensive documentation
3. **Load examples** - See working code
4. **Read error messages** - They explain what went wrong

### Reporting Bugs

Found a bug? Please report it on GitHub Issues with:
- Your operating system
- Python version
- Steps to reproduce
- Error messages (if any)
- Code that causes the issue

---

## Tips for Success

### For Beginners

1. **Start with PILOT or BASIC** - Simplest languages
2. **Load example programs** - Learn by studying working code
3. **Experiment** - Change values and see what happens
4. **Read error messages** - They tell you what to fix
5. **Save often** - Protect your work

### For Teachers

1. **Use the projector-friendly Large font**
2. **Demonstrate with example programs**
3. **Have students compare languages**
4. **Use turtle graphics for visual feedback**
5. **Create custom examples for your lessons**

### For Programmers

1. **Compare implementations** - Same algorithm in different languages
2. **Study the interpreters** - See how languages work internally
3. **Try unusual paradigms** - Forth, Prolog, Logo
4. **Contribute** - Add features or languages
5. **Share your programs** - Help others learn

---

## Next Steps

Now that you know the IDE, explore:

1. **[Language Reference](LANGUAGE_REFERENCE.md)** - Syntax for all 9 languages
2. **[Example Programs](../examples/README.md)** - Working code to study
3. **[Technical Manual](TECHNICAL_MANUAL.md)** - How the IDE works internally
4. **[Developer Guide](DEVELOPER_GUIDE.md)** - Extend and customize

---

**Happy Programming Through the Ages!** 🕰️

© 2025 Honey Badger Universe | Educational Software
