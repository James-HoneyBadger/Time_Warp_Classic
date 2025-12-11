# Time_Warp Classic - Quick Start Guide

**Get up and running in 5 minutes!**

---

## 1. Install Python (if needed)

**Windows/Mac:**
- Download from [python.org](https://www.python.org/downloads/)
- Run installer (check "Add to PATH")
- Verify: Open terminal, type `python --version`

**Linux:**
```bash
sudo apt install python3 python3-pip  # Debian/Ubuntu
sudo dnf install python3 python3-pip  # Fedora
```

---

## 2. Get Time_Warp Classic

```bash
git clone https://github.com/James-HoneyBadger/Time_Warp_Classic.git
cd Time_Warp_Classic
```

Or download and extract the ZIP from GitHub.

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

That's it! The IDE installs packages automatically if needed.

---

## 4. Launch the IDE

```bash
python Time_Warp.py
```

The IDE window opens automatically.

---

## 5. Write Your First Program

### Try BASIC (Classic Programming):

1. Select **BASIC** from the dropdown
2. Type this code:
   ```basic
   10 PRINT "Hello from the past!"
   20 FOR I = 1 TO 5
   30   PRINT "Count: "; I
   40 NEXT I
   50 END
   ```
3. Press **F5** or click **▶ Run**
4. See output on the right!

### Try Logo (Turtle Graphics):

1. Select **Logo** from the dropdown
2. Type this code:
   ```logo
   REPEAT 4 [
     FORWARD 100
     RIGHT 90
   ]
   ```
3. Press **F5**
4. Watch the turtle draw a square!

---

## 6. Load an Example

1. Click **Program → Load Example**
2. Choose **Logo → Colorful Spiral**
3. Press **F5** to run
4. See a colorful spiral appear!

---

## Common Tasks

### Save Your Work
- Press **Ctrl+S**
- Choose location and filename
- Use correct extension (`.bas`, `.logo`, etc.)

### Open a File
- Press **Ctrl+O**
- Navigate to your file
- Select and open

### Change Theme
- **Preferences → Color Theme**
- Choose Light, Dark, or Classic

### Change Font Size
- **Preferences → Font Size**
- Choose from 9pt to 16pt

### Clear Everything
- **View → Clear Editor** - Clear code
- **View → Clear Output** - Clear output text
- **View → Clear Canvas** - Clear graphics

---

## Keyboard Shortcuts (Most Used)

| Key | Action |
|-----|--------|
| **F5** | Run program |
| **F1** | Show help |
| **Ctrl+S** | Save file |
| **Ctrl+O** | Open file |
| **Ctrl+Z** | Undo |
| **Ctrl+C** | Copy |
| **Ctrl+V** | Paste |

---

## Try All 9 Languages

### Vintage Languages (1960s-1970s)

**PILOT** - Educational
```pilot
T:Hello, World!
A:What is your name?
T:Nice to meet you, *NAME*!
```

**BASIC** - Line-numbered
```basic
10 PRINT "Hello, World!"
20 INPUT "Name: ", N$
30 PRINT "Hello, "; N$
```

**Logo** - Turtle graphics
```logo
REPEAT 36 [FORWARD 10 RIGHT 10]
```

**Pascal** - Structured
```pascal
program Hello;
begin
  WriteLn('Hello, World!');
end.
```

**Prolog** - Logic
```prolog
parent(john, mary).
?- parent(john, mary).
```

**Forth** - Stack-based
```forth
: SQUARE DUP * ;
5 SQUARE .
```

### Modern Languages (1980s-1990s)

**Perl** - Text processing
```perl
print "Hello, World!\n";
```

**Python** - General purpose
```python
print("Hello, World!")
```

**JavaScript** - Web scripting
```javascript
console.log("Hello, World!");
```

---

## Next Steps

1. **Read the [User Manual](USER_MANUAL.md)** - Complete guide
2. **Try all examples** - Program → Load Example
3. **Learn each language** - See [Language Reference](LANGUAGE_REFERENCE.md)
4. **Experiment** - Modify examples and see what happens
5. **Create your own programs** - Start simple, build up

---

## Getting Help

- **Press F1** in the IDE for built-in help
- **Check [docs/](.)** for comprehensive documentation
- **Look at examples/** for working code
- **Read error messages** - they tell you what's wrong

---

## Troubleshooting

### "Python not found"
- Install Python 3.9+ from python.org
- Add Python to PATH during installation

### "Module not found"
- Run: `pip install -r requirements.txt`
- Or let the IDE auto-install on first launch

### Program doesn't run
- Check language dropdown matches your code
- Look for syntax errors in output
- Try an example program first to verify IDE works

### Graphics don't show
- Check View → Graphics Panel is visible
- Use PENDOWN in turtle graphics
- Verify you're using Logo or BASIC turtle commands

---

**You're Ready to Code!** 🚀

Explore 9 programming languages and enjoy the journey through computing history.

---

© 2025 Honey Badger Universe | Quick Start Guide
