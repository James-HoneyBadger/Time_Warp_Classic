#!/usr/bin/env python3
"""
Time_Warp Interpreter - Core Multi-Language Execution Engine

The Time_WarpInterpreter is the central execution engine for the Time_Warp IDE,
providing unified support for 9 programming languages through a single interface.

Supported Languages:
- TW PILOT: Educational language with simple commands (T:, A:, J:, Y:, N:)
- TW BASIC: Classic line-numbered programming (PRINT, LET, GOTO, FOR)
- TW Logo: Turtle graphics programming (FORWARD, RIGHT, REPEAT)
- TW Pascal: Structured programming (BEGIN, END, VAR, PROCEDURE)
- TW Prolog: Logic programming (?- queries, :- rules)
- TW Forth: Stack-based programming (DUP, DROP, SWAP, arithmetic)
- Perl: Modern scripting language
- Python: Full Python execution
- JavaScript: JavaScript execution

Key Features:
- Unified variable management across all languages
- Turtle graphics integration for visual languages
- Expression evaluation with variable interpolation
- Program flow control (jumps, loops, conditionals)
- Error handling and debugging support
- Extensible architecture for adding new languages

The interpreter maintains state across program execution including variables,
program lines, execution position, and turtle graphics state.
"""
# pylint: disable=C0302,C0301,C0103,C0115,C0116,W0613,R0903,C0413,W0718,R0902,R0915,C0415,W0404,W0621,R0913,R0917,R0914,W0612,W0108,W0123,R0911,R0912,R1705,W0611,W0718,R0902,R0915,C0415,W0404,W0621,R0913,R0917,R0914,W0612,W0108,W0123,R0911,R0912,R1705,W0611

import tkinter as tk
from tkinter import simpledialog
import re
import random
import math

# Optional PIL import - gracefully handle missing dependency
PIL_AVAILABLE = False
Image = None
ImageTk = None

try:
    from PIL import Image as PILImage, ImageTk as PILImageTk

    Image = PILImage
    ImageTk = PILImageTk
    PIL_AVAILABLE = True
except ImportError:
    # Create dummy classes to prevent errors when PIL is not available
    class _DummyImage:
        @staticmethod
        def open(path):
            return None

        @staticmethod
        def new(mode, size, color=0):
            return None

    class _DummyImageTk:
        @staticmethod
        def PhotoImage(image=None, file=None):
            return None

    Image = _DummyImage  # type: ignore[assignment]
    ImageTk = _DummyImageTk  # type: ignore[assignment]
    print("ℹ️  PIL/Pillow not available - image features disabled")

# Import language executors
from .languages import (  # noqa: E402
    TwPilotExecutor,
    TwBasicExecutor,
    TwLogoExecutor,
    TwPascalExecutor,
    TwPrologExecutor,
    TwForthExecutor,
    PerlExecutor,
    PythonExecutor,
    JavaScriptExecutor,
)

# Import performance optimizations
try:
    from .optimizations.performance_optimizer import (
        OptimizedInterpreterMixin,  # pylint: disable=unused-import
        performance_optimizer,
        optimize_for_production,
    )

    PERFORMANCE_OPTIMIZATIONS_AVAILABLE = True
except ImportError:
    # Create dummy mixin if optimizations not available
    class _OptimizedInterpreterMixin:  # type: ignore[no-redef]
        def optimized_output(self, text):
            return text

        def cleanup_resources(self):
            return {}

        def get_performance_stats(self):
            return {}

    OptimizedInterpreterMixin = _OptimizedInterpreterMixin

    def optimize_for_production():
        return {}

    performance_optimizer = None
    PERFORMANCE_OPTIMIZATIONS_AVAILABLE = False

# Import supporting classes (will need to be extracted to their own modules later)
try:
    # Try to import from actual modules first
    from games.engine import GameManager  # type: ignore[attr-defined]
    from .audio import AudioEngine  # type: ignore[attr-defined]
    from .hardware import (  # type: ignore[attr-defined]
        RPiController,
        RobotInterface,
        GameController,
        SensorVisualizer,
    )
    from .iot import (  # type: ignore[attr-defined]
        IoTDeviceManager,
        SmartHomeHub,
        SensorNetwork,
    )
    from .utilities import (  # type: ignore[attr-defined]
        Mixer,
        Tween,
        Timer,
        Particle,
    )
    from .networking import CollaborationManager  # type: ignore[attr-defined]

    ArduinoController = None  # Not implemented yet
    AdvancedRobotInterface = None  # Not implemented yet

    # Create MultiplayerGameManager as subclass of GameManager
    class MultiplayerGameManager(GameManager):  # type: ignore[misc,valid-type]
        def __init__(self, *args, **kwargs):
            super().__init__()

