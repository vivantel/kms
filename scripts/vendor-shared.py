#!/usr/bin/env python3
"""Copy plugins/kms/shared/ and plugins/kms/templates/ files into the skill directories that read them.

Why: a Kilo remote-skills install caches only the files each skill's `files` list names, inside that
skill's own directory (a `..` entry drops the skill), so a sibling `shared/` never arrives. The
skills therefore read `shared/<file>` and `templates/<type>/<file>` relative to their own directory,
which is the same path on every agent. `plugins/kms/shared/` and `plugins/kms/templates/` stay the
source of truth; the unit test `evals/lint/unit/test_vendored.py` fails when a copy drifts.

Usage: python3 scripts/vendor-shared.py [--check]   (default: write the copies and index.json files)
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "plugins" / "kms"
MODEL = ["artifact-model.md"]
WRITE = ["artifact-model.md", "admission.md"]
NEEDS = {  # skill -> (shared files, whether it reads templates/)
    "bootstrap": (WRITE, True),
    "capture": (WRITE, False),
    "decide": (WRITE, False),
    "lint": (MODEL + ["lint_check.py"], True),
    "roadmap": (WRITE, False),
    "uninstall": ([], True),
}


def wanted():
    out = {}
    for skill, (shared, templates) in NEEDS.items():
        for f in shared:
            out[Path("skills", skill, "shared", f)] = ROOT / "shared" / f
        if templates:
            for t in sorted((ROOT / "templates").rglob("*")):
                if t.is_file():
                    out[Path("skills", skill, "templates", t.relative_to(ROOT / "templates"))] = t
    return out


def main():
    check = "--check" in sys.argv
    bad = []
    for dest, src in wanted().items():
        d = ROOT / dest
        if check:
            if not d.is_file() or d.read_bytes() != src.read_bytes():
                bad.append(str(dest))
        else:
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, d)
    idx_path = ROOT / "skills" / "index.json"
    idx = json.loads(idx_path.read_text())
    for entry in idx["skills"]:
        extra = sorted(str(p.relative_to(Path("skills", entry["name"]))) for p in wanted() if p.parts[1] == entry["name"])
        files = ["SKILL.md", "examples.md"] + extra
        if check:
            if entry["files"] != files:
                bad.append(f"index.json {entry['name']}")
        else:
            entry["files"] = files
    if check:
        if bad:
            print("out of date:", ", ".join(bad))
            sys.exit(1)
    else:
        idx_path.write_text(json.dumps(idx, indent=2) + "\n")


if __name__ == "__main__":
    main()
