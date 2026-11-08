"""Unit cases for the lint matrix: the committed fixtures match the generator, the checker agrees
with the labels, and the scorer rejects a model that answers YES to everything or NO to
everything. Run: python3 -m unittest discover evals/lint-matrix"""

import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402
import score  # noqa: E402

LABELS = json.loads((HERE / "labels.json").read_text(encoding="utf-8"))
ALL = set(LABELS["structural"] + LABELS["judgment"])
PINNED = sorted(c for c, v in LABELS["cases"].items() if v.get("variant") == "pinned")


def runs(answer, repeats=3):
    return [(c, answer(c)) for c in LABELS["cases"] for _ in range(repeats)]


class Matrix(unittest.TestCase):
    def test_committed_files_match_generator(self):
        on_disk = {str(p.relative_to(HERE)): p.read_text(encoding="utf-8") for p in (HERE / "cases").rglob("*") if p.is_file()}
        built = {k: v for k, v in build.build().items() if k.startswith("cases/")}
        self.assertEqual(on_disk, built)

    def test_one_case_per_check_plus_clean(self):
        self.assertEqual(sorted(LABELS["cases"]), sorted(["clean"] + [f"c{n:02d}" for n in sorted(ALL)] + PINNED))
        self.assertEqual(ALL, set(range(1, 25)))

    def test_oracle_scores_perfectly(self):
        rep = score.score(runs(lambda c: set(LABELS["cases"][c]["expected"])), LABELS)
        self.assertEqual(rep["clean_false_alarm_rate"], 0)
        for chk, s in rep["checks"].items():
            self.assertEqual((s["precision"], s["recall"], s["variance"]), (1.0, 1.0, 0.0), chk)

    def test_yes_to_everything_fails_clean_control(self):
        rep = score.score(runs(lambda c: set(ALL)), LABELS)
        self.assertEqual(rep["clean_false_alarm_rate"], 1.0)
        for s in rep["checks"].values():
            self.assertEqual(s["recall"], 1.0)
            self.assertLess(s["precision"], 0.1)

    def test_no_to_everything_has_no_recall(self):
        rep = score.score(runs(lambda c: set()), LABELS)
        self.assertEqual(rep["clean_false_alarm_rate"], 0)
        self.assertTrue(all(s["recall"] == 0 for s in rep["checks"].values()))

    def test_pinned_cases(self):
        self.assertEqual(PINNED, ["p13-changed", "p13-control"])
        oracle = score.score(runs(lambda c: set(LABELS["cases"][c]["expected"])), LABELS)
        self.assertEqual(oracle["pinned_13"], {"recall": 1.0, "false_alarm_rate": 0.0, "runs": 6})
        yes = score.score(runs(lambda c: set(ALL)), LABELS)
        self.assertEqual((yes["pinned_13"]["recall"], yes["pinned_13"]["false_alarm_rate"]), (1.0, 1.0))
        no = score.score(runs(lambda c: set()), LABELS)
        self.assertEqual(no["pinned_13"]["recall"], 0.0)
        # pinned runs do not leak into the unpinned check-13 row or the clean control
        self.assertEqual(oracle["checks"][13]["tp"], 3)
        self.assertEqual(yes["clean_false_alarm_rate"], 1.0)

    def test_variance_and_invalid(self):
        rs = [("c05", {5}), ("c05", set()), ("c05", None)]
        rep = score.score(rs, LABELS)
        self.assertEqual(rep["invalid"], 1)
        self.assertEqual(rep["checks"][5]["variance"], 0.5)

    def test_parse(self):
        self.assertEqual(score.parse("x\nLINT_FINDINGS: 1, 7"), {1, 7})
        self.assertEqual(score.parse("LINT_FINDINGS: NONE"), set())
        self.assertEqual(score.parse("LINT_FINDINGS: 1\nmore\nLINT_FINDINGS: 2."), {2})
        self.assertIsNone(score.parse("LINT_FINDINGS: 1|2"))
        self.assertIsNone(score.parse("no answer"))


if __name__ == "__main__":
    unittest.main()
