# Changelog

All notable changes to Time Warp Classic are recorded here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Web IDE input.** When a running program reads input (BASIC `INPUT`, PILOT
  `A:`, Pascal `readln`, or stdin in Python/JavaScript/Perl), the console bar
  becomes its stdin. Time spent waiting does not count toward the built-in
  languages' time limit. New `POST /api/input` endpoint and `input` stream
  event.
- **Web IDE Stop** button (`Ctrl+.`), backed by `POST /api/stop`. Every
  streamed run now opens with a `start` event that carries its run id, and
  closing the tab stops the run.
- **BASIC direct mode in the web console bar.** Numbered lines edit the program
  in the editor, and `LIST`, `RUN`, `NEW` and `RENUMBER` work on it, as on the
  desktop.
- **Open… / Save** (`Ctrl+S`) for local files, and the editor is autosaved to
  browser storage. Loading an example over edited text asks first.
- **Pascal `TRACE OFF` / `TRACE ON`.** Switches off the per-statement trace
  lines (`✅ X := 1`, `📝 Declared variables`, …) that clutter loops, and
  brings them back.
- **PILOT `%` system variables in text.** `T:%answer`, `T:%matched` and the
  other `%…` variables are now substituted in `T:`/`MT:`/`TH:` text.
- **Web IDE colour themes.** Nine themes from the desktop IDE, chosen from a
  header menu and remembered between visits.
- **Breakpoints and single-stepping.** Click a gutter line to set a breakpoint;
  the run stops there with `BREAK IN n`. Pause, Step and Resume buttons let a
  running built-in-language program be frozen and advanced one line at a time.
- **Clickable errors.** `?ERROR IN n` and `BREAK IN n` lines in the console
  jump to that editor line when clicked.
- **Share links.** The program and language are kept in the URL hash, so small
  programs can be shared as a link.
- **Server-side drafts.** Save, open and delete programs on the server via the
  drafts menu (`GET/POST/DELETE /api/drafts`) or the new `--drafts-dir`
  service option. Run limits are now configurable with `--max-output-lines`,
  `--input-timeout` and `--max-iterations`.

### Fixed

- In the web IDE, `INPUT` read from the **server's** terminal and Python's
  `input()` hung until the time limit; direct-mode `INPUT` is now refused with a
  hint.
- The web console bar ran `10 PRINT 1` immediately instead of storing the line,
  and `LIST`/`RUN` did nothing.
- A program that printed in a tight loop could freeze the browser tab. Output is
  now capped at 20,000 lines per run on the server and 5,000 lines in the
  console.
- Ovals and rectangles drawn as canvas overlays had the wrong size, and Tk
  colour names with spaces (`"light blue"`) were not drawn.
- Syntax highlighting could leave the editor text invisible when the highlight
  request failed. It now falls back to plain text.
- Turtle chatter (*Pen up*, *Turtle returned to home position*, …) from Logo,
  BASIC and PILOT no longer appears in the web IDE or `--run` output. The
  desktop console still shows it.
- Pascal's `🚀 Starting program` line is gone from normal output (it is now
  debug-only, without the emoji).
- A Logo loop that hits its safety cap (`REPEAT` at 5000 commands, or
  `WHILE`/`UNTIL`/`DO.WHILE`/`DO.UNTIL` at 10000 iterations) now reports an
  error instead of a plain note, so it counts in the exit status and error
  history.
- The desktop About dialog now reads the real version instead of a hardcoded
  one.
- `python3 Time_Warp.py --web` now loads plugin languages from
  `~/.timewarp/plugins` and `TIMEWARP_PLUGIN_PATH`. Before this, only the
  desktop's **Open Web IDE** had them. In the web server, a plugin language's
  output after the first run went to that run's interpreter and was lost.
- `--run` (and exported runners) now pass the terminal's stdin to Python,
  JavaScript and Perl programs. Before this, `input()` waited until the time
  limit.
- Malformed `Content-Length` headers and non-UTF-8 bodies are answered with
  `400` instead of an unhandled exception. The `Server` header reports the real
  version.
- The narrow-screen layout stacks the panes, and the pane divider can be moved
  from the keyboard.

### Documentation

- `docs/dev/WEB.md` rewritten to describe input, Stop, direct mode, the full API
  and its limits. It no longer claims that the web edition has no turtle canvas
  or that busy requests are queued.
- README, setup, user guides, developer references and language references were
  checked against the code. Wrong or stale statements are corrected and the tone
  is plainer.

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
