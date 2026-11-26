"""Parse fixtures: run the checker's split_frontmatter over every case in cases/ and compare the parsed data and the error class with the
case's expected.json. A vendored copy of lint_check.py is tested by pointing CHECKER at it:
CHECKER=path/to/lint_check.py python3 -m unittest discover evals/lint/frontmatter"""

import datetime
import importlib.util
import json
import os
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = os.environ.get("CHECKER") or str(HERE.parents[2] / "plugins" / "kms" / "shared" / "lint_check.py")
_spec = importlib.util.spec_from_file_location("lint_check_under_test", CHECKER)
lc = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(lc)


def norm(v):
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.isoformat()
    if isinstance(v, dict):
        return {k: norm(x) for k, x in v.items()}
    if isinstance(v, list):
        return [norm(x) for x in v]
    return v


class FrontmatterParse(unittest.TestCase):
    def test_cases(self):
        names = sorted(p.name[: -len(".expected.json")] for p in (HERE / "cases").glob("*.expected.json"))
        self.assertTrue(names)
        for name in names:
            with self.subTest(case=name):
                exp = json.loads((HERE / "cases" / f"{name}.expected.json").read_text())
                data, err = lc.split_frontmatter(lc.read(HERE / "cases" / f"{name}.md"))
                self.assertEqual({"data": norm(data), "error": err.split(":")[0] if err else None}, exp)

    def test_every_case_has_both_files(self):
        md = {p.stem for p in (HERE / "cases").glob("*.md")}
        js = {p.name[: -len(".expected.json")] for p in (HERE / "cases").glob("*.expected.json")}
        self.assertEqual(md, js)


if __name__ == "__main__":
    unittest.main()
