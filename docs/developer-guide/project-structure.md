# Time_Warp - Current Project Structure

## 📁 Actual Directory Organization

### Root Directory
```
Time_Warp_Classic/
├── Time_Warp.py              # Unified entry point with dependency checking
├── timewarp                  # CLI wrapper script (executable)
├── README.md                 # Main project documentation
├── requirements.txt          # Python dependencies
├── pyproject.toml           # Modern Python project configuration
├── .flake8                  # Code linting configuration
├── .gitignore               # Git ignore patterns
├── .pre-commit-config.yaml  # Pre-commit hooks
├── .mypy_cache/             # MyPy type checking cache
├── .venv/                   # Virtual environment (auto-created)
├── .vscode/                 # VS Code workspace settings
├── __pycache__/             # Python bytecode cache
└── .git/                    # Git repository
```

### Core Interpreter System
```
core/
├── __init__.py              # Core module initialization
├── interpreter.py           # Central execution engine for all languages
├── languages/               # Language-specific executors
│   ├── __init__.py
│   ├── basic.py             # TW BASIC with Turbo BASIC extensions
│   ├── forth.py             # Forth stack-based programming
│   ├── javascript.py        # JavaScript execution
│   ├── javascript_executor.py # JS execution wrapper
│   ├── logo.py              # Logo turtle graphics
│   ├── pascal.py            # Pascal structured programming
│   ├── perl.py              # Perl text processing
│   ├── pilot.py             # PILOT educational language
│   ├── prolog.py            # Prolog logic programming
│   ├── python.py            # Python execution
│   └── python_executor.py   # Python execution wrapper
├── features/                # Advanced features
│   └── code_templates.py    # Code template system
└── utilities/               # Helper utilities
    └── __init__.py
```

### Documentation
```
docs/
├── README.md                # Documentation index
├── CLI.md                   # CLI documentation
├── CHANGELOG.md             # Version history
├── LICENSE                  # Project license
├── MODULAR_ARCHITECTURE.md  # Architecture documentation
├── PROJECT_STRUCTURE.md     # This file
├── DIRECTORY_STRUCTURE.md   # Directory organization
├── GITHUB_INTEGRATION.md    # GitHub integration
├── DEMO_GAMES.md            # Game demonstrations
├── VERSION_1_1_ROADMAP.md    # Development roadmap
├── compiler.md              # Compiler documentation
├── developer-guide/
│   └── CONTRIBUTING.md      # Contributing guidelines
├── development/
│   └── FILE_ORGANIZATION.md  # File organization guide
├── guides/
│   ├── GITHUB_RELEASE_ASSETS.md
│   └── GITHUB_RELEASE_UPDATE_INSTRUCTIONS.md
├── languages/
│   ├── basic.md             # BASIC language guide
│   ├── logo.md              # Logo language guide
│   ├── pilot.md             # PILOT language guide
│   └── PILOT_EXTENDED_COMMANDS.md
├── releases/
│   ├── GITHUB_RELEASE_INSTRUCTIONS.md
│   ├── RELEASE_NOTES_v1.2.0.md
│   ├── RELEASE_NOTES_v1.3.0.md
│   ├── RELEASE_READY_v1.2.0.md
│   └── RELEASE_UPDATE_STEPS.md
└── reports/
    ├── CRISIS_RESOLUTION_SUCCESS.md
    ├── GITHUB_PUSH_ISSUE_RESOLVED.md
    ├── ISSUES_RESOLVED.md
    └── VSCODE_DEBUG_FIX.md
```

### Example Programs
```
examples/
├── README.md                # Examples documentation
├── PROGRAMS_INDEX.md        # Program index
├── basic/                   # BASIC example programs
├── forth/                   # Forth example programs
├── javascript/              # JavaScript example programs
├── logo/                    # Logo example programs
├── pascal/                  # Pascal example programs
├── perl/                    # Perl example programs
├── pilot/                   # PILOT example programs
└── python/                  # Python example programs
```

### Development Scripts
```
scripts/
├── README.md                # Scripts documentation
├── timewarp-cli.py          # CLI implementation
├── create_github_release.sh
├── install_dependencies.py
├── integration_tests.py
├── launch.py
├── launch_Time_Warp.sh
├── prepare_release.sh
├── run_all_tests.py
├── run_tests.py
├── run_tests_ci.py
├── run_tests_minimal.py
├── run_tests_production.py
├── run_tests_ultra_minimal.py
├── setup.py
├── setup_dev.sh
├── standardize_names.py
└── start.sh
```

