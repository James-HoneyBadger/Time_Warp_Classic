# Language Plugins

Time Warp Classic has nine languages built in. A plugin adds a tenth (or
eleventh, or twentieth) without touching the code: a JSON manifest names an
external runtime, and the IDE treats that language the way it treats Python,
JavaScript and Perl. The whole program goes into a temporary file, the
runtime runs it in a child process, and its output streams into the console.

Plugins are configuration, not code. A broken manifest is reported and
skipped; it cannot affect the built-in languages.

## How it fits together

```
~/.timewarp/plugins/*.json                core/plugins.py
TIMEWARP_PLUGIN_PATH dirs   ──────────►   discover_plugins() -> PluginSpec, problems
                                          PluginRegistry
                                               │  interp.plugins = registry
                                               ▼
                       Time_WarpInterpreter.run_program(text, language="Ruby")
                                               │  registry.executor(interp, "Ruby")
                                               ▼
                       core/languages/plugin_executor.py  PluginExecutor
                       (a SubprocessExecutor configured from the spec)
```

`run_program()` checks the built-in names first, so a plugin can never
shadow PILOT, BASIC and the rest; the manifest parser also rejects those
names outright.

## Where manifests live

```
~/.timewarp/plugins/ruby.json           # a single-file manifest
~/.timewarp/plugins/lua/plugin.json     # or a folder with plugin.json inside
```

In each plugin folder, every top-level `*.json` file is read, plus
`plugin.json` in each direct sub-folder, in sorted order. Nothing deeper is
searched.

`~/.timewarp/plugins` is always searched first. To add more folders, set
`TIMEWARP_PLUGIN_PATH` to a list separated by the OS path separator (`:` on
Linux and macOS, `;` on Windows). If two manifests use the same `name`
(case-insensitive), the first one found wins and the later one is reported.

The quickest way to start is **Preferences → Plugins → Create Example Plugin**.
It writes `example-python.json` to `~/.timewarp/plugins` (an existing file is
left alone) and reloads. That manifest defines **PyPlugin**, which runs
`python3 -u` on `.tppy` files with a 20-second timeout.

## Manifest reference

Only `name` and `executable` are required. String values are trimmed; a
`null` value counts as absent.

