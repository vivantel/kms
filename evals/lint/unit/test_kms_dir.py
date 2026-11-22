"""Knowledge-directory resolution: --docs, then kms-dir: in AGENTS.md, then .vivantel/akasha/docs, then docs/."""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "plugins" / "kms" / "shared"))
from lint_check import Linter  # noqa: E402


class KmsDir(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def mk(self, *dirs, agents=None):
        for d in dirs:
            (self.root / d).mkdir(parents=True)
        if agents is not None:
            (self.root / "AGENTS.md").write_text(agents)

    def docs(self, **kw):
        return Linter(self.root, **kw).docs.relative_to(self.root.resolve()).as_posix()

    def test_kms_dir_line_wins_over_layout(self):
        self.mk("docs/decisions", "kb/x", agents="<!-- kms:start -->\nkms-dir: kb/x\n<!-- kms:end -->\n")
        self.assertEqual(self.docs(), "kb/x")

    def test_flag_wins_over_kms_dir(self):
        self.mk("docs/decisions", agents="<!-- kms:start -->\nkms-dir: kb\n<!-- kms:end -->\n")
        self.assertEqual(self.docs(docs="docs"), "docs")

    def test_line_outside_block_ignored(self):
        self.mk("docs/decisions", agents="kms-dir: kb\n")
        self.assertEqual(self.docs(), "docs")

    def test_unsafe_path_ignored(self):
        self.mk("docs/decisions", agents="<!-- kms:start -->\nkms-dir: ../out\n<!-- kms:end -->\n")
        self.assertEqual(self.docs(), "docs")

    def test_new_default_path(self):
        self.mk(".vivantel/akasha/docs/decisions")
        self.assertEqual(self.docs(), ".vivantel/akasha/docs")

    def test_new_default_beats_unrelated_docs(self):
        self.mk(".vivantel/akasha/docs/decisions", "docs")  # a Sphinx docs/ without decisions/
        self.assertEqual(self.docs(), ".vivantel/akasha/docs")

    def test_old_docs_unchanged(self):
        self.mk("docs/decisions")
        self.assertEqual(self.docs(), "docs")

    def test_fallback_root_dir(self):
        self.mk("knowledge/decisions")
        self.assertEqual(self.docs(), "knowledge")


if __name__ == "__main__":
    unittest.main()
