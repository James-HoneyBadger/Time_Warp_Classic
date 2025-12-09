# Time_Warp - Current Directory Structure

## 📁 Actual Project Organization

The Time_Warp interpreter follows a clean, organized structure focused on educational programming:

```
Time_Warp_Classic/                     # Root project directory
├── 📄 Time_Warp.py                    # Unified entry point with dependency checking
├── 📄 timewarp                        # CLI wrapper script
├── 📄 README.md                       # Main project documentation
├── 📄 requirements.txt                # Python dependencies
├── 📄 pyproject.toml                  # Modern Python configuration
├── 📄 .flake8                         # Code linting configuration
├── 📄 .gitignore                      # Git ignore patterns
├── 📄 .pre-commit-config.yaml         # Pre-commit hooks
│
├── 📁 core/                           # Core interpreter system
│   ├── 📄 __init__.py                 # Core module initialization
│   ├── 📄 interpreter.py              # Central execution engine
│   ├── 📁 languages/                  # Language-specific executors
│   │   ├── 📄 __init__.py
│   │   ├── 📄 basic.py                # TW BASIC (Turbo BASIC)
│   │   ├── 📄 forth.py                # Forth stack-based
│   │   ├── 📄 javascript.py           # JavaScript execution
│   │   ├── 📄 javascript_executor.py  # JS execution wrapper
│   │   ├── 📄 logo.py                 # Logo turtle graphics
│   │   ├── 📄 pascal.py               # Pascal structured
│   │   ├── 📄 perl.py                 # Perl text processing
│   │   ├── 📄 pilot.py                # PILOT educational
│   │   ├── 📄 prolog.py               # Prolog logic
│   │   ├── 📄 python.py               # Python execution
│   │   └── 📄 python_executor.py      # Python execution wrapper
│   ├── 📁 features/                   # Advanced features
│   │   └── 📄 code_templates.py       # Code template system
│   └── 📁 utilities/                  # Helper utilities
│       └── 📄 __init__.py
│
├── 📁 docs/                           # Documentation
│   ├── 📄 README.md                   # Documentation index
│   ├── 📄 CLI.md                      # CLI documentation
│   ├── 📄 CHANGELOG.md                # Version history
│   ├── 📄 LICENSE                     # Project license
│   ├── 📄 MODULAR_ARCHITECTURE.md     # Architecture documentation
│   ├── 📄 PROJECT_STRUCTURE.md        # Project structure guide
│   ├── 📄 DIRECTORY_STRUCTURE.md      # This file
│   ├── 📄 GITHUB_INTEGRATION.md       # GitHub integration
│   ├── 📄 DEMO_GAMES.md               # Game demonstrations
│   ├── 📄 VERSION_1_1_ROADMAP.md      # Development roadmap
│   ├── 📄 compiler.md                 # Compiler documentation
│   ├── 📄 README_v11.md               # Version 1.1 README
│   ├── 📁 developer-guide/            # Developer documentation
│   │   └── 📄 CONTRIBUTING.md         # Contributing guidelines
│   ├── 📁 development/                # Development docs
│   │   └── 📄 FILE_ORGANIZATION.md    # File organization guide
│   ├── 📁 guides/                     # General guides
│   │   ├── 📄 GITHUB_RELEASE_ASSETS.md
│   │   └── 📄 GITHUB_RELEASE_UPDATE_INSTRUCTIONS.md
│   ├── 📁 languages/                  # Language-specific guides
│   │   ├── 📄 basic.md                # BASIC language guide
│   │   ├── 📄 logo.md                 # Logo language guide
│   │   ├── 📄 pilot.md                # PILOT language guide
│   │   └── 📄 PILOT_EXTENDED_COMMANDS.md
│   ├── 📁 releases/                   # Release documentation
│   │   ├── 📄 GITHUB_RELEASE_INSTRUCTIONS.md
│   │   ├── 📄 RELEASE_NOTES_v1.2.0.md
│   │   ├── 📄 RELEASE_NOTES_v1.3.0.md
│   │   ├── 📄 RELEASE_READY_v1.2.0.md
│   │   └── 📄 RELEASE_UPDATE_STEPS.md
│   └── 📁 reports/                    # Project reports
│       ├── 📄 CRISIS_RESOLUTION_SUCCESS.md
│       ├── 📄 GITHUB_PUSH_ISSUE_RESOLVED.md
│       ├── 📄 ISSUES_RESOLVED.md
│       └── 📄 VSCODE_DEBUG_FIX.md
│
├── 📁 examples/                       # Sample programs
│   ├── 📄 README.md                   # Examples documentation
│   ├── 📄 PROGRAMS_INDEX.md           # Program index
│   ├── 📁 basic/                      # BASIC example programs
│   ├── 📁 forth/                      # Forth example programs
│   ├── 📁 javascript/                 # JavaScript example programs
│   ├── 📁 logo/                       # Logo example programs
│   ├── 📁 pascal/                     # Pascal example programs
│   ├── 📁 perl/                       # Perl example programs
│   ├── 📁 pilot/                      # PILOT example programs
│   ├── 📁 prolog/                     # Prolog example programs
│   └── 📁 python/                     # Python example programs
│
├── 📁 scripts/                        # Development scripts
│   ├── 📄 README.md                   # Scripts documentation
│   ├── 📄 timewarp-cli.py             # CLI implementation
│   ├── 📄 create_github_release.sh
│   ├── 📄 install_dependencies.py
│   ├── 📄 integration_tests.py
│   ├── 📄 launch.py
│   ├── 📄 launch_Time_Warp.sh
│   ├── 📄 prepare_release.sh
│   ├── 📄 run_all_tests.py
│   ├── 📄 run_tests.py
│   ├── 📄 run_tests_ci.py
│   ├── 📄 run_tests_minimal.py
│   ├── 📄 run_tests_production.py
│   ├── 📄 run_tests_ultra_minimal.py
│   ├── 📄 setup.py
│   ├── 📄 setup_dev.sh
│   ├── 📄 standardize_names.py
│   └── 📄 start.sh
│
└── 📁 src/                            # Extended features (future)
    └── 📁 timewarp/                   # Extended Time_Warp package
        ├── 📄 __init__.py
        ├── 📄 main.py
        ├── 📁 core/
        ├── 📁 games/
        ├── 📁 gui/
        └── 📁 utils/
```

