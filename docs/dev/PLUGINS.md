# Language Plugins

Time Warp Classic ships nine languages. A **plugin** adds another one without
touching the code: you write a small JSON manifest that names an external
runtime, and the IDE treats the language like Python, JavaScript or Perl —
the whole program is written to a temporary file and run by that runtime, with
its output streamed into the console.

No Python code is required, and plugins cannot break the built-in languages.

## Where manifests live

```
~/.timewarp/plugins/ruby.json          # single-file manifest
~/.timewarp/plugins/ruby/plugin.json   # or a folder with plugin.json inside
```

Every `*.json` file in the folder is read, and every sub-folder that contains
`plugin.json`. Extra folders can be searched by setting
`TIMEWARP_PLUGIN_PATH` to a `:`-separated (`;` on Windows) list of paths.
The first manifest found for a name wins; later duplicates are reported and
ignored.

The quickest start is **Preferences → Plugins → Create Example Plugin**, which
writes `example-python.json` into the folder and loads it immediately.

## Manifest reference

| Field | Required | Meaning |
|-------|----------|---------|
| `name` | yes | Language label shown in the selector (e.g. `"Ruby"`). Built-in names are reserved. |
| `executable` | yes | Runtime command or absolute path (`"ruby"`, `"lua"`, `"/opt/lua/bin/lua"`). |
| `extension` | no | File suffix for Save As and open-file detection (`".rb"`, `"rb"` — both accepted). Default `.txt`. |
| `args` | no | Runtime flags inserted before the script path (`["-u"]`). |
| `syntax` | no | [Pygments lexer alias](https://pygments.org/docs/lexers/) for highlighting (`"ruby"`, `"lua"`, `"python"`). Unknown aliases fall back to plain text. |
| `comment` | no | Line-comment marker (`"#"`, `"--"`, `";"`), used to stay quiet while completing inside comments. |
| `keywords` | no | Words offered by completion (`["def", "end", "puts"]`). |
| `timeout` | no | Seconds before the run is abandoned. Default `30`. |
| `description` | no | Free text; shown nowhere yet, kept for your own notes. |

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

Save that as `~/.timewarp/plugins/ruby.json`, choose **Ruby** in the language
selector, type `puts "hello"` and press **F5**. The console shows the output
and then `READY.`.

## Example: Lua with runtime flags

```json
{
  "name": "Lua",
  "executable": "lua5.4",
  "extension": ".lua",
  "args": [],
  "syntax": "lua",
  "comment": "--",
  "keywords": ["function", "end", "local", "print", "for", "while"]
}
```

## What the IDE does with a plugin

- **Language selector** — the name is appended after the nine built-ins.
- **Syntax highlighting** — from `syntax` (Pygments alias); `comment` keeps
  completion quiet inside comments.
- **Completion** — `keywords` are offered as you type and with Ctrl+Space.
- **Save As / open** — `extension` becomes the default suffix and is used to
  detect the language when a file is opened.
- **Run** — the program runs in one subprocess; console input is forwarded to
  its stdin, output streams line by line, **Ctrl+.** stops it, and the failing
  script line is reported as a clickable `?ERROR IN n`.

## Reloading and diagnostics

After editing or adding a manifest, use **Preferences → Plugins → Reload
Plugins**. Loaded languages are listed in the console:

```
Plugins loaded: Lua, Ruby
```

Anything that could not be loaded is reported with a `?PLUGIN:` prefix, for
example:

```
?PLUGIN: ruby.json: 'executable' is required
?PLUGIN: lua.json: 'Ruby' already loaded from /home/you/.timewarp/plugins/ruby.json
```

## Troubleshooting

| Message | Cause |
|---------|-------|
| `?RUBY NOT FOUND - the manifest asks for 'ruby', which is not on PATH` | The runtime is not on `PATH` and `executable` is not an existing file path. The plugin is also reported in the IDE output as `?PLUGIN: Ruby: …`. |
| `?PLUGIN: … is a built-in language` | `name` clashes with PILOT, BASIC, Logo, Pascal, Prolog, Forth, Perl, Python or JavaScript. |
| `?PLUGIN: … is required` | `name` or `executable` is missing or empty. |
| `?PLUGIN: … 'timeout' must be …` | `timeout` must be a positive number of seconds. |
| `Expecting property name …` | The manifest is not valid JSON (a trailing comma is the usual culprit). |

## Limitations

- A plugin is an **external runtime**, not an in-process interpreter: it cannot
  draw on the turtle canvas and has no debugger or breakpoints.
- One process per run — there is no shared session between runs.
- Only `name` and `executable` are required, but without `extension` and
  `syntax` the language behaves like plain text.
- Writing a new *built-in* language still means adding an executor under
  `core/languages/` as described in
  [TECHNICAL_REFERENCE.md](TECHNICAL_REFERENCE.md).
