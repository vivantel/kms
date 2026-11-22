"""The skills/ -> procedures/ rename: both names are read for one release; migrate.py --rename moves one to the other."""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SHARED = Path(__file__).resolve().parents[3] / "plugins" / "kms" / "shared"
sys.path.insert(0, str(SHARED))
from lint_check import Linter  # noqa: E402

PROC = "---\nid: 0001\ntitle: t\ntags: [a]\nstatus: active\n---\nbody\n"
TAGS = "---\nkms-registry: tags\n---\n- a: the a tag\n"


class Rename(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def build(self, name, tag="a"):
        d = self.root / "docs" / name
        d.mkdir(parents=True)
        (d / "tags.md").write_text(TAGS)
        (d / "p.md").write_text(PROC.replace("[a]", f"[{tag}]"))
        (self.root / "docs" / "decisions").mkdir(exist_ok=True)

    def findings(self):
        l = Linter(self.root, docs="docs")
        l.run()
        return l.findings

    def test_both_names_load_and_use_their_tags_list(self):
        for name in ("skills", "procedures"):
            with self.subTest(name=name):
                shutil.rmtree(self.root, ignore_errors=True)
                self.root.mkdir()
                self.build(name)
                self.assertFalse([f for f in self.findings() if f[0] == 21])
                (self.root / "docs" / name / "p.md").write_text(PROC.replace("[a]", "[zzz]"))
                self.assertTrue([f for f in self.findings() if "zzz" in str(f)])

    def test_migrate_rename_moves_dir_and_rewrites_mentions(self):
        self.build("skills")
        (self.root / "docs" / "decisions" / "0001-x.md").write_text("see docs/skills/tags.md\n")
        subprocess.run([sys.executable, str(SHARED / "migrate.py"), "--docs", str(self.root / "docs"), "--rename"], check=True, capture_output=True)
        self.assertTrue((self.root / "docs" / "procedures" / "tags.md").exists())
        self.assertFalse((self.root / "docs" / "skills").exists())
        self.assertIn("docs/procedures/tags.md", (self.root / "docs" / "decisions" / "0001-x.md").read_text())

    def test_migrate_rename_refuses_when_both_exist(self):
        self.build("skills")
        self.build("procedures")
        r = subprocess.run([sys.executable, str(SHARED / "migrate.py"), "--docs", str(self.root / "docs"), "--rename"], capture_output=True)
        self.assertNotEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
