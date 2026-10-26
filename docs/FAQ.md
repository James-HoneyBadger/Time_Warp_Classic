# Frequently Asked Questions

Common questions about Time Warp Classic.

## General Questions

### What is Time Warp Classic?

Time Warp Classic is a multi-language IDE that lets you write and run code in 9 different programming languages:
- BASIC, Python, JavaScript, Pascal, Prolog, Forth, Perl, Logo, and PILOT

It's designed for learning programming, teaching, and exploring different language paradigms.

### Who is it for?

- **Students:** Learn programming fundamentals
- **Teachers:** Teach multiple languages in one environment
- **Hobbyists:** Explore retro and modern languages
- **Developers:** Understand different language approaches

### Is it free?

Yes! Time Warp Classic is open-source and completely free to use.

### What platforms does it support?

- **Windows** (Python 3.9+)
- **macOS** (Python 3.9+)
- **Linux** (Python 3.9+)

### Can I use it offline?

Yes, Time Warp Classic runs completely offline. No internet connection needed.

---

## Installation & Setup

### How do I install Time Warp Classic?

1. Ensure Python 3.9+ is installed
2. Install tkinter if needed
3. Download or clone the repository
4. Run: `python Time_Warp.py`

See [QUICK_START.md](QUICK_START.md) for detailed instructions.

### Do I need to install anything else?

You need:
- Python 3.9 or higher
- tkinter (usually included with Python)
- Standard library (included)

Optional for some languages:
- Node.js for JavaScript (some features)

### How much disk space does it need?

About 50 MB for the application and examples.

### Can I run it from USB?

Yes, as long as Python is installed on the target computer.

---

## Using the IDE

### How do I write code?

1. Click in the editor area
2. Type your code
3. Select language from the dropdown
4. Click Run (or press F5)

### How do I select a language?

- Use the language dropdown above the editor

### What's the keyboard shortcut to run code?

See [QUICK_START.md](QUICK_START.md) for all shortcuts.

### Can I undo my changes?

Yes, use Ctrl+Z to undo and Ctrl+Y to redo.

### How do I clear the output?

Click the "Clear Output" button or use the menu.

### Can I save my code?

Yes. **File > Save** (Ctrl+S) writes to the file you opened; if the program has
never been saved, it asks where to put it. **File > Save As...**
(Ctrl+Shift+S) always asks, and proposes the extension that matches the
selected language (`.bas` for BASIC, `.logo` for Logo, and so on).

The title bar and status bar show a `*` while there are unsaved changes, and
New/Open ask before throwing them away. Closing the window asks first too.

### What does the status bar show?

The selected language, the file name (with `*` when modified), the caret
position (`Ln 12, Col 5`) and whether a program is `Ready` or `Running`.

### What file formats are supported?

Canonical extensions (one per language):
- `.pilot` - PILOT
- `.bas` - BASIC
- `.logo` - Logo
- `.pas` - Pascal
- `.pro` - Prolog
- `.fth` - Forth
- `.pl` - Perl
- `.py` - Python
- `.js` - JavaScript

Or save as `.txt` (universal text)

---

## Programming & Execution

### Why won't my code run?

Check:
1. Syntax errors in output panel
2. Correct language selected
3. Missing keywords (END, ENDIF, etc.)
4. Check examples for syntax

### How do I debug my code?

1. Add PRINT statements to trace execution
2. Type `TRON` in the BASIC console to trace every line that runs, `TROFF`
   to stop
3. Click an error message such as `?ERROR IN 120: ...` (or `BREAK IN 120`) to
   jump straight to that line in the editor
4. Run simpler versions of your program
5. Compare with example programs

### Can I use multiple languages in one program?

No, each program must be in one language.

### How big can programs be?

You can write very large programs, but performance depends on:
- Program complexity
- Data volume
- Computer resources
- Language efficiency

### Can I try BASIC statements without writing a whole program?

