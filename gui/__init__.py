"""
Time Warp Classic - GUI Package

Tkinter-based IDE interface for Time Warp Classic.

Components:
- app.py     — TimeWarpApp: main window, layout, code execution
- menus.py   — Menu bar construction (8 cascading menus)
- dialogs.py — Find/Replace, About, error history dialogs
- themes.py  — 9 color themes, font sizes, extension mappings
"""

from gui.app import TimeWarpApp

__all__ = ["TimeWarpApp"]
