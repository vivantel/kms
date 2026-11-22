#!/usr/bin/env python3
"""Migrate a knowledge directory from the 0.16 artifact shapes to the 1.0 schema (artifact-model.md).

Usage: migrate.py --docs DIR [--dry-run]

Mechanical edits only, idempotent: a second run changes nothing. All files are computed before any is
written, line endings are kept, and a fitness function that was a bare string becomes `{check: ...}` with no
`last-verified` (it was never verified; check 18 asks for a date, and a note lists each one).
  facts       drop `kind` and `governed-by`
  guardrails  scalar `governed-by` becomes a one-element list; `grounded-in` keeps fact ids only
              (removed ids are printed for re-derivation); `grounded-in: TBD` is dropped; a
              seeded provenance `derivation-note` becomes `TBD`
  decisions   drop `track`; a non-date `expires` moves to `expires-when`; string `fitness-functions` entries
              become `{check: ...}` maps
  registries  INDEX.md gets a first-line `kms-registry` comment; tags.md and docs-manifest.md get
              a `kms-registry` frontmatter field, and their rows leave the sibling INDEX.md
  --rename    also renames the type directory `skills/` to `procedures/` (refused when both exist) and rewrites
              `<dir>/skills/` path mentions inside the knowledge directory; without it nothing is renamed
Requires PyYAML.
"""

import argparse
import datetime
import json
import re
import sys
from pathlib import Path

import yaml

TYPES = ("facts", "decisions", "guardrails", "skills", "procedures")
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


def load(lines):
    """Parsed frontmatter mapping, or None when it does not parse (YAMLError, or ValueError for a calendar-invalid date) or is not a mapping."""
    try:
        data = yaml.safe_load("\n".join(lines)) or {}
    except (yaml.YAMLError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def value(block):
    return (load(block[1]) or {}).get(block[0])


def flow(items):
    """A YAML flow list; plain ids stay unquoted so an already migrated corpus is a fixed point."""
    return "[" + ", ".join(str(x) if re.fullmatch(r"[A-Za-z0-9][\w.\-]*", str(x)) else json.dumps(str(x), ensure_ascii=False) for x in items) + "]"


def jsonable(o):
    return o.isoformat() if isinstance(o, (datetime.date, datetime.datetime)) else str(o)


def read(p):
    return p.read_bytes().decode("utf-8")


def write(p, text):
    p.write_bytes(text.encode("utf-8"))


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
                parts = split(read(p).replace("\r\n", "\n"))
                if parts:
                    fm = load(parts[0]) or {}  # unparseable frontmatter: reported by lint_check, left alone here
                    ids[str(fm.get("id", p.stem))] = t
    return ids


def migrate_file(path, typ, ids, notes):
    raw = read(path)
    crlf = "\r\n" in raw
    text = raw.replace("\r\n", "\n")
    parts = split(text)
    if not parts:
        return raw
    head, tail = parts
    if load(head) is None:
        notes.append(f"{path.name}: unparseable frontmatter or not a mapping, skipped")
        return raw
    bl = blocks(head)
    has_when = any(k == "expires-when" for k, _ in bl)
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
            if v is not None and not isinstance(v, list):
                b = [key, [f"governed-by: {flow([v])}"]]
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
            b = [key, [f"grounded-in: {flow(facts)}"]]
        if typ == "guardrails" and key == "derivation-note":
            if "Seeded from kms's shipped guardrail templates" in " ".join(" ".join(lines).split()):
                b = [key, ["derivation-note: TBD"]]
        if key == "expires":
            v = value(b)
            if v is None:
                continue  # an empty `expires:` says nothing
            if not is_date(v):
                if not has_when:
                    keep.append(["expires-when", [f"expires-when: {json.dumps(str(v), ensure_ascii=False)}"]])
                continue
        if key == "fitness-functions":
            v = value(b)
            if isinstance(v, list) and any(not isinstance(e, dict) for e in v):
                out = ["fitness-functions:"]
                for e in v:
                    if isinstance(e, dict):
                        out.append("  - " + json.dumps(e, ensure_ascii=False, default=jsonable))
                    else:
                        out.append("  - check: " + json.dumps(str(e), ensure_ascii=False))
                        notes.append(f"{path.name}: fitness function `{str(e)[:40]}` has no `last-verified`: verify it and add the date")
                b = [key, out]
        keep.append(b)
    new = "\n".join(["---"] + [l for _, ls in keep for l in ls] + tail)
    return new.replace("\n", "\r\n") if crlf else new


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", required=True, metavar="DIR")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--rename", action="store_true")
    args = ap.parse_args()
    docs = Path(args.docs)
    renamed = False
    if args.rename and (docs / "skills").is_dir():
        if (docs / "procedures").exists():
            sys.exit("both skills/ and procedures/ exist under " + str(docs) + ": merge them by hand, then re-run")
        renamed = True
        if not args.dry_run:
            (docs / "skills").rename(docs / "procedures")
    ids = kinds_by_id(docs)
    notes, pending = [], []
    for t in TYPES:
        if renamed and args.dry_run and t == "procedures":
            continue
        for d in (docs / t, docs / t / "archive"):
            if not d.is_dir():
                continue
            for p in sorted(d.glob("*.md")):
                text = read(p)
                if p.name == "INDEX.md":
                    new = text if text.startswith("<!-- kms-registry:") else "<!-- kms-registry: index -->\n" + text
                    for name in REGISTRY_FILES:  # a registry is not an artifact: its row leaves the index
                        if (d / name).exists():
                            new = re.sub(rf"^{re.escape(name[:-3])},[^\n]*\r?\n?", "", new, flags=re.M)
                elif p.name in REGISTRY_FILES:
                    parts = split(text.replace("\r\n", "\n"))
                    new = text
                    if parts and "kms-registry" not in "\n".join(parts[0]):
                        new = "\n".join(["---"] + parts[0] + [f"kms-registry: {REGISTRY_FILES[p.name]}"] + parts[1])
                        new = new.replace("\n", "\r\n") if "\r\n" in text else new
                else:
                    new = migrate_file(p, t, ids, notes)
                if new != text:
                    pending.append((p, new))
    if renamed:  # path mentions follow the directory: `<name>/skills/` becomes `<name>/procedures/`
        pat = re.compile(rf"(?<![\w\-])({re.escape(docs.name)}/)skills/")
        for p in sorted(docs.rglob("*.md")):
            cur = dict(pending).get(p) or read(p)
            new = pat.sub(r"\1procedures/", cur)
            if new != cur:
                pending = [(a, b) for a, b in pending if a != p] + [(p, new)]
    if not args.dry_run:
        for p, new in pending:
            write(p, new)
    changed = [str(p) for p, _ in pending]
    for n in notes:
        print("re-derive: " + n)
    print(f"{len(changed)} file(s) {'would change' if args.dry_run else 'changed'}", file=sys.stderr)


if __name__ == "__main__":
    main()
