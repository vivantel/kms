#!/usr/bin/env python3
"""Post a per-case PR comment naming which eval case it's about.

promptfoo-action's own built-in PR comment (docs/decisions/0043-eval-harness-for-shipped-skill-changes.md's
amendment) never names which matrix case it's reporting on — running 5 cases in a matrix posts
5 byte-for-byte-identical comments, making it impossible to tell from the PR which one is which
without opening each. Disabled via `disable-comment: true` in .github/workflows/eval-skills.yml;
this script replaces it with one clearly-labeled comment per case.

Usage: post-eval-comment.py <case> <result-json-path> <pr-number> <run-url>
Reads GH_TOKEN from the environment (same as `gh`).
"""
import json
import subprocess
import sys

case, result_path, pr_number, run_url = sys.argv[1:5]

try:
    with open(result_path) as f:
        data = json.load(f)
    stats = data["results"]["stats"]
    passed = stats["successes"]
    failed = stats["failures"]
    url = data.get("shareableUrl")
except Exception as e:
    passed = failed = None
    url = None
    print(f"post-eval-comment: couldn't read {result_path}: {e}", file=sys.stderr)

if failed is None:
    icon = "⚠️"
    counts = "result unavailable — check the run log"
else:
    icon = "✅" if failed == 0 else "❌"
    counts = f"{passed} passed / {failed} failed"

body = f"**eval ({case})** — {icon} {counts}\n\n"
body += f"[View eval results]({url})" if url else f"[View this run]({run_url})"

subprocess.run(["gh", "pr", "comment", str(pr_number), "--body", body], check=False)
