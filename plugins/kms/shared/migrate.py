#!/usr/bin/env python3
"""Migrate a knowledge directory from the 0.16 artifact shapes to the 1.0 schema (artifact-model.md).

Usage: migrate.py --docs DIR [--dry-run]

Mechanical edits only, idempotent: a second run changes nothing.
  facts       drop `kind` and `governed-by`
  guardrails  scalar `governed-by` becomes a one-element list; `grounded-in` keeps fact ids only
              (removed ids are printed for re-derivation); `grounded-in: TBD` is dropped; a
              seeded provenance `derivation-note` becomes `TBD`
  decisions   drop `track`; a non-date `expires` moves to `expires-when`; string `fitness-functions` entries
              become `{check: ...}` maps
  registries  INDEX.md gets a first-line `kms-registry` comment; tags.md and docs-manifest.md get
              a `kms-registry` frontmatter field
Requires PyYAML.
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

import yaml

TYPES = ("facts", "decisions", "guardrails", "skills")
REGISTRY_FILES = {"tags.md": "tags", "docs-manifest.md": "docs-manifest"}


def split(text):
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i], lines[i:]
    return None


def blocks(head):
    """Top-level key blocks: list of [key, [lines]]; lines before the first key are kept under None."""
    out = []
    for line in head:
        m = re.match(r"^([\w\-]+):", line)
        if m:
            out.append([m.group(1), [line]])
        elif out:
            out[-1][1].append(line)
        else:
            out.append([None, [line]])
    return out


def value(block):
    return yaml.safe_load("\n".join(block[1])).get(block[0])


def is_date(v):
    if isinstance(v, (datetime.date, datetime.datetime)):
        return True
    try:
        datetime.date.fromisoformat(str(v))
        return True
    except ValueError:
        return False


def kinds_by_id(docs):
    ids = {}
    for t in TYPES:
        for d in (docs / t, docs / t / "archive"):
            for p in d.glob("*.md") if d.is_dir() else []:
                parts = split(p.read_text(encoding="utf-8"))
                if parts:
                    try:
                        fm = yaml.safe_load("\n".join(parts[0])) or {}
                    except yaml.YAMLError:
                        fm = {}  # unparseable frontmatter: reported by lint_check, left alone here
                    ids[str(fm.get("id", p.stem))] = t
    return ids


def migrate_file(path, typ, ids, notes):
    text = path.read_text(encoding="utf-8")
    parts = split(text)
    if not parts:
        return text
    head, tail = parts
    try:
        yaml.safe_load("\n".join(head))
    except yaml.YAMLError:
        notes.append(f"{path.name}: unparseable frontmatter, skipped")
        return text
    bl = blocks(head)
    keep = []
    for key, lines in bl:
        if key is None:
            keep.append([key, lines])
            continue
        b = [key, lines]
        if typ == "decisions" and key == "track":
            continue
        if typ == "facts" and key in ("kind", "governed-by"):
            continue
        if typ == "guardrails" and key == "governed-by":
            v = value(b)
            if not isinstance(v, list):
                b = [key, [f"governed-by: [{v}]"]]
        if typ == "guardrails" and key == "grounded-in":
            v = value(b)
            if v == "TBD":
                continue
            vals = v if isinstance(v, list) else [v]
            facts = [str(x) for x in vals if ids.get(str(x)) == "facts"]
            gone = [str(x) for x in vals if ids.get(str(x)) != "facts"]
            if gone:
                notes.append(f"{path.name}: grounded-in dropped {', '.join(gone)}: re-derive")
            if not facts:
                continue
            b = [key, ["grounded-in: [" + ", ".join(facts) + "]"]]
        if typ == "guardrails" and key == "derivation-note":
            if "Seeded from kms's shipped guardrail templates" in " ".join(" ".join(lines).split()):
                b = [key, ["derivation-note: TBD"]]
        if key == "expires":
            v = value(b)
            if not is_date(v):
                keep.append(["expires-when", [f"expires-when: {json.dumps(str(v))}"]])
                continue
        if key == "fitness-functions":
            v = value(b)
            if isinstance(v, list) and any(not isinstance(e, dict) for e in v):
                out = ["fitness-functions:"]
                for e in v:
                    out.append("  - check: " + json.dumps(e if not isinstance(e, dict) else e["check"], ensure_ascii=False)
                               if not isinstance(e, dict) else "  - " + json.dumps(e, ensure_ascii=False))
                b = [key, out]
        keep.append(b)
    new = "\n".join(["---"] + [l for _, ls in keep for l in ls] + tail)
    return new


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", required=True, metavar="DIR")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()
    docs = Path(args.docs)
    ids = kinds_by_id(docs)
    notes, changed = [], []
    for t in TYPES:
        for d in (docs / t, docs / t / "archive"):
            if not d.is_dir():
                continue
            for p in sorted(d.glob("*.md")):
                text = p.read_text(encoding="utf-8")
                if p.name == "INDEX.md":
                    new = text if text.startswith("<!-- kms-registry:") else "<!-- kms-registry: index -->\n" + text
                elif p.name in REGISTRY_FILES:
                    parts = split(text)
                    new = text
                    if parts and "kms-registry" not in "\n".join(parts[0]):
                        new = "\n".join(["---"] + parts[0] + [f"kms-registry: {REGISTRY_FILES[p.name]}"] + parts[1])
                else:
                    new = migrate_file(p, t, ids, notes)
                if new != text:
                    changed.append(str(p))
                    if not args.dry_run:
                        p.write_text(new, encoding="utf-8")
    for n in notes:
        print("re-derive: " + n)
    print(f"{len(changed)} file(s) {'would change' if args.dry_run else 'changed'}", file=sys.stderr)


if __name__ == "__main__":
    main()
