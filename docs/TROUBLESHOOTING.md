# Troubleshooting Guide

Solutions for common issues in Time Warp Classic.

## Getting Started Issues

### Cannot Find Time Warp Application

**Problem:** Python file won't launch

**Solutions:**
1. Ensure Python 3.9+ is installed: `python --version`
2. Install tkinter: `sudo apt-get install python3-tk` (Linux) or through Python installer (Windows)
3. Run from terminal: `python Time_Warp.py`

### Window Doesn't Open

**Problem:** Application hangs or no window appears

**Solutions:**
1. Check for errors in terminal
2. Try with `PYTHONUNBUFFERED=1 python Time_Warp.py`
3. Check Python PATH: `which python`
4. Reinstall tkinter

### Missing Dependencies

**Problem:** Import errors on startup

**Solutions:**
```bash
pip install -r requirements.txt
```

---

## Execution Issues

### Code Won't Run

**Problem:** Click Run but nothing happens

**Solutions:**
1. Ensure language is selected correctly
2. Check syntax for obvious errors
3. Look for error message in output panel
4. Try a simple program: `PRINT "Hello"`

### "Unknown Language" Error

**Problem:** Language not recognized

**Solutions:**
1. Check language dropdown
2. Enable "Auto-Detect Language"
3. Ensure code uses correct syntax
4. Try manual language selection

### "Syntax Error" Messages

**Problem:** "Syntax error at line X"

**Solutions:**
1. Check line for typos
2. Verify opening/closing brackets and parentheses
3. Check for missing keywords (END, ENDIF, etc.)
4. Look at comprehensive demo for examples

### No Output Shown

**Problem:** Code runs but produces no output

**Solutions:**
1. Code completed silently (add PRINT statements)
2. Output panel too small (resize window)
3. Clear button was pressed (run again)
4. Check for hidden output in error area

### Infinite Loop / Program Hangs

**Problem:** Program runs forever or doesn't respond

**Solutions:**
1. Press Ctrl+C in terminal to stop
2. Check loop conditions
3. Ensure loop has increment/terminator
4. Look for recursive functions without base case

---

## Language-Specific Issues

### BASIC

**Problem:** "REM" comment not recognized
- Solution: Use `REM` followed by space

**Problem:** Array index out of bounds
- Solution: Check array size in DIM statement

**Problem:** Undefined variable in expression
- Solution: Use LET to assign before use

### Python

**Problem:** Indentation errors
- Solution: Ensure consistent indentation (4 spaces)

**Problem:** "Name not defined" error
- Solution: Check variable spelling and scope

**Problem:** List index out of range
- Solution: Verify list size before accessing

### JavaScript

**Problem:** "Undefined" values
- Solution: Check variable declarations

**Problem:** "is not a function"
- Solution: Verify function name and arguments

### Prolog

**Problem:** No solutions found
- Solution: Check facts and rules
- Verify query syntax

**Problem:** Infinite recursion
- Solution: Ensure base case is reached

---

## GUI Issues

### Text Editing Problems

**Problem:** Text won't delete
- Solution: Try Backspace or Delete key

**Problem:** Find & Replace not working
- Solution: Check search term is spelled correctly

**Problem:** Line numbers incorrect
- Solution: Refresh editor (Ctrl+A then Ctrl+V)

### Display Issues

**Problem:** Text too small/large
- Solution: Adjust font size in Preferences

**Problem:** Syntax highlighting missing
- Solution: Check language selection

**Problem:** Output text is unreadable
- Solution: Change theme or font

---

## Performance Issues

### Program Runs Slowly

**Solutions:**
1. Reduce output volume (less PRINT statements)
2. Optimize loops (fewer iterations)
3. Reduce complexity (simpler expressions)
4. Check memory usage (close other apps)

### GUI Freezes During Execution

**Solutions:**
1. Reduce program size
2. Add more output statements for progress
3. Break into smaller programs
4. Upgrade hardware

### High Memory Usage

**Solutions:**
1. Limit array sizes
2. Close and reopen application
3. Reduce graphics resolution (Logo)
4. Use simpler data types

---

## File Operations

### Cannot Open File

**Problem:** "File not found" error

**Solutions:**
1. Verify file exists: `ls -l filename`
2. Use absolute path: `/home/user/program.bas`
3. Check file permissions: `chmod 644 filename`

### Cannot Save File

**Problem:** "Permission denied" error

**Solutions:**
1. Check write permissions: `chmod 755 directory`
2. Use different directory
3. Run as admin (not recommended)

### File Corruption

**Problem:** File opens but looks garbled

**Solutions:**
1. Check file encoding (should be UTF-8)
2. Open in text editor first
3. Recreate file
4. Restore from backup

---

## Advanced Troubleshooting

### Check System Requirements

```bash
python --version      # Should be 3.9+
python -m tkinter     # Should open test window
pip list             # Check installed packages
```

### Run Diagnostic Program

Create test_system.py:
```python
import sys
import tkinter as tk

print(f"Python: {sys.version}")
print(f"Platform: {sys.platform}")

try:
    root = tk.Tk()
    root.title("System Test")
    tk.Label(root, text="GUI works!").pack()
    root.after(1000, root.quit)
    root.mainloop()
except Exception as e:
    print(f"GUI error: {e}")
```

### Enable Debug Mode

Look for debug settings in code or check terminal output verbosity.

---

## Error Messages Reference

| Error | Meaning | Solution |
|-------|---------|----------|
| SyntaxError | Invalid syntax | Check code structure |
| NameError | Undefined variable | Define variable first |
| TypeError | Wrong data type | Check value type |
| ZeroDivisionError | Dividing by 0 | Check denominator |
| IndexError | Invalid index | Check bounds |
| KeyError | Missing dict key | Verify key exists |

---

## Getting Help

### Check Documentation
- [QUICK_START.md](QUICK_START.md) - Quick reference
- [LANGUAGE_TUTORIALS.md](user/LANGUAGE_TUTORIALS.md) - Learn languages
- [README.md](README.md) - Documentation index

### Run Examples
All working examples in `examples/` directory

### Check Demo Programs
Each language has comprehensive demo in:
`examples/[language]/comprehensive_demo.*`

### Search for Keywords
Use Find (Ctrl+F) in documentation

---

## Still Having Issues?

1. **Check the demos:** Are they working?
2. **Try simple code:** Can you run `PRINT "Hello"`?
3. **Review examples:** Look at similar working program
4. **Read error carefully:** Error message usually points to issue
5. **Search documentation:** Most issues covered here

---

**Happy Debugging! 🔧**
