# Time_Warp Classic - Technical Manual

**Version 1.3.0** | **For Developers and Advanced Users**

This technical manual provides comprehensive documentation of Time_Warp Classic's architecture, implementation details, and internals.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Components](#core-components)
3. [Language Execution System](#language-execution-system)
4. [Turtle Graphics Engine](#turtle-graphics-engine)
5. [GUI Framework](#gui-framework)
6. [Data Flow](#data-flow)
7. [Extension Points](#extension-points)
8. [Performance Considerations](#performance-considerations)

---

## Architecture Overview

### Design Philosophy

Time_Warp Classic follows these principles:

1. **Separation of Concerns** - Language executors are independent modules
2. **Unified Interface** - All languages use the same execution contract
3. **Educational First** - Clear error messages and debugging support
4. **Extensibility** - Easy to add new languages or features
5. **Simplicity** - Avoid over-engineering, keep it maintainable

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Time_Warp.py                         │
│              (Entry Point & GUI Manager)                 │
└─────────────────┬───────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────┐
│               core/interpreter.py                        │
│            (Central Execution Engine)                    │
│                                                          │
│  • Program dispatch                                      │
│  • Variable management                                   │
│  • Output handling                                       │
│  • Turtle graphics coordination                          │
└──────┬──────────────────────────────────────────────────┘
       │
       ├──→ core/languages/pilot.py      (PILOT)
       ├──→ core/languages/basic.py      (BASIC)
       ├──→ core/languages/logo.py       (Logo)
       ├──→ core/languages/pascal.py     (Pascal)
       ├──→ core/languages/prolog.py     (Prolog)
       ├──→ core/languages/forth.py      (Forth)
       ├──→ core/languages/perl.py       (Perl)
       ├──→ core/languages/python.py     (Python)
       └──→ core/languages/javascript.py (JavaScript)
```

### Directory Structure

```
Time_Warp_Classic/
├── Time_Warp.py                 # GUI and dependency management
├── core/
│   ├── interpreter.py           # Central execution engine
│   ├── languages/               # Language-specific executors
│   │   ├── __init__.py
│   │   ├── pilot.py
│   │   ├── basic.py
│   │   ├── logo.py
│   │   ├── pascal.py
│   │   ├── prolog.py
│   │   ├── forth.py
│   │   ├── perl.py
│   │   ├── python.py
│   │   ├── python_executor.py  # Python subprocess wrapper
│   │   ├── javascript.py
│   │   └── javascript_executor.py # Node.js subprocess wrapper
│   ├── features/
│   │   └── code_templates.py   # Code generation utilities
│   └── utilities/
│       └── __init__.py
├── examples/                    # Organized by language
├── docs/                       # Documentation
└── scripts/                    # CLI and utilities
```

---

## Core Components

### 1. Time_Warp.py - Main Application

**Responsibilities:**
- Dependency checking and installation
- GUI window creation and layout
- Menu system management
- File I/O operations
- Event handling and binding

**Key Classes:**

#### `DependencyChecker`
Manages Python package dependencies.

```python
class DependencyChecker:
    REQUIRED_PACKAGES = ["pygame", "PIL"]
    OPTIONAL_PACKAGES = ["pygments", "pytest", "black", "flake8"]
    
    def check_python_version(self) -> bool
    def check_package(self, package_name: str) -> bool
    def check_dependencies(self) -> bool
    def install_missing_packages(self) -> bool
    def run_full_check(self) -> bool
```

**GUI Components:**
- `menubar` - Top menu system (File, Edit, Program, View, Preferences, Help)
- `editor_text` - Code editor with undo/redo (ScrolledText widget)
- `output_text` - Program output display (ScrolledText widget)
- `turtle_canvas` - Graphics display (Tkinter Canvas)
- `input_entry` - User input field (Entry widget)
- `button_frame` - Control buttons (Run, Open, Save, Clear)

### 2. core/interpreter.py - Execution Engine

**Responsibilities:**
- Dispatching programs to language executors
- Managing global state (variables, turtle graphics)
- Coordinating output to GUI
- Handling user input
- Providing turtle graphics API

**Key Class: `Time_WarpInterpreter`**

#### Core Methods

```python
class Time_WarpInterpreter:
    def __init__(self, output_widget=None):
        """Initialize interpreter with optional GUI output widget"""
        
    def run_program(self, program: str, language: str = "pilot"):
        """Main entry point - execute a program in the specified language"""
        
    def log_output(self, text: str):
        """Send text to output display"""
        
    def get_input(self, prompt: str = "") -> str:
        """Get input from user (GUI or CLI)"""
        
    def evaluate_expression(self, expr: str) -> float:
        """Evaluate mathematical expressions safely"""
```

#### Turtle Graphics Methods

```python
    def init_turtle_graphics(self):
        """Initialize turtle graphics system"""
        
    def turtle_forward(self, distance: float):
        """Move turtle forward by distance units"""
        
    def turtle_turn(self, angle: float):
        """Turn turtle by angle degrees (positive = right)"""
        
    def turtle_penup(self):
        """Lift pen (stop drawing)"""
        
    def turtle_pendown(self):
        """Lower pen (start drawing)"""
        
    def clear_turtle_screen(self):
        """Clear canvas and reset turtle"""
        
    def update_turtle_display(self):
        """Redraw turtle position on canvas"""
```

#### State Management

```python
    self.variables = {}              # Global variable storage
    self.turtle_graphics = {}        # Turtle state
    self.ide_turtle_canvas = None    # GUI canvas reference
    self.output_widget = None        # GUI output reference
    self.debug_mode = False          # Debug logging flag
```

### 3. Language Executors

Each language has its own executor class in `core/languages/[language].py`.

#### Standard Executor Interface

All executors implement:

```python
class TwLanguageExecutor:
    def __init__(self, interpreter: Time_WarpInterpreter):
        """Initialize with reference to main interpreter"""
        self.interpreter = interpreter
        
    def execute_command(self, command: str) -> str:
        """
        Execute a single command in the language.
        
        Args:
            command: String containing the command to execute
            
        Returns:
            "continue" to proceed, "stop" to halt execution
        """
```

#### Example: Logo Executor

```python
class TwLogoExecutor:
    def execute_command(self, command: str) -> str:
        parts = command.strip().upper().split()
        if not parts:
            return "continue"
            
        cmd = parts[0]
        
        # Movement commands
        if cmd in ["FORWARD", "FD"]:
            distance = self._eval_argument(parts[1]) if len(parts) > 1 else 50
            self.interpreter.turtle_forward(distance)
            
        elif cmd in ["RIGHT", "RT"]:
            angle = self._eval_argument(parts[1]) if len(parts) > 1 else 90
            self.interpreter.turtle_turn(angle)
            
        # ... more commands ...
        
        return "continue"
```

---

## Language Execution System

### Execution Flow

1. **Program Input**
   - User clicks Run or presses F5
   - `Time_Warp.py` captures editor contents
   - Selected language is determined from dropdown

2. **Dispatch**
   - `interpreter.run_program(code, language)` is called
   - Interpreter selects appropriate language executor
   - Program is split into commands/lines

3. **Execution**
   - Each command is passed to `executor.execute_command()`
   - Executor parses and executes the command
   - State changes are applied (variables, turtle position, output)

4. **Output**
   - All output goes through `interpreter.log_output()`
   - GUI updates in real-time
   - Turtle graphics are drawn on canvas

5. **Completion**
   - Program finishes or encounters error
   - Final state is displayed
   - User can run again or edit code

### Language-Specific Implementations

#### Interpreted Languages (PILOT, BASIC, Logo, etc.)

These are fully interpreted within Python:

```python
# In interpreter.py
if language == "logo":
    from core.languages.logo import TwLogoExecutor
    executor = TwLogoExecutor(self)
    for command in commands:
        result = executor.execute_command(command)
        if result == "stop":
            break
```

#### External Languages (Python, JavaScript, Perl)

These use subprocess execution:

```python
# In python_executor.py
def execute_python_code(code: str, interpreter) -> tuple:
    """Execute Python code in subprocess"""
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=30
        )
        return (result.stdout, result.stderr, result.returncode)
    except Exception as e:
        return ("", str(e), 1)
```

---

## Turtle Graphics Engine

### Coordinate System

Time_Warp uses the **Logo convention**:

```
      (0, 200)
          │ 0° (North)
          │
(-200,0)──┼──(200,0)  90° (East)
          │
          │ 180° (South)
      (0,-200)
```

- **Origin**: Center of canvas (0, 0)
- **Heading**: 0° points North (up), increases clockwise
- **Canvas Coords**: Standard Tkinter (Y increases downward)

### Internal Representation

```python
turtle_graphics = {
    "x": 0.0,                    # Turtle X position
    "y": 0.0,                    # Turtle Y position
    "heading": 0.0,              # Heading in degrees (0° = North)
    "pen_down": True,            # Is pen drawing?
    "pen_color": "#000000",      # Current pen color
    "pen_width": 2,              # Pen thickness
    "lines": [],                 # List of drawn line segments
    "center_x": 300,             # Canvas center X
    "center_y": 200,             # Canvas center Y
    "visible": True              # Is turtle visible?
}
```

### Coordinate Conversion

Logo coordinates must be converted to canvas coordinates:

```python
def turtle_forward(self, distance):
    # Logo heading to mathematical angle
    logo_heading = self.turtle_graphics["heading"]
    math_angle_degrees = 90 - logo_heading  # Convert Logo → Math
    heading_rad = math.radians(math_angle_degrees)
    
    # Calculate new position
    old_x = self.turtle_graphics["x"]
    old_y = self.turtle_graphics["y"]
    new_x = old_x + distance * math.cos(heading_rad)
    new_y = old_y + distance * math.sin(heading_rad)
    
    # Draw line if pen is down
    if self.turtle_graphics["pen_down"]:
        # Convert Logo coords to canvas coords
        canvas_x1 = old_x + self.turtle_graphics["center_x"]
        canvas_y1 = self.turtle_graphics["center_y"] - old_y  # Flip Y
        canvas_x2 = new_x + self.turtle_graphics["center_x"]
        canvas_y2 = self.turtle_graphics["center_y"] - new_y  # Flip Y
        
        self.ide_turtle_canvas.create_line(
            canvas_x1, canvas_y1, canvas_x2, canvas_y2,
            fill=self.turtle_graphics["pen_color"],
            width=self.turtle_graphics["pen_width"]
        )
```

### Drawing the Turtle

The turtle itself is drawn as a triangle:

```python
def update_turtle_display(self):
    canvas = self.ide_turtle_canvas
    if not canvas:
        return
        
    # Clear old turtle
    canvas.delete("turtle")
    
    if not self.turtle_graphics.get("visible", True):
        return
        
    # Get turtle position in canvas coords
    x = self.turtle_graphics["x"] + self.turtle_graphics["center_x"]
    y = self.turtle_graphics["center_y"] - self.turtle_graphics["y"]
    
    # Convert Logo heading to canvas angle
    logo_heading = self.turtle_graphics["heading"]
    canvas_angle = -logo_heading  # Canvas angles increase clockwise from East
    angle_rad = math.radians(canvas_angle)
    
    # Calculate triangle points
    size = 10
    # Point 1: Forward direction
    x1 = x + size * math.cos(math.radians(90 - logo_heading))
    y1 = y - size * math.sin(math.radians(90 - logo_heading))
    # Points 2 & 3: Base of triangle
    x2 = x + size * math.cos(math.radians(210 - logo_heading))
    y2 = y - size * math.sin(math.radians(210 - logo_heading))
    x3 = x + size * math.cos(math.radians(330 - logo_heading))
    y3 = y - size * math.sin(math.radians(330 - logo_heading))
    
    # Draw triangle
    canvas.create_polygon(
        x1, y1, x2, y2, x3, y3,
        fill="green", outline="black",
        tags="turtle"
    )
```

---

## GUI Framework

### Tkinter Structure

Time_Warp uses Tkinter with a PanedWindow layout:

```python
# Main horizontal split
main_paned = tk.PanedWindow(root, orient=tk.HORIZONTAL)
main_paned.pack(fill=tk.BOTH, expand=True)

# Left: Editor
left_panel = tk.Frame(main_paned)
main_paned.add(left_panel, width=400)

# Right: Vertical split for output and graphics
right_panel = tk.Frame(main_paned)
main_paned.add(right_panel, width=800)

right_paned = tk.PanedWindow(right_panel, orient=tk.VERTICAL)
right_paned.pack(fill=tk.BOTH, expand=True)

# Output panel (top right)
output_frame = tk.LabelFrame(right_paned, text="Output")
right_paned.add(output_frame, height=300)

# Graphics panel (bottom right)
graphics_frame = tk.LabelFrame(right_paned, text="Turtle Graphics")
right_paned.add(graphics_frame, height=300)
```

### Event Handling

#### Keyboard Bindings

```python
root.bind("<F5>", lambda e: run_code())
root.bind("<F1>", lambda e: show_help())
root.bind("<Control-n>", lambda e: new_file())
root.bind("<Control-o>", lambda e: load_file())
root.bind("<Control-s>", lambda e: save_file())
root.bind("<Control-q>", lambda e: exit_app())
root.bind("<Control-z>", lambda e: undo_text())
root.bind("<Control-y>", lambda e: redo_text())
root.bind("<Control-a>", lambda e: select_all())
```

#### Menu Callbacks

```python
def run_code():
    code = editor_text.get("1.0", tk.END)
    language = language_var.get().lower()
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, "🚀 Running program...\\n\\n")
    
    try:
        interpreter.ide_turtle_canvas = turtle_canvas
        interpreter.run_program(code, language=language)
        output_text.insert(tk.END, "\\n✅ Program completed.\\n")
    except Exception as e:
        output_text.insert(tk.END, f"\\n❌ Error: {e}\\n")
```

---

## Data Flow

### Program Execution Data Flow

```
User Action (F5)
    │
    ▼
Time_Warp.py: run_code()
    │
    ├─→ Get code from editor_text widget
    ├─→ Get language from dropdown
    └─→ Clear output display
    │
    ▼
interpreter.run_program(code, language)
    │
    ├─→ Select language executor
    ├─→ Parse program into commands
    └─→ Execute each command
        │
        ├─→ Update variables
        ├─→ Call turtle graphics methods
        └─→ Generate output
            │
            ▼
interpreter.log_output(text)
    │
    ▼
output_widget.insert(tk.END, text)
    │
    ▼
Display updates in GUI
```

### Turtle Graphics Data Flow

```
Logo/BASIC Command (e.g., FORWARD 100)
    │
    ▼
Language Executor
    │
    ├─→ Parse command and arguments
    └─→ interpreter.turtle_forward(100)
        │
        ├─→ Calculate new position
        ├─→ Update turtle_graphics state
        ├─→ If pen_down:
        │   └─→ ide_turtle_canvas.create_line(...)
        └─→ update_turtle_display()
            │
            ├─→ Delete old turtle image
            └─→ Draw new turtle at new position
```

---

## Extension Points

### Adding a New Language

1. **Create Executor File**
   ```python
   # core/languages/mylang.py
   class TwMyLangExecutor:
       def __init__(self, interpreter):
           self.interpreter = interpreter
           
       def execute_command(self, command):
           # Parse and execute command
           return "continue"
   ```

2. **Register in Interpreter**
   ```python
   # In core/interpreter.py run_program()
   elif language == "mylang":
       from core.languages.mylang import TwMyLangExecutor
       executor = TwMyLangExecutor(self)
       # Execute program
   ```

3. **Add to GUI**
   ```python
   # In Time_Warp.py
   language_selector = tk.OptionMenu(
       editor_header,
       language_var,
       "PILOT", "BASIC", "Logo", ..., "MyLang"
   )
   ```

4. **Add Examples**
   ```bash
   mkdir examples/mylang
   # Add example programs
   ```

### Adding New Turtle Commands

Add methods to `Time_WarpInterpreter`:

```python
def turtle_circle(self, radius):
    """Draw a circle with the turtle"""
    # Implementation here
    
def turtle_dot(self, size):
    """Draw a dot at current position"""
    # Implementation here
```

Then call from language executors:

```python
elif cmd == "CIRCLE":
    radius = float(parts[1]) if len(parts) > 1 else 50
    self.interpreter.turtle_circle(radius)
```

---

## Performance Considerations

### Optimization Strategies

1. **Canvas Drawing**
   - Use `create_line()` instead of pixel-by-pixel drawing
   - Batch canvas updates when possible
   - Delete old turtle with tags instead of clearing entire canvas

2. **Text Output**
   - Buffer output and update GUI in chunks
   - Limit output size to prevent GUI lag
   - Use `update_idletasks()` for responsive UI

3. **Command Parsing**
   - Pre-split commands into tokens
   - Cache compiled regular expressions
   - Use string methods instead of regex when possible

4. **Memory Management**
   - Limit turtle graphics line history
   - Clear canvas periodically for long-running programs
   - Release references to old widgets

### Bottlenecks

**Known Performance Issues:**

1. **Tkinter Canvas** - Slow for many objects (>10,000 lines)
   - *Solution:* Implement canvas clearing or use PIL/pygame backend

2. **Text Widget Updates** - Can lag with large output
   - *Solution:* Limit output or use scrolling buffer

3. **Subprocess Overhead** - Python/JS execution has startup cost
   - *Solution:* Persistent subprocess for repeated execution

---

## Testing

### Manual Testing

1. **Language Testing** - Run all example programs
2. **Turtle Graphics** - Verify coordinate system
3. **GUI Testing** - Test all menus and buttons
4. **Error Handling** - Try invalid syntax in each language

### Automated Testing

```python
# tests/test_interpreter.py
import pytest
from core.interpreter import Time_WarpInterpreter

def test_logo_forward():
    interp = Time_WarpInterpreter()
    interp.init_turtle_graphics()
    interp.turtle_forward(100)
    assert interp.turtle_graphics["x"] == 0
    assert interp.turtle_graphics["y"] == 100
```

---

## Debugging

### Debug Mode

Enable debug output:

```python
interpreter = Time_WarpInterpreter()
interpreter.debug_mode = True
```

This prints internal state changes to console.

### Common Debug Points

1. **Command Parsing** - Print `parts` array
2. **Variable State** - Print `interpreter.variables`
3. **Turtle Position** - Print `turtle_graphics` dict
4. **Execution Flow** - Print each command before execution

---

**For More Information:**

- [Developer Guide](DEVELOPER_GUIDE.md) - Contributing guidelines
- [API Reference](API_REFERENCE.md) - Complete API documentation
- [Language Implementation](LANGUAGE_IMPLEMENTATION.md) - Detailed language specs

---

© 2025 Time_Warp Project | Technical Documentation
