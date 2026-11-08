"""Unit cases for the admission eval: the committed config matches the generator, and the scorer
fails a model that records everything (trivial group) or nothing (recall 0). Run:
python3 -m unittest discover evals/admission"""

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import build  # noqa: E402
import score  # noqa: E402

GOLD = score.load_gold(HERE / "cases.tsv")


def runs(answer, repeats=3):
    return [(c, answer(c)) for c in GOLD for _ in range(repeats)]


class Admission(unittest.TestCase):
    def test_committed_config_matches_generator(self):
        self.assertEqual((HERE / "promptfooconfig.yaml").read_text(encoding="utf-8"), build.build())

    def test_cases(self):
        self.assertEqual(len(GOLD), 66)
        self.assertEqual({g["group"] for g in GOLD.values()},
                         {"trivial", "significant", "transient", "pointer", "gcontrol", "decoy", "incode"})
        self.assertTrue(all(g["gold"] in score.CLASSES for g in GOLD.values()))

    def test_oracle_scores_perfectly(self):
        rep = score.score(runs(lambda c: GOLD[c]["gold"]), GOLD)
        self.assertEqual((rep["precision"], rep["recall"], rep["accuracy"]), (1.0, 1.0, 1.0))
        self.assertTrue(all(g["error_rate"] == 0 for g in rep["groups"].values()))

    def test_always_record_fails_trivial_group(self):
        rep = score.score(runs(lambda c: "decision"), GOLD)
        self.assertEqual(rep["recall"], 1.0)
        self.assertEqual(rep["groups"]["trivial"]["error_rate"], 1.0)
        self.assertLess(rep["precision"], 0.5)

    def test_never_record_has_no_recall(self):
        rep = score.score(runs(lambda c: "none"), GOLD)
        self.assertEqual(rep["recall"], 0.0)
        self.assertEqual(rep["groups"]["trivial"]["error_rate"], 0.0)

    def test_parse_and_invalid(self):
        self.assertEqual(score.parse("x\nADMISSION: decision"), "decision")
        self.assertEqual(score.parse("ADMISSION: fact\nADMISSION: `none`."), "none")
        self.assertIsNone(score.parse("ADMISSION: fact|decision"))
        self.assertIsNone(score.parse("no answer"))
        rep = score.score([("c01", "none"), ("c01", None)], GOLD)
        self.assertEqual(rep["invalid"], 1)


if __name__ == "__main__":
    unittest.main()
