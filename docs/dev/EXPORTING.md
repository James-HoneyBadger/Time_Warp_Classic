# Exporting a Runner

`File → Export Runner...` packages the program in the editor as a **standalone
runner**: a single `.pyz` file that executes the program and exits, with no
IDE, no project files and no third-party packages.

It is a [Python zipapp](https://docs.python.org/3/library/zipapp.html) — a zip
file with a `#!/usr/bin/env python3` line in front — so it needs only Python
3.9 or newer on the machine that runs it.

## Using it

1. Write the program and pick its language in the selector.
2. **File → Export Runner...**, choose where to save `myprog.pyz`.
3. Run it:

```
python myprog.pyz          # any platform
./myprog.pyz               # Linux / macOS, executable bit is set for you
```

The exit code is `0` when the program finished cleanly and `1` when it reported
an error, so exported runners work in scripts and CI.

The console in the IDE confirms the result:

```
Runner written to /home/you/Desktop/myprog.pyz
Run it with: python myprog.pyz
```

## What goes inside

```
myprog.pyz
├── __main__.py        # calls core.runner.run_source()
├── program_data.py    # NAME, LANGUAGE, PROGRAM (the source, embedded)
└── core/              # the interpreter package
```

Nothing is read from your installation at run time, and the language of the
embedded program can be changed only by exporting again.

## Command line

The same headless path is available directly from the checkout:

```
python Time_Warp.py --run myprog.twrun             # a bundle
python Time_Warp.py --run hello.bas --language basic
python Time_Warp.py --version
```

Exit codes: `0` success, `1` program error, `2` bad invocation (missing file,
missing `--language`, unreadable bundle).

`READY.` and `Interpreter ready.` are IDE messages and are not printed by the
runner; genuine `?ERROR IN n: ...` lines still are.

## Language support

| Languages | Inside the exported runner |
|-----------|---------------------------|
| PILOT, BASIC, Logo, Pascal, Prolog, Forth | Fully contained — only Python is needed |
| Python, JavaScript, Perl | Works if that runtime is installed on the target machine |
| Plugin languages | **Not included** — export from the IDE that has the plugin, or run the source with the runtime yourself |

Turtle graphics run in the IDE's headless stub mode: the drawing commands are
reported as text (`Drawing line from ... to ...`) because there is no window to
draw into.

Live console `INPUT` works when the runner is started from a terminal; the
prompt goes to stdout and the answer is read from stdin.

## Bundles

An exported runner embeds its program, so re-exporting is the way to change it.
If you would rather keep the source in version control, `core.export` also
writes `.twrun` bundles — small JSON files holding the language and the source:

```python
from core.export import RunBundle, write_bundle

write_bundle(RunBundle("basic", open("hello.bas").read(), name="hello"),
             "hello.twrun")
```

```bash
python Time_Warp.py --run hello.twrun
```

`.twrun` files are validated on load: a foreign JSON file, a newer bundle
version, or a missing language is refused with a clear message instead of
running the wrong thing.
