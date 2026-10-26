"""Tests for language plugins: manifests, discovery, registry and execution."""

import io
import json
import sys
from contextlib import redirect_stdout

import pytest

from core.interpreter import Time_WarpInterpreter
from core.languages.plugin_executor import PluginExecutor
from core.plugins import (
    DEFAULT_TIMEOUT,
    PluginError,
    PluginRegistry,
    PluginSpec,
    discover_plugins,
    parse_manifest,
    plugin_directories,
)


def _manifest(**overrides):
    data = {
        "name": "Rubyish",
        "executable": "ruby",
        "extension": "rb",
        "syntax": "ruby",
        "comment": "#",
        "keywords": ["def", "end", "puts"],
    }
    data.update(overrides)
    return data


def _write(directory, name="plugin.json", **overrides):
    path = directory / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_manifest(**overrides)), encoding="utf-8")
    return path


# ---------------------------------------------------------------- manifests

def test_minimal_manifest_gets_defaults():
    spec = parse_manifest({"name": "Lua", "executable": "lua"})

    assert spec.name == "Lua"
    assert spec.extension == ".txt"
    assert spec.timeout == DEFAULT_TIMEOUT
    assert spec.args == ()
    assert spec.keywords == ()


def test_manifest_fields_are_normalised():
    spec = parse_manifest(_manifest(extension="RB", args="-u", keywords="puts"))

    assert spec.extension == ".rb"
    assert spec.args == ("-u",)
    assert spec.keywords == ("puts",)


@pytest.mark.parametrize(
    "data",
    [
        {"executable": "ruby"},
        {"name": "Ruby"},
        {"name": "   ", "executable": "ruby"},
        {"name": 3, "executable": "ruby"},
        {"name": "Ruby", "executable": ["ruby"]},
    ],
)
def test_invalid_manifests_are_rejected(data):
    with pytest.raises(PluginError):
        parse_manifest(data)


def test_builtin_names_cannot_be_shadowed():
    with pytest.raises(PluginError):
        parse_manifest({"name": "Python", "executable": "python3"})


@pytest.mark.parametrize("timeout", ["30", 0, -1, None, True])
def test_timeout_must_be_positive_number(timeout):
    with pytest.raises(PluginError):
        parse_manifest({"name": "Lua", "executable": "lua", "timeout": timeout})


def test_manifest_round_trips():
    spec = parse_manifest(_manifest())

    assert parse_manifest(spec.to_manifest()) == spec


# ---------------------------------------------------------------- discovery

def test_file_and_folder_manifests_are_both_found(tmp_path):
    (tmp_path / "single.json").write_text(
        json.dumps({"name": "Lua", "executable": "lua"}), encoding="utf-8"
    )
    folder = tmp_path / "ruby"
    folder.mkdir()
    (folder / "plugin.json").write_text(
        json.dumps({"name": "Ruby", "executable": "ruby"}), encoding="utf-8"
    )

    specs, problems = discover_plugins([tmp_path])

    assert {spec.name for spec in specs} == {"Lua", "Ruby"}
    assert problems == []


def test_broken_manifest_does_not_stop_the_others(tmp_path):
    (tmp_path / "broken.json").write_text("{not json", encoding="utf-8")
    _write(tmp_path, "good.json")

    specs, problems = discover_plugins([tmp_path])

    assert [spec.name for spec in specs] == ["Rubyish"]
    assert len(problems) == 1 and "broken.json" in problems[0]


def test_duplicate_names_are_reported(tmp_path):
    first = tmp_path / "a"
    second = tmp_path / "b"
    _write(first)
    _write(second)

    specs, problems = discover_plugins([first, second])

    assert [spec.name for spec in specs] == ["Rubyish"]
    assert any("already loaded" in problem for problem in problems)


def test_missing_directory_is_harmless(tmp_path):
    specs, problems = discover_plugins([tmp_path / "nope"])

    assert specs == [] and problems == []


def test_plugin_directories_reads_the_environment(monkeypatch, tmp_path):
    extra = tmp_path / "extra"
    monkeypatch.setenv("TIMEWARP_PLUGIN_PATH", str(extra))

    directories = plugin_directories()

    assert extra in directories
    assert all(isinstance(entry, type(extra)) for entry in directories)


