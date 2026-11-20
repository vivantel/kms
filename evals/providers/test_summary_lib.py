import os, sys, unittest
sys.path.insert(0, os.path.dirname(__file__))
from summary_lib import is_infra, split_failures


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


if __name__ == "__main__":
    unittest.main()
