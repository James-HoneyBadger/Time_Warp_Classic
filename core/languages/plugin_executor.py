"""Executor for a language described by a plugin manifest.

Every plugin language is an external runtime, so it reuses the subprocess
infrastructure that Python, JavaScript and Perl already use: the whole script
is written to a temporary file, run with the manifest's executable and
arguments, and its output is streamed into the IDE console.
"""

from __future__ import annotations

import os
import shutil

from core.languages.base import SubprocessExecutor


class PluginExecutor(SubprocessExecutor):
    """Run a plugin language through the runtime named in its manifest."""

    def __init__(self, interpreter, spec):
        self.spec = spec
        self.lang_name = spec.name
        self.file_suffix = spec.extension or ".txt"
        self.executable_candidates = [spec.executable]
        self.extra_args = tuple(spec.args)
        self.timeout = spec.timeout
        super().__init__(interpreter)

    def _find_executable(self):
        """Resolve the manifest's executable without probing ``--version``.

        Plugin runtimes are not required to understand ``--version`` (many
        interpreters do not), so an explicit path or a plain ``PATH`` lookup
        is the reliable test.
        """
        candidate = self.spec.executable
        if not candidate:
            return None
        found = shutil.which(candidate)
        if found:
            return found
        return candidate if os.path.isfile(candidate) else None

    def missing_runtime_message(self):
        """Name the executable the manifest asked for."""
        return (
            f"?{self.lang_name.upper()} NOT FOUND - the manifest asks for "
            f"'{self.spec.executable}', which is not on PATH"
        )
