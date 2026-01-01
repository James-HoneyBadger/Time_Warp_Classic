#!/bin/bash
# Quick PyPI Release Script for Time Warp Classic
# Usage: bash release_to_pypi.sh [testpypi|pypi]

set -e

TARGET="${1:-testpypi}"

if [ "$TARGET" != "testpypi" ] && [ "$TARGET" != "pypi" ]; then
    echo "Usage: bash release_to_pypi.sh [testpypi|pypi]"
    echo ""
    echo "Examples:"
    echo "  bash release_to_pypi.sh testpypi  # Upload to test.pypi.org"
    echo "  bash release_to_pypi.sh pypi       # Upload to pypi.org"
    exit 1
fi

# Activate virtual environment if it exists
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
fi

echo "🧹 Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info time_warp.egg-info

echo "🔨 Building distributions..."
python -m build

echo "✅ Validating package..."
twine check dist/* --strict

if [ "$TARGET" = "testpypi" ]; then
    echo "📤 Uploading to TestPyPI..."
    echo "Username: __token__"
    read -sp "Password (PyPI token): " TOKEN
    echo
    twine upload --repository testpypi dist/* -u __token__ -p "$TOKEN"
    echo "✨ Upload to TestPyPI successful!"
    echo "Test installation: pip install --index-url https://test.pypi.org/simple/ time-warp"
else
    echo "📤 Uploading to PyPI..."
    echo "Username: __token__"
    read -sp "Password (PyPI token): " TOKEN
    echo
    twine upload dist/* -u __token__ -p "$TOKEN"
    echo "✨ Upload to PyPI successful!"
    echo "Package URL: https://pypi.org/project/time-warp/"
    echo "Installation: pip install time-warp"
fi
