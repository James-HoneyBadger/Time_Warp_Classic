"""
Stub / placeholder classes for features not yet implemented.

These are loaded as fallbacks when optional modules (games, audio, hardware,
IoT, networking, animation) are not installed.  Each stub provides the same
public API surface so the interpreter can instantiate them without error.
"""


# ---------------------------------------------------------------------------
# Audio
# ---------------------------------------------------------------------------

class AudioEngine:
    """Stub audio engine – no-ops for all calls."""

    class _SpatialStub:
        """Stub spatial audio sub-system – no-ops."""

        @staticmethod
        def set_listener_position(*args):
            """Stub: set listener position – no-op."""

    spatial_audio = _SpatialStub()

    def __init__(self) -> None:
        self.clips: dict = {}
        self.sound_library: dict = {}

    def load_audio(self, *a):
        """Stub: load an audio clip – always returns False."""
        return False

    def play_sound(self, *a):
        """Stub: play a sound – always returns None."""
        return None

    def stop_sound(self, *a):
        """Stub: stop a sound – always returns False."""
        return False

    def stop_all_sounds(self):
        """Stub: stop all sounds – no-op."""

    def play_music(self, *a):
        """Stub: play music – always returns False."""
        return False

    def stop_music(self, *a):
        """Stub: stop music – always returns False."""
        return False

    def set_master_volume(self, *a):
        """Stub: set master volume – no-op."""

    def set_sound_volume(self, *a):
        """Stub: set sound volume – no-op."""

    def set_music_volume(self, *a):
        """Stub: set music volume – no-op."""

    def get_audio_info(self):
        """Stub: return empty audio info dict."""
        return {"mixer_available": False, "loaded_clips": 0,
                "playing_sounds": 0, "built_in_sounds": []}


# ---------------------------------------------------------------------------
# Game / Multiplayer
# ---------------------------------------------------------------------------

class GameManager:
    """Stub game manager."""

    session_id = None
    game_mode = "cooperative"
    max_players = 8
    is_server = False
    game_state = "waiting"

    def __init__(self) -> None:
        self.players: dict = {}

    def set_output_callback(self, cb):
        """Stub: register output callback – no-op."""

    def create_object(self, *a):
        """Stub: create a scene object – always returns False."""
        return False

    def move_object(self, *a):
        """Stub: move a scene object – always returns False."""
        return False

    def set_gravity(self, *a):
        """Stub: set gravity – no-op."""

    def set_velocity(self, *a):
        """Stub: set object velocity – always returns False."""
        return False

    def check_collision(self, *a):
        """Stub: check collision – always returns False."""
        return False

    def render_scene(self, *a):
        """Stub: render scene – always returns False."""
        return False

    def update_physics(self, *a):
        """Stub: update physics – no-op."""

    def delete_object(self, *a):
        """Stub: delete a scene object – always returns False."""
        return False

    def list_objects(self):
        """Stub: list scene objects – always returns empty list."""
        return []

    def clear_scene(self):
        """Stub: clear the scene – no-op."""

    def get_object_info(self, *a):
        """Stub: get object info – always returns None."""
        return None

    def get_object(self, *a):
        """Stub: get a scene object – always returns None."""
        return None

    def get_game_info(self):
        """Stub: get game info – returns empty dict."""
        return {}

    def add_player(self, *a):
        """Stub: add a multiplayer player – raises NotImplementedError."""
        raise NotImplementedError("Multiplayer not available")

    def remove_player(self, *a):
        """Stub: remove a multiplayer player – raises NotImplementedError."""
        raise NotImplementedError("Multiplayer not available")

    def start_multiplayer_game(self):
        """Stub: start a multiplayer game – raises NotImplementedError."""
        raise NotImplementedError("Multiplayer not available")

    def end_multiplayer_game(self, *a):
        """Stub: end a multiplayer game – raises NotImplementedError."""
        raise NotImplementedError("Multiplayer not available")


