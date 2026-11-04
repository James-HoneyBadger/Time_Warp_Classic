# Setup

Installation and environment details for Time Warp Classic. For a tour of what
it does, see the [README](README.md); for a first program, the
[quick start](docs/QUICK_START.md).

## Requirements

| Need | For | Notes |
|------|-----|-------|
| Python 3.9+ | Everything | Package metadata lists 3.9 through 3.14 |
| Tkinter | Desktop IDE only | Bundled with python.org installers; a separate package on many Linux distros |
| `pygments` | Syntax highlighting | Desktop and web; plain text without it |
| `pygame-ce` | Some BASIC graphics statements | Optional at runtime |
| `Pillow` | Image features in the interpreter | Optional at runtime; a notice is printed when it is missing |
| `perl` | Perl programs | Must be on `PATH` |
| `node` or `nodejs` | JavaScript programs | Must be on `PATH` |

The three Python packages are listed in [`requirements.txt`](requirements.txt)
and in `pyproject.toml`, so every install route below pulls them in. The web
IDE and the `--run` command line runner do not need Tkinter.

Optional extras defined in `pyproject.toml`:

| Extra | Installs | Used by |
|-------|----------|---------|
| `metrics` | `psutil` | Real memory figures in **Performance → Show Statistics** |
| `test` | `pytest`, `pytest-cov`, `pytest-mock`, `pytest-xdist` | The test suite |
| `dev` | `build`, `twine`, `black`, `flake8` | Packaging and linting |

## Installing

### From PyPI

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install timewarp-classic      # or "timewarp-classic[metrics]"
timewarp                          # desktop IDE
```

The `timewarp` command takes the same options as `python3 Time_Warp.py`
(listed in the [README](README.md#command-line)).

### From a clone, with the launcher

```bash
git clone https://github.com/James-HoneyBadger/Time_Warp_Classic.git
cd Time_Warp_Classic
python3 run.py                    # any OS
./run.sh                          # Linux/macOS, plain bash
run.bat                           # Windows (uses "python")
```

All three accept the same flags:

| Flag | Effect |
|------|--------|
| `--clean` | Delete and recreate `venv/` |
| `--no-install` | Skip dependency installation (faster later starts) |
| `--help` | Usage (`run.py` only) |

`run.py`, step by step:

1. Checks for Python 3.9 or newer.
2. Creates `venv/` if needed and bootstraps `pip` inside it if it is missing.
3. If Tkinter is missing, offers to install it with the system package
   manager (`apt-get`, `dnf`, `yum`, `zypper`, `pacman`, `apk`, or Homebrew on
   macOS). It always asks first and uses `sudo` only when needed.
4. Upgrades `pip`, `setuptools` and `wheel`, then installs `pygame-ce` (skipped
   if some `pygame` is already importable), `pygments` and `Pillow`, one at a
   time so one failure does not block the rest. It also installs `pytest`,
   `pytest-cov`, `black` and `flake8`; failures there are ignored.
5. Verifies the imports, warns if there is no graphical display, and launches
   `Time_Warp.py`.

`run.sh` and `run.bat` follow the same steps, but only report a missing
Tkinter (with the command to install it) instead of offering to install it.

### From a clone, by hand

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python3 Time_Warp.py
```

### For development

```bash
python3 -m venv venv && source venv/bin/activate
pip install -e ".[test,dev]"      # or: pip install -r requirements-dev.txt
```

`requirements-dev.txt` covers the runtime packages plus `pytest`,
`pytest-cov`, `pytest-mock`, `pytest-xdist`, `black` and `flake8`.

## Tkinter

Check it with:

```bash
python3 -c "import tkinter; print(tkinter.TkVersion)"
```

If that fails with `No module named '_tkinter'` or `No module named 'tkinter'`:

| System | Command |
|--------|---------|
| Debian/Ubuntu | `sudo apt-get install python3-tk` |
| Fedora/RHEL | `sudo dnf install python3-tkinter` |
| Arch | `sudo pacman -S tk` |
| macOS (Homebrew Python) | `brew install python-tk` |
| Windows | Re-run the python.org installer and tick "tcl/tk and IDLE" |

A virtual environment uses the Tkinter of the Python it was created from, so
install the system package first, then recreate the venv
(`python3 run.py --clean`).

## Running

```bash
python3 Time_Warp.py                                  # desktop IDE
python3 Time_Warp.py --web                            # browser IDE, http://127.0.0.1:8000/
python3 Time_Warp.py --web --host 0.0.0.0 --port 8080 --timeout 30
python3 Time_Warp.py --run prog.bas --language basic  # headless, prints output
python3 Time_Warp.py --version
```

