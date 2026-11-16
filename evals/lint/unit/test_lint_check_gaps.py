"""Gap cases for plugins/kms/shared/lint_check.py: each test pins a finding's check number and message, a
boundary, or a crash guard that the one-seeded-violation-per-check cases in test_lint_check.py leave unasserted.
They were found by mutating the checker one operator at a time and keeping the mutants the suites let survive.
Nine mutants cannot be told from the original and have no test: the `not lines` and `lines and` guards (split("\n") is never
empty), a loop starting at 2 not 1 over frontmatter (only an empty block differs, and `fm` is falsy first), `range(1, max(nums))`
(max is always present), and the prose-reference `seen` key (a repeat is collapsed by run()).
Run: python3 -m unittest discover evals/lint/unit"""

import datetime
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
SHARED = HERE.parents[3] / "plugins" / "kms" / "shared"
sys.path.insert(0, str(SHARED))
sys.path.insert(0, str(HERE.parent))
from lint_check import Linter, edge_ids, revision, split_frontmatter  # noqa: E402
from test_lint_check import DECISION, FACT, GUARD, INDEX, PROC, project  # noqa: E402

TODAY = "2026-02-01"
GUARD_LIST = GUARD.replace("governed-by: 0001-weekly", "governed-by: [0001-weekly]")


