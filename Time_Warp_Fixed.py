#!/usr/bin/env python3
"""
Time Warp Classic - Multi-Language Programming Environment (Fixed Version)

A multi-language interpreter supporting 9 classic programming languages
with integrated turtle graphics.

Copyright © 2025 Honey Badger Universe. All rights reserved.
"""

import sys
import json
import subprocess
import os
from pathlib import Path
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog

def main():
    """Main entry point - launches Time Warp Classic."""
    
    print("🚀 Launching Time Warp Classic...")
    try:
        # Import core modules
        from core.interpreter import Time_WarpInterpreter
        from core.features.syntax_highlighting import SyntaxHighlightingText, LineNumberedText
        
        # Import GUI optimizer
        try:
            from core.optimizations.gui_optimizer import initialize_gui_optimizer
            GUI_OPTIMIZATIONS_AVAILABLE = True
        except ImportError:
            GUI_OPTIMIZATIONS_AVAILABLE = False
            initialize_gui_optimizer = None
        
        # Check if pygments is available
        try:
            import pygments
            PYGMENTS_AVAILABLE = True
        except ImportError:
            PYGMENTS_AVAILABLE = False
        
        # Settings file for persistence
        SETTINGS_FILE = Path.home() / ".timewarp_settings.json"
        
        def load_settings():
            """Load user settings from file."""
            try:
                if SETTINGS_FILE.exists():
                    with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                        return json.load(f)
            except Exception:
                pass
            return {"theme": "dark", "font_size": "medium", "font_family": "Courier"}
        
        def save_settings(theme, font_size, font_family):
            """Save user settings to file."""
            try:
                with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                    json.dump({"theme": theme, "font_size": font_size, "font_family": font_family}, f)
            except Exception:
                pass
        
        # Load saved settings
        settings = load_settings()
        current_theme = settings.get("theme", "dark")
        current_font = settings.get("font_size", "medium")
        current_font_family = settings.get("font_family", "Courier")
        
        # Create the main GUI window
        root = tk.Tk()
        root.title("Time Warp Classic - Multi-Language Programming Environment")
        root.geometry("1200x800")
        root.config(bg="#252526")
        
        print("✅ Creating GUI window...")
        
        # Initialize GUI optimizer for performance improvements
        if GUI_OPTIMIZATIONS_AVAILABLE and initialize_gui_optimizer:
            gui_optimizer = initialize_gui_optimizer(root)
            print("🚀 GUI optimizations enabled")
        else:
            gui_optimizer = None
            print("ℹ️  GUI optimizations not available")
        
        # Create a simple frame for testing
        frame = tk.Frame(root, bg="#252526")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        title_label = tk.Label(
            frame,
            text="Time Warp Classic",
            font=("Arial", 24, "bold"),
            bg="#252526",
            fg="#00FF00"
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            frame,
            text="Multi-Language Programming Environment",
            font=("Arial", 12),
            bg="#252526",
            fg="#FFFFFF"
        )
        subtitle_label.pack()
        
        info_label = tk.Label(
            frame,
            text="✅ IDE is running! Development in progress...\n\nSupported Languages:\nPILOT • BASIC • Logo • Pascal • Prolog • Forth • Perl • Python • JavaScript",
            font=("Courier", 10),
            bg="#252526",
            fg="#00FF00",
            justify=tk.LEFT
        )
        info_label.pack(pady=20)
        
        button = tk.Button(
            frame,
            text="Exit",
            command=root.quit,
            bg="#00FF00",
            fg="#000000",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        button.pack()
        
        # Ensure window is visible and focused
        root.deiconify()
        root.lift()
        root.focus_force()
        root.update()
        
        print("✅ GUI window created and displayed")
        print("🎮 Starting event loop...")
        
        # Start the GUI event loop
        root.mainloop()
        print("👋 Time Warp Classic closed")
        sys.exit(0)
        
    except Exception as e:
        print(f"❌ GUI launch failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
