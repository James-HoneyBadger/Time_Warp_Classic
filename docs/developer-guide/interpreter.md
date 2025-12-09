# Time_Warp - Interpreter System

## Overview

Time_Warp is an educational programming environment that interprets and executes code in real-time across multiple programming languages. Unlike compilers that create standalone executables, Time_Warp uses an interpreter architecture that provides immediate feedback and interactive execution with integrated turtle graphics.

## Architecture

### Core Interpreter (`core/interpreter.py`)

The `Time_WarpInterpreter` class is the central execution engine:

```python
class Time_WarpInterpreter:
    def __init__(self):
        self.turtle_canvas = TurtleCanvas()  # Graphics output
        self.language_executors = {}         # Language-specific executors
        self.current_language = None

    def execute(self, code: str, language: str) -> str:
        # Route execution to appropriate language executor
        executor = self.language_executors[language]
        return executor.execute_command(code)
```

### Language Executors (`core/languages/`)

Each supported language has a dedicated executor class that implements the `execute_command()` method:

```python
class LanguageExecutor:
    def execute_command(self, command: str) -> str:
        """Execute a command and return formatted output"""
        # Parse and execute language-specific syntax
        # Return result string or error message
        pass
```

## Supported Languages

### PILOT (`.pilot`)
Educational language with simple syntax for beginners:

**Commands:**
- `T:` - Type/Text output
- `A:` - Accept input
- `J:` - Jump to label
- `Y:` / `N:` - Conditional jumps
- `C:` - Compute variables
- `M:` - Match patterns

**Example:**
```
T:Hello World!
A:What is your name?
T:Welcome, #NAME!
```

### BASIC (`.bas`)
Line-numbered procedural programming:

**Features:**
- Numbered lines (10, 20, 30...)
- Variables and arrays
- FOR/NEXT loops
- IF/THEN/ELSE conditionals
- PRINT and INPUT statements

**Example:**
```
10 PRINT "Hello World!"
20 INPUT "Enter your name: ", NAME$
30 PRINT "Welcome, "; NAME$
```

### Logo (`.logo`)
Turtle graphics programming with procedures:

**Commands:**
- `FORWARD n` / `BACK n` - Move turtle
- `LEFT n` / `RIGHT n` - Turn turtle
- `PENUP` / `PENDOWN` - Control drawing
- `TO proc` / `END` - Define procedures

**Example:**
```
TO SQUARE :SIZE
  REPEAT 4 [FORWARD :SIZE RIGHT 90]
END

SQUARE 100
```

### Python (`.py`)
Full Python execution with turtle graphics integration:

**Features:**
- Complete Python syntax
- Import standard libraries
- Function definitions
- Object-oriented programming

**Example:**
```python
import turtle

def draw_square(size):
    for _ in range(4):
        turtle.forward(size)
        turtle.right(90)

draw_square(100)
```

### JavaScript (`.js`)
JavaScript execution environment:

**Features:**
- Modern JavaScript syntax
- Variables, functions, objects
- Array and string operations

**Example:**
```javascript
function greet(name) {
    console.log("Hello, " + name + "!");
}

greet("World");
```

### Perl (`.pl`)
Text processing and scripting:

**Features:**
- Regular expressions
- Text manipulation
- File operations

**Example:**
```perl
print "Hello World!\n";
$name = <STDIN>;
chomp $name;
print "Welcome, $name!\n";
```

## Execution Process

### Code Execution Flow

1. **Input Reception** - Code entered in editor or loaded from file
2. **Language Detection** - Determine target language from context or file extension
3. **Parsing** - Language executor parses commands/instructions
4. **Execution** - Commands executed with turtle graphics integration
5. **Output Display** - Results shown in output panel and graphics canvas
6. **Error Handling** - Syntax/runtime errors displayed with helpful messages

### Turtle Graphics Integration

All languages can access turtle graphics through the interpreter:

```python
# Available in all language executors
self.interpreter.turtle_canvas.forward(distance)
self.interpreter.turtle_canvas.right(angle)
self.interpreter.turtle_canvas.set_color(color)
```