except ImportError:
    # Fallback class definitions for missing modules

    class AudioEngine:  # type: ignore[no-redef]
        def __init__(self):
            pass

        def load_audio(self, *args):
            return False

        def play_sound(self, *args):
            return None

        def stop_sound(self, *args):
            return False

        def stop_all_sounds(self):
            pass

        def play_music(self, *args):
            return False

        def stop_music(self, *args):
            return False

        def set_master_volume(self, *args):
            pass

        def set_sound_volume(self, *args):
            pass

        def set_music_volume(self, *args):
            pass

        def get_audio_info(self):
            return {
                "mixer_available": False,
                "loaded_clips": 0,
                "playing_sounds": 0,
                "built_in_sounds": [],
            }

        clips: dict = {}
        sound_library: dict = {}
        spatial_audio = type("", (), {"set_listener_position": lambda *args: None})()

    class GameManager:  # type: ignore[no-redef]
        def __init__(self):
            pass

        def set_output_callback(self, callback):
            pass

        def create_object(self, *args):
            return False

        def move_object(self, *args):
            return False

        def set_gravity(self, *args):
            pass

        def set_velocity(self, *args):
            return False

        def check_collision(self, *args):
            return False

        def render_scene(self, *args):
            return False

        def update_physics(self, *args):
            pass

        def delete_object(self, *args):
            return False

        def list_objects(self):
            return []

        def clear_scene(self):
            pass

        def get_object_info(self, *args):
            return None

        def get_object(self, *args):
            return None

        def add_player(self, *args):
            return False, "Not implemented"

        def remove_player(self, *args):
            return False, "Not implemented"

        def start_multiplayer_game(self):
            return False, "Not implemented"

        def end_multiplayer_game(self, *args):
            return False, "Not implemented"

        def get_game_info(self):
            return {}

        players: dict = {}
        session_id = None
        game_mode = "cooperative"
        max_players = 8
        is_server = False
        game_state = "waiting"

    # In except block, define fallback MultiplayerGameManager
    class MultiplayerGameManager(GameManager):  # type: ignore[misc,no-redef]
        def __init__(self, *args, **kwargs):
            super().__init__()

    class CollaborationManager:  # type: ignore[no-redef]
        def __init__(self):
            self.network_manager = type(
                "",
                (),
                {
                    "start_server": lambda *args: (False, "Not implemented"),
                    "connect_to_server": lambda *args: (False, "Not implemented"),
                    "send_message": lambda *args: None,
                    "disconnect": lambda *args: None,
                    "is_server": False,
                    "is_client": False,
                    "running": False,
                },
            )()

    class ArduinoController:  # type: ignore[no-redef]
        def connect(self, *args):
            return False

        def send_command(self, *args):
            return False

        def read_sensor(self):
            return None

    class RPiController:  # type: ignore[no-redef]
        def set_pin_mode(self, *args):
            return False

        def digital_write(self, *args):
            return False

        def digital_read(self, *args):
            return False

    class RobotInterface:  # type: ignore[no-redef]
        def move_forward(self, *args):
            pass

        def move_backward(self, *args):
            pass

        def turn_left(self, *args):
            pass

        def turn_right(self, *args):
            pass

        def stop(self):
            pass

        def read_distance_sensor(self):
            return 30.0

        def read_light_sensor(self):
            return 50.0

    class GameController:  # type: ignore[no-redef]
        def update(self):
            return False

        def get_button(self, *args):
            return False

        def get_axis(self, *args):
            return 0.0

    class SensorVisualizer:  # type: ignore[no-redef]
        def __init__(self, canvas):
            pass

        def draw_chart(self, *args):
            pass

        def add_data_point(self, *args):
            pass

    class IoTDeviceManager:  # type: ignore[no-redef]
        def __init__(self):
            self.simulation_mode = True

        def discover_devices(self):
            return 0

        def connect_device(self, *args):
            return False

        def connect_all(self):
            return 0

        def get_device_data(self, *args):
            return None

        def send_device_command(self, *args):
            return "Not implemented"

        def create_device_group(self, *args):
            pass

        def control_group(self, *args):
            return "Not implemented"

    class SmartHomeHub:  # type: ignore[no-redef]
        def __init__(self):
            self.simulation_mode = True

        def setup_home(self):
            return {"discovered": 0, "connected": 0}

        def create_scene(self, *args):
            pass

        def activate_scene(self, *args):
            return "Not implemented"

        def set_environmental_target(self, *args):
            pass

        def monitor_environment(self):
            return []

    class SensorNetwork:  # type: ignore[no-redef]
        def __init__(self):
            self.simulation_mode = True

        def add_sensor(self, *args):
            pass

        def collect_data(self):
            return {}

        def analyze_trends(self, *args):
            return None

        def predict_values(self, *args):
            return None

    class AdvancedRobotInterface:  # type: ignore[no-redef]
        def __init__(self):
            self.simulation_mode = True
            self.mission_status = "idle"

        def plan_path(self, *args):
            return []

        def execute_mission(self, *args):
            return []

        def scan_environment(self):
            return {"lidar": {"range": 10.0}, "camera": {"objects": []}}

        def avoid_obstacle(self):
            return "no_obstacle"

        def learn_environment(self):
            return {"obstacles_detected": 0}

        def move_to_position(self, *args):
            pass

    class Mixer:  # type: ignore[no-redef]
        def __init__(self):
            self.registry = {}

        def snd(self, name, path, vol=0.8):
            self.registry[name] = path

        def play_snd(self, name):
            print(f"Playing sound: {name}")

    class Tween:  # type: ignore[no-redef]
        def __init__(self, store, key, a, b, dur_ms, ease="linear"):
            self.store = store
            self.key = key
            self.a = float(a)
            self.b = float(b)
            self.dur = max(1, int(dur_ms))
            self.t = 0
            self.done = False

        def step(self, dt):
            if self.done:
                return
            self.t += dt
            u = min(1.0, self.t / self.dur)
            self.store[self.key] = self.a + (self.b - self.a) * u
            if self.t >= self.dur:
                self.store[self.key] = self.b
                self.done = True

    class Timer:  # type: ignore[no-redef]
        def __init__(self, delay_ms, label):
            self.delay = max(0, int(delay_ms))
            self.label = label
            self.t = 0
            self.done = False

    class Particle:  # type: ignore[no-redef]
        def __init__(self, x, y, vx, vy, life):
            self.x = x
            self.y = y
            self.vx = vx
            self.vy = vy
            self.life = life
            self.size = 2
            self.color = "white"

        def step(self, dt):
            if self.life <= 0:
                return
            self.x += self.vx * dt / 1000.0
            self.y += self.vy * dt / 1000.0
            self.life -= dt


