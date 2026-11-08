#!/usr/bin/env python3
"""Score an admission run: precision and recall of "record", exact-class accuracy, per-group errors.

Usage: score.py promptfoo-output.json [cases.tsv]

Reads the promptfoo JSON from `eval -o`, takes each result's case id (`description`) and the last
`ADMISSION:` line of its output. A run with no such line is `invalid`: it counts against the valid
rate and is left out of the scores. "Record" means any class but none. Precision = recorded and
gold-record / recorded; recall = recorded and gold-record / gold-record; accuracy = the class equals
the gold class. Per group: the share of valid runs whose record/none call is wrong.
"""

import csv
import json
import re
import sys
from pathlib import Path

CLASSES = ("none", "fact", "decision", "guardrail", "procedure")
LINE = re.compile(r"ADMISSION:[ \t]*`?([A-Za-z]+)`?[ \t.]*$", re.M)


def parse(output):
    """Return the class named on the last ADMISSION line, or None when the run gave no usable answer."""
    hits = LINE.findall(output or "")
    if not hits:
        return None
    last = hits[-1].lower()
    return last if last in CLASSES else None


def load_gold(path):
    with open(path, encoding="utf-8", newline="") as f:
        return {r["id"]: r for r in csv.DictReader(f, delimiter="\t")}


def score(runs, gold):
    """runs: list of (case id, class or None). Returns a report dict."""
    valid = [(c, r) for c, r in runs if r is not None]
    tp = fp = fn = exact = 0
    groups = {}
    for case, got in valid:
        want = gold[case]["gold"]
        rec, rec_gold = got != "none", want != "none"
        tp += rec and rec_gold
        fp += rec and not rec_gold
        fn += rec_gold and not rec
        exact += got == want
        g = groups.setdefault(gold[case]["group"], [0, 0])
        g[0] += 1
        g[1] += rec != rec_gold
    return {
        "runs": len(runs), "invalid": len(runs) - len(valid),
        "precision": tp / (tp + fp) if tp + fp else None,
        "recall": tp / (tp + fn) if tp + fn else None,
        "accuracy": exact / len(valid) if valid else None,
        "groups": {k: {"runs": n, "wrong": w, "error_rate": w / n} for k, (n, w) in sorted(groups.items())},
        "tp": tp, "fp": fp, "fn": fn,
    }


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
    gold = load_gold(sys.argv[2] if len(sys.argv) > 2 else here / "cases.tsv")
    rep = score(load_runs(sys.argv[1]), gold)
    print(f"runs {rep['runs']}, invalid {rep['invalid']}, precision {fmt(rep['precision'])}, recall {fmt(rep['recall'])}, accuracy {fmt(rep['accuracy'])}")
    print("\ngroup        runs  wrong  error rate")
    for g, s in rep["groups"].items():
        print(f"{g:<12} {s['runs']:>4} {s['wrong']:>6}  {s['error_rate']:>9.2f}")
    return rep


if __name__ == "__main__":
    main()
