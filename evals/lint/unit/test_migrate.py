"""Unit cases for plugins/kms/shared/migrate.py. Run: python3 -m unittest discover -s evals/lint -t ."""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

MIGRATE = Path(__file__).resolve().parents[3] / "plugins" / "kms" / "shared" / "migrate.py"


def art(extra, body="Body.\n", id="0001-a", crlf=False):
    t = f"---\nid: {id}\ntitle: T\nstatus: active\ndate: 2026-01-01\ntags: [x]\n{extra}---\n{body}"
    return t.replace("\n", "\r\n") if crlf else t


class Migrate(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        for t in ("facts", "decisions", "guardrails", "skills"):
            (self.root / "docs" / t).mkdir(parents=True)

    def run_migrate(self):
        return subprocess.run([sys.executable, str(MIGRATE), "--docs", str(self.root / "docs")], capture_output=True, text=True)

    def put(self, rel, text):
        (self.root / "docs" / rel).write_bytes(text.encode("utf-8"))

    def get(self, rel):
        return (self.root / "docs" / rel).read_bytes().decode("utf-8")

    def test_empty_expires_is_dropped_and_existing_expires_when_wins(self):
        self.put("decisions/0001-a.md", art("expires:\n"))
        self.put("decisions/0002-b.md", art("expires: someday\nexpires-when: shipped\n", id="0002-b"))
        self.assertEqual(self.run_migrate().returncode, 0)
        self.assertNotIn("None", self.get("decisions/0001-a.md"))
        self.assertNotIn("expires:", self.get("decisions/0001-a.md"))
        self.assertEqual(self.get("decisions/0002-b.md").count("expires-when"), 1)

    def test_scalar_governed_by_with_punctuation_stays_parseable(self):
        self.put("guardrails/g.md", art('governed-by: "decision 62 (see #12)"\n', id="g"))
        self.run_migrate()
        self.assertIn('governed-by: ["decision 62 (see #12)"]', self.get("guardrails/g.md"))

    def test_mixed_fitness_functions_with_a_date_do_not_crash_and_notes_are_printed(self):
        self.put("decisions/0001-a.md", art('fitness-functions: ["str", {check: x, last-verified: 2026-01-05}]\n'))
        r = self.run_migrate()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("has no `last-verified`", r.stdout)

    def test_non_mapping_frontmatter_and_invalid_date_are_skipped(self):
        self.put("facts/0001-a.md", "---\n- a\n- b\n---\nBody\n")
        self.put("facts/0002-b.md", art("", id="0002-b").replace("2026-01-01", "2026-02-30"))
        r = self.run_migrate()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.get("facts/0001-a.md"), "---\n- a\n- b\n---\nBody\n")

    def test_crlf_is_kept(self):
        self.put("decisions/0001-a.md", art("track: process\n", crlf=True))
        self.run_migrate()
        out = self.get("decisions/0001-a.md")
        self.assertNotIn("track", out)
        self.assertNotIn("\n", out.replace("\r\n", ""))

    def test_registry_rows_leave_the_index_and_a_second_run_changes_nothing(self):
        self.put("skills/tags.md", "---\nid: tags\ntitle: Tags\nstatus: active\ndate: 2026-01-01\ntags: [x]\n---\nx — y\n")
        self.put("skills/INDEX.md", "id,title,tags,status\ntags,Tags,x,active\n")
        self.run_migrate()
        self.assertNotIn("\ntags,", self.get("skills/INDEX.md"))
        self.assertIn("kms-registry: tags", self.get("skills/tags.md"))
        self.assertIn("0 file(s) changed", self.run_migrate().stderr)


if __name__ == "__main__":
    unittest.main()