The web server binds to `127.0.0.1` by default. Use `--host 0.0.0.0` only
when you mean to expose it (for example inside a container); it runs whatever
code it is sent. `--timeout` is the per-run limit in seconds (default 10).
The server, its limits and its JSON API are described in
[docs/dev/WEB.md](docs/dev/WEB.md).

### Headless machines

Tk needs an X11 or Wayland display. Without one, either use the web IDE or
run the desktop IDE under a virtual framebuffer:

```bash
xvfb-run -a python3 Time_Warp.py
```

## Files Time Warp writes

| Path | Contents |
|------|----------|
| `~/.timewarp_settings.json` | Theme, font family, font size and other preferences |
| `~/.timewarp/plugins/` | Language plugin manifests (`*.json` or `<name>/plugin.json`) |
| `venv/` | Virtual environment created by the launchers |

Extra plugin directories can be added with the `TIMEWARP_PLUGIN_PATH`
environment variable; see [docs/dev/PLUGINS.md](docs/dev/PLUGINS.md).

## Docker

Two images are built from this repository:

| Image | Dockerfile | Needs a display |
|-------|------------|-----------------|
| `ghcr.io/james-honeybadger/time-warp-classic-web` | [`Dockerfile.web`](Dockerfile.web) | No |
| `ghcr.io/james-honeybadger/time-warp-classic` | [`Dockerfile`](Dockerfile) | Yes (X11) |

```bash
# Web IDE on http://localhost:8000
docker run --rm -p 8000:8000 ghcr.io/james-honeybadger/time-warp-classic-web:latest

# Desktop IDE with X11 forwarding
xhost +local:docker
docker run --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix \
  ghcr.io/james-honeybadger/time-warp-classic:latest

# Build locally
docker build -f Dockerfile.web -t time-warp-classic-web .
```

Published tags are `latest`, `X.Y`, `X.Y.Z` and `vX.Y.Z`, for `linux/amd64`
and `linux/arm64`. Pin a version instead of `latest` for reproducible setups.
The web image installs only `pygments`, runs as a non-root user and has a
health check on `/healthz`. Neither image includes Node.js, so JavaScript
shows as runtime missing.

## Tests and linting

```bash
python3 -m pytest                       # whole suite (tests/)
python3 -m pytest tests/test_web.py     # one file
python3 -m pytest -n auto               # parallel, needs pytest-xdist
python3 -m pytest --cov                 # coverage of core/ and gui/, needs pytest-cov
xvfb-run -a python3 -m pytest           # include GUI tests on a headless machine
black --check .
flake8
```

Tests that need a display skip themselves when neither `DISPLAY` nor
`WAYLAND_DISPLAY` is set. `python3 scripts/run_tests.py` is the wrapper the
IDE's **Test → Run Full Test Suite** uses; it runs pytest quietly over
`tests/`.

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `python3: command not found` | Install Python 3.9+; on Windows use `python` or `py -3` |
| `No module named '_tkinter'` | See [Tkinter](#tkinter) |
| "No graphical display detected" | Use `--web`, or `xvfb-run -a` |
| A language shows **(runtime missing)** | Install `perl` or Node.js and make sure it is on `PATH` |
| A package fails to build during install | Install build headers (`python3-dev` / `python3-devel`, or `xcode-select --install` on macOS), then `python3 run.py --clean` |
| `venv/` is broken | `python3 run.py --clean`, or delete `venv/` and start again |
| Port 8000 already in use | `--port 0` picks a free port, or choose another |

More in [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) and
[docs/FAQ.md](docs/FAQ.md).

## Linux desktop entry

`~/.local/share/applications/time-warp-classic.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=Time Warp Classic
Comment=Retro multi-language IDE
Exec=python3 /home/you/Time_Warp_Classic/run.py --no-install
Path=/home/you/Time_Warp_Classic
Terminal=false
Categories=Development;IDE;Education;
```

Run `python3 run.py` once from a terminal first so `venv/` exists.

## Releasing (maintainers)

Releases are tag-driven GitHub Actions workflows:

| Tag | Workflow | Publishes to |
|-----|----------|--------------|
| `vX.Y.Z` | `.github/workflows/publish-pypi.yml` | PyPI |
| `vX.Y.Z-rcN`, `-betaN`, `-alphaN` | `.github/workflows/publish-testpypi.yml` | TestPyPI |
| `v*` | `.github/workflows/publish-ghcr.yml`, `publish-ghcr-web.yml` | GHCR images |

```bash
git tag v1.6.1-rc1 && git push origin v1.6.1-rc1   # TestPyPI
git tag v1.6.1 && git push origin v1.6.1           # PyPI + images
```

The GHCR workflows can also be run by hand with an extra `tag` input to
rebuild an existing release. One-time setup: Trusted Publishers on PyPI and
TestPyPI for this repository, and GitHub environments named `pypi` and
`testpypi`.

## License

MIT. See [LICENSE](LICENSE).
