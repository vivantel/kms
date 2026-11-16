"""Unit cases for plugins/kms/shared/lint_check.py: a clean project yields nothing, and one
seeded mutation per check yields exactly that check. Run: python3 -m unittest discover evals/lint/unit"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "plugins" / "kms" / "shared"))
from lint_check import Linter, revision  # noqa: E402

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
        "CHANGELOG.md": "# Changelog\n",
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
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def checks(self, kw=None, **over):
        kw = kw or {}
        project(self.root, **over)
        return sorted({c for c, _, _ in Linter(self.root, today="2026-02-01", **kw).run()})

    def test_clean_project(self):
        self.assertEqual(self.checks(), [])

    def test_1_dangling(self):
        # the fact loses its only referrer, so check 7 also fires
        self.assertEqual(self.checks(**{"docs/guardrails/changelog.md": GUARD.replace("[0001-cadence]", "[0099-none]")}), [1, 7])

    def test_2_missing_field(self):
        self.assertEqual(self.checks(**{"docs/decisions/0001-weekly.md": DECISION.replace("date: 2026-01-01\n", "")}), [2])

    def test_2_bare_string_list(self):
        self.assertEqual(self.checks(**{"docs/guardrails/changelog.md": GUARD.replace("[0001-cadence]", "0001-cadence")}), [2])

    def test_unterminated_frontmatter_still_checked(self):
        bad = GUARD.replace("---\nBody.\n", "").replace("[0001-cadence]", "[0099-none]")
        project(self.root, **{"docs/guardrails/changelog.md": bad})
        got = {(c, m) for c, _, m in Linter(self.root).run()}
        self.assertIn((2, "unterminated frontmatter"), got)
        self.assertTrue(any(c == 1 for c, _ in got))

    def test_2_tbd_marker_is_not_a_list_violation(self):
        self.assertEqual(self.checks(**{"docs/guardrails/changelog.md": GUARD.replace("[0001-cadence]", "TBD")}), [7])

    def test_9_skips_decisions(self):
        self.assertEqual(self.checks(**{"docs/decisions/0001-weekly.md": DECISION.replace("Body.", "See docs/guardrails/gone.md.")}), [])

    def test_2_bad_status(self):
        got = self.checks(**{"docs/skills/deploy.md": PROC.replace("status: active", "status: live")})
        self.assertIn(2, got)

    def test_3_gap_is_advisory(self):
        # the added fact is unreferenced, so check 7 also fires
        self.assertEqual(
            self.checks(**{"docs/facts/0003-x.md": FACT.replace("0001-cadence", "0003-x"), "docs/facts/INDEX.md": INDEX.format("0001-cadence,Releases are weekly,release,active\n0003-x,Releases are weekly,release,active")}),
            [7],  # a gap is advisory (a warning), not a finding
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

    def test_track_is_an_older_shape(self):
        # `track` was dropped (decision 0079): advisory by default, a finding under --strict
        over = {"docs/decisions/0001-weekly.md": DECISION.replace("tags: [release]", "tags: [release]\ntrack: process")}
        self.assertEqual(self.checks(**over), [])
        self.assertIn(2, self.checks(kw={"strict": True}, **over))

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

    # --- pinned edges (check 13) ---

    def pinned(self, **over):
        """Project whose guardrail is pinned to the current fact and decision; `over` then edits files."""
        project(self.root)
        Linter(self.root).pin("docs/guardrails/changelog.md")
        for rel, text in over.items():
            (Path(self.root) / rel).write_text(text, encoding="utf-8")
        return sorted({c for c, _, _ in Linter(self.root).run()})

    def test_facts_need_no_kind_or_governed_by(self):
        bare = FACT.replace("kind: environmental\n", "").replace("governed-by: 0001-weekly\n", "")
        self.assertEqual(self.checks(**{"docs/facts/0001-cadence.md": bare}), [])
        self.assertEqual(self.checks(**{"docs/facts/0001-cadence.md": FACT.replace("environmental", "mixed")}), [])

    def test_scope_valid_on_fact_is_clean(self):
        f = FACT.replace("governed-by: 0001-weekly", "scope: {component: release-job, environment: ci}\ngoverned-by: 0001-weekly")
        self.assertEqual(self.checks(**{"docs/facts/0001-cadence.md": f}), [])

    def test_2_scope_bad_shape(self):
        for bad in ("[ci]", "{}", "{region: eu}", "{version: ''}", "ci"):
            with self.subTest(bad=bad):
                f = FACT.replace("governed-by: 0001-weekly", f"scope: {bad}\ngoverned-by: 0001-weekly")
                self.assertEqual(self.checks(**{"docs/facts/0001-cadence.md": f}), [2])

    def test_2_scope_on_decision(self):
        d = DECISION.replace("tags:", "scope: {component: x}\ntags:")
        self.assertEqual(self.checks(**{"docs/decisions/0001-weekly.md": d}), [2])

    def test_pin_writes_map_and_is_clean(self):
        self.assertEqual(self.pinned(), [])
        text = (Path(self.root) / "docs/guardrails/changelog.md").read_text()
        self.assertIn("pinned:\n  0001-weekly: ", text)
        self.assertIn("  0001-cadence: ", text)

    def test_pin_is_idempotent(self):
        project(self.root)
        for _ in range(2):
            Linter(self.root).pin("docs/guardrails/changelog.md")
        text = (Path(self.root) / "docs/guardrails/changelog.md").read_text()
        self.assertEqual(text.count("pinned:"), 1)

    def test_13_source_body_changed(self):
        self.assertEqual(self.pinned(**{"docs/facts/0001-cadence.md": FACT.replace("Body.", "Releases are now monthly.")}), [13])

    def test_13_ignores_lifecycle_fields(self):
        # pins track content, not lifecycle (decision 0077): retiring a pinned fact is never check 13; check 1 asks to re-derive
        # (the pin makes it a finding, not an older-shape advisory) and check 20 is about the file's location
        self.assertEqual(
            self.pinned(**{"docs/facts/0001-cadence.md": FACT.replace("status: active", "status: deprecated"),
                           "docs/facts/INDEX.md": INDEX.format("0001-cadence,Releases are weekly,release,deprecated")}),
            [1, 20],
        )

    def test_retired_pinned_decision_is_a_finding_without_strict(self):
        checks = self.pinned(**{"docs/decisions/0001-weekly.md": DECISION.replace("status: active", "status: superseded\nsuperseded-by: 0001-weekly")})
        self.assertIn(1, checks)
        self.assertNotIn(13, checks)

    def test_13_ignores_date_cosmetics_and_own_edges(self):
        self.assertEqual(
            self.pinned(**{"docs/facts/0001-cadence.md": FACT.replace("date: 2026-01-01", "date: 2026-06-01").replace("Body.", "Body.\n\n")}),
            [],
        )

    def test_13_unpinned_edge_is_left_to_the_model(self):
        self.assertEqual(self.checks(**{"docs/facts/0001-cadence.md": FACT.replace("Body.", "Changed.")}), [])

    def test_2_pin_for_non_edge(self):
        g = GUARD.replace("derivation-note", "pinned:\n  0099-none: abc\nderivation-note")
        self.assertEqual(self.checks(**{"docs/guardrails/changelog.md": g}), [2])

    def test_13_precision_recall_on_seeded_changes(self):
        """Seed one source change per case and one untouched control per case; the checker must flag exactly the changed ones."""
        changes = [
            lambda: {"docs/facts/0001-cadence.md": FACT.replace("Body.", "Different claim.")},
            lambda: {"docs/facts/0001-cadence.md": FACT.replace("weekly", "monthly")},
            lambda: {"docs/decisions/0001-weekly.md": DECISION.replace("Body.", "Ship daily.")},
            lambda: {"docs/decisions/0001-weekly.md": DECISION.replace("Ship weekly", "Ship daily")},
        ]
        controls = [
            lambda: {},
            lambda: {"docs/facts/0001-cadence.md": FACT.replace("date: 2026-01-01", "date: 2026-02-02")},
            lambda: {"docs/guardrails/changelog.md": None},
        ]
        tp = sum(13 in self._flagged(c()) for c in changes)
        fp = sum(13 in self._flagged(c()) for c in controls)
        self.assertEqual((tp, fp), (len(changes), 0))

    def _flagged(self, over):
        shutil.rmtree(self.root)
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        return self.pinned(**{k: v for k, v in over.items() if v is not None})

    def test_revision_ignores_edge_fields_and_whitespace(self):
        a = revision(FACT)
        self.assertEqual(a, revision(FACT.replace("governed-by: 0001-weekly", "governed-by: 0002-x")))
        self.assertEqual(a, revision(FACT.replace("Body.", "Body.  \n")))
        self.assertNotEqual(a, revision(FACT.replace("Body.", "Other.")))

    def test_deterministic(self):
        project(self.root, **{"docs/skills/deploy.md": PROC.replace("[release]", "[nope]")})
        self.assertEqual(Linter(self.root).run(), Linter(self.root).run())


class LintCheckBugFixes(unittest.TestCase):
    """Step 1.2 of docs/plans/kms-review-and-redesign.md: one case per fixed defect."""

    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def run_checks(self, **over):
        project(self.root, **over)
        return Linter(self.root).run()

    def seeded(self, ver):
        tmpl = Path(self.root, "plugins/kms/templates/guardrails/seeded.md")
        tmpl.parent.mkdir(parents=True, exist_ok=True)
        tmpl.write_text("---\nid: seeded\ntemplate-version: 2\n---\n")
        g = GUARD.replace("id: changelog", "id: seeded").replace("tags: [release]", f"tags: [release]\nkms-seeded: true\nkms-template-version: {ver}")
        return {"docs/guardrails/seeded.md": g, "docs/guardrails/INDEX.md": INDEX.format(
            "changelog,Every release has a changelog entry,release,active\nseeded,Every release has a changelog entry,release,active")}

    def test_12_quoted_template_version_does_not_crash(self):
        got = self.run_checks(**self.seeded('"1"'))
        self.assertEqual([(c, m) for c, _, m in got if c == 12], [(12, "seeded from template version 1, template is at 2")])

    def test_12_non_numeric_template_version_is_a_finding(self):
        got = self.run_checks(**self.seeded("two"))
        self.assertTrue(any(c == 12 and "not a number" in m for c, _, m in got))

    def test_7_seeded_guardrail_is_not_an_orphan(self):
        got = self.run_checks(**self.seeded(2))
        self.assertFalse([f for f in got if f[0] == 7])

    def test_unparseable_frontmatter_does_not_cascade(self):
        bad = GUARD.replace("title: Every release has a changelog entry", "title: Every release: has an entry")
        got = self.run_checks(**{"docs/guardrails/changelog.md": bad})
        self.assertEqual(sorted({c for c, _, _ in got}), [2])

    def test_docs_dir_is_autodetected_and_overridable(self):
        project(self.root)
        Path(self.root, "docs").rename(Path(self.root, "knowledge"))
        self.assertEqual(Linter(self.root).docs.name, "knowledge")
        self.assertEqual(Linter(self.root).run(), [])
        self.assertEqual(Linter(self.root, "knowledge").run(), [])

    def test_empty_project_warns(self):
        self.assertTrue(Linter(self.root).warnings)

    def test_9_keys_on_type_and_name_and_follows_archive(self):
        both = "See docs/facts/gone.md, docs/guardrails/gone.md, docs/guardrails/archive/old.md."
        got = [m for c, _, m in self.run_checks(**{"docs/skills/deploy.md": PROC.replace("Body, see changelog.", both + " changelog")}) if c == 9]
        self.assertEqual(len(got), 3)

    def test_9_scans_readme_and_live_plans_not_archived_plans(self):
        got = self.run_checks(**{
            "README.md": "see docs/facts/gone.md",
            "docs/plans/p.md": "see docs/facts/gone2.md",
            "docs/plans/archive/q.md": "see docs/facts/gone3.md",
        })
        self.assertEqual(sorted(f for c, f, _ in got if c == 9), ["README.md", "docs/plans/p.md"])

    def test_3_duplicate_id_and_pin_refuses(self):
        over = {"docs/guardrails/changelog.md": GUARD.replace("id: changelog", "id: 0001-weekly")}
        got = self.run_checks(**over)
        self.assertTrue(any(c == 3 and "used by 2 files" in m for c, _, m in got))
        with self.assertRaises(SystemExit):
            Linter(self.root).pin("docs/guardrails/changelog.md")

    def test_21_tags_md_accepts_bullets_and_separators(self):
        for line in ("- release — meaning", "* release - meaning", "release: meaning", "release (umbrella) — meaning"):
            tags = TAGS.replace("release — release process", line)
            self.assertEqual([f for f in self.run_checks(**{"docs/skills/tags.md": tags}) if f[0] == 21], [], line)

    def test_pin_quotes_values_and_preserves_crlf(self):
        project(self.root, **{"docs/guardrails/changelog.md": None})
        g = Path(self.root, "docs/guardrails/changelog.md")
        g.write_bytes(GUARD.replace("\n", "\r\n").encode())
        Linter(self.root).pin("docs/guardrails/changelog.md")
        raw = g.read_bytes().decode()
        self.assertRegex(raw, r'  0001-weekly: "[0-9a-f]{12}"\r\n')
        self.assertNotIn("\n", raw.replace("\r\n", ""))

    def test_pin_unterminated_frontmatter_is_a_message(self):
        bad = GUARD.replace("---\nBody.\n", "")
        project(self.root, **{"docs/guardrails/changelog.md": bad})
        with self.assertRaises(SystemExit) as cm:
            Linter(self.root).pin("docs/guardrails/changelog.md")
        self.assertIn("unterminated", str(cm.exception))

    def test_2_tags_must_be_a_list(self):
        got = self.run_checks(**{"docs/skills/deploy.md": PROC.replace("tags: [release]", "tags: release")})
        self.assertTrue(any(c == 2 and "`tags` must be a YAML list" in m for c, _, m in got))


if __name__ == "__main__":
    unittest.main()


class NewRules(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def run_checks(self, today="2026-02-01", **over):
        kw = over.pop("kw", {})
        project(self.root, **over)
        lin = Linter(self.root, today=today, **kw)
        return sorted({c for c, _, _ in lin.run()}), lin

    def test_legacy_shapes_are_advisory_then_strict_findings(self):
        checks, lin = self.run_checks()
        self.assertEqual(checks, [])
        self.assertTrue(any("older shape: docs/facts/0001-cadence.md" in w for w in lin.warnings))
        checks, _ = self.run_checks(kw={"strict": True})
        self.assertEqual(checks, [2])

    def test_strict_clean_new_shape(self):
        over = {
            "docs/facts/0001-cadence.md": FACT.replace("kind: environmental\ngoverned-by: 0001-weekly\n", "source: CHANGELOG.md\n"),
            "docs/guardrails/changelog.md": GUARD.replace("governed-by: 0001-weekly", "governed-by: [0001-weekly]"),
        }
        self.assertEqual(self.run_checks(kw={"strict": True}, **over)[0], [])

    def test_4_expired_date(self):
        self.assertEqual(self.run_checks(today="2026-03-01", **{"docs/decisions/0001-weekly.md": DECISION.replace("tags: [release]", "tags: [release]\nexpires: 2026-02-01")})[0], [4])

    def test_17_stale_draft_and_open_question_exemption(self):
        d = DECISION.replace("status: active", "status: draft")
        idx = {"docs/decisions/INDEX.md": INDEX.format("0001-weekly,Ship weekly,release,draft")}
        self.assertEqual(self.run_checks(today="2026-09-01", **{"docs/decisions/0001-weekly.md": d}, **idx)[0], [17])
        q = d.replace("tags: [release]", "tags: [release]\nexpires-when: the test closes")
        self.assertEqual(self.run_checks(today="2026-09-01", **{"docs/decisions/0001-weekly.md": q}, **idx)[0], [])

    def test_18_fitness_function_staleness(self):
        ff = "tags: [release]\nfitness-functions:\n  - {check: weekly tag, enforced-by: ci, last-verified: 2026-01-01}"
        over = {"docs/decisions/0001-weekly.md": DECISION.replace("tags: [release]", ff)}
        self.assertEqual(self.run_checks(today="2026-02-01", **over)[0], [])
        self.assertEqual(self.run_checks(today="2026-09-01", **over)[0], [18])

    def test_24_completed_plan_not_archived(self):
        plan = "---\nid: p\n---\n### 1 [done]\n### 2 [done]\n"
        self.assertEqual(self.run_checks(**{"docs/plans/p.md": plan})[0], [24])
        self.assertEqual(self.run_checks(**{"docs/plans/p.md": plan.replace("### 2 [done]", "### 2 [pending]")})[0], [])

    def test_7_fact_with_source_is_not_an_orphan(self):
        fact = FACT.replace("kind: environmental\ngoverned-by: 0001-weekly\n", "source: CHANGELOG.md\n")
        guard = GUARD.replace("grounded-in: [0001-cadence]\n", "")
        self.assertEqual(self.run_checks(**{"docs/facts/0001-cadence.md": fact, "docs/guardrails/changelog.md": guard})[0], [])
        self.assertEqual(self.run_checks(**{"docs/facts/0001-cadence.md": FACT, "docs/guardrails/changelog.md": guard})[0], [7])

    def test_registry_is_skipped(self):
        reg = "---\nkms-registry: roles\n---\nnot an artifact\n"
        self.assertEqual(self.run_checks(**{"docs/skills/roles.md": reg})[0], [])

    def test_refs(self):
        project(self.root)
        self.assertEqual(Linter(self.root).refs("0001-weekly"), ["docs/facts/0001-cadence.md", "docs/guardrails/changelog.md"])

    def test_governed_by_superseded_decision(self):
        over = {"docs/decisions/0001-weekly.md": DECISION.replace("status: active", "status: superseded\nsuperseded-by: 0002-x"),
                "docs/guardrails/changelog.md": GUARD.replace("governed-by: 0001-weekly", "governed-by: [0001-weekly]")}
        checks, _ = self.run_checks(kw={"strict": True}, **over)
        self.assertIn(1, checks)

    def test_calendar_invalid_date_is_a_finding_not_a_crash(self):
        checks, _ = self.run_checks(**{"docs/decisions/0001-weekly.md": DECISION.replace("2026-01-01", "2026-02-30")})
        self.assertIn(2, checks)

    def test_absolute_docs_with_relative_root(self):
        import os
        project(self.root)
        cwd = os.getcwd()
        os.chdir(self.root)
        try:
            lin = Linter(".", docs=str(Path(self.root).resolve() / "docs"), today="2026-02-01")
            self.assertEqual(sorted({c for c, _, _ in lin.run()}), [])
        finally:
            os.chdir(cwd)

    def test_scalar_fitness_functions_is_check_2(self):
        checks, _ = self.run_checks(**{"docs/decisions/0001-weekly.md": DECISION.replace("tags: [release]", "tags: [release]\nfitness-functions: true")})
        self.assertEqual(checks, [2])

    def test_open_question_still_gets_check_18(self):
        fm = "status: draft\nexpires-when: answered\nfitness-functions: [{check: x}]"
        checks, _ = self.run_checks(**{"docs/decisions/0001-weekly.md": DECISION.replace("status: active", fm)})
        self.assertIn(18, checks)
        self.assertNotIn(17, checks)

    def test_plan_step_headings(self):
        plan = "### 1 [done]\n### 2 [done]\n### Step 3: C [pending]\n"
        self.assertNotIn(24, self.run_checks(**{"docs/plans/p.md": plan})[0])
        self.assertNotIn(24, self.run_checks(**{"docs/plans/p.md": "### 1 [done]\n### 2.10 [done, except x: blocked]\n"})[0])
        self.assertIn(24, self.run_checks(**{"docs/plans/p.md": "## Step 1. A [done]\n### 2 [done]\n"})[0])

    def test_tags_frontmatter_keys_are_not_tags(self):
        checks, _ = self.run_checks(**{"docs/decisions/0001-weekly.md": DECISION.replace("[release]", "[status]")})
        self.assertIn(21, checks)

    def test_dot_slash_prose_reference_is_checked(self):
        checks, _ = self.run_checks(**{"README.md": "see ./docs/facts/gone.md\n"})
        self.assertIn(9, checks)

    def test_archived_target_of_a_live_path_is_check_9(self):
        over = {"README.md": "see docs/facts/0002-old.md\n", "docs/facts/archive/0002-old.md": FACT.replace("0001-cadence", "0002-old")}
        self.assertIn(9, self.run_checks(**over)[0])
        over["README.md"] = "see docs/facts/archive/0002-old.md\n"
        self.assertNotIn(9, self.run_checks(**over)[0])

    def test_non_utf8_file_does_not_abort(self):
        project(self.root)
        (Path(self.root) / "README.md").write_bytes("Caf\xe9 docs/facts/0001-cadence.md".encode("latin-1"))
        Linter(self.root, today="2026-02-01").run()

    def test_linter_is_reentrant(self):
        project(self.root)
        lin = Linter(self.root, today="2026-02-01")
        first = lin.run()
        self.assertEqual(lin.run(), first)

    def test_date_that_is_not_a_date_is_check_2(self):
        checks, _ = self.run_checks(**{"docs/decisions/0001-weekly.md": DECISION.replace("2026-01-01", "soon")})
        self.assertIn(2, checks)