# ---------------------------------------------------------------- registry

@pytest.fixture
def registry(tmp_path):
    _write(tmp_path)
    return PluginRegistry.load([tmp_path])


def test_registry_lookups_are_case_insensitive(registry):
    assert len(registry) == 1
    assert registry.names() == ["Rubyish"]
    assert registry.get("rubyish").name == "Rubyish"
    assert registry.get("RUBYISH").executable == "ruby"
    assert registry.get("cobol") is None


def test_registry_maps_extensions(registry):
    assert registry.extension_map() == {".rb": "Rubyish"}


def test_registry_caches_executors(registry):
    interpreter = Time_WarpInterpreter()

    first = registry.executor(interpreter, "Rubyish")
    second = registry.executor(interpreter, "rubyish")

    assert isinstance(first, PluginExecutor)
    assert first is second
    assert registry.executor(interpreter, "Pascal") is None


def test_example_manifest_is_valid_and_not_overwritten(tmp_path):
    path = PluginRegistry.write_example(tmp_path)
    spec = parse_manifest(json.loads(path.read_text()))
    path.write_text(json.dumps({"name": "Edited", "executable": "x"}))

    again = PluginRegistry.write_example(tmp_path)

    assert spec.name == "PyPlugin"
    assert again == path
    assert "Edited" in path.read_text()


# ---------------------------------------------------------------- executor

def test_executor_takes_its_settings_from_the_manifest():
    spec = PluginSpec(
        name="Lua", executable="lua", extension=".lua", args=("-e",),
        timeout=12.5,
    )
    executor = PluginExecutor(Time_WarpInterpreter(), spec)

    assert executor.lang_name == "Lua"
    assert executor.file_suffix == ".lua"
    assert executor.extra_args == ("-e",)
    assert executor.timeout == 12.5
    assert executor.executable_candidates == ["lua"]


def test_missing_runtime_leaves_executable_unset():
    spec = PluginSpec(name="Ghost", executable="definitely-not-a-runtime-xyz")

    assert PluginExecutor(Time_WarpInterpreter(), spec).executable is None


# ------------------------------------------------------------ end to end

@pytest.fixture
def python_plugin(tmp_path):
    """A plugin that runs Python through the host interpreter."""
    (tmp_path / "pyplugin.json").write_text(
        json.dumps(
            {
                "name": "PyPlugin",
                "executable": sys.executable,
                "extension": ".tppy",
                "args": ["-u"],
                "syntax": "python",
                "comment": "#",
                "keywords": ["print", "def"],
            }
        ),
        encoding="utf-8",
    )
    registry = PluginRegistry.load([tmp_path])
    interpreter = Time_WarpInterpreter()
    interpreter.plugins = registry
    return interpreter


def test_plugin_program_runs_through_the_runtime(python_plugin):
    out = io.StringIO()
    with redirect_stdout(out):
        python_plugin.run_program('print("from the plugin")\n', language="PyPlugin")

    printed = out.getvalue()
    assert "from the plugin" in printed
    assert "READY." in printed


def test_plugin_errors_report_the_script_line(python_plugin):
    out = io.StringIO()
    with redirect_stdout(out):
        python_plugin.run_program(
            'print("first")\nraise ValueError("boom")\n', language="PyPlugin"
        )

    assert "?ERROR IN 2" in out.getvalue()


def test_plugin_without_runtime_reports_the_missing_executable(tmp_path):
    (tmp_path / "ghost.json").write_text(
        json.dumps({"name": "Ghostlang", "executable": "no-such-runtime-xyz"}),
        encoding="utf-8",
    )
    interpreter = Time_WarpInterpreter()
    interpreter.plugins = PluginRegistry.load([tmp_path])

    out = io.StringIO()
    with redirect_stdout(out):
        interpreter.run_program("anything", language="Ghostlang")

    assert "NOT FOUND" in out.getvalue()


def test_registry_is_optional_for_builtin_languages():
    """No registry installed: built-in dispatch must be untouched."""
    interpreter = Time_WarpInterpreter()
    out = io.StringIO()
    with redirect_stdout(out):
        interpreter.run_program('10 PRINT "HI"', language="basic")

    assert "HI" in out.getvalue()