class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Time_WarpInterpreter:  # pylint: disable=too-many-public-methods
    """
    Main interpreter class for the Time_Warp IDE.

    This class manages the execution of programs written in multiple programming languages,
    providing a unified interface for code execution, variable management, and turtle graphics.

    Key responsibilities:
    - Parse and execute programs in 9 different languages
    - Manage global variables across program execution
    - Handle turtle graphics for visual programming languages
    - Provide debugging and execution control features
    - Route commands to appropriate language-specific executors

    The interpreter maintains execution state including current line, variables, call stack,
    and turtle graphics position. It automatically detects the programming language based
    on command syntax and routes execution to the appropriate language executor.

    Attributes:
        variables (dict): Global variable storage shared across all languages
        program_lines (list): Parsed program lines for execution
        current_line (int): Current execution position in the program
        turtle_graphics (dict): State of the turtle graphics system
        running (bool): Whether a program is currently executing
        debug_mode (bool): Whether debug output is enabled
        current_language_mode (str): Explicitly set language mode (optional)

    Language Support:
        - PILOT: Educational commands with T:, A:, J:, Y:, N: syntax
        - BASIC: Line-numbered programming with PRINT, LET, GOTO
        - Logo: Turtle graphics with FORWARD, RIGHT, REPEAT
        - Pascal: Structured programming with BEGIN/END blocks
        - Prolog: Logic programming with ?- queries and :- rules
        - Forth: Stack-based programming with DUP, DROP, SWAP
        - Perl: Modern scripting with full Perl syntax
        - Python: Python execution with standard library access
        - JavaScript: JavaScript execution with Node.js-style environment
    """

    def __init__(self, output_widget=None):
        """
        Initialize the Time_Warp interpreter.

        Args:
            output_widget: Tkinter text widget for output (optional).
                          If None, output goes to console.
        """
        # Program execution state
        self.output_widget = output_widget
        self.variables = {}  # Global variable storage
        self.labels = {}  # PILOT label definitions
        self.program_lines = []  # Parsed program lines
        self.current_line = 0  # Current execution position
        self.stack = []  # General purpose stack
        self.for_stack = []  # FOR loop stack for BASIC
        self.do_stack = []  # DO loop stack for Turbo BASIC
        self.while_stack = []  # WHILE loop stack for Turbo BASIC
        self.select_stack = []  # SELECT CASE stack for Turbo BASIC
        self.match_flag = False  # PILOT Y/N match flag
        self._last_match_set = False  # Internal PILOT flag
        self.running = False  # Execution state flag

        # Debugging and breakpoints
        self.debug_mode = False
        self.breakpoints = set()

        # Turtle graphics system (initialized lazily)
        self.turtle_graphics = None

        # IDE integration attributes
        self.ide_turtle_canvas = None  # IDE-provided turtle canvas widget

        # Call stack for debugging (compatibility)
        self.call_stack = []

        # Turtle color palette and state
        self._turtle_color_index = 0
        self._turtle_color_palette = [
            "black",
            "red",
            "blue",
            "green",
            "purple",
            "orange",
            "teal",
            "magenta",
        ]

        # Turtle tracing and persistence
        self.turtle_trace = False
        self.preserve_turtle_canvas = False

        # Profiling and macros (future features)
        self.macros = {}
        self._macro_call_stack = []
        self.profile_enabled = False
        self.profile_stats = {}

        # UCBLogo data structures
        self.logo_arrays = {}  # Array storage: name -> list or nested lists
        self.property_lists = {}  # Property list storage: name -> dict
        self.logo_error_handler = None  # Error handler procedure
        self.logo_procedures = {}  # Logo procedure definitions: name -> (params, body)
        self.logo_special_vars = {
            "ALLOWGETSET": False,  # Allow GETSET operations
            "CASEIGNOREDP": False,  # Case insensitive predicates
            "FULLPRINTP": False,  # Full print mode
            "PRINTDEPTHLIMIT": 10,  # Print depth limit
            "PRINTWIDTHLIMIT": 80,  # Print width limit
        }

        # Game and multimedia frameworks (placeholder implementations)
        self.game_manager = GameManager()
        self.game_manager.set_output_callback(self.log_output)

        self.multiplayer_game = MultiplayerGameManager(
            canvas=None, is_server=False, network_manager=None
        )

        # Audio system
        self.audio_engine = AudioEngine()

        # Collaboration framework
        self.collaboration_manager = CollaborationManager()

        # Default graphics settings
        self.default_pen_style = "solid"

        # Animation and media systems
        self.mixer = Mixer()
        self.tweens = []
        self.timers = []
        self.particles = []
        self.sprites = {}
        self.last_ms = None

        # Hardware integration (simulation mode)
        self.arduino = ArduinoController() if ArduinoController else None
        self.rpi = RPiController() if RPiController else None
        self.robot = RobotInterface() if RobotInterface else None
        self.controller = GameController() if GameController else None
        self.sensor_viz = None  # Initialized with turtle graphics

        # IoT and robotics systems (simulation mode)
        self.iot_manager = IoTDeviceManager() if IoTDeviceManager else None
        self.iot_devices = self.iot_manager
        if self.iot_devices:
            self.iot_devices.simulation_mode = True

        self.smart_home = SmartHomeHub() if SmartHomeHub else None
        if self.smart_home:
            self.smart_home.simulation_mode = True

        self.sensor_network = SensorNetwork() if SensorNetwork else None
        if self.sensor_network:
            self.sensor_network.simulation_mode = True

        self.advanced_robot = (
            AdvancedRobotInterface() if AdvancedRobotInterface else None
        )
        if self.advanced_robot:
            self.advanced_robot.simulation_mode = True

        # Initialize language executors
        self.pilot_executor = TwPilotExecutor(self)
        self.basic_executor = TwBasicExecutor(self)
        self.logo_executor = TwLogoExecutor(self)
        self.pascal_executor = TwPascalExecutor(self)
        self.prolog_executor = TwPrologExecutor(self)
        self.forth_executor = TwForthExecutor(self)
        self.perl_executor = PerlExecutor(self)
        self.python_executor = PythonExecutor(self)
        self.javascript_executor = JavaScriptExecutor(self)

        # Language mode (optional explicit setting)
        self.current_language_mode = None
        self.current_language = None

    def set_language_mode(self, mode):
        """Set the current language mode for script execution"""
        valid_modes = [
            "pilot",
            "basic",
            "logo",
            "python",
            "javascript",
            "perl",
            "pascal",
            "prolog",
            "forth",
        ]
        if mode in valid_modes:
            self.current_language_mode = mode
            self.log_output(f"Language mode set to: {mode}")
        else:
            self.log_output(f"Invalid language mode: {mode}")

    def init_turtle_graphics(self):
        """Initialize turtle graphics system"""
        if self.turtle_graphics:
            return  # Already initialized

        self.turtle_graphics = {
            "x": 0.0,
            "y": 0.0,
            "heading": 0.0,
            "pen_down": True,
            "pen_color": self._turtle_color_palette[self._turtle_color_index],
            "pen_size": 2,
            "visible": True,
            "canvas": None,
            "window": None,
            "center_x": 300,  # Default center
            "center_y": 200,  # Default center
            "lines": [],  # Track drawn objects for clearing
            "sprites": {},  # Sprite management
            "pen_style": getattr(self, "default_pen_style", "solid"),
            "fill_color": "",  # Fill color for shapes
            "hud_visible": False,  # Whether HUD is displayed
            "images": [],  # Store image references to prevent garbage collection
        }

        # Check if we have IDE turtle canvas available first
        if hasattr(self, "ide_turtle_canvas") and self.ide_turtle_canvas:
            self.debug_output("🐢 Using IDE integrated turtle graphics")
            self.turtle_graphics["canvas"] = self.ide_turtle_canvas
            self.turtle_graphics["window"] = None  # No separate window needed

            # Get actual canvas dimensions for proper centering
            try:
                # Force canvas to update its geometry
                self.ide_turtle_canvas.update_idletasks()
                canvas_width = self.ide_turtle_canvas.winfo_width()
                canvas_height = self.ide_turtle_canvas.winfo_height()

                # If canvas hasn't been laid out yet, use configured dimensions
                if canvas_width <= 1 or canvas_height <= 1:
                    canvas_width = int(self.ide_turtle_canvas.cget("width") or 600)
                    canvas_height = int(self.ide_turtle_canvas.cget("height") or 400)

                self.turtle_graphics["center_x"] = canvas_width // 2
                self.turtle_graphics["center_y"] = canvas_height // 2
                self.debug_output(
                    f"📐 Canvas size: {canvas_width}x{canvas_height}, center: ({self.turtle_graphics['center_x']}, {self.turtle_graphics['center_y']})"
                )
            except Exception as e:
                # Fallback to known canvas size
                self.turtle_graphics["center_x"] = 300
                self.turtle_graphics["center_y"] = 200
                self.debug_output(f"📐 Using fallback canvas center: (300, 200) - {e}")

            self.update_turtle_display()
            # Force canvas update to ensure it's ready for drawing
            if hasattr(self, "ide_turtle_canvas"):
                self.ide_turtle_canvas.update_idletasks()
        else:
            # Headless mode - provide a minimal stub so drawing operations record metadata
            class _HeadlessCanvas:
                def __init__(self):
                    # Record created drawing ops so tests can assert on them
                    self.created = []
                    self._id_counter = 1

                def _record(self, kind, args, kwargs):
                    item_id = self._id_counter
                    self._id_counter += 1
                    self.created.append({"id": item_id, "type": kind, "args": args, "kwargs": kwargs})
                    return item_id

                def create_line(self, *args, **kwargs):
                    return self._record("line", args, kwargs)

                def create_oval(self, *args, **kwargs):
                    return self._record("oval", args, kwargs)

                def create_rectangle(self, *args, **kwargs):
                    return self._record("rectangle", args, kwargs)

                def create_polygon(self, *args, **kwargs):
                    return self._record("polygon", args, kwargs)

                def create_text(self, *args, **kwargs):
                    return self._record("text", args, kwargs)

                def create_image(self, *args, **kwargs):
                    return self._record("image", args, kwargs)

                def bbox(self, *args, **kwargs):
                    return (0, 0, 0, 0)

                def configure(self, **kwargs):
                    pass

                def winfo_width(self):
                    return 600

                def winfo_height(self):
                    return 400

                def xview(self):
                    return (0.0, 1.0)

                def yview(self):
                    return (0.0, 1.0)

                def xview_moveto(self, f):
                    pass

                def yview_moveto(self, f):
                    pass

                def update_idletasks(self):
                    pass

                def update(self):
                    pass

                def delete(self, *args, **kwargs):
                    pass

            self.turtle_graphics["canvas"] = _HeadlessCanvas()
            self.log_output("Turtle graphics initialized (headless stub mode)")

    def turtle_forward(self, distance):
        """Move turtle forward by distance units

        Uses Logo/turtle graphics convention where:
        - 0° = North (up on screen)
        - 90° = East (right)
        - 180° = South (down)
        - 270° = West (left)
        """
        if not self.turtle_graphics:
            self.init_turtle_graphics()

        import math

        # Convert Logo heading to math radians
        # Logo: 0° = North (up), clockwise
        # Math: 0° = East (right), counter-clockwise
        # Conversion: math_angle = 90 - logo_heading
        logo_heading = self.turtle_graphics["heading"]
        math_angle_degrees = 90 - logo_heading
        heading_rad = math.radians(math_angle_degrees)

        old_x = self.turtle_graphics["x"]
        old_y = self.turtle_graphics["y"]

        # Calculate movement in turtle coordinate space
        # Positive Y = up on screen (north), Negative Y = down (south)
        new_x = old_x + distance * math.cos(heading_rad)
        new_y = old_y + distance * math.sin(heading_rad)

        # Update turtle graphics state
        self.turtle_graphics["x"] = new_x
        self.turtle_graphics["y"] = new_y

        # Sync to interpreter variables
        self.variables["TURTLE_X"] = new_x
        self.variables["TURTLE_Y"] = new_y
        self.variables["TURTLE_HEADING"] = self.turtle_graphics["heading"]

        # Draw line if pen is down
        if self.turtle_graphics["pen_down"]:
            canvas = self.turtle_graphics.get("canvas")
            if canvas:
                # Convert turtle coordinates to canvas coordinates
                # Canvas: Y increases downward, so flip the turtle Y coordinate
                canvas_old_x = old_x + self.turtle_graphics["center_x"]
                canvas_old_y = self.turtle_graphics["center_y"] - old_y  # Flip Y for canvas
                canvas_new_x = new_x + self.turtle_graphics["center_x"]
                canvas_new_y = self.turtle_graphics["center_y"] - new_y  # Flip Y for canvas

                self.log_output(
                    f"🎨 Drawing line from ({canvas_old_x:.1f}, {canvas_old_y:.1f}) to ({canvas_new_x:.1f}, {canvas_new_y:.1f})"
                )

                line_id = canvas.create_line(
                    canvas_old_x,
                    canvas_old_y,
                    canvas_new_x,
                    canvas_new_y,
                    fill=self.turtle_graphics["pen_color"],
                    width=self.turtle_graphics["pen_size"],
                )
                self.turtle_graphics["lines"].append(line_id)

                # Force canvas update to show the line immediately
                try:
                    canvas.update_idletasks()
                except Exception:
                    pass

        self.update_turtle_display()
        self.log_output("Turtle moved")

    def turtle_turn(self, angle):
        """Turn turtle by angle degrees"""
        if not self.turtle_graphics:
            self.init_turtle_graphics()

        self.turtle_graphics["heading"] = (
            self.turtle_graphics["heading"] + angle
        ) % 360
        # Sync heading variable
        self.variables["TURTLE_HEADING"] = self.turtle_graphics["heading"]
        self.update_turtle_display()

    def turtle_home(self):
        """Move turtle to home position (0,0) and reset heading"""
        if not self.turtle_graphics:
            self.init_turtle_graphics()

        self.turtle_graphics["x"] = 0.0
        self.turtle_graphics["y"] = 0.0
        self.turtle_graphics["heading"] = 0.0
        self.update_turtle_display()

    def turtle_set_color(self, color):
        """Update pen color for turtle drawing"""
        if not self.turtle_graphics:
            self.init_turtle_graphics()
        self.turtle_graphics["pen_color"] = str(color)
        self.update_turtle_display()

    def turtle_set_pen_size(self, size):
        """Update pen size for turtle drawing"""
        if not self.turtle_graphics:
            self.init_turtle_graphics()
        try:
            pen_size = max(1, int(size))
        except Exception:
            pen_size = 1
        self.turtle_graphics["pen_size"] = pen_size
        self.update_turtle_display()

    def turtle_setxy(self, x, y):
        """Move turtle to specific coordinates"""
        if not self.turtle_graphics:
            self.init_turtle_graphics()

        self.turtle_graphics["x"] = x
        self.turtle_graphics["y"] = y
        self.update_turtle_display()

    def update_turtle_display(self):
        """Update the turtle display on canvas

        Draws turtle as triangle pointing in the Logo heading direction where:
        - 0° = North (up)
        - 90° = East (right)
        - 180° = South (down)
        - 270° = West (left)
        """
        if not self.turtle_graphics or not self.turtle_graphics["canvas"]:
            return

        canvas = self.turtle_graphics["canvas"]

        # Remove old turtle
        canvas.delete("turtle")

        # Draw new turtle if visible
        if self.turtle_graphics["visible"]:
            import math

            # Get canvas coordinates (Y flipped from turtle coordinates)
            x = self.turtle_graphics["x"] + self.turtle_graphics["center_x"]
            y = self.turtle_graphics["center_y"] - self.turtle_graphics["y"]

            # Convert Logo heading to canvas drawing angle
            # Logo: 0° = North (up), clockwise
            # Canvas/Math: 0° = East (right), counter-clockwise
            logo_heading = self.turtle_graphics["heading"]
            canvas_angle = math.radians(90 - logo_heading)  # Same conversion as movement

            # Draw turtle as a triangle pointing in heading direction
            size = 10

            # Calculate triangle points (tip points in direction of travel)
            tip_x = x + size * math.cos(canvas_angle)
            tip_y = y - size * math.sin(canvas_angle)  # Y flipped for canvas

            # Left corner (120° from tip)
            left_angle = canvas_angle + math.radians(140)
            left_x = x + size * 0.6 * math.cos(left_angle)
            left_y = y - size * 0.6 * math.sin(left_angle)

            # Right corner (120° from tip, other direction)
            right_angle = canvas_angle - math.radians(140)
            right_x = x + size * 0.6 * math.cos(right_angle)
            right_y = y - size * 0.6 * math.sin(right_angle)

            # Create turtle triangle
            canvas.create_polygon(
                tip_x,
                tip_y,
                left_x,
                left_y,
                right_x,
                right_y,
                fill="green",
                outline="darkgreen",
                width=2,
                tags="turtle",
            )

    def clear_turtle_screen(self):
        """Clear the turtle screen"""
        if not self.turtle_graphics:
            self.init_turtle_graphics()

        if self.turtle_graphics["canvas"]:
            # Remove all drawn lines
            for line_id in self.turtle_graphics["lines"]:
                self.turtle_graphics["canvas"].delete(line_id)
            self.turtle_graphics["lines"].clear()

            # Clear all sprites
            if "sprites" in self.turtle_graphics:
                for sprite_name, sprite_data in self.turtle_graphics["sprites"].items():
                    if sprite_data["canvas_id"]:
                        self.turtle_graphics["canvas"].delete(sprite_data["canvas_id"])
                        sprite_data["canvas_id"] = None
                        sprite_data["visible"] = False

            self.update_turtle_display()

    def reset(self):
        """Reset interpreter state"""
        self.variables = {}
        self.labels = {}
        self.program_lines = []
        self.current_line = 0
        self.stack = []
        self.for_stack = []
        self.match_flag = False
        self._last_match_set = False
        self.running = False

        # Reset Time_Warp animation and media systems
        self.tweens = []
        self.timers = []
        self.particles = []
        self.sprites = {}
        self.last_ms = None

    def log_output(self, text):
        """Log output to widget or console"""
        if self.output_widget:
            try:
                self.output_widget.insert(tk.END, str(text) + "\n")
                self.output_widget.see(tk.END)
            except Exception:
                print(text)
        else:
            print(text)

    def debug_output(self, text):
        """Log debug output only when debug mode is enabled"""
        if self.debug_mode:
            self.log_output(text)

    def parse_line(self, line):
        """Parse a program line for line number and command"""
        line = line.strip()
        match = re.match(r"^(\d+)\s+(.*)", line)
        if match:
            line_number, command = match.groups()
            return int(line_number), command.strip()
        return None, line.strip()

    def resolve_variables(self, text):
        """Resolve variables in text using *VARIABLE* syntax, %SYSTEMVAR% syntax, or bare variable names"""
        if not isinstance(text, str):
            return text

        # Handle variables marked with *VARIABLE* syntax first
        import re

        def replace_var(match):
            var_name = match.group(1).upper()
            return str(self.variables.get(var_name, ""))

        def replace_system_var(match):
            var_name = match.group(1).lower()
            # Check if we have a PILOT executor with system variables
            if hasattr(self, "pilot_executor") and hasattr(
                self.pilot_executor, "system_vars"
            ):
                return str(self.pilot_executor.system_vars.get(var_name, ""))
            return ""

        # Replace %SYSTEMVAR% patterns with system variable values (PILOT 73)
        resolved = re.sub(r"%([A-Za-z_][A-Za-z0-9_]*)%", replace_system_var, text)

        # Replace *VARIABLE* patterns with actual values
        resolved = re.sub(r"\*([A-Za-z_][A-Za-z0-9_]*)\*", replace_var, resolved)

        # If no *VARIABLE* or %SYSTEMVAR% patterns were found and the text is a simple variable name,
        # try to resolve it as a bare variable
        if "*" not in resolved and "%" not in resolved and resolved == text:
            # Check if the entire text is a valid variable name
            if re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", text.strip()):
                var_name = text.strip().upper()
                if var_name in self.variables:
                    return str(self.variables[var_name])

        return resolved

    def parse_command_args(self, argument):
        """Parse command arguments handling quoted strings properly"""
        args = []
        current_arg = ""
        in_quotes = False
        i = 0

        while i < len(argument):
            char = argument[i]

            if char == '"' and (i == 0 or argument[i - 1] != "\\"):
                in_quotes = not in_quotes
                current_arg += char
            elif char == " " and not in_quotes:
                if current_arg.strip():
                    args.append(current_arg.strip())
                    current_arg = ""
                # Skip multiple spaces
                while i + 1 < len(argument) and argument[i + 1] == " ":
                    i += 1
            else:
                current_arg += char

            i += 1

        if current_arg.strip():
            args.append(current_arg.strip())

        return args

    def evaluate_expression(self, expr):
        """Safely evaluate mathematical expressions with variables"""
        # Replace variables.
        # First substitute explicit *VAR* interpolation (used in many programs).
        for var_name, var_value in self.variables.items():
            # Only quote non-numeric values
            if isinstance(var_value, (int, float)):
                val_repr = str(var_value)
            else:
                val_repr = f'"{var_value}"'
            # Replace *VAR* occurrences first
            expr = expr.replace(f"*{var_name}*", val_repr)

        # Safe evaluation of mathematical & simple string expressions
        allowed_names = {
            "abs": abs,
            "round": round,
            "int": int,
            "float": float,
            "max": max,
            "min": min,
            "len": len,
            "str": str,
            # RND accepts 0 or 1 args in many example programs
            "RND": (lambda *a: random.random() if not a else random.random() * a[0]),
            "INT": int,
            "ABS": abs,
            "VAL": lambda x: float(x) if "." in str(x) else int(x),
            "UPPER": lambda x: str(x).upper(),
            "LOWER": lambda x: str(x).lower(),
            "MID": (
                lambda s, start, length: (
                    str(s)[int(start) - 1 : int(start) - 1 + int(length)]
                    if isinstance(s, (str, int, float))
                    else ""
                )
            ),
            # BASIC-style functions
            "STR$": lambda x: str(x),
            "CHR$": lambda x: chr(int(x)),
            "ASC": lambda x: ord(str(x)[0]) if str(x) else 0,
            "LEN": lambda x: len(str(x)),
            "LEFT$": lambda s, n: str(s)[: int(n)],
            "RIGHT$": lambda s, n: str(s)[-int(n) :] if int(n) > 0 else "",
            # Turbo BASIC enhanced functions
            "CEIL": lambda x: (
                int(-(-float(x) // 1))
                if float(x) < 0
                else int(float(x) + 0.999999) if float(x) % 1 != 0 else int(float(x))
            ),
            "FIX": lambda x: int(float(x)) if float(x) >= 0 else -int(-float(x)),
            "EXP2": lambda x: 2 ** float(x),
            "EXP10": lambda x: 10 ** float(x),
            "LOG2": lambda x: math.log2(float(x)) if float(x) > 0 else 0,
            "LOG10": lambda x: math.log10(float(x)) if float(x) > 0 else 0,
            "CHR": lambda x: chr(int(x)),
            "UCASE": lambda x: str(x).upper(),
            "LCASE": lambda x: str(x).lower(),
            "BIN": lambda x: bin(int(x))[2:],
            "OCT": lambda x: oct(int(x))[2:],
            "HEX": lambda x: hex(int(x))[2:],
        }

        # Handle array access first (e.g., BULLETS(I,0) -> array value)
        import re

        array_pattern = r"([A-Za-z_][A-Za-z0-9_]*)\(([^)]+)\)"

        def replace_array_access(match):
            array_name = match.group(1)
            indices_str = match.group(2)
            try:
                # Check if this is actually a function call, not array access
                # If the name is in allowed_names, it's a function call
                if array_name in allowed_names:
                    return match.group(0)  # Return unchanged

                if array_name in self.variables:
                    array_var = self.variables[array_name]
                    if isinstance(array_var, dict):
                        # Evaluate each index
                        indices = [
                            int(self.evaluate_expression(idx.strip()))
                            for idx in indices_str.split(",")
                        ]

                        # Navigate through the array structure
                        current = array_var
                        for idx in indices:
                            if isinstance(current, dict) and idx in current:
                                current = current[idx]
                            else:
                                return "0"  # Default value for uninitialized array elements
                        return str(current)
                return "0"
            except Exception:
                return "0"

        expr = re.sub(array_pattern, replace_array_access, expr)

        # Then replace bare variable names using word boundaries to avoid
        # accidental substring replacements (e.g. A vs AB).
        # Sort variables by length (longest first) to prevent A from interfering with A$
        for var_name, var_value in sorted(
            self.variables.items(), key=lambda x: len(x[0]), reverse=True
        ):
            if isinstance(var_value, dict):
                continue  # Skip arrays, they're handled above
            if isinstance(var_value, (int, float)):
                val_repr = str(var_value)
            else:
                val_repr = f'"{var_value}"'
            try:
                # Handle variables with $ in the name (BASIC string variables)
                if "$" in var_name:
                    # Use a pattern that matches the variable name followed by word boundary or end of string
                    pattern = rf"\b{re.escape(var_name)}(?=\s|$|[^A-Za-z0-9_$]|$)"
                    expr = re.sub(pattern, val_repr, expr)
                else:
                    # Standard word boundary matching for regular variables
                    expr = re.sub(rf"\b{re.escape(var_name)}\b", val_repr, expr)
            except re.error:
                # fallback to plain replace if regex fails for unusual names
                expr = expr.replace(var_name, val_repr)

        # Safe evaluation of mathematical & simple string expressions
        safe_dict = {"__builtins__": {}}
        safe_dict.update(allowed_names)

        # Replace custom functions (rudimentary)
        expr = expr.replace("RND(1)", str(random.random()))
        expr = expr.replace("RND()", str(random.random()))

        # Convert BASIC operators to Python equivalents
        expr = re.sub(r"\bMOD\b", "%", expr, flags=re.IGNORECASE)  # MOD -> %
        expr = re.sub(r"<>", "!=", expr)  # <> -> !=

        # Handle BASIC functions with $ in the name
        import re

        # STR$(x) function
        def replace_str_func(match):
            arg = match.group(1)
            try:
                val = self.evaluate_expression(arg)
                return f'"{str(val)}"'
            except Exception:
                return f'"{arg}"'

        expr = re.sub(r"STR\$\(([^)]+)\)", replace_str_func, expr)

        # CHR$(x) function
        def replace_chr_func(match):
            arg = match.group(1)
            try:
                val = int(self.evaluate_expression(arg))
                return f'"{chr(val)}"'
            except Exception:
                return '""'

        expr = re.sub(r"CHR\$\(([^)]+)\)", replace_chr_func, expr)

        # LEFT$(s,n) and RIGHT$(s,n) functions
        def replace_left_func(match):
            args = match.group(1).split(",")
            if len(args) == 2:
                try:
                    s = str(self.evaluate_expression(args[0].strip()))
                    n = int(self.evaluate_expression(args[1].strip()))
                    return f'"{s[:n]}"'
                except Exception:
                    pass
            return '""'

        expr = re.sub(r"LEFT\$\(([^)]+)\)", replace_left_func, expr)

        def replace_right_func(match):
            args = match.group(1).split(",")
            if len(args) == 2:
                try:
                    s = str(self.evaluate_expression(args[0].strip()))
                    n = int(self.evaluate_expression(args[1].strip()))
                    return f'"{s[-n:] if n > 0 else ""}"'
                except Exception:
                    pass
            return '""'

        expr = re.sub(r"RIGHT\$\(([^)]+)\)", replace_right_func, expr)

        try:
            return eval(expr, safe_dict)
        except ZeroDivisionError:
            self.log_output("Expression error: Division by zero")
            return "ERROR: Division by zero"
        except TypeError as te:
            # Attempt intelligent fallback for string + int concatenation
            if "can only concatenate str" in str(te):
                try:
                    # Tokenize by + and rebuild as string if any side is quoted text
                    parts = [p.strip() for p in re.split(r"(?<!\\)\+", expr)]
                    if len(parts) > 1:
                        resolved_parts = []
                        for p in parts:
                            # Try normal eval for each part
                            try:
                                val = eval(p, safe_dict)
                            except Exception:
                                val = p.strip("\"'")
                            resolved_parts.append(str(val))
                        return "".join(resolved_parts)
                except Exception:
                    pass
            self.log_output(f"Expression error: {te}")
            return 0
        except Exception as e:
            # Better fallback handling for different expression types
            try:
                # If it's a quoted string, return the unquoted content
                stripped = expr.strip()
                if stripped.startswith('"') and stripped.endswith('"'):
                    return stripped[1:-1]

                # If numeric-looking, try to parse as number
                if re.fullmatch(r"[-+]?\d+(?:\.\d+)?", stripped):
                    return float(stripped) if "." in stripped else int(stripped)

                # If it's a simple variable name that wasn't resolved, return as string
                if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", stripped):
                    return stripped

                # For complex expressions that failed, return the original expression
                return stripped
            except Exception:
                pass
            self.log_output(f"Expression error: {e}")
            return expr  # Return original instead of 0

    def interpolate_text(self, text: str) -> str:
        """Interpolate *VAR* tokens and evaluate *expr* tokens inside a text string.

        This central helper is used by T: and MT: to keep interpolation logic
        consistent and reduce duplication.
        """
        # First replace explicit variable occurrences like *VAR*
        for var_name, var_value in self.variables.items():
            text = text.replace(f"*{var_name}*", str(var_value))

        # Then evaluate expression-like tokens remaining between *...*
        try:
            tokens = re.findall(r"\*(.+?)\*", text)
            for tok in tokens:
                # If we've already replaced this as a variable, skip
                if tok in self.variables:
                    continue
                tok_stripped = tok.strip()
                # If token looks like a numeric literal, just use it
                if re.fullmatch(r"[-+]?\d+(?:\.\d+)?", tok_stripped):
                    text = text.replace(f"*{tok}*", tok_stripped)
                    continue
                # Heuristic: if token contains expression characters, try to eval
                if re.search(r"[\(\)\+\-\*/%<>=]", tok):
                    try:
                        val = self.evaluate_expression(tok)
                        text = text.replace(f"*{tok}*", str(val))
                    except Exception:
                        # leave token as-is on error
                        pass
        except Exception:
            pass

        return text

    def get_user_input(self, prompt=""):
        """Get input from user"""
        if self.output_widget:
            # Use dialog for GUI environment
            result = simpledialog.askstring("Input", prompt)
            if result is not None:
                # Echo the input to the output for visibility
                self.log_output(result)
                return result
            return ""
        else:
            # Use console input for command line
            return input(prompt)

    # Note: For brevity, I'm including just the core structure. The full implementation would include
    # all the command handling methods (_handle_runtime_command, etc.)
    # that were in the original class. This is the basic framework that can be extended.

    def determine_command_type(self, command, language_mode=None):
        """Determine which language the command belongs to"""
        command = command.strip()

        # If explicit language mode is set, use that for modern languages
        if language_mode:
            language_mode_lower = language_mode.lower()
            if language_mode_lower == "python":
                return "python"
            elif language_mode_lower == "javascript":
                return "javascript"
            elif language_mode_lower == "perl":
                return "perl"
            elif language_mode_lower == "pascal":
                return "pascal"
            elif language_mode_lower == "prolog":
                return "prolog"
            elif language_mode_lower == "forth":
                return "forth"
            elif language_mode_lower == "basic":
                return "basic"
            elif language_mode_lower == "logo":
                return "logo"
            elif language_mode_lower == "pilot":
                # In PILOT mode, handle comments and commands
                if command.startswith("*"):
                    return "pilot"  # Comment line
                elif len(command) > 1 and command[1] == ":":
                    return "pilot"  # PILOT command
                # Fall through to other checks

        # PILOT commands start with a letter followed by colon
        if len(command) > 1 and command[1] == ":":
            return "pilot"

        # Prolog commands
        if (
            command.startswith("?-")
            or ":-" in command
            or command.upper()
            in ["LISTING", "LISTING.", "TRACE", "TRACE.", "NOTRACE", "NOTRACE."]
        ):
            return "prolog"

        # BASIC commands (check before Forth since some keywords overlap)
        basic_commands = [
            "LET",
            "PRINT",
            "INPUT",
            "GOTO",
            "IF",
            "THEN",
            "FOR",
            "TO",
            "NEXT",
            "GOSUB",
            "RETURN",
            "END",
            "REM",
            "DIM",
            # Turbo BASIC Structured Programming
            "DO",
            "LOOP",
            "WHILE",
            "WEND",
            "EXIT",
            "SELECT",
            "CASE",
            "END SELECT",  # Compound command
            # Turbo BASIC Enhanced Commands
            "INCR",
            "DECR",
            "SWAP",
            "RANDOMIZE",
            "DELAY",
            "DRAW",
            "PALETTE",
            "CALL",
            # Turbo BASIC Math/String Functions
            "SIN",
            "COS",
            "TAN",
            "SQRT",
            "ABS",
            "INT",
            "RND",
            "CEIL",
            "FIX",
            "EXP",
            "EXP2",
            "EXP10",
            "LOG",
            "LOG2",
            "LOG10",
            "LEN",
            "MID",
            "LEFT",
            "RIGHT",
            "INSTR",
            "STR",
            "VAL",
            "CHR",
            "ASC",
            "UCASE",
            "LCASE",
            "BIN",
            "OCT",
            "HEX",
        ]

        # Game commands are BASIC
        cmd_first_word = command.split()[0].upper()
        cmd_two_words = (
            " ".join(command.split()[:2]).upper()
            if len(command.split()) >= 2
            else cmd_first_word
        )
        self.debug_output(
            f"Command type check: '{command}' -> first='{cmd_first_word}', two='{cmd_two_words}'"
        )
        if (
            cmd_first_word in basic_commands
            or cmd_two_words in basic_commands
            or cmd_first_word.startswith("GAME")
        ):
            return "basic"

        # Forth commands - stack operations, arithmetic, word definitions
        forth_words = [
            "DUP",
            "DROP",
            "SWAP",
            "OVER",
            "ROT",
            "-ROT",
            "+",
            "-",
            "*",
            "/",
            "MOD",
            "NEGATE",
            "=",
            "<",
            ">",
            "<=",
            ">=",
            "<>",
            "AND",
            "OR",
            "XOR",
            "INVERT",
            ".",
            "EMIT",
            "CR",
            "SPACE",
            "SPACES",
            "@",
            "!",
            "C@",
            "C!",
            ":",
            ";",
            "CONSTANT",
            "VARIABLE",
            "IF",
            "THEN",
            "ELSE",
            "BEGIN",
            "UNTIL",
            "WHILE",
            "REPEAT",
            "I",
            "J",
            "SEE",
            "WORDS",
            "FORGET",
        ]
        cmd_first_word = command.split()[0].upper() if command.split() else ""
        if cmd_first_word in forth_words or command.startswith(":"):
            return "forth"

        # Pascal commands
        pascal_keywords = [
            "PROGRAM",
            "BEGIN",
            "END",
            "VAR",
            "CONST",
            "PROCEDURE",
            "FUNCTION",
            "IF",
            "THEN",
            "ELSE",
            "WHILE",
            "FOR",
            "TO",
            "DOWNTO",
            "REPEAT",
            "UNTIL",
            "OF",
            "READLN",
            "WRITELN",
            "WRITE",
        ]
        cmd_first_word = command.split()[0].upper() if command.split() else ""
        cmd_two_words = (
            " ".join(command.split()[:2]).upper()
            if len(command.split()) >= 2
            else cmd_first_word
        )

        # Check for compound BASIC commands first
        basic_two_words = ["END SELECT"]
        if cmd_two_words in basic_two_words:
            return "basic"

        if cmd_first_word in pascal_keywords or ":=" in command:
            return "pascal"

        # Logo commands
        logo_commands = [
            "FORWARD",
            "FD",
            "BACK",
            "BK",
            "LEFT",
            "LT",
            "RIGHT",
            "RT",
            "PENUP",
            "PU",
            "PENDOWN",
            "PD",
            "CLEARSCREEN",
            "CS",
            "HOME",
            "SETXY",
            "REPEAT",
            "COLOR",
            "SETCOLOR",
            "SETCOLOUR",
            "SETPENSIZE",
            "PENSTYLE",
        ]
        if command.split()[0].upper() in logo_commands:
            return "logo"

        # Default to PILOT for simple commands
        return "pilot"

    def execute_line(self, line):
        """Execute a single line of code"""
        line_num, command = self.parse_line(line)

        # For interactive execution, treat leading-number lines as data (not labels)
        # if a non-BASIC language mode is active. This allows languages like Forth
        # to accept lines that start with numeric literals (e.g. "5 DUP .").
        if line_num is not None and self.current_language_mode:
            if self.current_language_mode.lower() != "basic":
                # Don't treat this as a line label for other languages
                command = line.strip()
                line_num = None

        if not command:
            return "continue"

        # Skip whole-line comments that start with comment markers commonly used
        # across example files (e.g., ';' used in PILOT/Logo, '#' used in some scripts)
        stripped = command.lstrip()
        # Treat ';' or '#' as whole-line comments for non-Forth languages.
        # In Forth, ';' is the end-of-definition word, so it must be executed.
        if self.current_language_mode != "forth":
            if stripped.startswith(";") or stripped.startswith("#"):
                return "continue"

        # Determine command type and execute
        cmd_type = self.determine_command_type(command, self.current_language_mode)
        self.debug_output(f"Command '{command}' determined as type: {cmd_type}")

        if cmd_type == "pilot":
            return self.pilot_executor.execute_command(command)
        elif cmd_type == "basic":
            return self.basic_executor.execute_command(command)
        elif cmd_type == "logo":
            return self.logo_executor.execute_command(command)
        elif cmd_type == "pascal":
            return self.pascal_executor.execute_command(command)
        elif cmd_type == "prolog":
            return self.prolog_executor.execute_command(command)
        elif cmd_type == "forth":
            return self.forth_executor.execute_command(command)
        elif cmd_type == "perl":
            return self.perl_executor.execute_command(command)
        elif cmd_type == "python":
            return self.python_executor.execute_command(command)
        elif cmd_type == "javascript":
            return self.javascript_executor.execute_command(command)

        return "continue"

    def load_program(self, program_text):
        """Load and parse a program"""
        # Reset program state but preserve variables
        self.labels = {}
        self.program_lines = []
        self.current_line = 0
        self.stack = []
        self.for_stack = []
        self.match_flag = False
        self._last_match_set = False
        self.running = False

        # Reset Time_Warp animation and media systems but preserve variables
        self.tweens = []
        self.timers = []
        self.particles = []
        self.sprites = {}
        self.last_ms = None

        lines = program_text.strip().split("\n")

        # Parse lines and collect labels
        self.program_lines = []
        for i, line in enumerate(lines):
            # For Forth (and other non-BASIC languages), keep the line intact so
            # leading numbers aren't misinterpreted as line labels.
            if self.current_language_mode and self.current_language_mode != "basic":
                command = line.strip()
                self.program_lines.append((None, command))
            else:
                line_num, command = self.parse_line(line)
                self.program_lines.append((line_num, command))

                # Collect PILOT labels
                if command.startswith("L:"):
                    label = command[2:].strip()
                    self.labels[label] = i

        return True

    def run_program(
        self, program_text, language=None
    ):  # pylint: disable=too-many-branches
        """Run a complete program

        Args:
            program_text (str): The program code to execute
            language (str, optional): The programming language ('pilot', 'basic', 'logo', etc.)
                                     Defaults to auto-detection
        """
        # Store language preference
        if language:
            self.current_language = language.lower()
            self.current_language_mode = language.lower()

        # Preprocess Logo programs to handle multi-line REPEAT blocks
        if language and language.lower() == "logo":
            program_text = self._preprocess_logo_program(program_text)

        if not self.load_program(program_text):
            self.log_output("Error loading program")
            return False

        self.running = True
        self.current_line = 0
        max_iterations = 10000  # Prevent infinite loops
        iterations = 0

        try:
            while (
                self.current_line < len(self.program_lines)
                and self.running
                and iterations < max_iterations
            ):
                iterations += 1

                if self.debug_mode and self.current_line in self.breakpoints:
                    self.log_output(f"Breakpoint hit at line {self.current_line}")

                _line_num, command = self.program_lines[self.current_line]

                # Skip empty lines
                if not command.strip():
                    self.current_line += 1
                    continue

                result = self.execute_line(command)

                if result == "end":
                    break
                if isinstance(result, str) and result.startswith("jump:"):
                    try:
                        jump_target = int(result.split(":")[1])
                        self.current_line = jump_target
                        continue
                    except (ValueError, IndexError):
                        pass
                elif result == "error":
                    self.log_output("Program terminated due to error")
                    break

                self.current_line += 1

            if iterations >= max_iterations:
                self.log_output("Program stopped: Maximum iterations reached")

        except Exception as e:
            self.log_output(f"Runtime error: {e}")
        finally:
            self.running = False
            self.log_output("Program execution completed")

        return True

    # Additional methods for debugger control, etc.
    def step(self):
        """Execute a single line and pause"""
        # Implementation would go here
        pass  # pylint: disable=unnecessary-pass

    def stop_program(self):
        """Stop program execution"""
        self.running = False

    def set_debug_mode(self, enabled):
        """Enable/disable debug mode"""
        self.debug_mode = enabled

    def toggle_breakpoint(self, line_number):
        """Toggle breakpoint at line"""
        if line_number in self.breakpoints:
            self.breakpoints.remove(line_number)
        else:
            self.breakpoints.add(line_number)

    def turtle_circle(self, radius):
        """Draw a circle with given radius"""
        if not self.turtle_graphics:
            self.init_turtle_graphics()

        if not self.turtle_graphics["canvas"] or not self.turtle_graphics["pen_down"]:
            return

        # Draw circle at current position
        canvas = self.turtle_graphics["canvas"]
        center_x = self.turtle_graphics["x"] + self.turtle_graphics["center_x"]
        center_y = self.turtle_graphics["center_y"] - self.turtle_graphics["y"]

        circle_id = canvas.create_oval(
            center_x - radius,
            center_y - radius,
            center_x + radius,
            center_y + radius,
            outline=self.turtle_graphics["pen_color"],
            width=self.turtle_graphics["pen_size"],
        )
        self.turtle_graphics["lines"].append(circle_id)

    def turtle_dot(self, size):
        """Draw a filled dot at current position"""
        if not self.turtle_graphics:
            self.init_turtle_graphics()

        if not self.turtle_graphics["canvas"]:
            return

        canvas = self.turtle_graphics["canvas"]
        center_x = self.turtle_graphics["x"] + self.turtle_graphics["center_x"]
        center_y = self.turtle_graphics["center_y"] - self.turtle_graphics["y"]

        dot_id = canvas.create_oval(
            center_x - size // 2,
            center_y - size // 2,
            center_x + size // 2,
            center_y + size // 2,
            fill=self.turtle_graphics["pen_color"],
            outline=self.turtle_graphics["pen_color"],
        )
        self.turtle_graphics["lines"].append(dot_id)

    def turtle_rect(self, width, height, filled=False):
        """Draw a rectangle at current position"""
        if not self.turtle_graphics:
            self.init_turtle_graphics()

        if not self.turtle_graphics["canvas"]:
            return

        canvas = self.turtle_graphics["canvas"]
        x = self.turtle_graphics["x"] + self.turtle_graphics["center_x"]
        y = self.turtle_graphics["center_y"] - self.turtle_graphics["y"]

        rect_id = canvas.create_rectangle(
            x,
            y,
            x + width,
            y + height,
            outline=self.turtle_graphics["pen_color"],
            fill=self.turtle_graphics.get("fill_color", "") if filled else "",
            width=self.turtle_graphics["pen_size"],
        )
        self.turtle_graphics["lines"].append(rect_id)

    def turtle_text(self, text, size=12):
        """Draw text at current position"""
        if not self.turtle_graphics:
            self.init_turtle_graphics()

        if not self.turtle_graphics["canvas"]:
            return

        canvas = self.turtle_graphics["canvas"]
        x = self.turtle_graphics["x"] + self.turtle_graphics["center_x"]
        y = self.turtle_graphics["center_y"] - self.turtle_graphics["y"]

        text_id = canvas.create_text(
            x,
            y,
            text=text,
            font=("Arial", int(size)),
            fill=self.turtle_graphics["pen_color"],
            anchor="nw",
        )
        self.turtle_graphics["lines"].append(text_id)

    def _preprocess_logo_program(self, program_text):
        """Preprocess Logo program to handle TO/END procedures and multi-line REPEAT blocks"""
        lines = program_text.split("\n")
        processed_lines = []
        i = 0

        while i < len(lines):
            line = lines[i].strip()

            # Handle TO/END procedure definitions
            if line.upper().startswith("TO "):
                # Extract procedure definition
                proc_def = line[3:].strip().split()
                if not proc_def:
                    i += 1
                    continue

                proc_name = proc_def[0].upper()
                proc_params = [p for p in proc_def[1:] if p.startswith(":")]
                proc_body = []

                # Collect procedure body until END, handling multi-line blocks
                i += 1
                while i < len(lines):
                    body_line = lines[i].strip()
                    if body_line.upper() == "END":
                        break
                    if body_line and not body_line.startswith(";"):
                        # Check if this line starts a bracket block (IF or REPEAT)
                        if "[" in body_line and "]" not in body_line:
                            # Multi-line block - collect until brackets balance
                            block_lines = [body_line]
                            bracket_depth = body_line.count("[") - body_line.count("]")
                            i += 1
                            while i < len(lines) and bracket_depth > 0:
                                next_line = lines[i].strip()
                                if next_line and not next_line.startswith(";"):
                                    block_lines.append(next_line)
                                    bracket_depth += next_line.count("[") - next_line.count("]")
                                i += 1
                            # Store block as multi-line with newline delimiter
                            proc_body.append("\n".join(block_lines))
                            continue
                        else:
                            proc_body.append(body_line)
                    i += 1

                # Store procedure definition
                self.logo_procedures[proc_name] = (proc_params, proc_body)
                self.log_output(f"📝 Defined procedure {proc_name}{proc_params}")
                self.debug_output(
                    f"Defined Logo procedure: {proc_name} with params {proc_params}"
                )
                i += 1
                continue

            # Check if this is a REPEAT command with opening bracket
            elif line.upper().startswith("REPEAT ") and "[" in line and "]" not in line:
                # Multi-line REPEAT block
                repeat_block = line
                i += 1
                bracket_depth = line.count("[") - line.count("]")

                # Collect lines until brackets are balanced
                while i < len(lines) and bracket_depth > 0:
                    next_line = lines[i].strip()
                    if next_line and not next_line.startswith(
                        ";"
                    ):  # Skip empty and comments
                        repeat_block += " " + next_line
                        bracket_depth += next_line.count("[") - next_line.count("]")
                    i += 1

                processed_lines.append(repeat_block)
            else:
                processed_lines.append(line)
                i += 1

        return "\n".join(processed_lines)


def create_demo_program():
    """Create a demo Time_Warp program"""
    return """L:START
T:Welcome to Time Warp Interpreter Demo!
A:NAME
T:Hello *NAME*! Let's do some math.
U:X=10
U:Y=20
T:X = *X*, Y = *Y*
U:SUM=*X*+*Y*
T:Sum of X and Y is *SUM*
T:
T:Let's count to 5:
U:COUNT=1
L:LOOP
Y:*COUNT* > 5
J:END_LOOP
T:Count: *COUNT*
U:COUNT=*COUNT*+1
J:LOOP
L:END_LOOP
T:
T:Program completed. Thanks for using Time Warp!
END"""


if __name__ == "__main__":
    # Simple test when run directly
    interpreter = Time_WarpInterpreter()
    DEMO_PROGRAM = create_demo_program()
    print("Running Time Warp interpreter demo...")
    interpreter.run_program(DEMO_PROGRAM)
