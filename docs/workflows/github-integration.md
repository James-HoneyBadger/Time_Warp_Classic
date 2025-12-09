# 🔗 Time_Warp - GitHub Integration

## GitHub Repository Overview

Time_Warp is hosted on GitHub as an open-source educational programming project. This guide covers basic Git and GitHub workflows for contributors and users.

## 📥 Getting the Code

### Clone the Repository
```bash
git clone https://github.com/your-username/Time_Warp_Classic.git
cd Time_Warp_Classic
```

### Download ZIP (Alternative)
If you don't want to use Git:
1. Go to the [GitHub repository](https://github.com/your-username/Time_Warp_Classic)
2. Click the green "Code" button
3. Select "Download ZIP"
4. Extract the ZIP file to your desired location

## 🚀 Running Time_Warp

### Basic Startup
```bash
# Navigate to the project directory
cd Time_Warp_Classic

# Run the main GUI application
python Time_Warp.py

# Or use the CLI wrapper
python Time_Warp.py

# Or use the shell script (Linux/macOS)
./scripts/start.sh
```

### Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
python scripts/run_tests.py

# Run a specific test file
python -m pytest tests/test_interpreter.py -v
```

## 🤝 Contributing to the Project

### Fork and Clone
1. Fork the repository on GitHub
2. Clone your fork:
```bash
git clone https://github.com/your-username/Time_Warp_Classic.git
cd Time_Warp_Classic
git remote add upstream https://github.com/original-owner/Time_Warp_Classic.git
```

### Development Workflow
```bash
# Create a feature branch
git checkout -b feature/your-feature-name

# Make your changes
# Edit files, add features, fix bugs

# Test your changes
python scripts/run_tests.py

# Commit your work
git add .
git commit -m "Add: Brief description of your changes"

# Push to your fork
git push origin feature/your-feature-name

# Create a Pull Request on GitHub
```

### Code Standards
- Follow PEP 8 Python style guidelines
- Add docstrings to new functions and classes
- Include tests for new features
- Update documentation for significant changes
- Use meaningful commit messages

## 🐛 Reporting Issues

### Bug Reports
1. Check if the issue already exists in [GitHub Issues](https://github.com/your-username/Time_Warp_Classic/issues)
2. If not, create a new issue with:
   - Clear title describing the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Your system information (OS, Python version)
   - Error messages or screenshots

### Feature Requests
1. Check existing issues for similar requests
2. Create a new issue with:
   - Clear description of the proposed feature
   - Use case or problem it solves
   - Any implementation ideas

## 📚 Documentation Updates

### Updating Docs
The project documentation is in the `docs/` directory. To update:
1. Edit the relevant `.md` files
2. Test that formatting looks correct
3. Commit and create a pull request

### Adding Examples
New example programs go in `examples/` subdirectories:
- `examples/pilot/` for PILOT programs
- `examples/basic/` for BASIC programs
- `examples/logo/` for Logo programs
- etc.

## 🔄 Staying Updated

### Sync with Upstream
```bash
# Fetch latest changes from the main repository
git fetch upstream

# Merge updates into your local main branch
git checkout main
git merge upstream/main

# Update your feature branches
git checkout feature/your-branch
git rebase main
```

### Release Updates
- Watch the repository for new releases
- Check the changelog (`docs/CHANGELOG.md`) for updates
- Update your local copy when new versions are released

## 🏗️ Build and Release Process

### For Maintainers
The `scripts/` directory contains release tools:
- `scripts/prepare_release.sh` - Prepare a new release
- `scripts/create_github_release.sh` - Create GitHub release
- `scripts/run_tests_ci.py` - CI testing script

### Release Checklist
- [ ] Update version numbers in relevant files
- [ ] Update CHANGELOG.md
- [ ] Run full test suite
- [ ] Test on multiple platforms
- [ ] Create GitHub release with release notes
- [ ] Update documentation if needed

## 📞 Getting Help

### Community Support
- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For general questions and discussions
- **Documentation**: Check `docs/` directory first

### Development Help
- **Contributing Guide**: `docs/developer-guide/CONTRIBUTING.md`
- **Code of Conduct**: Standard open-source guidelines
- **Development Docs**: `docs/development/` directory

---

**Time_Warp** is a community-driven project. Contributions, bug reports, and feature requests are welcome! 🎉