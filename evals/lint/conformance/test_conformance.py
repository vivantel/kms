"""Conformance: run the checker's CLI over every case in cases/ and compare (check, file) pairs with
the case's expected.json. A vendored copy of lint_check.py is tested by pointing CHECKER at it:
CHECKER=path/to/lint_check.py python3 -m unittest discover evals/lint/conformance"""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = os.environ.get("CHECKER") or str(HERE.parents[2] / "plugins" / "kms" / "shared" / "lint_check.py")


class Conformance(unittest.TestCase):
    def test_cases(self):
        names = sorted(p.name[: -len(".expected.json")] for p in (HERE / "cases").glob("*.expected.json"))
        self.assertTrue(names)
        for name in names:
            with self.subTest(case=name):
                exp = json.loads((HERE / "cases" / f"{name}.expected.json").read_text())
                r = subprocess.run([sys.executable, CHECKER, "--root", str(HERE / "cases" / name), "--json", "--today", "2026-11-08", *exp["args"]],
                                   capture_output=True, text=True)
                got = sorted({(x["check"], x["file"]) for x in json.loads(r.stdout)})
                self.assertEqual(got, sorted({(x["check"], x["file"]) for x in exp["findings"]}))
                self.assertEqual(r.returncode, 1 if exp["findings"] else 0)

    def test_generator_is_current(self):
        r = subprocess.run([sys.executable, str(HERE / "build.py"), "--check"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_one_case_per_rule(self):
        rules = {1, 2, 3, 4, 7, 9, 12, 13, 17, 18, 19, 20, 21, 24}
        covered = {x["check"] for p in (HERE / "cases").glob("*.expected.json") for x in json.loads(p.read_text())["findings"]}
        self.assertEqual(rules - covered, set())


if __name__ == "__main__":
    unittest.main()
