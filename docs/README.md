# Time Warp Classic documentation

A map of the docs, grouped by what you are trying to do. Installation lives in
[SETUP.md](../SETUP.md); the project overview is the top-level
[README](../README.md).

## Start here

| Document | Read it when |
|----------|--------------|
| [Quick start](QUICK_START.md) | You want a program running in a few minutes |
| [Setup](../SETUP.md) | Installing, Tkinter, venvs, Docker, tests, releasing |
| [Example programs](../examples/README.md) | You learn faster from working code |
| [FAQ](FAQ.md) | You have a "can it do X?" question |
| [Troubleshooting](TROUBLESHOOTING.md) | Something does not start or does not run |
| [Changelog](../CHANGELOG.md) | You want to know what changed in a release |

## Learning the languages

[Language tutorials](user/LANGUAGE_TUTORIALS.md) walk through all nine. The
references cover each dialect as Time Warp implements it:

| Built-in interpreters | External runtimes |
|-----------------------|-------------------|
| [BASIC](languages/BASIC_REFERENCE.md) | [Python](languages/PYTHON_REFERENCE.md) |
| [PILOT](languages/PILOT_REFERENCE.md) | [JavaScript](languages/JAVASCRIPT_REFERENCE.md) (Node.js) |
| [Logo](languages/LOGO_REFERENCE.md) | [Perl](languages/PERL_REFERENCE.md) |
| [Pascal](languages/PASCAL_REFERENCE.md) | |
| [Prolog](languages/PROLOG_REFERENCE.md) | |
| [Forth](languages/FORTH_REFERENCE.md) | |

Example programs, two or three per language:
[BASIC](../examples/basic/), [PILOT](../examples/pilot/),
[Logo](../examples/logo/), [Pascal](../examples/pascal/),
[Prolog](../examples/prolog/), [Forth](../examples/forth/),
[Python](../examples/python/), [JavaScript](../examples/javascript/),
[Perl](../examples/perl/).

For turtle graphics, start with the Logo reference; BASIC has turtle
commands too.

## Beyond the desktop window

| Document | Covers |
|----------|--------|
| [Web IDE](dev/WEB.md) | `--web`, the browser IDE, its limits and the JSON API |
| [Exporting](dev/EXPORTING.md) | **File → Export Runner...** and standalone `.pyz` runners |
| [Plugins](dev/PLUGINS.md) | Adding a language you already have installed with a JSON manifest |

## Working on Time Warp itself

| Document | Covers |
|----------|--------|
| [Technical reference](dev/TECHNICAL_REFERENCE.md) | Architecture, the interpreter, executors, adding a language |
| [Setup → Tests and linting](../SETUP.md#tests-and-linting) | pytest, coverage, GUI tests on headless machines |
| [Setup → Releasing](../SETUP.md#releasing-maintainers) | Tag-based PyPI, TestPyPI and GHCR publishing |

Source starts at [`Time_Warp.py`](../Time_Warp.py), then
[`core/interpreter.py`](../core/interpreter.py),
[`core/languages/`](../core/languages/), [`gui/`](../gui/) and
[`web/`](../web/).

## Layout

```text
docs/
├── README.md               # This map
├── INDEX.md                # Pointer to this map
├── QUICK_START.md
├── FAQ.md
├── TROUBLESHOOTING.md
├── user/
│   └── LANGUAGE_TUTORIALS.md
├── languages/              # One *_REFERENCE.md per language (9 files)
└── dev/
    ├── TECHNICAL_REFERENCE.md
    ├── WEB.md
    ├── EXPORTING.md
    └── PLUGINS.md
```

Found something wrong or out of date? Open an issue or a pull request at
<https://github.com/James-HoneyBadger/Time_Warp_Classic>.
