"""
Dialog windows for Time Warp Classic.

Find, Replace, Error History, and About dialogs.
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox


class FindDialog:
    """Find dialog for searching text in the editor."""

    def __init__(self, parent, editor_text, output_text):
        self.editor = editor_text
        self.output = output_text

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Find")
        self.dialog.geometry("400x150")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Search term
        tk.Label(self.dialog, text="Find:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(
            self.dialog, textvariable=self.search_var, width=30
        )
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        self.search_entry.focus()

        # Options
        options_frame = tk.Frame(self.dialog)
        options_frame.grid(row=1, column=0, columnspan=2, pady=5)

        self.case_var = tk.BooleanVar()
        self.whole_var = tk.BooleanVar()
        self.regex_var = tk.BooleanVar()

        tk.Checkbutton(options_frame, text="Case sensitive", variable=self.case_var).pack(
            side=tk.LEFT, padx=5
        )
        tk.Checkbutton(options_frame, text="Whole word", variable=self.whole_var).pack(
            side=tk.LEFT, padx=5
        )
        tk.Checkbutton(options_frame, text="Regex", variable=self.regex_var).pack(
            side=tk.LEFT, padx=5
        )

        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Find", command=self._do_find, width=10).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(button_frame, text="Find Next", command=self._do_find, width=10).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(
            button_frame, text="Close", command=self.dialog.destroy, width=10
        ).pack(side=tk.LEFT, padx=5)

        self.search_entry.bind("<Return>", lambda e: self._do_find())
        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())

    def _do_find(self):
        search_term = self.search_var.get()
        if not search_term:
            return
        self.editor.clear_search_highlights()
        match = self.editor.find_text(
            search_term,
            start_pos=self.editor.index(tk.INSERT),
            case_sensitive=self.case_var.get(),
            whole_word=self.whole_var.get(),
            regex=self.regex_var.get(),
        )
        if match:
            start_idx, end_idx = match
            self.editor.tag_remove("sel", "1.0", tk.END)
            self.editor.tag_add("sel", start_idx, end_idx)
            self.editor.mark_set(tk.INSERT, end_idx)
            self.editor.see(start_idx)
            self.editor.highlight_search_results(
                search_term,
                case_sensitive=self.case_var.get(),
                whole_word=self.whole_var.get(),
                regex=self.regex_var.get(),
            )
            self.output.insert(tk.END, f"Found '{search_term}' at {start_idx}\n")
        else:
            self.output.insert(tk.END, f"'{search_term}' not found\n")


class ReplaceDialog:
    """Find and replace dialog."""

    def __init__(self, parent, editor_text, output_text):
        self.editor = editor_text
        self.output = output_text

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Replace")
        self.dialog.geometry("400x180")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Search term
        tk.Label(self.dialog, text="Find:").grid(
            row=0, column=0, padx=5, pady=5, sticky="e"
        )
        self.search_var = tk.StringVar()
        tk.Entry(self.dialog, textvariable=self.search_var, width=30).grid(
            row=0, column=1, padx=5, pady=5
        )

        # Replace term
        tk.Label(self.dialog, text="Replace:").grid(
            row=1, column=0, padx=5, pady=5, sticky="e"
        )
        self.replace_var = tk.StringVar()
        tk.Entry(self.dialog, textvariable=self.replace_var, width=30).grid(
            row=1, column=1, padx=5, pady=5
        )

        # Options
        options_frame = tk.Frame(self.dialog)
        options_frame.grid(row=2, column=0, columnspan=2, pady=5)

        self.case_var = tk.BooleanVar()
        self.whole_var = tk.BooleanVar()
        self.regex_var = tk.BooleanVar()

        tk.Checkbutton(options_frame, text="Case sensitive", variable=self.case_var).pack(
            side=tk.LEFT, padx=5
        )
        tk.Checkbutton(options_frame, text="Whole word", variable=self.whole_var).pack(
            side=tk.LEFT, padx=5
        )
        tk.Checkbutton(options_frame, text="Regex", variable=self.regex_var).pack(
            side=tk.LEFT, padx=5
        )

        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(button_frame, text="Replace", command=self._do_replace, width=10).pack(
            side=tk.LEFT, padx=5
        )
        tk.Button(
            button_frame, text="Replace All", command=self._replace_all, width=10
        ).pack(side=tk.LEFT, padx=5)
        tk.Button(
            button_frame, text="Close", command=self.dialog.destroy, width=10
        ).pack(side=tk.LEFT, padx=5)

        self.dialog.bind("<Escape>", lambda e: self.dialog.destroy())

    def _do_replace(self):
        search_term = self.search_var.get()
        replace_term = self.replace_var.get()
        if not search_term:
            return
        replaced = self.editor.replace_text(
            search_term,
            replace_term,
            start_pos=self.editor.index(tk.INSERT),
            case_sensitive=self.case_var.get(),
            whole_word=self.whole_var.get(),
            regex=self.regex_var.get(),
        )
        if replaced:
            self.output.insert(
                tk.END, f"Replaced '{search_term}' with '{replace_term}'\n"
            )
            self.editor.highlight_search_results(
                search_term,
                case_sensitive=self.case_var.get(),
                whole_word=self.whole_var.get(),
                regex=self.regex_var.get(),
            )
        else:
            self.output.insert(tk.END, f"'{search_term}' not found\n")

    def _replace_all(self):
        search_term = self.search_var.get()
        replace_term = self.replace_var.get()
        if not search_term:
            return
        count = self.editor.replace_all(
            search_term,
            replace_term,
            case_sensitive=self.case_var.get(),
            whole_word=self.whole_var.get(),
            regex=self.regex_var.get(),
        )
        self.output.insert(
            tk.END,
            f"Replaced {count} occurrence(s) of '{search_term}' with '{replace_term}'\n",
        )
        self.editor.clear_search_highlights()


def show_error_history(parent, interpreter):
    """Show the error history in a dialog."""
    if not hasattr(interpreter, "error_history") or not interpreter.error_history:
        messagebox.showinfo("Error History", "No errors recorded.")
        return

    history_text = "Recent Errors:\n\n"
    for i, error in enumerate(interpreter.error_history[-10:], 1):
        history_text += f"{i}. Line {error.get('line', 'N/A')}: {error['message']}\n"

    history_window = tk.Toplevel(parent)
    history_window.title("Error History")
    history_window.geometry("600x400")

    text_widget = scrolledtext.ScrolledText(history_window, wrap=tk.WORD)
    text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    text_widget.insert(tk.END, history_text)
    text_widget.config(state=tk.DISABLED)


def show_about(parent):
    """Show about dialog."""
    sep = "-" * 32
    about_text = (
        f"{sep}\n"
        "Time Warp Classic\n"
        "Version 1.3.0\n\n"
        "Back-to-basics Tkinter IDE for 9 vintage\n"
        "+ modern languages with turtle graphics.\n\n"
        "FEATURES:\n"
        "  \u2022 6 built-in language interpreters\n"
        "  \u2022 3 external runtime executors\n"
        "  \u2022 Syntax highlighting (Pygments)\n"
        "  \u2022 Turtle graphics canvas\n"
        "  \u2022 9 color themes with persistence\n"
        "  \u2022 Customizable fonts\n"
        "  \u2022 Debug tools & error history\n\n"
        "LANGUAGES:\n"
        "  PILOT \u2022 BASIC \u2022 Logo \u2022 Pascal\n"
        "  Prolog \u2022 Forth \u2022 Perl \u2022 Python \u2022 JavaScript\n\n"
        f"{sep}\n"
        "Copyright \u00a9 2025\u20132026 Honey Badger Universe"
    )
    messagebox.showinfo("Time Warp Classic", about_text)
