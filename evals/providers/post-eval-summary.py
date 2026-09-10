#!/usr/bin/env python3
"""Post one PR comment summarizing every eval case's result, instead of one comment per case.

Running 5 cases in a matrix used to post 5 separate comments — GitHub notifies once per
comment, so a single workflow run generated 5 near-identical notifications, one per case,
readable only by opening each. This reads every exported eval-result-<case>.json in a
directory and posts a single comment with one row per case, plus a collapsed detail section
per *failed* case — the actual prompt, the actual model output, and which assertion(s) failed
and why — so "what was tested against what" is answerable from the PR itself, without opening
promptfoo.app or the Actions log.

Usage: post-eval-summary.py <results-dir> <pr-number> <run-url>
Reads GH_TOKEN from the environment (same as `gh`).

Link construction: `promptfoo export eval latest` never persists the `shareableUrl` promptfoo
prints when --share succeeds (confirmed by inspecting the exported JSON — the field exists in
the schema but is always null) — the real link is https://www.promptfoo.app/eval/<evalId>,
built from `evalId`, which *is* persisted. Only valid if sharing actually ran (PROMPTFOO_API_KEY
set); falls back to the workflow run link otherwise, since a constructed link would 404 without
a share.
"""
import glob
import json
import os
import re
import subprocess
import sys

results_dir, pr_number, run_url = sys.argv[1:4]


def truncate(text, limit, head=False):
    text = "" if text is None else str(text)
    if len(text) <= limit:
        return text
    return text[:limit] + "…" if head else "…" + text[-limit:]


rows = []
details = []
for path in sorted(glob.glob(os.path.join(results_dir, "eval-result-*.json"))):
    m = re.search(r"eval-result-(.+)\.json$", os.path.basename(path))
    case = m.group(1) if m else os.path.basename(path)
    try:
        with open(path) as f:
            data = json.load(f)
        stats = data["results"]["stats"]
        passed, failed = stats["successes"], stats["failures"]
        eval_id = data.get("evalId")
        shared = bool(os.environ.get("PROMPTFOO_API_KEY"))
        link = f"https://www.promptfoo.app/eval/{eval_id}" if (shared and eval_id) else run_url
        icon = "✅" if failed == 0 else "❌"
        rows.append((case, icon, f"{passed} passed / {failed} failed", link))

        if failed:
            for result in data["results"]["results"]:
                if result.get("success"):
                    continue
                prompt = result.get("prompt", {}).get("raw", "")
                output = result.get("response", {}).get("output", "")
                grading = result.get("gradingResult") or {}
                failed_assertions = [
                    c for c in grading.get("componentResults", []) if not c.get("pass")
                ] or [grading]  # a bare regex/contains failure has no componentResults list

                block = [f"<details>\n<summary>❌ <code>{case}</code> — what was tested</summary>\n"]
                block.append("**Invocation prompt:**\n```\n" + truncate(prompt, 800, head=True) + "\n```\n")
                for c in failed_assertions:
                    assertion = c.get("assertion") or {}
                    a_type = assertion.get("type", "?")
                    a_value = truncate(assertion.get("value", ""), 400, head=True)
                    reason = truncate(c.get("reason", ""), 600, head=True)
                    block.append(f"**Failed assertion** (`{a_type}`):\n```\n{a_value}\n```\n**Why:**\n> {reason}\n")
                block.append("**Actual output** (end of transcript):\n```\n" + truncate(output, 1500) + "\n```\n")
                block.append("</details>")
                details.append("\n".join(block))
    except Exception as e:
        rows.append((case, "⚠️", f"result unavailable: {e}", run_url))

if not rows:
    print("post-eval-summary: no eval-result-*.json files found", file=sys.stderr)
    sys.exit(0)

lines = ["| Case | Result | Details |", "|---|---|---|"]
for case, icon, counts, link in rows:
    lines.append(f"| `{case}` | {icon} {counts} | [view]({link}) |")
body = "**Eval results**\n\n" + "\n".join(lines)
if details:
    body += "\n\n" + "\n\n".join(details)
body += f"\n\n[Full run]({run_url})"

subprocess.run(["gh", "pr", "comment", str(pr_number), "--body", body], check=False)