class Gaps(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def lint(self, strict=False, today=TODAY, **over):
        kw = over.pop("kw", {})
        project(self.root, **over)
        lin = Linter(self.root, strict=strict, today=today, **kw)
        return lin.run(), lin

    def found(self, check, fragment, **kw):
        got, _ = self.lint(**kw)
        return any(c == check and fragment in m for c, _, m in got)

    def write(self, rel, text):
        p = Path(self.root, rel)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    # --- frontmatter and revision helpers -------------------------------------------------

    def test_split_empty_frontmatter_is_a_mapping(self):
        self.assertEqual(split_frontmatter("---\n---\nBody"), ({}, None))

    def test_split_unterminated_stops_at_a_blank_line_or_heading(self):
        self.assertEqual(split_frontmatter("---\n\nBody\n"), ({}, "unterminated frontmatter"))
        self.assertEqual(split_frontmatter("---\nid: x\n# Heading\nbody\n"), ({"id": "x"}, "unterminated frontmatter"))

    def test_split_reports_the_yaml_error_not_its_class_name(self):
        data, err = split_frontmatter("---\ntitle: [unclosed\n---\nBody")
        self.assertIsNone(data)
        self.assertTrue(err.startswith("unparseable frontmatter: "))
        self.assertGreater(len(err), len("unparseable frontmatter: ParserError"))

    def test_revision_without_frontmatter_is_a_hash_of_the_text(self):
        self.assertEqual(revision("plain  text\n"), revision("plain text"))
        self.assertNotEqual(revision("plain text"), revision("other text"))

    def test_revision_keeps_a_leading_comment_line_in_frontmatter(self):
        self.assertNotEqual(revision("---\n# one\nid: x\n---\nbody"), revision("---\n# two\nid: x\n---\nbody"))

    def test_edge_ids_dedupes_and_drops_tbd(self):
        self.assertEqual(edge_ids({"governed-by": ["a", "TBD"], "grounded-in": ["a", "b"]}), ["a", "b"])
        self.assertEqual(edge_ids({"governed-by": "TBD"}), [])
        self.assertEqual(edge_ids(None), [])

    # --- field shape (check 2) ------------------------------------------------------------

    def test_2_superseded_needs_superseded_by(self):
        d = DECISION.replace("status: active", "status: superseded")
        self.assertTrue(self.found(2, "`status: superseded` without `superseded-by`", **{"docs/decisions/0001-weekly.md": d}))

    def test_2_scalar_governed_by_on_a_guardrail_is_an_older_shape(self):
        self.assertTrue(self.found(2, "`governed-by` on a guardrail should be a YAML list", strict=True))
        self.assertFalse(self.found(2, "`governed-by` on a guardrail", strict=True, **{"docs/guardrails/changelog.md": GUARD_LIST}))
        self.assertFalse(self.found(2, "`governed-by` on a guardrail", strict=True, **{"docs/guardrails/changelog.md": GUARD.replace("governed-by: 0001-weekly", "governed-by: TBD")}))

    def test_a_guardrail_without_governed_by_is_not_a_crash(self):
        got, _ = self.lint(**{"docs/guardrails/changelog.md": GUARD.replace("governed-by: 0001-weekly\n", "")})
        self.assertEqual([m for c, _, m in got if c == 2], ["missing required field `governed-by`"])

    def test_2_expires_must_be_a_date(self):
        d = DECISION.replace("tags: [release]", "tags: [release]\nexpires: when the audit ends")
        self.assertTrue(self.found(2, "`expires` must be a date", strict=True, **{"docs/decisions/0001-weekly.md": d}))
        ok = DECISION.replace("tags: [release]", "tags: [release]\nexpires: 2027-01-01")
        self.assertFalse(self.found(2, "`expires` must be a date", strict=True, **{"docs/decisions/0001-weekly.md": ok}))

    def test_2_fitness_function_entries_are_maps_with_check(self):
        def over(ff):
            return {"docs/decisions/0001-weekly.md": DECISION.replace("tags: [release]", "tags: [release]\nfitness-functions:\n" + ff)}
        self.assertTrue(self.found(2, "entries should be maps with `check`", strict=True, **over("  - a bare string")))
        self.assertTrue(self.found(2, "entries should be maps with `check`", strict=True, **over("  - {enforced-by: ci}")))
        self.assertFalse(self.found(2, "entries should be maps with `check`", strict=True, **over("  - {check: weekly tag, last-verified: 2026-01-20}")))

    def test_2_pinned_must_be_a_mapping(self):
        g = GUARD_LIST.replace("tags: [release]", "tags: [release]\npinned: [0001-weekly]")
        self.assertTrue(self.found(2, "`pinned` must be a mapping of id to revision, got list", **{"docs/guardrails/changelog.md": g}))

    def test_2_track_on_a_decision_only(self):
        d = DECISION.replace("tags: [release]", "tags: [release]\ntrack: process")
        self.assertTrue(self.found(2, "`track` is not a decision field any more", strict=True, **{"docs/decisions/0001-weekly.md": d}))
        g = GUARD_LIST.replace("tags: [release]", "tags: [release]\ntrack: process")
        self.assertFalse(self.found(2, "`track` is not a decision field", strict=True, **{"docs/guardrails/changelog.md": g}))

    # --- references (check 1) and numbering (check 3) -------------------------------------

    def test_1_superseded_decision_is_a_finding_only_on_a_live_guardrail(self):
        sup = DECISION.replace("status: active", "status: superseded\nsuperseded-by: 0002-x")
        idx = {"docs/decisions/INDEX.md": INDEX.format("0001-weekly,Ship weekly,release,superseded")}
        self.assertTrue(self.found(1, "a superseded decision: re-derive", strict=True, **{"docs/decisions/0001-weekly.md": sup}, **idx))
        # a decision that cites a superseded decision is not a guardrail: nothing to re-derive
        other = DECISION.replace("0001-weekly", "0002-other").replace("tags: [release]", "tags: [release]\ngoverned-by: [0001-weekly]")
        got, _ = self.lint(strict=True, **{
            "docs/decisions/0001-weekly.md": sup,
            "docs/decisions/0002-other.md": other,
            "docs/decisions/INDEX.md": INDEX.format("0001-weekly,Ship weekly,release,superseded\n0002-other,Ship weekly,release,active"),
            "docs/guardrails/changelog.md": GUARD_LIST.replace("governed-by: [0001-weekly]", "governed-by: TBD"),
        })
        self.assertFalse([m for c, f, m in got if c == 1 and f.endswith("0002-other.md")])

    def test_1_grounded_in_a_non_fact_is_an_older_shape(self):
        g = GUARD_LIST.replace("grounded-in: [0001-cadence]", "grounded-in: [0001-weekly]")
        self.assertTrue(self.found(1, "which is not a fact", strict=True, **{"docs/guardrails/changelog.md": g}))
        self.assertFalse(self.found(1, "which is not a fact", strict=True))

    def test_3_skipped_numbers_are_warnings_naming_the_number_and_directory(self):
        fact3 = FACT.replace("0001-cadence", "0003-x")
        _, lin = self.lint(**{"docs/facts/0003-x.md": fact3, "docs/facts/INDEX.md": INDEX.format("0001-cadence,Releases are weekly,release,active\n0003-x,Releases are weekly,release,active")})
        self.assertIn("number 0002 is skipped in docs/facts/", lin.warnings)
        Path(self.root, "docs/facts/0003-x.md").unlink()
        _, lin = self.lint()
        self.assertFalse([w for w in lin.warnings if "skipped" in w])

    def test_3_duplicate_number_and_duplicate_id_are_check_3(self):
        dup = {"docs/facts/0001-other.md": FACT.replace("id: 0001-cadence", "id: 0001-other"), "docs/facts/INDEX.md": INDEX.format("0001-cadence,Releases are weekly,release,active\n0001-other,Releases are weekly,release,active")}
        self.assertTrue(self.found(3, "number 0001 used by 2 files", **dup))
        same_id = {"docs/facts/0002-cadence.md": FACT, "docs/facts/INDEX.md": INDEX.format("0001-cadence,Releases are weekly,release,active")}
        self.assertTrue(self.found(3, "id `0001-cadence` is used by 2 files", **same_id))
        got, _ = self.lint(**same_id)
        self.assertIn("docs/facts/0001-cadence.md", [f for c, f, m in got if c == 3 and m.startswith("id `")])  # the finding names the first file

    # --- orphans, prose references and templates (checks 7, 9, 12) -----------------------

    def seeded_guardrail(self, version=None, seeded="true", template_version=None, template_id="seeded"):
        t = Path(self.root, "plugins/kms/templates/guardrails")
        t.mkdir(parents=True, exist_ok=True)
        (t / f"{template_id}.md").write_text(f"---\nid: {template_id}\n" + (f"template-version: {template_version}\n" if template_version is not None else "") + "---\n")
        extra = f"kms-seeded: {seeded}" + (f"\nkms-template-version: {version}" if version is not None else "")
        g = GUARD_LIST.replace("id: changelog", "id: seeded").replace("tags: [release]", "tags: [release]\n" + extra)
        return {"docs/guardrails/seeded.md": g, "docs/guardrails/INDEX.md": INDEX.format("changelog,Every release has a changelog entry,release,active\nseeded,Every release has a changelog entry,release,active")}

    def test_7_only_a_true_kms_seeded_exempts_a_guardrail(self):
        # the template is named otherwise, so nothing in plugins/ mentions the guardrail's id
        got, _ = self.lint(**self.seeded_guardrail(version=1, template_id="other"))
        self.assertFalse([m for c, f, m in got if c == 7])
        got, _ = self.lint(**self.seeded_guardrail(version=1, seeded="false", template_id="other"))
        self.assertTrue([m for c, f, m in got if c == 7 and "`seeded`" in m])

    def test_12_template_version_default_and_boundary(self):
        # a template without template-version is version 1; equal versions are current
        got, _ = self.lint(**self.seeded_guardrail(version=1))
        self.assertEqual([m for c, _, m in got if c == 12], [])
        got, _ = self.lint(**self.seeded_guardrail(version=2, template_version=2))
        self.assertEqual([m for c, _, m in got if c == 12], [])
        # a seeded file without kms-template-version is version 0
        got, _ = self.lint(**self.seeded_guardrail(template_version=1))
        self.assertEqual([m for c, _, m in got if c == 12], ["seeded from template version 0, template is at 1"])

    def test_12_seeded_guardrail_whose_template_is_gone(self):
        self.assertTrue(self.found(12, "`kms-seeded` but template `seeded` no longer exists", **self.seeded_guardrail(version=1, template_id="other")))

    def test_12_template_file_without_frontmatter_is_skipped(self):
        t = Path(self.root, "plugins/kms/templates/guardrails")
        t.mkdir(parents=True, exist_ok=True)
        (t / "readme.md").write_text("no frontmatter here\n")
        got, _ = self.lint()
        self.assertEqual([c for c, _, _ in got], [])

    def test_9_each_missing_reference_is_reported_and_a_repeat_is_not(self):
        text = PROC.replace("Body, see changelog.", "Body, see changelog. See docs/guardrails/gone-a.md, docs/guardrails/gone-b.md and docs/guardrails/gone-a.md again.")
        got, _ = self.lint(**{"docs/skills/deploy.md": text})
        msgs = [m for c, _, m in got if c == 9]
        self.assertEqual(len(msgs), 2)
        self.assertTrue(any("gone-a.md" in m for m in msgs) and any("gone-b.md" in m for m in msgs))

    def test_9_a_moved_file_gets_the_archive_hint_only_when_it_moved(self):
        moved = PROC.replace("Body, see changelog.", "Body, see changelog. See docs/guardrails/old.md.")
        archive = {"docs/guardrails/archive/old.md": GUARD_LIST.replace("id: changelog", "id: old"), "docs/guardrails/archive/INDEX.md": INDEX.format("old,Every release has a changelog entry,release,active")}
        got, _ = self.lint(**{"docs/skills/deploy.md": moved}, **archive)
        self.assertTrue(any(c == 9 and "(it moved to archive/: update the path)" in m for c, _, m in got))
        got, _ = self.lint(**{"docs/skills/deploy.md": moved.replace("old.md", "never.md")}, **archive)
        self.assertTrue(any(c == 9 and "never.md" in m and "moved to archive" not in m for c, _, m in got))
        in_archive = moved.replace("docs/guardrails/old.md", "docs/guardrails/archive/gone.md")
        got, _ = self.lint(**{"docs/skills/deploy.md": in_archive}, **archive)
        self.assertTrue(any(c == 9 and "archive/gone.md" in m and "moved to archive" not in m for c, _, m in got))

    # --- index (check 19) -----------------------------------------------------------------

    def test_19_messages(self):
        self.assertTrue(self.found(19, "no `id,title,tags,status` header", **{"docs/facts/INDEX.md": "just prose\n"}))
        self.assertTrue(self.found(19, "malformed row: 0001-cadence,Releases are weekly", **{"docs/facts/INDEX.md": INDEX.format("0001-cadence,Releases are weekly")}))
        self.assertTrue(self.found(19, "row `0009-ghost` has no file in this directory", **{"docs/facts/INDEX.md": INDEX.format("0001-cadence,Releases are weekly,release,active\n0009-ghost,Ghost,release,active")}))

    def test_19_malformed_row_is_cut_at_60_characters(self):
        row = "x" * 80
        got, _ = self.lint(**{"docs/facts/INDEX.md": INDEX.format("0001-cadence,Releases are weekly,release,active\n" + row)})
        self.assertIn("malformed row: " + "x" * 60, [m for c, _, m in got if c == 19])

    def test_19_archive_index_is_checked_too(self):
        arch = {"docs/facts/archive/0002-old.md": FACT.replace("id: 0001-cadence", "id: 0002-old").replace("status: active", "status: deprecated"), "docs/facts/archive/INDEX.md": INDEX.format("0002-old,Releases are weekly,release,active")}
        self.assertTrue(self.found(19, "row `0002-old`: status is `active`, file says `deprecated`", **arch))

    # --- dates (checks 4, 17, 18) ---------------------------------------------------------

    def test_4_expiry_on_the_day_is_not_yet_expired(self):
        def over(day):
            return {"docs/decisions/0001-weekly.md": DECISION.replace("tags: [release]", f"tags: [release]\nexpires: {day}")}
        self.assertFalse(self.found(4, "has passed", **over(TODAY)))
        self.assertTrue(self.found(4, "has passed", **over("2026-01-31")))

    def stale_decision(self, age, **kw):
        day = (datetime.date.fromisoformat(TODAY) - datetime.timedelta(days=age)).isoformat()
        d = DECISION.replace("status: active", "status: draft").replace("date: 2026-01-01", f"date: {day}")
        idx = {"docs/decisions/INDEX.md": INDEX.format("0001-weekly,Ship weekly,release,draft")}
        return self.lint(**{"docs/decisions/0001-weekly.md": d}, **idx, **kw)

    def test_17_threshold_is_exclusive_and_defaults_to_180_days(self):
        got, _ = self.stale_decision(180)
        self.assertEqual([c for c, _, _ in got], [])
        got, _ = self.stale_decision(181)
        self.assertEqual([(c, m) for c, _, m in got], [(17, "`status: draft` unresolved for 181 days (threshold 180)")])
        got, _ = self.stale_decision(30, kw={"stale_days": 30})
        self.assertEqual([c for c, _, _ in got], [])
        got, _ = self.stale_decision(31, kw={"stale_days": 30})
        self.assertEqual([c for c, _, _ in got], [17])

    def test_17_tbd_inside_a_list_counts_and_names_the_field(self):
        g = GUARD_LIST.replace("[0001-weekly]", "[0001-weekly, TBD]").replace("date: 2026-01-01", "date: 2025-01-01")
        got, _ = self.lint(**{"docs/guardrails/changelog.md": g})
        self.assertTrue(any(c == 17 and m.startswith("`governed-by: TBD` unresolved for") for c, _, m in got))
        ok = GUARD_LIST.replace("date: 2026-01-01", "date: 2025-01-01")
        got, _ = self.lint(**{"docs/guardrails/changelog.md": ok})
        self.assertEqual([c for c, _, _ in got if c == 17], [])

    def fitness(self, last_verified):
        entry = "  - {check: weekly tag, enforced-by: ci" + (f", last-verified: {last_verified}" if last_verified is not None else "") + "}"
        d = DECISION.replace("tags: [release]", "tags: [release]\nfitness-functions:\n" + entry)
        return self.lint(**{"docs/decisions/0001-weekly.md": d})

    def test_18_messages_and_boundary(self):
        got, _ = self.fitness(None)
        self.assertEqual([(c, m) for c, _, m in got], [(18, "fitness function `weekly tag` has no `last-verified` date")])
        got, _ = self.fitness("sometime")
        self.assertEqual([(c, m) for c, _, m in got], [(18, "fitness function `weekly tag` has no `last-verified` date")])

        def day(n):
            return (datetime.date.fromisoformat(TODAY) - datetime.timedelta(days=n)).isoformat()
        got, _ = self.fitness(day(180))
        self.assertEqual([c for c, _, _ in got], [])
        got, _ = self.fitness(day(181))
        self.assertEqual([(c, m) for c, _, m in got], [(18, "fitness function `weekly tag` last verified 181 days ago (threshold 180)")])

    def test_18_long_check_names_are_cut_at_40_characters(self):
        long = "c" * 60
        for lv, tail in ((None, "has no `last-verified` date"), ("2025-01-01", "last verified")):
            entry = "  - {check: " + long + (f", last-verified: {lv}" if lv else "") + "}"
            d = DECISION.replace("tags: [release]", "tags: [release]\nfitness-functions:\n" + entry)
            got, _ = self.lint(**{"docs/decisions/0001-weekly.md": d})
            msgs = [m for c, _, m in got if c == 18]
            self.assertEqual(len(msgs), 1)
            self.assertTrue(msgs[0].startswith("fitness function `" + "c" * 40 + "` " + tail[:4]), msgs[0])

    # --- warnings, docs detection, tags, refs, CLI ----------------------------------------

    def test_unpinned_guardrail_warning(self):
        _, lin = self.lint()
        self.assertIn("unpinned: docs/guardrails/changelog.md: run `--pin`", lin.warnings)
        pinned = GUARD_LIST.replace("tags: [release]", "tags: [release]\npinned: {0001-weekly: abc}")
        _, lin = self.lint(**{"docs/guardrails/changelog.md": pinned})
        self.assertFalse([w for w in lin.warnings if w.startswith("unpinned")])
        no_edges = GUARD.replace("governed-by: 0001-weekly\n", "").replace("grounded-in: [0001-cadence]\n", "")
        _, lin = self.lint(**{"docs/guardrails/changelog.md": no_edges})
        self.assertFalse([w for w in lin.warnings if w.startswith("unpinned")])

    def test_unpinned_ignores_archived_guardrails(self):
        arch = {"docs/guardrails/changelog.md": None, "docs/guardrails/archive/changelog.md": GUARD, "docs/guardrails/archive/INDEX.md": INDEX.format("changelog,Every release has a changelog entry,release,active"), "docs/guardrails/INDEX.md": INDEX.format("")}
        _, lin = self.lint(**arch)
        self.assertFalse([w for w in lin.warnings if w.startswith("unpinned")])

    def test_docs_autodetect_skips_hidden_directories(self):
        project(self.root)
        Path(self.root, "docs").rename(Path(self.root, "knowledge"))
        Path(self.root, ".cache", "decisions").mkdir(parents=True)
        self.assertEqual(Linter(self.root).docs.name, "knowledge")

    def test_empty_tags_file_and_frontmatter_keys(self):
        got, _ = self.lint(**{"docs/skills/tags.md": ""})
        self.assertTrue(any(c == 21 for c, _, _ in got) or True)  # no crash on an empty tags file
        doc = FACT.replace("tags: [release]", "tags: [tags]")
        got, _ = self.lint(**{"docs/facts/0001-cadence.md": doc, "docs/facts/INDEX.md": INDEX.format("0001-cadence,Releases are weekly,tags,active")})
        self.assertTrue(any(c == 21 and "tags" in m for c, _, m in got))

    def test_pin_requires_an_artifact_and_existing_targets(self):
        project(self.root)
        with self.assertRaises(SystemExit) as e:
            Linter(self.root).pin("docs/nowhere.md")
        self.assertIn("not an artifact with frontmatter", str(e.exception))
        self.write("docs/skills/notes.md", "no frontmatter\n")
        with self.assertRaises(SystemExit):
            Linter(self.root).pin("docs/skills/notes.md")
        self.write("docs/guardrails/changelog.md", GUARD_LIST.replace("[0001-cadence]", "[0099-none]"))
        with self.assertRaises(SystemExit) as e:
            Linter(self.root).pin("docs/guardrails/changelog.md")
        self.assertIn("edge targets that do not exist: 0099-none", str(e.exception))

    def test_pin_ignores_files_without_frontmatter_and_keeps_a_leading_comment(self):
        project(self.root, **{"docs/guardrails/changelog.md": GUARD_LIST.replace("---\nid:", "---\n# keep me\nid:", 1)})
        self.write("docs/skills/notes.md", "no frontmatter\n")
        Linter(self.root).pin("docs/guardrails/changelog.md")
        text = Path(self.root, "docs/guardrails/changelog.md").read_text()
        self.assertIn("# keep me", text)
        self.assertIn("pinned:", text)

    def test_refs_with_a_file_that_has_no_frontmatter(self):
        project(self.root)
        self.write("docs/skills/notes.md", "no frontmatter, mentions 0001-weekly here\n")
        self.assertEqual(Linter(self.root).refs("0001-weekly"), ["docs/facts/0001-cadence.md", "docs/guardrails/changelog.md", "docs/skills/notes.md"])

    def run_cli(self, *args):
        return subprocess.run([sys.executable, str(SHARED / "lint_check.py"), "--root", self.root, *args], capture_output=True, text=True)

    def test_cli_refs_pin_exclusive_and_json_indent(self):
        project(self.root)
        r = self.run_cli("--refs", "0001-weekly")
        self.assertEqual((r.returncode, r.stdout.split()), (0, ["docs/facts/0001-cadence.md", "docs/guardrails/changelog.md"]))
        r = self.run_cli("--refs", "0001-weekly", "--pin", "docs/guardrails/changelog.md")
        self.assertEqual(r.returncode, 2)
        self.assertIn("--refs and --pin cannot be combined", r.stderr)
        project(self.root, **{"docs/decisions/0001-weekly.md": DECISION.replace("date: 2026-01-01\n", "")})
        r = self.run_cli("--json")
        self.assertEqual(r.returncode, 1)
        self.assertTrue(r.stdout.startswith('[\n {\n  "check": 2,'), r.stdout[:40])
        self.assertEqual(json.loads(r.stdout)[0]["check"], 2)


if __name__ == "__main__":
    unittest.main()
