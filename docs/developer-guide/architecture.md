# Time_Warp - Actual Architecture

## 🎯 Simple, Educational Interpreter Architecture

Time_Warp is a straightforward educational programming environment built with Python. It supports 9 programming languages through a unified interpreter system with turtle graphics capabilities.

## 🧩 Core Architecture Components

### 🎯 **Central Interpreter (`core/interpreter.py`)**

The heart of Time_Warp is a single `Time_WarpInterpreter` class that:
- Manages execution context across all supported languages
- Provides unified error handling and output formatting
- Integrates turtle graphics canvas for visual programming
- Handles file loading and program execution

### 🗣️ **Language Executors (`core/languages/`)**

Each language has a dedicated executor class following a consistent pattern:

```python
class LanguageExecutor:
    def execute_command(self, command: str) -> str:
        # Parse and execute language-specific commands
        # Return formatted output or error messages
        pass
```

**Supported Languages:**
- **PILOT** (`pilot.py`) - Educational language with turtle graphics
- **BASIC** (`basic.py`) - Line-numbered procedural programming
- **Logo** (`logo.py`) - Turtle graphics with procedures
- **Python** (`python.py` + `python_executor.py`) - Full Python execution
- **JavaScript** (`javascript.py` + `javascript_executor.py`) - JavaScript runtime
- **Perl** (`perl.py`) - Text processing and scripting
- **Pascal** (`pascal.py`) - Structured programming
- **Prolog** (`prolog.py`) - Logic programming
- **Forth** (`forth.py`) - Stack-based programming

### 🎨 **User Interface System**

**Entry Point (`Time_Warp.py`)**:
- Dependency checking and validation
- CLI interface (default mode)
- Unified application launcher

**CLI Interface (`scripts/timewarp-cli.py`)**:
- Command-line program execution
- Syntax-highlighted code display
- Text-based turtle graphics output

## 🏗️ **Design Principles**

### Educational Focus
- **Command-Line Interface** - Simple CLI for program execution and testing
- **Immediate Feedback** - Real-time execution and visual output
- **Progressive Learning** - Languages from simple (PILOT) to advanced (Python)
- **Comprehensive Examples** - Sample programs for each language
- **Flexible Usage** - CLI-based with batch processing capabilities

### Maintainable Code
- **Single Responsibility** - Each language executor handles one language
- **Consistent Patterns** - All executors follow the same interface
- **Clear Separation** - Entry point, CLI, interpreter, and languages are distinct
- **Modular Design** - Components can be developed independently
- **Unified Entry** - Single entry point with mode selection

## 📊 **Technical Specifications**

### Language Support Matrix

| Language | Status | Turtle Graphics | Examples |
|----------|--------|-----------------|----------|
| **PILOT** | ✅ Complete | ✅ | 10+ programs |
| **BASIC** | ✅ Complete | ✅ | 8+ programs |
| **Logo** | ✅ Complete | ✅ | 6+ programs |
| **Python** | ✅ Complete | ✅ | 5+ programs |
| **JavaScript** | ✅ Complete | ✅ | 3+ programs |
| **Perl** | ✅ Complete | ✅ | 2+ programs |
| **Pascal** | ✅ Complete | ✅ | 2+ programs |
| **Prolog** | ✅ Complete | ✅ | 1+ programs |
| **Forth** | ✅ Complete | ✅ | 1+ programs |

### Code Statistics
- **Core Modules**: ~15 Python files
- **Language Executors**: 9 dedicated classes
- **Test Coverage**: Basic integration tests
- **Documentation**: Comprehensive user and developer guides
- **Example Programs**: 40+ educational demonstrations

## 🔄 **Execution Flow**

### Program Execution
1. **Code Input** → User provides code via CLI or file
2. **Language Detection** → Interpreter identifies target language
3. **Command Parsing** → Language executor processes commands
4. **Execution** → Commands run with turtle graphics integration
5. **Output Display** → Results shown in terminal and graphics window

### Component Communication
- **CLI** calls `interpreter.execute()` with code
- **Interpreter** dispatches to appropriate language executor
- **Executor** returns formatted output or error messages
- **CLI** displays results and manages turtle graphics window

## 🎯 **Extension Mechanisms**

### Adding New Languages
1. Create executor class in `core/languages/new_lang.py`
2. Implement `execute_command(command: str) -> str` method
3. Register in interpreter's language mapping
4. Add syntax highlighting support to CLI interface

### CLI Extensions
- Extend command-line interface with new commands
- Add support for additional file formats and languages

## 🚀 **Current Capabilities**

### Core Features
- **Multi-language Support** - 9 programming languages
- **Turtle Graphics** - Visual programming with immediate feedback
- **File Operations** - Load/save programs with proper extensions
- **Syntax Highlighting** - Pygments-based highlighting for all supported languages

### Educational Value
- **Progressive Difficulty** - From simple PILOT to full Python
- **Visual Learning** - Turtle graphics for algorithmic thinking
- **Interactive Environment** - Real-time execution and experimentation
- **Comprehensive Examples** - Learn by studying working programs

---

This architecture prioritizes simplicity, educational effectiveness, and maintainability over complex features. The system successfully teaches programming concepts through multiple languages while remaining easy to understand and extend.