class MultiplayerGameManager(GameManager):
    """Stub multiplayer game manager – all multiplayer calls are no-ops."""

    def __init__(self, *a, **kw) -> None:
        """Initialise stub multiplayer game manager."""
        super().__init__()

    def add_player(self, *a):
        """Stub: add player – no-op."""

    def remove_player(self, *a):
        """Stub: remove player – no-op."""

    def start_multiplayer_game(self):
        """Stub: start multiplayer game – no-op."""

    def end_multiplayer_game(self, *a):
        """Stub: end multiplayer game – no-op."""


# ---------------------------------------------------------------------------
# Collaboration / Networking
# ---------------------------------------------------------------------------

class _NetworkManager:
    """Stub network manager – raises NotImplementedError for all calls."""

    is_server = False
    is_client = False
    running = False

    def start_server(self, *a):
        """Stub: start server – raises NotImplementedError."""
        raise NotImplementedError("Networking not available")

    def connect_to_server(self, *a):
        """Stub: connect to server – raises NotImplementedError."""
        raise NotImplementedError("Networking not available")

    def send_message(self, *a):
        """Stub: send message – raises NotImplementedError."""
        raise NotImplementedError("Networking not available")

    def disconnect(self, *a):
        """Stub: disconnect – raises NotImplementedError."""
        raise NotImplementedError("Networking not available")


class CollaborationManager:
    """Stub collaboration manager backed by a no-op network manager."""

    def __init__(self) -> None:
        """Initialise with a stub network manager."""
        self.network_manager = _NetworkManager()


# ---------------------------------------------------------------------------
# Hardware
# ---------------------------------------------------------------------------

class ArduinoController:
    """Stub Arduino controller – all calls are no-ops or return sentinel values."""

    def connect(self, *a):
        """Stub: connect to Arduino – always returns False."""
        return False

    def send_command(self, *a):
        """Stub: send a command – always returns False."""
        return False

    def read_sensor(self):
        """Stub: read sensor value – always returns None."""
        return None


class RPiController:
    """Stub Raspberry Pi GPIO controller – all calls are no-ops."""

    def set_pin_mode(self, *a):
        """Stub: set pin mode – always returns False."""
        return False

    def digital_write(self, *a):
        """Stub: digital write – always returns False."""
        return False

    def digital_read(self, *a):
        """Stub: digital read – always returns False."""
        return False


class RobotInterface:
    """Stub robot interface – movement calls are no-ops."""

    def move_forward(self, *a):
        """Stub: move forward – no-op."""

    def move_backward(self, *a):
        """Stub: move backward – no-op."""

    def turn_left(self, *a):
        """Stub: turn left – no-op."""

    def turn_right(self, *a):
        """Stub: turn right – no-op."""

    def stop(self):
        """Stub: stop robot – no-op."""

    def read_distance_sensor(self):
        """Stub: read distance sensor – returns 30.0 cm."""
        return 30.0

    def read_light_sensor(self):
        """Stub: read light sensor – returns 50.0 (ambient)."""
        return 50.0


class GameController:
    """Stub game-controller / joystick – all inputs return neutral values."""

    def update(self):
        """Stub: poll events – always returns False."""
        return False

    def get_button(self, *a):
        """Stub: get button state – always returns False."""
        return False

    def get_axis(self, *a):
        """Stub: get axis value – always returns 0.0."""
        return 0.0


class SensorVisualizer:
    """Stub sensor visualiser – drawing methods are no-ops."""

    def __init__(self, canvas=None) -> None:
        """Initialise stub sensor visualiser."""

    def draw_chart(self, *a):
        """Stub: draw chart – no-op."""

    def add_data_point(self, *a):
        """Stub: add data point – no-op."""


# ---------------------------------------------------------------------------
# IoT
# ---------------------------------------------------------------------------

class IoTDeviceManager:
    """Stub IoT device manager – runs in simulation mode."""

    simulation_mode = True

    def discover_devices(self):
        """Stub: discover IoT devices – always returns 0."""
        return 0

    def connect_device(self, *a):
        """Stub: connect to a device – always returns False."""
        return False

    def connect_all(self):
        """Stub: connect all devices – always returns 0."""
        return 0

    def get_device_data(self, *a):
        """Stub: get device data – always returns None."""
        return None

    def send_device_command(self, *a):
        """Stub: send device command – raises NotImplementedError."""
        raise NotImplementedError("IoT not available")

    def create_device_group(self, *a):
        """Stub: create device group – raises NotImplementedError."""
        raise NotImplementedError("IoT not available")

    def control_group(self, *a):
        """Stub: control device group – raises NotImplementedError."""
        raise NotImplementedError("IoT not available")