### Development & Testing
```
scripts/                    # Development scripts
├── README.md               # Scripts documentation
├── prepare_release.sh      # Release preparation
├── run_all_tests.py        # Master test runner
├── run_tests.py            # Basic test runner
├── run_tests_ci.py         # CI/CD test runner
├── setup.py                # Installation script
├── install_dependencies.py # Dependency installer
├── launch.py               # Python launcher
├── launch_Time_Warp.sh     # Shell launcher
├── launch_Time_Warp.bat    # Windows launcher
├── start.sh                # Quick start script
├── build/                  # Build-related scripts
└── development/            # Development utilities

tests/                      # Test suite organization
├── README.md               # Testing documentation
├── unit/                   # Unit tests
├── integration/            # Integration tests
├── fixtures/               # Test data and fixtures
├── verification/           # Verification test suite
├── sample_outputs/         # Test output samples
├── test_results/           # Test execution results
├── tests/                  # Additional test modules
├── test_*.py               # Individual test modules
├── theme_test.py           # Theme testing
└── verify_working.py       # Working verification
```

### Documentation (Organized)
```
docs/                       # Documentation files
├── PROJECT_STRUCTURE.md    # This file - project organization
├── README_v11.md           # Version 1.1 features
├── DIRECTORY_STRUCTURE.md  # Directory organization guide
├── MODULAR_ARCHITECTURE.md # Architecture documentation
├── GITHUB_INTEGRATION.md   # GitHub integration guide
├── VERSION_1_1_ROADMAP.md  # Development roadmap
├── LICENSE                 # MIT license
├── compiler.md             # Compiler documentation
├── user-guide/             # End-user documentation
├── developer-guide/        # Contributing and development docs
├── api/                    # API reference documentation
├── languages/              # Language-specific guides
├── development/            # Development documentation
├── guides/                 # General guides
├── reports/                # Project and development reports
└── releases/               # Release documentation
```

### Example Programs
```
examples/                   # Sample programs and tutorials
├── README.md               # Examples documentation
├── PROGRAMS_INDEX.md       # Program index and descriptions
├── BASIC/                  # BASIC language examples
├── Logo/                   # Logo turtle graphics examples
├── PILOT/                  # PILOT educational examples
├── Python/                 # Python scripting examples
├── basic/                  # Additional BASIC examples
├── logo/                   # Additional Logo examples
├── pilot/                  # Additional PILOT examples
├── games/                  # Game development examples
├── sample_*.py             # Sample program files
└── analysis_results.json   # Program analysis results
```

### Marketing & Community
```
marketing/                  # Marketing materials and outreach
├── README.md               # Marketing documentation
├── marketing_summary.md    # Marketing strategy summary
├── graphics/               # Marketing graphics and assets
├── social_media/           # Social media content
├── devto_article.md        # Dev.to article content
├── educational_outreach_email.txt # Educational outreach
└── REDDIT_SIDEPROJECT_ANNOUNCEMENT.md # Reddit announcement
```

### Release Management
```
release/                    # Release management
└── v1.1/                   # Version 1.1 release files
```

### Configuration & Metadata
```
.github/                    # GitHub workflows & templates
.vscode/                    # VS Code configuration
.gitignore                  # Git ignore patterns
.pre-commit-config.yaml     # Pre-commit hooks
.Time_Warp/                 # Application data directory
└── .venv/                  # Python virtual environment
```

## 🎯 Key Files

### Primary Entry Points
- `Time_Warp.py` - Unified entry point with dependency checking
- `src/timewarp/main.py` - Core application module
- `scripts/launch.py` - Cross-platform launcher

### Configuration
- `Time_Warp.code-workspace` - VS Code workspace settings
- `pyproject.toml` - Modern Python project configuration
- `requirements.txt` - Runtime dependencies
- `pytest.ini` - Test configuration

### Testing
- `tests/verification/` - Master verification suite
- `tests/unit/` - Unit test modules
- `tests/integration/` - Integration test modules
- `scripts/run_all_tests.py` - Master test runner

## 🚀 Usage

### Direct Execution
```bash
python Time_Warp.py        # Main entry point
python -m src.timewarp.main # Module execution
```

### Via Scripts
```bash
python scripts/launch.py   # Cross-platform launcher
./scripts/start.sh         # Quick start script
```

### VS Code Integration
- Use Ctrl+F5 or F5 to run/debug
- Pre-configured launch configurations
- Integrated terminal and task support

## 📊 Project Statistics

- **Languages Supported**: 6 (PILOT, BASIC, Logo, Python, JavaScript, Perl)
- **Themes Available**: 8 (4 dark, 4 light)
- **Test Coverage**: 23 comprehensive tests
- **Total Files**: ~200+ organized files
- **Code Quality**: All tests passing ✅

This clean, organized structure makes Time_Warp 1.1 professional, maintainable, and ready for production use.# Time_Warp - Current Directory Structure

## 📁 Actual Project Organization

The Time_Warp follows a clean, organized structure focused on educational programming:

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