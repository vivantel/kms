#!/usr/bin/env python3
"""Score a lint-matrix run: per-check precision, recall and run-to-run variance.

Usage: score.py promptfoo-output.json [labels.json]

Reads the promptfoo JSON from `eval -o`, takes each result's case name (`description`) and the
last `LINT_FINDINGS:` line of its output, and compares the reported check numbers with
labels.json. A run with no such line (timeout, model stopped early) is `invalid`: it counts
against the valid-run rate and is left out of precision and recall.

Precision for check c = reported-and-expected / reported. Recall = reported-and-expected /
expected. Variance = mean, over the cases where c is expected or was reported at least once, of
the sample variance of the 0/1 "c was reported" indicator across repeats. The clean control's
false-alarm rate is the share of valid clean runs that reported anything.
"""

import json
import re
import sys
from pathlib import Path

LINE = re.compile(r"LINT_FINDINGS:[ \t]*([^\n]*)")


def parse(output):
    """Return the set of reported checks, or None when the run gave no usable answer."""
    hits = LINE.findall(output or "")
    if not hits:
        return None
    last = hits[-1].strip().strip("`").strip()
    if re.fullmatch(r"NONE\.?", last, re.I):
        return set()
    last = last.rstrip(".")
    if not re.fullmatch(r"\d{1,2}(\s*,\s*\d{1,2})*", last):
        return None  # echoed the template or free text
    return {int(x) for x in re.findall(r"\d+", last)}


def variance(xs):
    n = len(xs)
    if n < 2:
        return 0.0
    m = sum(xs) / n
    return sum((x - m) ** 2 for x in xs) / (n - 1)


def score(runs, labels):
    """runs: list of (case, reported set or None). Returns a report dict."""
    structural, judgment = labels["structural"], labels["judgment"]
    cases = labels["cases"]
    valid = [(c, r) for c, r in runs if r is not None]
    n_invalid = len(runs) - len(valid)
    pinned = [(c, r) for c, r in valid if cases[c].get("variant") == "pinned"]
    valid = [(c, r) for c, r in valid if cases[c].get("variant") != "pinned"]
    report = {"runs": len(runs), "invalid": n_invalid, "checks": {}}
    clean = [r for c, r in valid if cases[c]["target"] is None]
    report["clean_false_alarm_rate"] = (sum(1 for r in clean if r) / len(clean)) if clean else None
    for chk in structural + judgment:
        tp = fp = fn = 0
        cells = {}
        for case, reported in valid:
            exp = chk in cases[case]["expected"]
            got = chk in reported
            tp += exp and got
            fp += got and not exp
            fn += exp and not got
            cells.setdefault(case, []).append(int(got))
        vs = [variance(v) for case, v in cells.items() if chk in cases[case]["expected"] or any(v)]
        report["checks"][chk] = {
            "kind": "structural" if chk in structural else "judgment",
            "precision": tp / (tp + fp) if tp + fp else None,
            "recall": tp / (tp + fn) if tp + fn else None,
            "variance": sum(vs) / len(vs) if vs else 0.0,
            "tp": tp, "fp": fp, "fn": fn,
        }
    changed = [r for c, r in pinned if cases[c]["target"] == 13]
    control = [r for c, r in pinned if cases[c]["target"] is None]
    report["pinned_13"] = {  # check 13 where the edge carries a pin; the source changed, or did not
        "recall": (sum(13 in r for r in changed) / len(changed)) if changed else None,
        "false_alarm_rate": (sum(13 in r for r in control) / len(control)) if control else None,
        "runs": len(pinned),
    }
    return report


def load_runs(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    results = data.get("results", data)
    results = results.get("results", results) if isinstance(results, dict) else results
    runs = []
    for r in results:
        case = r.get("description") or (r.get("testCase") or {}).get("description")
        out = (r.get("response") or {}).get("output", r.get("output"))
        runs.append((case, parse(out if isinstance(out, str) else json.dumps(out))))
    return runs


def fmt(x):
    return "  - " if x is None else f"{x:.2f}"


def main():
    here = Path(__file__).resolve().parent
    labels = json.loads(Path(sys.argv[2] if len(sys.argv) > 2 else here / "labels.json").read_text(encoding="utf-8"))
    rep = score(load_runs(sys.argv[1]), labels)
    print(f"runs {rep['runs']}, invalid {rep['invalid']}, clean-control false-alarm rate {fmt(rep['clean_false_alarm_rate'])}")
    p = rep["pinned_13"]
    print(f"pinned check 13 ({p['runs']} runs): recall {fmt(p['recall'])}, false-alarm rate {fmt(p['false_alarm_rate'])}")
    for kind in ("structural", "judgment"):
        print(f"\n{kind} checks\ncheck  precision  recall  variance   tp  fp  fn")
        for chk, s in rep["checks"].items():
            if s["kind"] == kind:
                print(f"{chk:>5}  {fmt(s['precision']):>9}  {fmt(s['recall']):>6}  {s['variance']:>8.2f}  {s['tp']:>3} {s['fp']:>3} {s['fn']:>3}")
    return rep


if __name__ == "__main__":
    main()
