"""Check 25 (stale or missing fact source) and the lint-nudge hook's knowledge-directory detection.
Run: python3 -m unittest discover evals/lint/unit"""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
SHARED = HERE.parents[3] / "plugins" / "kms" / "shared"
HOOK = HERE.parents[3] / "plugins" / "kms" / "hooks" / "lint-nudge.sh"
sys.path.insert(0, str(SHARED))
sys.path.insert(0, str(HERE.parent))
from lint_check import Linter  # noqa: E402
from test_lint_check import project  # noqa: E402

TODAY = "2026-02-01"
FACT = """---
id: 0002-limit
title: Vendor limit
status: active
date: 2026-01-01
tags: [release]
{extra}---
Body.
"""


class Check25(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def lint(self, extra):
        project(self.root, **{"docs/facts/0002-limit.md": FACT.format(extra=extra)})
        lin = Linter(self.root, today=TODAY)
        return [m for c, _, m in lin.run() if c == 25], lin.warnings

    def test_url_source_verified_long_ago_is_stale(self):
        got, _ = self.lint("source: https://x.example/limits\nlast-verified: 2025-01-01\n")
        self.assertEqual(len(got), 1)
        self.assertIn("days ago", got[0])

    def test_command_source_verified_long_ago_is_stale(self):
        got, _ = self.lint("source: kilo run --help\nlast-verified: 2025-01-01\n")
        self.assertEqual(len(got), 1)

    def test_recent_url_source_is_clean(self):
        got, _ = self.lint("source: https://x.example/limits\nlast-verified: 2026-01-15\n")
        self.assertEqual(got, [])

    def test_missing_repo_path_source_is_a_finding(self):
        got, _ = self.lint("source: plugins/kms/gone.json\nlast-verified: 2026-01-15\n")
        self.assertEqual(len(got), 1)
        self.assertIn("no longer exists", got[0])

    def test_existing_repo_path_source_is_clean_however_old(self):
        Path(self.root, "pkg.json").write_text("{}")
        got, _ = self.lint("source: pkg.json\nlast-verified: 2024-01-01\n")
        self.assertEqual(got, [])

    def test_no_last_verified_is_one_advisory_line_not_a_finding(self):
        got, warnings = self.lint("source: https://x.example/limits\n")
        self.assertEqual(got, [])
        self.assertEqual(len([w for w in warnings if "never verified" in w]), 1)

    def test_fact_without_source_is_ignored(self):
        got, warnings = self.lint("")
        self.assertEqual(got, [])
        self.assertFalse([w for w in warnings if "never verified" in w])


class Nudge(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def git(self, *a):
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
        subprocess.run(["git", *a], cwd=self.root, check=True, capture_output=True, env=env)

    def nudge(self, kb, commits=6, agents=None):
        self.git("init", "-q")
        if agents:
            (Path(self.root) / "AGENTS.md").write_text(agents)
        (Path(self.root) / kb / "decisions").mkdir(parents=True)
        for i in range(commits):
            (Path(self.root) / kb / "decisions" / f"{i:04d}-x.md").write_text(str(i))
            self.git("add", "-A")
            self.git("commit", "-qm", f"c{i}")
        return subprocess.run(["sh", str(HOOK)], cwd=self.root, capture_output=True, text=True).stdout

    def test_knowledge_directory_other_than_docs_is_counted(self):
        out = self.nudge("knowledge")
        self.assertIn("6 commit(s)", out)
        self.assertIn("knowledge/", out)

    def test_docs_still_works(self):
        self.assertIn("docs/", self.nudge("docs"))

    def test_new_default_path_is_counted(self):
        self.assertIn(".vivantel/akasha/docs/", self.nudge(".vivantel/akasha/docs"))

    def test_kms_dir_line_is_counted(self):
        out = self.nudge("kb/x", agents="<!-- kms:start -->\nkms-dir: kb/x\n<!-- kms:end -->\n")
        self.assertIn("kb/x/", out)

    def test_below_threshold_is_silent(self):
        self.assertEqual(self.nudge("knowledge", commits=3), "")


if __name__ == "__main__":
    unittest.main()
