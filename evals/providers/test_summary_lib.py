import os, sys, unittest
sys.path.insert(0, os.path.dirname(__file__))
import re
from summary_lib import is_infra, split_failures, advisory_cases, harness_reason


class T(unittest.TestCase):
    def test_marker_in_output(self):
        self.assertTrue(is_infra({"success": False, "response": {"output": "=== HARNESS ERROR: Model not found: x ==="}}))

    def test_marker_in_error(self):
        self.assertTrue(is_infra({"success": False, "error": "Error: === HARNESS ERROR: kilo unavailable ==="}))

    def test_plain_failure_is_skill(self):
        self.assertFalse(is_infra({"success": False, "response": {"output": "no trailer"}}))

    def test_split(self):
        rs = [{"success": True}, {"success": False, "response": {"output": "=== HARNESS ERROR: x"}}, {"success": False, "response": {"output": "x"}}]
        skill, infra = split_failures(rs)
        self.assertEqual((len(skill), len(infra)), (1, 1))


    def test_start_up_collision_is_infra(self):
        self.assertEqual(harness_reason("x\nFailed query: CREATE TABLE workspace (id)\n"), "kilo start-up collision")
        self.assertEqual(harness_reason("Error: Unexpected error\n"), "kilo start-up collision")

    def test_ordinary_answer_is_not(self):
        self.assertEqual(harness_reason("An unexpected error is handled in foo.py; CREATE TABLE users"), "")

    def test_workflow_lists_equal_the_file(self):
        root = os.path.join(os.path.dirname(__file__), "..", "..")
        want = advisory_cases(os.path.join(root, "evals", "advisory-cases.txt"))
        wf = open(os.path.join(root, ".github", "workflows", "eval-skills.yml")).read()
        lists = re.findall(r"fromJSON\('(\[[^']*\])'\), matrix\.case", wf)
        self.assertEqual(len(lists), 2)
        import json
        for l in lists:
            self.assertEqual(set(json.loads(l)), want)


if __name__ == "__main__":
    unittest.main()