class SmartHomeHub:
    """Stub smart home hub – runs in simulation mode."""

    simulation_mode = True

    def setup_home(self):
        """Stub: set up home automation – returns zero-device summary."""
        return {"discovered": 0, "connected": 0}

    def create_scene(self, *a):
        """Stub: create automation scene – no-op."""

    def activate_scene(self, *a):
        """Stub: activate automation scene – raises NotImplementedError."""
        raise NotImplementedError("Smart home not available")

    def set_environmental_target(self, *a):
        """Stub: set environmental target – no-op."""

    def monitor_environment(self):
        """Stub: monitor environment – always returns empty list."""
        return []


class SensorNetwork:
    """Stub sensor network – runs in simulation mode."""

    simulation_mode = True

    def add_sensor(self, *a):
        """Stub: add a sensor to the network – no-op."""

    def collect_data(self):
        """Stub: collect sensor data – always returns empty dict."""
        return {}

    def analyze_trends(self, *a):
        """Stub: analyse sensor trends – always returns None."""
        return None

    def predict_values(self, *a):
        """Stub: predict sensor values – always returns None."""
        return None


class AdvancedRobotInterface:
    """Stub advanced robot interface – runs in simulation mode."""

    simulation_mode = True
    mission_status = "idle"

    def plan_path(self, *a):
        """Stub: plan navigation path – always returns empty list."""
        return []

    def execute_mission(self, *a):
        """Stub: execute robot mission – always returns empty list."""
        return []

    def scan_environment(self):
        """Stub: scan environment – returns minimal dummy sensor data."""
        return {"lidar": {"range": 10.0}, "camera": {"objects": []}}

    def avoid_obstacle(self):
        """Stub: obstacle avoidance – returns 'no_obstacle'."""
        return "no_obstacle"

    def learn_environment(self):
        """Stub: learn from environment – returns zero-obstacle summary."""
        return {"obstacles_detected": 0}

    def move_to_position(self, *a):
        """Stub: move to position – no-op."""


# ---------------------------------------------------------------------------
# Animation utilities
# ---------------------------------------------------------------------------

class Mixer:
    """Stub audio mixer – registers sound paths but never plays them."""

    def __init__(self) -> None:
        """Initialise stub mixer with an empty sound registry."""
        self.registry: dict[str, str] = {}

    def snd(self, name, path, vol=0.8):
        """Stub: register a sound path – stored but never loaded."""
        self.registry[name] = path

    def play_snd(self, name):
        """Stub: play a registered sound – no-op."""


class Tween:
    """Lightweight linear tween that interpolates a value in a store dict."""

    def __init__(self, store, key, a, b, dur_ms, ease="linear") -> None:
        self.store = store
        self.key = key
        self.a = float(a)
        self.b = float(b)
        self.dur = max(1, int(dur_ms))
        self.t = 0
        self.done = False

    def step(self, dt):
        """Advance the tween by dt milliseconds."""
        if self.done:
            return
        self.t += dt
        u = min(1.0, self.t / self.dur)
        self.store[self.key] = self.a + (self.b - self.a) * u
        if self.t >= self.dur:
            self.store[self.key] = self.b
            self.done = True


class Timer:
    """Lightweight countdown timer used by the animation utilities."""

    def __init__(self, delay_ms, label) -> None:
        self.delay = max(0, int(delay_ms))
        self.label = label
        self.t = 0
        self.done = False


class Particle:
    """Simple particle for stub particle-system effects."""

    def __init__(self, x, y, vx, vy, life) -> None:
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.life = life
        self.size = 2
        self.color = "white"

    def step(self, dt):
        """Advance particle position by dt milliseconds."""
        if self.life <= 0:
            return
        self.x += self.vx * dt / 1000.0
        self.y += self.vy * dt / 1000.0
        self.life -= dt