### Error Handling

Graceful error handling with educational messages:

```python
try:
    result = self.execute_language_specific_code(code)
    return result
except Exception as e:
    error_msg = f"❌ Error in {self.language_name}: {str(e)}"
    self.interpreter.display_error(error_msg)
    return None
```

## Usage

### Interactive Execution

The primary way to run programs is through the Time_Warp CLI:

1. **Launch**: `python Time_Warp.py`
2. **Select Language**: Choose from supported languages
3. **Write Code**: Use the editor with basic syntax highlighting
4. **Execute**: Click run or use keyboard shortcut
5. **View Results**: See output and turtle graphics in real-time

### Command Line Interface

Time_Warp also provides a CLI for batch execution:

```bash
# Run a program file
python Time_Warp.py --cli program.pilot

# Execute code directly
python Time_Warp.py --cli -c "T:Hello World!"

# Specify language explicitly
python Time_Warp.py --cli -l basic program.bas
```

### Program File Formats

- **PILOT**: `.pilot` extension
- **BASIC**: `.bas` extension
- **Logo**: `.logo` extension
- **Python**: `.py` extension
- **JavaScript**: `.js` extension
- **Perl**: `.pl` extension

## Technical Details

### Performance Characteristics

- **Execution Speed**: Immediate interpretation (no compilation step)
- **Memory Usage**: Minimal footprint for educational use
- **Platform Support**: Cross-platform (Windows, macOS, Linux)
- **Graphics Performance**: Real-time turtle graphics rendering

### Extensibility

The interpreter architecture supports adding new languages:

1. Create executor class in `core/languages/new_lang.py`
2. Implement `execute_command(command: str) -> str` method
3. Register executor in interpreter's language mapping
4. Add file extension and syntax highlighting support

## Educational Benefits

### Immediate Feedback
- **Real-time Execution** - See results instantly as you code
- **Visual Learning** - Turtle graphics make abstract concepts concrete
- **Error Education** - Clear error messages help learning
- **Interactive Exploration** - Experiment and iterate quickly

### Progressive Learning
- **Simple to Complex** - Languages range from PILOT to full Python
- **Consistent Concepts** - Programming fundamentals apply across languages
- **Visual Reinforcement** - Graphics provide immediate understanding
- **Self-Paced** - Learn at your own speed with comprehensive examples

## Troubleshooting

### Common Issues

**"Language not supported"**
- Check that the language is selected in the CLI
- Verify file extension matches the language

**"Syntax error"**
- Review language-specific syntax rules
- Check for missing semicolons, parentheses, etc.
- Use examples as reference

**"Graphics not displaying"**
- Ensure turtle graphics commands are used
- Check that the canvas is visible in the CLI output
- Try running a simple graphics example first

**"Import errors"**
- Python/Perl imports may have path issues
- Check that required modules are available
- Use relative imports when possible

### Debug Tips

- **Start Simple** - Test with basic commands before complex programs
- **Check Examples** - Compare with working examples in `examples/`
- **Isolate Issues** - Comment out sections to find problematic code
- **Use Print/Debug** - Add output statements to trace execution

## Development

### Adding Language Support

To add a new programming language:

1. **Create Executor** - New class in `core/languages/`
2. **Implement Interface** - `execute_command()` method
3. **Handle Syntax** - Parse and execute language constructs
4. **Integrate Graphics** - Support turtle graphics if applicable
5. **Add Tests** - Unit tests for the new executor
6. **Update UI** - Add language selection and file handling

### Testing

Run the test suite to ensure interpreter functionality:

```bash
# Run all tests
python scripts/run_tests.py

# Test specific language
python -m pytest tests/test_pilot.py -v

# Test interpreter core
python -m pytest tests/test_interpreter.py -v
```

## See Also

- [Time_Warp User Guide](../README.md)
- [Language References](languages/)
- [Example Programs](../examples/)
- [GitHub Repository](https://github.com/your-username/Time_Warp_Classic)