| Key | Type | Default | Meaning |
|-----|------|---------|---------|
| `name` | string | required | Label in the language selector, e.g. `"Ruby"`. The nine built-in names are reserved, case-insensitively. |
| `executable` | string | required | Command looked up on `PATH` (`"ruby"`), or a path to an existing file (`"/opt/lua/bin/lua"`). |
| `extension` | string | `".txt"` | Default suffix for Save As, and the suffix that selects this language when a file is opened. `"rb"`, `".rb"` and `".RB"` all become `".rb"`. |
| `args` | list of strings | `[]` | Arguments placed between the executable and the script path. A single string counts as a one-item list. |
| `syntax` | string | `""` | [Pygments lexer alias](https://pygments.org/docs/lexers/) used for highlighting (`"ruby"`, `"lua"`). Empty or unknown aliases give plain text. |
| `comment` | string | `""` | Line-comment marker (`"#"`, `"--"`). Completion stays quiet after it. |
| `keywords` | list of strings | `[]` | Words offered by completion. A single string counts as a one-item list. |
| `timeout` | number | `30` | Seconds before the child process is killed. Must be greater than zero, and `true`/`false` are rejected. |
| `description` | string | `""` | Free text for your own notes. Nothing displays it. |

Unknown keys are ignored.

The runtime is started as `[executable, *args, /path/to/tmpXXXX<extension>]`
with no shell. Its stdout and stderr are merged into the console.

The default extension has one side effect. A manifest with no `extension`
claims `.txt`, so opening any `.txt` file in the IDE selects that plugin.
Give every plugin a real extension.

## Example: Ruby

```json
{
  "name": "Ruby",
  "description": "Ruby 3 via the system ruby",
  "executable": "ruby",
  "extension": ".rb",
  "syntax": "ruby",
  "comment": "#",
  "keywords": ["def", "end", "puts", "require", "class", "module"],
  "timeout": 30
}
```

Save that as `~/.timewarp/plugins/ruby.json`, then use **Preferences → Plugins
→ Reload Plugins** (or restart). Choose **Ruby** in the language selector,
type `puts "hello"` and press **F5**. The console shows `hello`, then
`READY.`.

## Example: Lua in a folder

`~/.timewarp/plugins/lua/plugin.json`:

```json
{
  "name": "Lua",
  "executable": "lua5.4",
  "extension": ".lua",
  "syntax": "lua",
  "comment": "--",
  "keywords": ["function", "end", "local", "print", "for", "while"]
}
```

## What the IDE does with a plugin

- **Language selector**: plugin names come after the nine built-ins, sorted.
  A plugin whose runtime cannot be found is labelled
  `Name (runtime missing)`.
- **Highlighting**: the `syntax` lexer, in the desktop editor and in the
  browser IDE.
- **Completion**: `keywords` are offered as you type and on Ctrl+Space.
  Nothing is offered after the `comment` marker.
- **Files**: `extension` is the Save As default and selects the language on
  Open.
- **Run (F5)**: one child process per run. Output streams line by line.
  Lines typed into the console bar while it runs are sent to the program's
  stdin. **Stop** (Ctrl+.) kills the process and prints `BREAK`.
- **Errors**: a non-zero exit is reported as `?ERROR IN n: <last line of
  output>` if a Python-, Node- or Perl-style traceback names the script
  line, and as `?ERROR: ...` otherwise. A `?HINT:` line may follow. Click an
  `?ERROR IN n` line to jump to that line in the editor.
- **Web IDE**: `python3 Time_Warp.py --web` loads the same plugin folders
  (`~/.timewarp/plugins` and `TIMEWARP_PLUGIN_PATH`) and prints
  `plugin skipped: ...` for each broken manifest. **Program → Open Web IDE**
  passes the desktop's loaded plugins to the server it starts.

`python3 Time_Warp.py --run` and exported runners never load the plugin
folder, so plugin languages are not available there (see
[EXPORTING.md](EXPORTING.md)).

## Reloading and diagnostics

After you edit or add a manifest, use **Preferences → Plugins → Reload
Plugins**. Loaded languages are listed in the console:

```
Plugins loaded: Lua, Ruby
```

Problems are reported with a `?PLUGIN:` prefix and the manifest's file name
(not its folder):

```
?PLUGIN: Lua: 'lua5.4' was not found on PATH
?PLUGIN: ruby.json: 'executable' is required
?PLUGIN: plugin.json: 'Ruby' already loaded from /home/you/.timewarp/plugins/ruby.json
?PLUGIN: broken.json: Illegal trailing comma before end of object: line 1 column 36 (char 35)
```

The JSON error text comes from Python's `json` module and varies between
Python versions. **Preferences → Plugins → Open Plugins Folder** creates the
folder if it does not exist, prints `Plugin folder: <path>` and opens it in
the file manager.

## Troubleshooting

| Message | Cause |
|---------|-------|
| `?PLUGIN: <name>: '<exe>' was not found on PATH` | The runtime is not on `PATH`, and `executable` is not an existing file. The plugin still loads. |
| `?<NAME> NOT FOUND - the manifest asks for '<exe>', which is not on PATH` | You ran a plugin whose runtime is missing. |
| `?PLUGIN: <file>: '<name>' is a built-in language` | `name` clashes with PILOT, BASIC, Logo, Pascal, Prolog, Forth, Perl, Python or JavaScript. |
| `?PLUGIN: <file>: 'name' is required` (or `'executable'`) | The key is missing, empty or only whitespace. |
| `?PLUGIN: <file>: '<key>' must be a string` | A string key holds a number, list or other value. |
| `?PLUGIN: <file>: 'args' must be a list of strings` / `must contain only strings` | `args` or `keywords` has the wrong shape. |
| `?PLUGIN: <file>: 'timeout' must be a number of seconds` / `must be greater than zero` | `timeout` is not a positive number. |
| `?PLUGIN: <file>: manifest must be a JSON object` | The file holds a list or a bare value. |
| `?PLUGIN: <file>: <JSON error>` | The file is not valid JSON. A trailing comma is the usual cause. |
| `?ERROR: <Name> script timed out after Ns` | The program ran longer than `timeout`. |

## Python API

Everything above is available from `core/plugins.py` without Tk.

| Name | Notes |
|------|-------|
| `parse_manifest(data, source=None)` | Validates a decoded JSON object. Returns a `PluginSpec` or raises `PluginError` (a `ValueError`). |
| `plugin_directories(directories=None)` | Returns *directories* as `Path`s when given. Otherwise returns `[DEFAULT_PLUGIN_DIR, *TIMEWARP_PLUGIN_PATH]`. |
| `discover_plugins(directories=None)` | Returns `(specs, problems)`. `problems` is a list of strings. |
| `PluginSpec` | Frozen dataclass with `name`, `executable`, `extension`, `args` (tuple), `syntax`, `comment`, `keywords` (tuple), `timeout` (float), `description` and `source` (manifest path). Also has `.language` (lower-case name) and `.to_manifest()`. |
| `PluginRegistry(specs=(), problems=())` | Lookup table. Build one with `PluginRegistry.load(directories=None)`. |
| `registry.names()` | Plugin names, sorted. `len(registry)` and `for spec in registry` work too. |
| `registry.get(name)` | `PluginSpec` or `None`. The lookup is case-insensitive. |
| `registry.extension_map()` | `{".rb": "Ruby", ...}` |
| `registry.problems` | The problem strings from discovery. |
| `registry.executor(interpreter, name)` | A `PluginExecutor` for that language, or `None`. |
| `PluginRegistry.write_example(directory=None)` | Writes `example-python.json` and returns its path. |
| `DEFAULT_PLUGIN_DIR`, `PLUGIN_PATH_ENV`, `RESERVED_LANGUAGES`, `DEFAULT_TIMEOUT` | Constants. |

`PluginExecutor(interpreter, spec)` in `core/languages/plugin_executor.py`
subclasses `SubprocessExecutor` (see
[TECHNICAL_REFERENCE.md](TECHNICAL_REFERENCE.md#language-executors)). It
finds the runtime with `shutil.which()`, or accepts an existing file path. It
does not probe `--version`.

Running a plugin from your own code:

```python
import contextlib
import io

from core.interpreter import Time_WarpInterpreter
from core.plugins import PluginRegistry

registry = PluginRegistry.load(["my-plugins"])   # only this folder
print(registry.names(), registry.problems)

with contextlib.redirect_stdout(io.StringIO()):  # hide "Interpreter ready."
    interp = Time_WarpInterpreter()
interp.plugins = registry
interp.run_program('print("hello from a plugin")\nprint(6 * 7)\n', language="PyPlugin")
# hello from a plugin
# 42
# READY.
```

Here `my-plugins/` holds the example manifest.

`registry.executor(interpreter, name)` caches one executor per language and
reuses it while the same interpreter asks. A different interpreter gets a new
executor bound to it, so one registry can be shared by many interpreters (the
web server uses a fresh interpreter for every run).

## Limitations

- A plugin runs an external program. It cannot draw on the turtle canvas,
  and breakpoints and step-through do not apply to it.
- Each run is a fresh process, so no state carries over from one run to the
  next.
- The console bar does not run plugin code. With a plugin selected and no
  program running, a typed line is not sent to the plugin runtime. It goes
  through the built-in line detection instead (`set_language_mode()` accepts
  only built-in names), so it usually does nothing.
- Programs that read stdin get only the lines you type into the console bar
  while they run. In the browser IDE they get only the lines in the run's
  input box.
- To add a built-in, in-process language you still have to write an executor.
  See [TECHNICAL_REFERENCE.md](TECHNICAL_REFERENCE.md#adding-a-language).