Yes — select **BASIC** and type into the **Console** bar. Statements run
immediately (`PRINT 2+2`), numbered lines are stored in the editor
(`10 PRINT "HI"`), and `LIST` / `RUN` / `RENUMBER` / `NEW` / `HELP` work as
they did on a home computer.

### Can Python, JavaScript or Perl programs ask for input?

Yes. When such a program calls `input()` (or reads stdin), type the answer in the
**Console** bar and press Enter — the line is passed to the running script.
Output is streamed line by line as it is printed. (A prompt written without a
newline, such as `input("Name: ")`, is shown together with your answer rather
than on its own line.)

If the script fails, the console reports `?ERROR IN <line>: <message>` using the
line number from the script itself; click that line to jump to it in the editor.

### Is there a time limit for execution?

**For built-in languages** (BASIC, Logo, PILOT, Pascal, Prolog, Forth): No timeout — programs run until completion or manual stop. Press the red **Stop** button (or Ctrl+.) to end a run, including endless loops.

**For subprocess languages** (Python, JavaScript, Perl): Yes — a **30-second timeout** is enforced. If your program takes longer than 30 seconds, it will be terminated automatically.

### What happens if I create an infinite loop?

**Built-in languages:** The program runs until you press **Stop** (or Ctrl+.) in the GUI — there is no artificial iteration limit. The console then reports `BREAK IN <line>`.
**Subprocess languages:** Press **Stop** to kill the process, or let the 30-second timeout end it automatically.

---

## Language-Specific Questions

### Which language should I learn first?

**For beginners:** BASIC or Logo (visual feedback)
**For modern syntax:** Python
**For understanding paradigms:** Prolog (logic)

See [LANGUAGE_TUTORIALS.md](user/LANGUAGE_TUTORIALS.md) for learning guides.

### Can I run JavaScript without Node.js?

Some features work with built-in executor. Advanced features may require Node.js.

### How does Prolog differ from other languages?

Prolog is a **logic language** where you:
1. Define facts
2. Define rules
3. Query the system
4. Backtracking finds solutions

### What's the difference between Forth and other languages?

Forth is **stack-based**:
- Operations use a stack
- Reverse Polish notation (postfix)
- Very compact and efficient

### Can I use graphics in all languages?

**Logo** has full turtle graphics support with shapes, colors, and procedures.
**BASIC** has turtle graphics (FORWARD, RIGHT, etc.) and direct graphics (PSET, LINE, BOX, CIRCLE).
**PILOT** has turtle graphics via the `G:` command prefix (G:LINE, G:CIRCLE, G:RECT).
Other languages focus on text output.

### Where can I find example programs?

Each language has example programs in the `examples/` directory:
- Two example programs per language demonstrating real-world use
- Additional examples (hello world, specific features)

---

## Files & Projects

### Where are my files saved?

In the directory you specify. Usually current directory or Documents.

### Can I open files from other editors?

Yes, Time Warp can open any text file with appropriate code.

### Can I share my programs?

Yes! Save as `.txt` or language extension and share with others.

### What's the examples directory for?

`examples/` contains comprehensive demo programs for each language showing:
- All major features
- Working examples
- Good practices

**See them:** [examples/README.md](../examples/README.md)

---

## Errors & Troubleshooting

### I see "Syntax Error" but my code looks correct

Check:
1. Matching parentheses/brackets
2. Correct keywords (ENDIF not ENDFI)
3. Proper indentation
4. Compare with examples

For more help: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### What does "Unknown language" mean?

The language detector couldn't identify the language. Try:
1. Selecting language manually
2. Using more distinctive keywords
3. Disabling auto-detect

### Can I modify the application?

Yes, it's open-source! Check [TECHNICAL_REFERENCE.md](dev/TECHNICAL_REFERENCE.md) for architecture details.

### Where do I report bugs?

File an issue on the GitHub repository with:
- What you were trying to do
- What happened
- What you expected
- Your Python version

