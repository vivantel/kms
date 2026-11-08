"""Unit cases for plugins/kms/shared/lint_check.py: a clean project yields nothing, and one
seeded mutation per check yields exactly that check. Run: python3 -m unittest discover evals/lint/unit"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "plugins" / "kms" / "shared"))
from lint_check import Linter  # noqa: E402

FACT = """---
id: 0001-cadence
title: Releases are weekly
status: active
date: 2026-01-01
tags: [release]
kind: environmental
governed-by: 0001-weekly
---
Body.
"""
DECISION = """---
id: 0001-weekly
title: Ship weekly
status: active
date: 2026-01-01
tags: [release]
track: process
---
Body.
"""
GUARD = """---
id: changelog
title: Every release has a changelog entry
status: active
date: 2026-01-01
tags: [release]
governed-by: 0001-weekly
grounded-in: [0001-cadence]
derivation-note: Weekly cadence implies a weekly entry.
---
Body.
"""
PROC = """---
id: deploy
title: Deploy steps
status: active
date: 2026-01-01
tags: [release]
---
Body, see changelog.
"""
TAGS = "---\nid: tags\ntitle: Tags\nstatus: active\ndate: 2026-01-01\ntags: [release]\n---\nrelease — release process\n"
INDEX = "id,title,tags,status\n{}\n"


def project(root, **over):
    files = {
        "docs/facts/0001-cadence.md": FACT,
        "docs/decisions/0001-weekly.md": DECISION,
        "docs/guardrails/changelog.md": GUARD,
        "docs/skills/deploy.md": PROC,
        "docs/skills/tags.md": TAGS,
        "docs/facts/INDEX.md": INDEX.format("0001-cadence,Releases are weekly,release,active"),
        "docs/decisions/INDEX.md": INDEX.format("0001-weekly,Ship weekly,release,active"),
        "docs/guardrails/INDEX.md": INDEX.format("changelog,Every release has a changelog entry,release,active"),
        "docs/skills/INDEX.md": INDEX.format("deploy,Deploy steps,release,active\ntags,Tags,release,active"),
        "plugins/kms/templates/guardrails/.keep": "",
    }
    files.update(over)
    for rel, text in files.items():
        if text is None:
            continue
        p = Path(root) / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")


class LintCheck(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root)

    def checks(self, **over):
        project(self.root, **over)
        return sorted({c for c, _, _ in Linter(self.root).run()})

    def test_clean_project(self):
        self.assertEqual(self.checks(), [])

    def test_1_dangling(self):
        # the fact loses its only referrer, so check 7 also fires
        self.assertEqual(self.checks(**{"docs/guardrails/changelog.md": GUARD.replace("[0001-cadence]", "[0099-none]")}), [1, 7])

    def test_2_missing_field(self):
        self.assertEqual(self.checks(**{"docs/decisions/0001-weekly.md": DECISION.replace("track: process\n", "")}), [2])

    def test_2_bare_string_list(self):
        self.assertEqual(self.checks(**{"docs/guardrails/changelog.md": GUARD.replace("[0001-cadence]", "0001-cadence")}), [2])

    def test_unterminated_frontmatter_still_checked(self):
        bad = GUARD.replace("---\nBody.\n", "").replace("[0001-cadence]", "[0099-none]")
        project(self.root, **{"docs/guardrails/changelog.md": bad})
        got = {(c, m) for c, _, m in Linter(self.root).run()}
        self.assertIn((2, "unterminated frontmatter"), got)
        self.assertTrue(any(c == 1 for c, _ in got))

    def test_2_bad_status(self):
        got = self.checks(**{"docs/skills/deploy.md": PROC.replace("status: active", "status: live")})
        self.assertIn(2, got)

    def test_3_gap(self):
        # the added fact is unreferenced, so check 7 also fires
        self.assertEqual(
            self.checks(**{"docs/facts/0003-x.md": FACT.replace("0001-cadence", "0003-x"), "docs/facts/INDEX.md": INDEX.format("0001-cadence,Releases are weekly,release,active\n0003-x,Releases are weekly,release,active")}),
            [3, 7],
        )

    def test_7_orphan(self):
        self.assertEqual(self.checks(**{"docs/skills/deploy.md": PROC.replace(", see changelog", "")}), [7])

    def test_9_stale_path(self):
        self.assertEqual(self.checks(**{"docs/skills/deploy.md": PROC.replace("see changelog", "see changelog and docs/guardrails/gone.md")}), [9])

    def test_9_placeholder_exempt(self):
        self.assertEqual(self.checks(**{"docs/skills/deploy.md": PROC.replace("see changelog", "see changelog and docs/facts/NNNN-slug.md")}), [])

    def test_12_template_missing(self):
        project(self.root)
        t = Path(self.root, "plugins/kms/templates/guardrails/extra.md")
        t.write_text("---\ntemplate-version: 1\nid: extra\n---\n")
        self.assertEqual(sorted({c for c, _, _ in Linter(self.root).run()}), [12])

    def test_15_track_both(self):
        self.assertEqual(self.checks(**{"docs/decisions/0001-weekly.md": DECISION.replace("track: process", "track: both")}), [15])

    def test_19_index_row_missing(self):
        self.assertEqual(self.checks(**{"docs/decisions/INDEX.md": INDEX.format("")}), [19])

    def test_19_title_mismatch(self):
        self.assertEqual(self.checks(**{"docs/decisions/INDEX.md": INDEX.format("0001-weekly,Ship daily,release,active")}), [19])

    def test_20_superseded_not_archived(self):
        got = self.checks(**{
            "docs/decisions/0001-weekly.md": DECISION.replace("status: active", "status: superseded\nsuperseded-by: 0001-weekly"),
            "docs/decisions/INDEX.md": INDEX.format("0001-weekly,Ship weekly,release,superseded"),
        })
        self.assertEqual(got, [20])

    def test_21_tag_off_list(self):
        self.assertEqual(self.checks(**{"docs/skills/deploy.md": PROC.replace("[release]", "[nope]"), "docs/skills/INDEX.md": INDEX.format("deploy,Deploy steps,nope,active\ntags,Tags,release,active")}), [21])

    def test_deterministic(self):
        project(self.root, **{"docs/skills/deploy.md": PROC.replace("[release]", "[nope]")})
        self.assertEqual(Linter(self.root).run(), Linter(self.root).run())


if __name__ == "__main__":
    unittest.main()
