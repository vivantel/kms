#!/usr/bin/env python3
"""Deterministic structural checks for the `lint` skill.

Usage: lint_check.py [--root DIR] [--json]

Runs the lint checks that need only frontmatter, file names and file text: 1, 2, 3, 7, 9, 12,
15, 19, 20, 21 (numbers as in plugins/kms/skills/lint/SKILL.md). No model is involved; output is
sorted, so identical input gives identical output. Exit status 1 when anything is found.
Requires PyYAML.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import yaml

TYPES = ("facts", "decisions", "guardrails", "skills")
BASE_FIELDS = ("id", "title", "status", "date", "tags")
TYPE_FIELDS = {
    "facts": ("kind", "governed-by"),
    "guardrails": ("governed-by", "grounded-in", "derivation-note"),
    "decisions": ("track",),
}
STATUSES = ("draft", "active", "superseded", "deprecated")
REF_FIELDS = ("governed-by", "grounded-in", "superseded-by", "governed-facts", "operationalizes")
LIST_FIELDS = ("grounded-in", "governed-facts", "operationalizes")
PROSE_REF = re.compile(r"docs/(facts|decisions|guardrails|skills)/([\w.\-]+\.md)")
NUMBERED = re.compile(r"^(\d{4})-")


def split_frontmatter(text):
    """Return (dict or None, error or None); both are set for an unterminated block that still parses. Frontmatter is the block between a first line '---' and the next
    line that is exactly '---'."""
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        return None, "no frontmatter"
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            try:
                data = yaml.safe_load("\n".join(lines[1:i])) or {}
            except yaml.YAMLError as e:
                return None, "unparseable frontmatter: " + str(e).splitlines()[0]
            if not isinstance(data, dict):
                return None, "frontmatter is not a mapping"
            return data, None
    # No closing '---': read up to the first blank line or heading, so the file's other
    # violations are still checked, and report the missing delimiter.
    end = len(lines)
    for i in range(1, len(lines)):
        if not lines[i].strip() or lines[i].startswith("#"):
            end = i
            break
    try:
        data = yaml.safe_load("\n".join(lines[1:end])) or {}
    except yaml.YAMLError:
        return None, "unterminated frontmatter"
    return (data, "unterminated frontmatter") if isinstance(data, dict) else (None, "unterminated frontmatter")


class Linter:
    def __init__(self, root):
        self.root = Path(root)
        self.findings = []  # (check, path, message)
        self.arts = []  # dicts: type, archived, path, rel, fm, text
        self.ids = set()

    def add(self, check, rel, msg):
        self.findings.append((check, str(rel), msg))

    def rel(self, p):
        return p.relative_to(self.root)

    def load(self):
        for t in TYPES:
            for archived in (False, True):
                d = self.root / "docs" / t / ("archive" if archived else "")
                if not d.is_dir():
                    continue
                for p in sorted(d.glob("*.md")):
                    if p.name == "INDEX.md":
                        continue
                    text = p.read_text(encoding="utf-8")
                    fm, err = split_frontmatter(text)
                    self.arts.append(
                        dict(type=t, archived=archived, path=p, rel=self.rel(p), fm=fm, text=text, err=err)
                    )
                    if err:
                        self.add(2, self.rel(p), err)
                    if fm is not None and "id" in fm:
                        self.ids.add(str(fm["id"]))

    def tags_list(self):
        p = self.root / "docs" / "skills" / "tags.md"
        if not p.exists():
            return None
        tags = set()
        for line in p.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^([a-z0-9][\w\-]*)(?: \(umbrella\))? — ", line)
            if m:
                tags.add(m.group(1))
        return tags

    # --- checks ---

    def check_fields(self):  # 2, 15
        for a in self.arts:
            fm, rel = a["fm"], a["rel"]
            if fm is None:
                continue
            for f in BASE_FIELDS + TYPE_FIELDS.get(a["type"], ()):
                if f not in fm:
                    self.add(2, rel, f"missing required field `{f}`")
            st = fm.get("status")
            if "status" in fm and st not in STATUSES:
                self.add(2, rel, f"`status` is `{st}`, not one of {' | '.join(STATUSES)}")
            if st == "superseded" and "superseded-by" not in fm:
                self.add(2, rel, "`status: superseded` without `superseded-by`")
            for f in LIST_FIELDS:
                if f in fm and not isinstance(fm[f], list) and fm[f] != "TBD":
                    self.add(2, rel, f"`{f}` must be a YAML list, got {type(fm[f]).__name__}")
            if a["type"] == "decisions" and "track" in fm and fm["track"] not in ("product", "process"):
                self.add(15, rel, f"`track` is `{fm['track']}`, must be exactly `product` or `process`")

    def check_dangling(self):  # 1
        for a in self.arts:
            fm = a["fm"] or {}
            for f in REF_FIELDS:
                v = fm.get(f)
                if v is None:
                    continue
                for r in v if isinstance(v, list) else [v]:
                    r = str(r)
                    if r != "TBD" and r not in self.ids:
                        self.add(1, a["rel"], f"`{f}` points at `{r}`, which does not exist")

    def check_numbering(self):  # 3
        for t in ("facts", "decisions"):
            nums = {}
            for a in self.arts:
                if a["type"] != t:
                    continue
                m = NUMBERED.match(a["path"].name)
                if m:
                    nums.setdefault(int(m.group(1)), []).append(a["rel"])
            for n, rels in sorted(nums.items()):
                if len(rels) > 1:
                    self.add(3, f"docs/{t}/", f"number {n:04d} used by {len(rels)} files: " + ", ".join(map(str, rels)))
            if nums:
                for n in range(1, max(nums)):
                    if n not in nums:
                        self.add(3, f"docs/{t}/", f"number {n:04d} is skipped")

    def check_orphans(self):  # 7
        corpus = []
        for a in self.arts:
            corpus.append((a["path"], a["text"]))
        for p in sorted((self.root / "plugins").glob("**/*.md")) if (self.root / "plugins").is_dir() else []:
            corpus.append((p, p.read_text(encoding="utf-8")))
        for a in self.arts:
            if a["type"] not in ("facts", "guardrails") or a["archived"] or not a["fm"] or "id" not in a["fm"]:
                continue
            pat = re.compile(r"(?<![\w\-])" + re.escape(str(a["fm"]["id"])) + r"(?![\w\-])")
            if not any(p != a["path"] and pat.search(t) for p, t in corpus):
                self.add(7, a["rel"], f"nothing references `{a['fm']['id']}`")

    def check_prose_refs(self):  # 9
        for a in self.arts:
            if a["archived"] or a["type"] == "decisions":  # decisions are immutable (check 20)
                continue
            seen = set()
            for m in PROSE_REF.finditer(a["text"]):
                t, name = m.groups()
                if "NNNN" in name or name in seen:
                    continue
                seen.add(name)
                d = self.root / "docs" / t
                if not (d / name).exists() and not (d / "archive" / name).exists():
                    self.add(9, a["rel"], f"mentions `docs/{t}/{name}`, which does not exist")

    def check_templates(self):  # 12
        tdir = self.root / "plugins" / "kms" / "templates"
        if not tdir.is_dir():
            tdir = Path(__file__).resolve().parent.parent / "templates"
        if not tdir.is_dir():
            return
        for sub in sorted(p for p in tdir.iterdir() if p.is_dir()):
            tmpl = {}
            for p in sorted(sub.glob("*.md")):
                fm, _ = split_frontmatter(p.read_text(encoding="utf-8"))
                if fm and "id" in fm:
                    tmpl[str(fm["id"])] = fm.get("template-version", 1)
            have = {
                str(a["fm"]["id"]): a
                for a in self.arts
                if a["type"] == sub.name and not a["archived"] and a["fm"] and "id" in a["fm"]
            }
            for tid, ver in tmpl.items():
                if tid not in have:
                    self.add(12, f"docs/{sub.name}/", f"template `{tid}` has no file here")
                elif have[tid]["fm"].get("kms-seeded") is True:
                    cur = have[tid]["fm"].get("kms-template-version", 0)
                    if cur < ver:
                        self.add(12, have[tid]["rel"], f"seeded from template version {cur}, template is at {ver}")
            for hid, a in have.items():
                if a["fm"].get("kms-seeded") is True and hid not in tmpl:
                    self.add(12, a["rel"], f"`kms-seeded` but template `{hid}` no longer exists")

    def check_index(self):  # 19
        for t in TYPES:
            for archived in (False, True):
                d = self.root / "docs" / t / ("archive" if archived else "")
                idx = d / "INDEX.md"
                if not d.is_dir() or not idx.exists():
                    continue
                rel = self.rel(idx)
                rows = {}
                lines = idx.read_text(encoding="utf-8").splitlines()
                try:
                    start = next(i for i, l in enumerate(lines) if l.startswith("id,"))
                except StopIteration:
                    self.add(19, rel, "no `id,title,tags,status` header")
                    continue
                for cells in csv.reader(l for l in lines[start + 1 :] if l.strip()):
                    if len(cells) != 4:
                        self.add(19, rel, f"malformed row: {','.join(cells)[:60]}")
                    else:
                        rows[cells[0]] = cells
                files = {
                    str(a["fm"]["id"]): a
                    for a in self.arts
                    if a["type"] == t and a["archived"] == archived and a["fm"] and "id" in a["fm"]
                }
                for fid, a in files.items():
                    if fid not in rows:
                        self.add(19, rel, f"no row for `{fid}`")
                        continue
                    fm = a["fm"]
                    tags = fm.get("tags")
                    tags = ", ".join(map(str, tags)) if isinstance(tags, list) else str(tags)
                    want = [fid, str(fm.get("title")), tags, str(fm.get("status"))]
                    for name, w, g in zip(("title", "tags", "status"), want[1:], rows[fid][1:]):
                        if w != g:
                            self.add(19, rel, f"row `{fid}`: {name} is `{g}`, file says `{w}`")
                for rid in rows:
                    if rid not in files:
                        self.add(19, rel, f"row `{rid}` has no file in this directory")

    def check_archive(self):  # 20
        for a in self.arts:
            if not a["archived"] and a["fm"] and a["fm"].get("status") in ("superseded", "deprecated"):
                self.add(20, a["rel"], f"`status: {a['fm']['status']}` but not under archive/")

    def check_tags(self):  # 21
        allowed = self.tags_list()
        if allowed is None:
            return
        for a in self.arts:
            tags = (a["fm"] or {}).get("tags")
            if isinstance(tags, str):
                tags = [tags]
            for tag in tags if isinstance(tags, list) else []:
                if str(tag) not in allowed:
                    self.add(21, a["rel"], f"tag `{tag}` is not in docs/skills/tags.md")

    def run(self):
        self.load()
        for c in (
            self.check_fields,
            self.check_dangling,
            self.check_numbering,
            self.check_orphans,
            self.check_prose_refs,
            self.check_templates,
            self.check_index,
            self.check_archive,
            self.check_tags,
        ):
            c()
        self.findings = sorted(set(self.findings))
        return self.findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    findings = Linter(args.root).run()
    if args.json:
        print(json.dumps([dict(check=c, file=f, message=m) for c, f, m in findings], indent=1))
    else:
        for c, f, m in findings:
            print(f"check {c}: {f}: {m}")
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