---

## Performance & Optimization

### Why is my program slow?

Possible causes:
- Large loops (reduce iterations)
- Complex calculations
- Graphics rendering (Logo)
- System resources

Solutions:
- Optimize algorithm
- Reduce output
- Upgrade computer

### How much output is too much?

Generally works well up to thousands of lines. Very large output may slow display.

### Can I run programs in the background?

Not currently, but you can:
1. Split into smaller programs
2. Run multiple instances
3. Save output to file for later review

---

## Customization & Preferences

### Can I change the font?

Yes, in Preferences:
- Font family
- Font size
- Font style

### Can I change the color scheme?

Yes, use Preferences > Theme to:
- Select built-in themes
- Customize colors
- Save custom themes

### Can I add keyboard shortcuts?

Check Preferences for shortcuts configuration.

### Can I change the default language?

The default is BASIC, but auto-detect can make Python default if you prefer.

---

## Features & Capabilities

### Can I import external libraries?

Python supports standard library imports. Other languages limited by sandbox.

### Can I use the internet in my programs?

Some languages (Python) can make HTTP requests if libraries available.

### Can I create graphical user interfaces?

Logo has turtle graphics. HTML/CSS rendering not available.

### Can I create games?

Yes! Python or JavaScript are good choices. Logo for graphics.

---

## Getting Help & Learning

### Where should I start?

1. Read [QUICK_START.md](QUICK_START.md)
2. Run example programs
3. Try [LANGUAGE_TUTORIALS.md](user/LANGUAGE_TUTORIALS.md)
4. Read [README.md](README.md)

### Where are the complete language references?

In `docs/languages/` directory:
- [BASIC_REFERENCE.md](languages/BASIC_REFERENCE.md)
- [PYTHON_REFERENCE.md](languages/PYTHON_REFERENCE.md)
- And 7 more...

### Can I learn multiple languages?

Yes, that's one of Time Warp's strengths! The application makes it easy to switch between languages.

### Are there exercises or challenges?

Yes! Examples directory has programs to study and modify.

### Is there a community?

Check GitHub repository for discussions and community links.

---

## Advanced Topics

### How do I extend Time Warp?

See [TECHNICAL_REFERENCE.md](dev/TECHNICAL_REFERENCE.md) for:
- Architecture overview
- Adding new languages
- Adding new features
- Plugin development

### Can I create custom languages?

Yes, see [TECHNICAL_REFERENCE.md](dev/TECHNICAL_REFERENCE.md) for how to implement a language.

### How does the language detection work?

The interpreter:
1. Scans for language-specific keywords
2. Analyzes syntax patterns
3. Checks file extensions
4. Returns most likely language

### Can I use Time Warp in a classroom?

Yes! It's designed for education. Multiple students can:
- Use same installation
- Create own programs
- Learn different languages
- Compare implementations

---

## Statistics & Facts

### How many languages are supported?

**9 languages:**
1. BASIC
2. Python
3. JavaScript
4. Pascal
5. Prolog
6. Forth
7. Perl
8. Logo
9. PILOT

### How many lines of code in Time Warp?

Several thousand lines of Python implementing the interpreter and IDE.

### When was it created?

Time Warp Classic is a modern retro-computing project honoring classic languages.

---

## Before You Go

### Quick Tips

1. **Use examples:** They show best practices
2. **Read errors carefully:** They're usually helpful
3. **Try simple first:** Build up complexity gradually
4. **Experiment:** Try variations on examples
5. **Have fun:** Programming is creative!

### Useful Resources

- [INDEX.md](INDEX.md) - Documentation index
- [examples/README.md](../examples/README.md) - Program examples
- [QUICK_START.md](QUICK_START.md) - Get started in 5 minutes
- [README.md](README.md) - Complete documentation index

---

**Have a question not answered here? Check the other documentation files or create an issue on GitHub.**

**Happy Programming! 🚀**
