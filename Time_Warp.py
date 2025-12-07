#!/usr/bin/env python3
"""
Time_Warp IDE - Simple Educational Programming Environment

A minimal Tkinter-based IDE for running multi-language programs
through the Time_Warp interpreter.

Supports PILOT, BASIC, Logo, Pascal, Prolog, Forth, Perl,
Python, and JavaScript execution.

Features:
- Simple text editor with Courier font
- One-click program execution
- Integrated interpreter with 9+ language support
- Turtle graphics for visual languages
- Educational error messages

Usage:
    python Time_Warp.py

The IDE provides a basic text editing interface where users can
write and execute programs in multiple programming languages with
immediate visual feedback.
"""

import tkinter as tk
from tkinter import messagebox
from core.interpreter import Time_WarpInterpreter


class TimeWarpApp:
    """
    Main application class for the Time_Warp IDE.

    Creates a simple GUI with:
    - Text area for code editing
    - Run button for program execution
    - Integrated Time_Warp interpreter for multi-language support
    """

    def __init__(self, root):
        """
        Initialize the Time_Warp IDE application.

        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("Time_Warp IDE v1.1")
        self.root.geometry("900x700")  # Set reasonable default size
        self.root.configure(bg="#f0f0f0")

        # Create title frame
        title_frame = tk.Frame(root, bg="#2c3e50", height=50)
        title_frame.pack(fill="x")
        title_label = tk.Label(
            title_frame,
            text="🚀 Time_Warp IDE - Multi-Language Programming Environment",
            font=("Arial", 14, "bold"),
            bg="#2c3e50",
            fg="white",
            pady=10,
        )
        title_label.pack()

        # Create language selector frame
        lang_frame = tk.Frame(root, bg="#ecf0f1", height=40)
        lang_frame.pack(fill="x", padx=10, pady=5)
        lang_text = (
            "Language: PILOT, BASIC, Logo, Python, "
            "JavaScript, Perl, Pascal, Forth, Prolog"
        )
        lang_label = tk.Label(
            lang_frame,
            text=lang_text,
            font=("Arial", 10),
            bg="#ecf0f1",
        )
        lang_label.pack(anchor="w")

        # Create main text editing area
        self.text_area = tk.Text(
            root,
            wrap="word",
            font=("Courier", 11),
            undo=True,  # Enable undo/redo
            padx=10,
            pady=10,
            bg="white",
            fg="#333",
            insertbackground="#2c3e50",
            relief="solid",
            borderwidth=1,
        )
        self.text_area.pack(expand=True, fill="both", padx=10, pady=5)

        # Insert welcome text
        welcome_msg = (
            "# Welcome to Time_Warp IDE!\n"
            "# Enter your program below and press F5\n"
            "\n# Example PILOT program:\n"
            "# T: Hello World\n"
            "# A: This is an example\n"
            "# J: _end\n"
            "# _end: T: Done!"
        )
        self.text_area.insert("1.0", welcome_msg)

        # Create button frame
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(fill="x", padx=10, pady=10)

        # Create run button
        self.run_button = tk.Button(
            button_frame,
            text="▶ Run Program (F5)",
            command=self.run_program,
            font=("Arial", 11, "bold"),
            bg="#27ae60",
            fg="white",
            height=2,
            activebackground="#229954",
            relief="raised",
            bd=2,
        )
        self.run_button.pack(side="left", fill="x", expand=True, padx=5)

        # Create clear button
        self.clear_button = tk.Button(
            button_frame,
            text="🗑️ Clear",
            command=self.clear_program,
            font=("Arial", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            height=2,
            activebackground="#c0392b",
            relief="raised",
            bd=2,
        )
        self.clear_button.pack(side="left", fill="x", expand=True, padx=5)

        # Initialize the Time_Warp interpreter
        self.interpreter = Time_WarpInterpreter()

        # Bind keyboard shortcuts
        self.root.bind("<F5>", lambda e: self.run_program())
        self.root.bind("<Control-r>", lambda e: self.run_program())

        # Set up window close handler
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def clear_program(self):
        """Clear the text area."""
        self.text_area.delete("1.0", "end")

    def run_program(self):
        """
        Execute the program currently in the text area.

        Gets the code from the text widget, validates it's not empty,
        and runs it through the Time_Warp interpreter.
        """
        program_code = self.text_area.get("1.0", "end").strip()

        if not program_code:
            msg = (
                "Please enter a program to run.\n\n"
                "Try copying one of the examples from "
                "the README.md file."
            )
            messagebox.showwarning("No Code", msg)
            return

        try:
            # Clear any previous output in interpreter
            # Run the program through the interpreter
            self.interpreter.run_program(program_code)

            # Show success message
            msg = (
                "Program execution finished!\n\n"
                "Check the console output for results."
            )
            messagebox.showinfo("Program Complete", msg)

        except (RuntimeError, ValueError, OSError) as err:
            error_msg = f"An error occurred: {str(err)}"
            messagebox.showerror("Execution Error", error_msg)

    def on_closing(self):
        """Handle window close event."""
        msg = "Do you want to quit Time_Warp IDE?"
        if messagebox.askokcancel("Quit", msg):
            self.root.destroy()


def main():
    """
    Main entry point for the Time_Warp IDE application.

    Creates the Tkinter root window and starts the application.
    """
    root = tk.Tk()
    TimeWarpApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