## 📋 Directory Descriptions

### Core Components
- **`core/`**: The heart of Time_Warp - interpreter and language executors
- **`Time_Warp.py`**: Main GUI application using Tkinter
- **`timewarp`**: CLI wrapper for command-line usage

### Documentation
- **`docs/`**: Comprehensive documentation covering all aspects
- **Language guides** in `docs/languages/` for each supported language
- **Developer docs** in `docs/developer-guide/` and `docs/development/`

### Examples & Samples
- **`examples/`**: Sample programs for all supported languages

### Development Tools
- **`scripts/`**: Utility scripts for development, testing, and deployment
- **Build and test scripts** for CI/CD integration

### Future Extensions
- **`src/timewarp/`**: Placeholder for extended features and advanced capabilities
│   └── 📁 v1.1/                       # Version 1.1 release files
│
├── 📁 .github/                        # GitHub configuration
│   ├── 📄 copilot-instructions.md     # GitHub Copilot guide
│   └── 📁 workflows/                  # CI/CD automation workflows
│
├── 📁 .vscode/                        # VS Code configuration
├── 📁 .Time_Warp/                     # Application data directory
└── 📁 .venv/                          # Python virtual environment
```

## 🎯 Key Architecture Highlights

### Professional Python Package Structure
- **src/timewarp/** - Modern Python package layout following best practices
- **Proper entry points** - `Time_Warp.py` main entry, `src/timewarp/main.py` core app
- **Clean separation** - Core logic, GUI, utilities, and games properly separated

### Educational Focus
- **Multi-language support** - PILOT, BASIC, Logo, Python, JavaScript, Perl
- **Visual programming** - Turtle graphics for immediate feedback
- **Comprehensive examples** - 50+ sample programs across all languages
- **Progressive learning** - From simple to advanced concepts

### Professional Development
- **Modern configuration** - pyproject.toml, pytest.ini, pre-commit hooks
- **Comprehensive testing** - Unit, integration, and verification tests
- **Clean documentation** - Organized guides for users and developers

### Project Management
- **Marketing ready** - Complete promotional materials and outreach
- **Release management** - Structured release process and documentation
- **CI/CD pipeline** - GitHub workflows for automation
- **Professional standards** - Code quality, testing, and documentation

## 📊 Project Statistics

| Category | Count | Description |
|----------|-------|-------------|
| **Languages Supported** | 6 | PILOT, BASIC, Logo, Python, JavaScript, Perl |
| **Built-in Themes** | 8 | 4 dark themes, 4 light themes |
| **Example Programs** | 50+ | Educational demonstrations |
| **Test Modules** | 30+ | Comprehensive test coverage |
| **Documentation Files** | 25+ | User and developer guides |

## 🚀 Usage Patterns

### Direct Execution
```bash
python Time_Warp.py        # Main entry point
python -m src.timewarp.main # Module execution
```

### Development Scripts
```bash
python scripts/launch.py   # Cross-platform launcher
./scripts/start.sh         # Quick start script
python scripts/run_all_tests.py # Test execution
```

### Package Installation
```bash
pip install -e .           # Development installation
pip install timewarp       # Production installation (future)
```

## 🔧 Maintenance Guidelines

### Directory Organization Principles
1. **Single Responsibility** - Each directory has a clear, focused purpose
2. **Separation of Concerns** - Source code, tests, docs, and scripts separated
3. **Professional Standards** - Following Python package best practices
4. **Educational Focus** - All organization supports learning goals

### File Naming Conventions
- **Source files** - Clear, descriptive names following Python conventions
- **Test files** - `test_*.py` for unit tests, organized by category
- **Documentation** - Uppercase for main docs, lowercase for specific guides
- **Examples** - Language-specific directories with descriptive filenames

This clean, professional structure makes Time_Warp maintainable, contributor-friendly, and ready for serious educational use and distribution.