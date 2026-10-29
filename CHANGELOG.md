# Changelog

All notable changes to Time Warp Classic are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.6.0] - 2026-10-29

### Changed

- **Errors now carry a suggestion.** A short `?HINT:` line is printed under
  errors the interpreter recognises (division by zero, undefined names,
  syntax errors, missing modules, endless loops, timeouts, …) and points at the
  language reference. The hint is stored with the error in `error_history`
  and shown in the Debug → Error History dialog, which now also lists the time
  of each error. Hosts can disable the lines with `error_hints = False`.
- **Runtime readiness is visible.** Languages that need an external runtime
  (`perl`, `node`) are marked *(runtime missing)* in the language menu, the
  status bar and the web IDE's language picker, and a one-line note is
  printed the first time such a language is selected. Running one now explains
  how to install the runtime; plugin languages name the manifest `executable`
  that could not be found, and are listed with that reason in the plugin report.
- **Debug state is visible while it matters.** The status bar shows how many
  breakpoints are set whenever Debug Mode is on, refreshed from the Debug menu,
  F9, Clear All Breakpoints and the BASIC `TRON`/`TROFF` console commands.
  In the web IDE, `?HINT:` lines are styled as suggestions rather than errors
  and the language picker, status line and console have accessible labels.

## [1.5.0] - 2026-10-26

This release also contains everything that was prepared for 1.4.0, which was
never published to PyPI (the published versions were 1.3.0 and 1.3.4).

### Added

- **Word completion** in the editor: language-aware suggestions for all nine
  languages as you type, `Ctrl+Space` to list every word, Enter/Tab to accept,
  Esc to dismiss, a Preferences toggle, and silence inside comments and
  strings.
- **Language plugins**: a JSON manifest in `~/.timewarp/plugins` teaches the
  IDE a language that runs through an existing runtime (Ruby, Lua, Go, …),
  with completion keywords, a Pygments syntax alias, Save-As extension and
  clickable error lines. Preferences → Plugins manages and reloads them.
  Documented in `docs/dev/PLUGINS.md`.
- **Standalone runner export**: `File → Export Runner…` writes a `.pyz` that
  runs the program with nothing but Python 3.9+; `.twrun` bundles hold the
  language and source. New `Time_Warp.py --run FILE [--language LANG]` and
  `--version` command line with exit codes 0/1/2. Documented in
  `docs/dev/EXPORTING.md`.
- **Web IDE**: `Time_Warp.py --web [--host] [--port] [--timeout]` serves the
  editor in a browser (or **Program → Open Web IDE**), with streamed output,
  a turtle graphics canvas sent as run-length encoded delta frames, a
  persistent REPL bar, Pygments syntax highlighting, an examples picker and a
  `/healthz` endpoint. `Dockerfile.web` builds a container image. Documented in
  `docs/dev/WEB.md`.
- **Console REPL** in the desktop IDE: for the built-in interpreters (BASIC
  direct mode, Logo, Pascal, Pilot, Forth) the console bar evaluates statements
  in a persistent interpreter, so variables, the Forth stack and the turtle
  position carry across lines. Python, JavaScript, Perl and plugin languages
  run each line in a fresh process, so their state does not persist.
  `Program → Reset Console REPL` clears the session.
- **Pascal**: block forms of `WHILE`, `IF/ELSE`, `FOR` and `REPEAT` now nest
  correctly, including `BEGIN` written on the statement's own line, and
  statements on the `REPEAT` line belong to the loop body.

### Changed

- Direct-mode BASIC, error reporting (`?ERROR IN n`, `BREAK IN n`), the Stop
  control and streamed subprocess output were reworked so runs no longer freeze
  the window; error lines name the editor line and are clickable.
- `examples/` is now a package, so the shipped examples are included in the
  wheel and resolve from an installed copy as well as a checkout.
- `tkinter` is optional for the interpreter, so the CLI, exported runners and
  web server work on installs (and container images) without Tk.

### Fixed

- Pascal `WHILE … DO BEGIN` no longer spins the loop header and then runs the
  body once; nested inline `BEGIN` blocks no longer close their parent early.
- Reported error and BREAK line numbers follow the editor, including programs
  that start with blank lines.
- A latched Stop no longer makes the next console `INPUT` cancel itself.
- Stop now reaches loop bodies in the Pascal and Logo executors.
- A breakpoint hit reports `BREAK IN n` once and no longer claims `READY.`.
- The web server shuts down promptly on `SIGTERM` (it runs as PID 1 in a
  container, where the default signal action is ignored).
- `E303`/`F401` lint regressions; the launcher asks before installing a system
  package instead of escalating silently.

### Tests

345 tests, up from 139, covering run control, GUI menus and documents, direct
mode, interpreters, plugins, export, the web server, the canvas and
highlighting. GUI tests run under a real display and keep their settings in a
temporary file.

## [1.3.4]

Published to PyPI. See the repository tags `v1.3.0` and `v1.3.4`.

[1.5.0]: https://github.com/James-HoneyBadger/Time_Warp_Classic/compare/v1.3.4...v1.5.0
