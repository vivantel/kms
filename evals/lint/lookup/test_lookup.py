import json
import pathlib
import unittest

HERE = pathlib.Path(__file__).parent


class LookupFixtures(unittest.TestCase):
    def test_expected_ids_exist_in_corpus(self):
        ids = {p.stem for p in (HERE / "corpus" / "docs").rglob("*.md") if p.name != "INDEX.md"}
        queries = json.loads((HERE / "queries.json").read_text())
        self.assertEqual(len({q["name"] for q in queries}), len(queries))
        for q in queries:
            for i in q["ids"]:
                self.assertIn(i, ids, q["name"])


if __name__ == "__main__":
    unittest.main()
