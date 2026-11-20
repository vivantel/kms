"""Each skill's vendored shared/ and templates/ copies equal the originals, and index.json lists them."""
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


class Vendored(unittest.TestCase):
    def test_copies_and_index_are_current(self):
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "vendor-shared.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr + "\nrun: python3 scripts/vendor-shared.py")

    def test_no_skill_reads_a_sibling_directory(self):
        for p in (ROOT / "plugins" / "kms" / "skills").glob("*/SKILL.md"):
            self.assertNotIn("../../", p.read_text(), p.name)


if __name__ == "__main__":
    unittest.main()
