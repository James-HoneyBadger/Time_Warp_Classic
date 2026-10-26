"""User-installed language plugins.

A plugin is a small JSON manifest that teaches the IDE a language it does not
ship with.  The language is then run through an external runtime, exactly like
Python, JavaScript and Perl are, so nothing has to be compiled into the app.

Manifests live in ``~/.timewarp/plugins/`` (or any directory named in the
``TIMEWARP_PLUGIN_PATH`` environment variable) as either::

    ~/.timewarp/plugins/ruby.json
    ~/.timewarp/plugins/ruby/plugin.json

and look like::

    {
      "name": "Ruby",
      "executable": "ruby",
      "extension": ".rb",
      "args": [],
      "syntax": "ruby",
      "comment": "#",
      "keywords": ["def", "end", "puts"],
      "timeout": 30,
      "description": "Ruby 3 via the system ruby"
    }

``name`` and ``executable`` are required; everything else is optional.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_PLUGIN_DIR = Path.home() / ".timewarp" / "plugins"
PLUGIN_PATH_ENV = "TIMEWARP_PLUGIN_PATH"

# Names that are already built in; a plugin may not shadow them.
RESERVED_LANGUAGES = frozenset(
    {
        "pilot", "basic", "logo", "pascal", "prolog", "forth",
        "perl", "python", "javascript",
    }
)

DEFAULT_TIMEOUT = 30


class PluginError(ValueError):
    """A manifest could not be understood."""


@dataclass(frozen=True)
class PluginSpec:
    """One plugin language, as described by its manifest."""

    name: str
    executable: str
    extension: str = ""
    args: tuple = ()
    syntax: str = ""
    comment: str = ""
    keywords: tuple = ()
    timeout: float = DEFAULT_TIMEOUT
    description: str = ""
    source: Path | None = field(default=None, compare=False)

    @property
    def language(self):
        """Label shown in the language selector."""
        return self.name

    def to_manifest(self):
        """Return the manifest dictionary for this spec."""
        data = {
            "name": self.name,
            "executable": self.executable,
            "extension": self.extension,
            "args": list(self.args),
            "syntax": self.syntax,
            "comment": self.comment,
            "keywords": list(self.keywords),
            "timeout": self.timeout,
            "description": self.description,
        }
        return data


def _string(data, key, default="", required=False):
    value = data.get(key, default)
    if value is None:
        value = default
    if not isinstance(value, str):
        raise PluginError(f"'{key}' must be a string")
    value = value.strip()
    if required and not value:
        raise PluginError(f"'{key}' is required")
    return value


def _string_list(data, key):
    value = data.get(key, [])
    if value is None:
        return ()
    if isinstance(value, str):
        # A single string is a common slip; accept it as a one-item list.
        return (value.strip(),) if value.strip() else ()
    if not isinstance(value, (list, tuple)):
        raise PluginError(f"'{key}' must be a list of strings")
    items = []
    for item in value:
        if not isinstance(item, str):
            raise PluginError(f"'{key}' must contain only strings")
        if item.strip():
            items.append(item.strip())
    return tuple(items)


def _normalise_extension(value):
    if not value:
        return ""
    extension = value.strip().lower()
    if not extension.startswith("."):
        extension = "." + extension
    return extension


def parse_manifest(data, source=None):
    """Validate *data* (a decoded JSON object) and return a :class:`PluginSpec`."""
    if not isinstance(data, dict):
        raise PluginError("manifest must be a JSON object")

    name = _string(data, "name", required=True)
    if name.lower() in RESERVED_LANGUAGES:
        raise PluginError(f"'{name}' is a built-in language")

    executable = _string(data, "executable", required=True)
    timeout = data.get("timeout", DEFAULT_TIMEOUT)
    if not isinstance(timeout, (int, float)) or isinstance(timeout, bool):
        raise PluginError("'timeout' must be a number of seconds")
    if timeout <= 0:
        raise PluginError("'timeout' must be greater than zero")

    return PluginSpec(
        name=name,
        executable=executable,
        extension=_normalise_extension(_string(data, "extension", "txt")),
        args=_string_list(data, "args"),
        syntax=_string(data, "syntax"),
        comment=_string(data, "comment"),
        keywords=_string_list(data, "keywords"),
        timeout=float(timeout),
        description=_string(data, "description"),
        source=source,
    )


def plugin_directories(directories=None):
    """Directories to search for manifests, most specific first."""
    if directories is not None:
        return [Path(directory) for directory in directories]

    found = [DEFAULT_PLUGIN_DIR]
    extra = os.environ.get(PLUGIN_PATH_ENV, "")
    for entry in extra.split(os.pathsep):
        entry = entry.strip()
        if entry:
            found.append(Path(entry))
    return found


def _manifest_files(directory):
    """Yield candidate manifest paths inside *directory*."""
    directory = Path(directory)
    if not directory.is_dir():
        return
    for child in sorted(directory.iterdir()):
        if child.is_file() and child.suffix.lower() == ".json":
            yield child
        elif child.is_dir() and (child / "plugin.json").is_file():
            yield child / "plugin.json"


def discover_plugins(directories=None):
    """Load every manifest found, returning ``(specs, problems)``.

    Problems are human-readable strings; a broken plugin never stops the
    others from loading, and an earlier directory wins over a later one.
    """
    specs = {}
    problems = []
    for directory in plugin_directories(directories):
        for manifest in _manifest_files(directory):
            try:
                with open(manifest, "r", encoding="utf-8") as handle:
                    data = json.load(handle)
                spec = parse_manifest(data, source=manifest)
            except (OSError, json.JSONDecodeError) as exc:
                problems.append(f"{manifest.name}: {exc}")
                continue
            except PluginError as exc:
                problems.append(f"{manifest.name}: {exc}")
                continue

            key = spec.name.lower()
            if key in specs:
                problems.append(
                    f"{manifest.name}: '{spec.name}' already loaded from "
                    f"{specs[key].source}"
                )
                continue
            specs[key] = spec
    return list(specs.values()), problems


class PluginRegistry:
    """The plugin languages available to this session."""

    def __init__(self, specs=(), problems=()):
        self._specs = {}
        self._executors = {}
        for spec in specs:
            self._specs.setdefault(spec.name.lower(), spec)
        self.problems = list(problems)

    @classmethod
    def load(cls, directories=None):
        """Discover plugins on disk and build a registry."""
        specs, problems = discover_plugins(directories)
        return cls(specs, problems)

    # ---- lookups -----------------------------------------------------

    def __len__(self):
        return len(self._specs)

    def __iter__(self):
        return iter(sorted(self._specs.values(), key=lambda spec: spec.name.lower()))

    def names(self):
        """Plugin language labels, sorted by name."""
        return [spec.name for spec in self]

    def get(self, language):
        """The spec for *language* (case-insensitive), or None."""
        if not language:
            return None
        return self._specs.get(str(language).strip().lower())

    def extension_map(self):
        """``{".rb": "Ruby"}`` for every plugin that declares an extension."""
        mapping = {}
        for spec in self:
            if spec.extension:
                mapping.setdefault(spec.extension, spec.name)
        return mapping

    def executor(self, interpreter, language):
        """A ready-to-use executor for *language*, or None."""
        spec = self.get(language)
        if spec is None:
            return None
        key = spec.name.lower()
        if key not in self._executors:
            from core.languages.plugin_executor import PluginExecutor

            self._executors[key] = PluginExecutor(interpreter, spec)
        return self._executors[key]

    # ---- authoring helpers -------------------------------------------

    @staticmethod
    def write_example(directory=None):
        """Create a commented example manifest and return its path."""
        target_dir = Path(directory) if directory else DEFAULT_PLUGIN_DIR
        target_dir.mkdir(parents=True, exist_ok=True)
        target = target_dir / "example-python.json"
        if target.exists():
            return target

        example = {
            "name": "PyPlugin",
            "description": "Example plugin: runs Python through a manifest",
            "executable": "python3",
            "extension": ".tppy",
            "args": ["-u"],
            "syntax": "python",
            "comment": "#",
            "keywords": ["def", "class", "print", "import"],
            "timeout": 20,
        }
        target.write_text(json.dumps(example, indent=2) + "\n", encoding="utf-8")
        return target
