"""
Theme definitions and application logic for Time Warp Classic.

Each theme is a dictionary mapping widget roles to color values.
"""

THEMES = {
    "light": {
        "name": "Light",
        "text_bg": "white",
        "text_fg": "black",
        "canvas_bg": "white",
        "canvas_border": "#cccccc",
        "root_bg": "#f0f0f0",
        "frame_bg": "#f0f0f0",
        "editor_frame_bg": "white",
        "editor_frame_fg": "black",
        "input_bg": "white",
        "input_fg": "black",
    },
    "dark": {
        "name": "Dark",
        "text_bg": "#1e1e1e",
        "text_fg": "#d4d4d4",
        "canvas_bg": "#2d2d2d",
        "canvas_border": "#3e3e3e",
        "root_bg": "#252526",
        "frame_bg": "#252526",
        "editor_frame_bg": "#252526",
        "editor_frame_fg": "#d4d4d4",
        "input_bg": "#1e1e1e",
        "input_fg": "#d4d4d4",
    },
    "classic": {
        "name": "Classic",
        "text_bg": "white",
        "text_fg": "black",
        "canvas_bg": "#fffef0",
        "canvas_border": "#cccccc",
        "root_bg": "#e0e0e0",
        "frame_bg": "#e0e0e0",
        "editor_frame_bg": "#e0e0e0",
        "editor_frame_fg": "black",
        "input_bg": "white",
        "input_fg": "black",
    },
    "solarized_dark": {
        "name": "Solarized Dark",
        "text_bg": "#002b36",
        "text_fg": "#839496",
        "canvas_bg": "#073642",
        "canvas_border": "#586e75",
        "root_bg": "#002b36",
        "frame_bg": "#002b36",
        "editor_frame_bg": "#002b36",
        "editor_frame_fg": "#839496",
        "input_bg": "#073642",
        "input_fg": "#839496",
    },
    "solarized_light": {
        "name": "Solarized Light",
        "text_bg": "#fdf6e3",
        "text_fg": "#657b83",
        "canvas_bg": "#eee8d5",
        "canvas_border": "#93a1a1",
        "root_bg": "#fdf6e3",
        "frame_bg": "#fdf6e3",
        "editor_frame_bg": "#fdf6e3",
        "editor_frame_fg": "#657b83",
        "input_bg": "#eee8d5",
        "input_fg": "#657b83",
    },
    "monokai": {
        "name": "Monokai",
        "text_bg": "#272822",
        "text_fg": "#f8f8f2",
        "canvas_bg": "#3e3d32",
        "canvas_border": "#75715e",
        "root_bg": "#272822",
        "frame_bg": "#272822",
        "editor_frame_bg": "#272822",
        "editor_frame_fg": "#f8f8f2",
        "input_bg": "#3e3d32",
        "input_fg": "#f8f8f2",
    },
    "dracula": {
        "name": "Dracula",
        "text_bg": "#282a36",
        "text_fg": "#f8f8f2",
        "canvas_bg": "#44475a",
        "canvas_border": "#6272a4",
        "root_bg": "#282a36",
        "frame_bg": "#282a36",
        "editor_frame_bg": "#282a36",
        "editor_frame_fg": "#f8f8f2",
        "input_bg": "#44475a",
        "input_fg": "#f8f8f2",
    },
    "nord": {
        "name": "Nord",
        "text_bg": "#2e3440",
        "text_fg": "#d8dee9",
        "canvas_bg": "#3b4252",
        "canvas_border": "#4c566a",
        "root_bg": "#2e3440",
        "frame_bg": "#2e3440",
        "editor_frame_bg": "#2e3440",
        "editor_frame_fg": "#d8dee9",
        "input_bg": "#3b4252",
        "input_fg": "#d8dee9",
    },
    "high_contrast": {
        "name": "High Contrast",
        "text_bg": "black",
        "text_fg": "white",
        "canvas_bg": "#0a0a0a",
        "canvas_border": "white",
        "root_bg": "black",
        "frame_bg": "black",
        "editor_frame_bg": "black",
        "editor_frame_fg": "white",
        "input_bg": "#0a0a0a",
        "input_fg": "white",
    },
}

# Mapping from theme key to line-number background color
LINE_NUMBER_BG = {
    "dark": "#1e1e1e",
    "light": "#f0f0f0",
    "monokai": "#272822",
    "classic": "#ffffff",
    "solarized_dark": "#002b36",
    "solarized_light": "#fdf6e3",
    "dracula": "#282a36",
    "nord": "#2e3440",
    "high_contrast": "#000000",
}

FONT_SIZES = {
    "tiny": {"name": "Tiny (8pt)", "editor": 8, "output": 8},
    "small": {"name": "Small (10pt)", "editor": 10, "output": 9},
    "medium": {"name": "Medium (12pt)", "editor": 12, "output": 11},
    "large": {"name": "Large (14pt)", "editor": 14, "output": 13},
    "xlarge": {"name": "Extra Large (16pt)", "editor": 16, "output": 15},
    "xxlarge": {"name": "Huge (18pt)", "editor": 18, "output": 17},
    "xxxlarge": {"name": "Giant (22pt)", "editor": 22, "output": 20},
}

# Unified extension-to-language mapping (single source of truth)
#
# Canonical extensions (one per language, used in examples and Save dialog):
#   PILOT .pilot | BASIC .bas   | Logo .logo | Python .py  | JavaScript .js
#   Perl  .pl    | Pascal .pas  | Forth .fth | Prolog .pro
#
# Additional accepted extensions are listed after the canonical one.
EXT_TO_LANG = {
    # Canonical first, then alternates
    ".pilot": "PILOT",
    ".pil": "PILOT",
    ".bas": "BASIC",
    ".logo": "Logo",
    ".lgo": "Logo",
    ".py": "Python",
    ".js": "JavaScript",
    ".pl": "Perl",
    ".pm": "Perl",
    ".pas": "Pascal",
    ".pp": "Pascal",
    ".fth": "Forth",
    ".4th": "Forth",
    ".fs": "Forth",
    ".pro": "Prolog",
    ".prolog": "Prolog",
}

SUPPORTED_LANGUAGES = [
    "PILOT", "BASIC", "Logo", "Pascal", "Prolog",
    "Forth", "Perl", "Python", "JavaScript",
]
