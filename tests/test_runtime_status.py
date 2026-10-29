"""Runtime readiness, as reported to the IDE, the CLI and the web UI."""

from core.languages.catalog import (
    missing_runtime_hint, required_runtime, runtime_available,
)


def test_builtin_languages_need_no_runtime():
    for language in (
        "PILOT", "BASIC", "Logo", "Pascal", "Prolog", "Forth", "Python",
    ):
        assert runtime_available(language) is True
        assert required_runtime(language) == ()


def test_external_languages_name_their_commands():
    assert required_runtime("JavaScript") == ("node", "nodejs")
    assert required_runtime("perl") == ("perl",)


def test_missing_runtime_is_detected_from_the_executable():
    assert runtime_available("Ruby", "definitely-not-a-real-runtime-xyz") is False


def test_install_hints_cover_the_external_runtimes():
    assert "Node.js" in missing_runtime_hint("JavaScript")
    assert "Perl" in missing_runtime_hint("perl")
    assert missing_runtime_hint("BASIC") == ""


def test_plugin_message_names_the_manifest_executable():
    from core.languages.plugin_executor import PluginExecutor
    from core.plugins import parse_manifest

    spec = parse_manifest({"name": "Ruby", "executable": "no-such-ruby-xyz"})
    executor = PluginExecutor(object(), spec)

    assert executor.executable is None
    assert "no-such-ruby-xyz" in executor.missing_runtime_message()
