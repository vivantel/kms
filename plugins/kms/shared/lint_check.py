#!/usr/bin/env python3
"""Deterministic structural checks for the `lint` skill.

Usage: lint_check.py [--root DIR] [--docs DIR] [--json] [--strict] [--stale-days N] [--today DATE]
       lint_check.py [--root DIR] --refs ID        list the files that cite ID
       lint_check.py --version                     print the schema version this checker implements
       lint_check.py [--root DIR] --pin FILE   record the current revision of FILE's edge targets

Runs the lint checks that need only frontmatter, file names and file text: 1, 2, 3, 4, 7, 9, 12,
17, 18, 19, 20, 21, 24 (numbers as in plugins/kms/skills/lint/SKILL.md), and the pinned part of 13: an
edge (`governed-by`, `grounded-in`) that carries a pin in the file's `pinned` map is stale when
its target no longer hashes to the pin. Edges without a pin are left to the model. No model is
involved; output is sorted, so identical input gives identical output. Exit status 1 when
anything is found. Requires PyYAML.

A file in an older shape (fact `kind`/`governed-by`, a scalar guardrail `governed-by`, a string
`fitness-functions` entry, a non-date `expires`) yields one advisory line on stderr and no
finding; `--strict` turns those into findings (check 2).

A pin is the first 12 hex digits of the SHA-256 of the target file with its edge fields
(`governed-by`, `grounded-in`, `pinned`) and `date` removed from the frontmatter and all
whitespace runs collapsed (decision 0062).
"""

SCHEMA_VERSION = "1.0.0"  # first line of shared/artifact-model.md

import argparse
import csv
import datetime
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

import yaml

TYPES = ("facts", "decisions", "guardrails", "skills")
BASE_FIELDS = ("id", "title", "status", "date", "tags")
TYPE_FIELDS = {
    "guardrails": ("governed-by", "derivation-note"),
}
STATUSES = ("draft", "active", "superseded", "deprecated")
REF_FIELDS = ("governed-by", "grounded-in", "superseded-by", "governed-facts", "operationalizes")
LIST_FIELDS = ("grounded-in", "governed-facts", "operationalizes")
STALE_DAYS = 180
STEP = re.compile(r"^#{2,4}\s+[^\n]*?\[(done|pending|blocked)([^\]]*)\]", re.M)


def read(p):
    """File text; bytes that are not UTF-8 are replaced so one stray file cannot abort the run."""
    return Path(p).read_text(encoding="utf-8", errors="replace")


def as_date(v):
    if isinstance(v, datetime.datetime):
        return v.date()
    if isinstance(v, datetime.date):
        return v
    try:
        return datetime.date.fromisoformat(str(v))
    except ValueError:
        return None
NUMBERED = re.compile(r"^(\d{4})-")
EDGE_FIELDS = ("governed-by", "grounded-in")
PIN_IGNORED = EDGE_FIELDS + ("pinned", "date", "accepted-by", "last-verified", "status", "superseded-by", "expires", "expires-when")
SCOPE_KEYS = ("component", "environment", "version")


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
            except (yaml.YAMLError, ValueError) as e:  # ValueError: calendar-invalid timestamps
                return None, "unparseable frontmatter: " + (str(e).splitlines() or [type(e).__name__])[0]
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


def revision(text):
    """Pin value for an artifact file: a hash of its text without edge fields and `date`."""
    lines = text.split("\n")
    out, skipping, in_fm = [], False, False
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                in_fm = True
                head, body = lines[1:i], lines[i:]
                break
    if in_fm:
        for line in head:
            m = re.match(r"^([\w\-]+):", line)
            if m:
                skipping = m.group(1) in PIN_IGNORED
            if not skipping:
                out.append(line)
        norm = "\n".join(out + body)
    else:
        norm = text
    return hashlib.sha256(" ".join(norm.split()).encode("utf-8")).hexdigest()[:12]


def edge_ids(fm):
    ids = []
    for f in EDGE_FIELDS:
        v = (fm or {}).get(f)
        for r in v if isinstance(v, list) else ([] if v is None else [v]):
            if str(r) != "TBD" and str(r) not in ids:
                ids.append(str(r))
    return ids


class Linter:
    def __init__(self, root, docs=None, strict=False, stale_days=STALE_DAYS, today=None):
        self.strict = strict
        self.stale_days = stale_days
        self.today = as_date(today) if today else datetime.date.today()
        self.legacy_files = {}  # rel -> [message]
        self.root = Path(root).resolve()
        self.docs = self.find_docs(docs)
        try:
            self.dn = self.docs.relative_to(self.root).as_posix()
        except ValueError:
            self.dn = self.docs.as_posix()
        self.prose_ref = re.compile(
            r"(?<![\w\-/])(?:\.{1,2}/)*" + re.escape(self.dn) + r"/(facts|decisions|guardrails|skills)/(?:archive/)?([\w.\-]+\.md)"
        )
        self.findings = []  # (check, path, message)
        self.warnings = []
        self.arts = []  # dicts: type, archived, path, rel, fm, text
        self.ids = set()
        self.broken = set()  # (type, archived, id) of files whose frontmatter did not parse
        if not any((self.docs / t).is_dir() for t in TYPES):
            self.warnings.append(f"no {'/'.join(TYPES)} directories under {self.dn}/: nothing was checked (use --docs DIR)")

    def find_docs(self, docs):
        if docs:
            d = Path(docs)
            return d.resolve() if d.is_absolute() else self.root / d
        if (self.root / "docs").is_dir():
            return self.root / "docs"
        try:
            for d in sorted(p for p in self.root.iterdir() if p.is_dir() and not p.name.startswith(".")):
                if (d / "decisions").is_dir():
                    return d
        except OSError:
            pass
        return self.root / "docs"

    def add(self, check, rel, msg):
        self.findings.append((check, str(rel), msg))

    def legacy(self, check, rel, msg):
        """A finding under --strict, else one advisory line per file for an older-shape field."""
        if self.strict:
            self.add(check, rel, msg)
        else:
            self.legacy_files.setdefault(str(rel), []).append(msg)

    def is_registry(self, text, fm):
        return bool(fm and "kms-registry" in fm) or text.lstrip().startswith("<!-- kms-registry:")

    def age(self, d):
        d = as_date(d)
        return None if d is None else (self.today - d).days

    def rel(self, p):
        try:
            return p.relative_to(self.root)
        except ValueError:
            return p

    def load(self):
        self.arts, self.ids, self.broken = [], set(), set()  # reentrant: run() then pin() must not double-count
        for t in TYPES:
            for archived in (False, True):
                d = self.docs / t / ("archive" if archived else "")
                if not d.is_dir():
                    continue
                for p in sorted(d.glob("*.md")):
                    if p.name == "INDEX.md":
                        continue
                    text = read(p)
                    fm, err = split_frontmatter(text)
                    if self.is_registry(text, fm):
                        continue
                    self.arts.append(
                        dict(type=t, archived=archived, path=p, rel=self.rel(p), fm=fm, text=text, err=err)
                    )
                    if err:
                        self.add(2, self.rel(p), err)
                    if fm is not None and "id" in fm:
                        self.ids.add(str(fm["id"]))
                    elif fm is None:
                        self.ids.add(p.stem)
                        self.broken.add((t, archived, p.stem))

    def tags_list(self):
        p = self.docs / "skills" / "tags.md"
        if not p.exists():
            return None
        tags = set()
        lines = read(p).splitlines()
        if lines and lines[0].strip() == "---":  # frontmatter keys are not tags
            end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), -1)
            lines = lines[end + 1:]
        for line in lines:
            m = re.match(r"^\s*(?:[-*]\s+)?([a-z0-9][\w\-]*)(?: \(umbrella\))?(?:\s+[—–-]\s+|:\s+)", line)
            if m:
                tags.add(m.group(1))
        return tags

    # --- checks ---

    def check_fields(self):  # 2
        for a in self.arts:
            fm, rel = a["fm"], a["rel"]
            if fm is None:
                continue
            for f in BASE_FIELDS + TYPE_FIELDS.get(a["type"], ()):
                if f not in fm:
                    self.add(2, rel, f"missing required field `{f}`")
            if "date" in fm and as_date(fm["date"]) is None and str(fm["date"]) != "TBD":
                self.add(2, rel, f"`date: {fm['date']}` is not a date (YYYY-MM-DD)")
            st = fm.get("status")
            if "status" in fm and st not in STATUSES:
                self.add(2, rel, f"`status` is `{st}`, not one of {' | '.join(STATUSES)}")
            if st == "superseded" and "superseded-by" not in fm:
                self.add(2, rel, "`status: superseded` without `superseded-by`")
            if a["type"] == "guardrails" and "governed-by" in fm and not isinstance(fm["governed-by"], list) and fm["governed-by"] != "TBD":
                self.legacy(2, rel, "`governed-by` on a guardrail should be a YAML list of decision ids")
            if a["type"] == "facts":
                for f in ("kind", "governed-by"):
                    if f in fm:
                        self.legacy(2, rel, f"`{f}` is not a fact field any more")
            if "expires" in fm and as_date(fm["expires"]) is None:
                self.legacy(2, rel, "`expires` must be a date; move a condition to `expires-when`")
            ff = fm.get("fitness-functions")
            if isinstance(ff, list):
                for e in ff:
                    if not isinstance(e, dict) or "check" not in e:
                        self.legacy(2, rel, "`fitness-functions` entries should be maps with `check`")
                        break
            for f in LIST_FIELDS:
                if f in fm and not isinstance(fm[f], list) and fm[f] != "TBD":
                    self.add(2, rel, f"`{f}` must be a YAML list, got {type(fm[f]).__name__}")
            if "tags" in fm and not isinstance(fm["tags"], list):
                self.add(2, rel, f"`tags` must be a YAML list, got {type(fm['tags']).__name__}")
            if "pinned" in fm:
                pins = fm["pinned"]
                if not isinstance(pins, dict):
                    self.add(2, rel, f"`pinned` must be a mapping of id to revision, got {type(pins).__name__}")
                else:
                    for k in pins:
                        if str(k) not in edge_ids(fm):
                            self.add(2, rel, f"`pinned` has `{k}`, which is not in `governed-by` or `grounded-in`")
            if "scope" in fm:
                if a["type"] != "facts":
                    self.add(2, rel, "`scope` is only defined on facts")
                else:
                    self.check_scope(rel, fm["scope"])
            if a["type"] == "decisions" and "track" in fm:
                self.legacy(2, rel, "`track` is not a decision field any more")

    def check_scope(self, rel, sc):
        if not isinstance(sc, dict) or not sc:
            self.add(2, rel, f"`scope` must be a non-empty mapping of {' | '.join(SCOPE_KEYS)} to a value, got {type(sc).__name__}")
            return
        for k, v in sc.items():
            if k not in SCOPE_KEYS:
                self.add(2, rel, f"`scope` has `{k}`, not one of {' | '.join(SCOPE_KEYS)}")
            elif not isinstance(v, (str, int, float)) or isinstance(v, bool) or not str(v).strip():
                self.add(2, rel, f"`scope.{k}` must be a non-empty string")

    def check_dangling(self):  # 1
        by_id = {str(a["fm"]["id"]): a for a in self.arts if a["fm"] and "id" in a["fm"]}
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
                    elif r != "TBD" and a["type"] == "guardrails" and not a["archived"]:
                        t = by_id.get(r)
                        # a pin says the guardrail was derived from the source's content, so a retired source is a finding, not an older shape
                        pinned = bool((a["fm"] or {}).get("pinned"))
                        report = self.add if pinned else self.legacy
                        tstatus = (t["fm"] or {}).get("status") if t else None
                        if t and f == "governed-by" and t["type"] == "decisions" and tstatus == "superseded":
                            report(1, a["rel"], f"`governed-by` points at `{r}`, a superseded decision: re-derive")
                        if t and f == "grounded-in" and t["type"] == "facts" and tstatus in ("deprecated", "superseded") and pinned:
                            self.add(1, a["rel"], f"`grounded-in` points at `{r}`, a {tstatus} fact: re-derive")
                        if t and f == "grounded-in" and t["type"] != "facts":
                            self.legacy(1, a["rel"], f"`grounded-in` points at `{r}`, which is not a fact")

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
                    self.add(3, f"{self.dn}/{t}/", f"number {n:04d} used by {len(rels)} files: " + ", ".join(map(str, rels)))
            if nums:
                for n in range(1, max(nums)):
                    if n not in nums:
                        self.warnings.append(f"number {n:04d} is skipped in {self.dn}/{t}/")  # gaps follow deletions and parallel numbering; only duplicates are findings
        owners = {}
        for a in self.arts:
            if a["fm"] and "id" in a["fm"]:
                owners.setdefault(str(a["fm"]["id"]), []).append(str(a["rel"]))
        for i, rels in sorted(owners.items()):
            if len(rels) > 1:
                self.add(3, rels[0], f"id `{i}` is used by {len(rels)} files: " + ", ".join(rels))

    def check_pins(self):  # 13, pinned edges only
        by_id = {str(a["fm"]["id"]): a for a in self.arts if a["fm"] and "id" in a["fm"]}
        for a in self.arts:
            pins = (a["fm"] or {}).get("pinned")
            if not isinstance(pins, dict):
                continue
            for k, want in pins.items():
                t = by_id.get(str(k))
                if t is not None and str(k) in edge_ids(a["fm"]) and revision(t["text"]) != str(want):
                    self.add(13, a["rel"], f"pinned `{k}` at {want}, but it is now {revision(t['text'])}: re-derive and re-pin")

    def pin(self, target):
        """Rewrite FILE's `pinned` map to the current revision of every edge target."""
        self.load()
        path = Path(target)
        path = path if path.is_absolute() else self.root / path
        a = next((x for x in self.arts if x["path"].resolve() == path.resolve()), None)
        if a is None or not a["fm"]:
            raise SystemExit(f"{target}: not an artifact with frontmatter")
        by_id = {str(x["fm"]["id"]): x for x in self.arts if x["fm"] and "id" in x["fm"]}
        dup = [i for i, n in Counter(str(x["fm"]["id"]) for x in self.arts if x["fm"] and "id" in x["fm"]).items() if n > 1]
        ids = edge_ids(a["fm"])
        if any(i in dup for i in ids + [str(a["fm"].get("id"))]):
            raise SystemExit("ambiguous id (used by more than one file): refusing to pin; fix check 3 first")
        missing = [i for i in ids if i not in by_id]
        if missing:
            raise SystemExit("edge targets that do not exist: " + ", ".join(missing))
        raw = path.read_bytes().decode("utf-8")
        crlf = "\r\n" in raw
        lines = raw.replace("\r\n", "\n").split("\n")
        end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
        if end is None:
            raise SystemExit(f"{target}: unterminated frontmatter (no closing `---`); fix that first")
        head = []
        skipping = False
        for line in lines[1:end]:
            m = re.match(r"^([\w\-]+):", line)
            if m:
                skipping = m.group(1) == "pinned"
            if not skipping:
                head.append(line)
        if ids:
            head.append("pinned:")
            head += [f'  {i}: "{revision(by_id[i]["text"])}"' for i in ids]
        out = "\n".join(["---"] + head + lines[end:])
        with path.open("w", encoding="utf-8", newline="") as f:
            f.write(out.replace("\n", "\r\n") if crlf else out)

    def check_orphans(self):  # 7
        corpus = []
        for a in self.arts:
            corpus.append((a["path"], a["text"]))
        for p in sorted((self.root / "plugins").glob("**/*.md")) if (self.root / "plugins").is_dir() else []:
            corpus.append((p, read(p)))
        for a in self.arts:
            if a["type"] not in ("facts", "guardrails") or a["archived"] or not a["fm"] or "id" not in a["fm"]:
                continue
            if a["type"] == "guardrails" and a["fm"].get("enforced-by"):  # enforced by a named check, so not orphaned
                continue
            if a["fm"].get("kms-seeded") is True:  # a seeded guardrail is referenced by its template, not by project files
                continue
            if a["type"] == "facts" and a["fm"].get("source"):  # a fact with a source is not noise
                continue
            pat = re.compile(r"(?<![\w\-])" + re.escape(str(a["fm"]["id"])) + r"(?![\w\-])")
            if not any(p != a["path"] and pat.search(t) for p, t in corpus):
                self.add(7, a["rel"], f"nothing references `{a['fm']['id']}`")

    def check_prose_refs(self):  # 9
        corpus = [(a["rel"], a["text"]) for a in self.arts if not a["archived"] and a["type"] != "decisions"]  # decisions are immutable (check 20)
        extra = [self.root / n for n in ("README.md", "AGENTS.md", "CONTRIBUTING.md")]
        plans = self.docs / "plans"  # archived plans are history: they may name files long since removed
        extra += sorted(p for p in plans.glob("*.md")) if plans.is_dir() else []
        for p in extra:
            if p.is_file():
                corpus.append((self.rel(p), read(p)))
        for rel, text in corpus:
            seen = set()
            for m in self.prose_ref.finditer(text):
                t, name = m.groups()
                if "NNNN" in name or m.group(0) in seen:
                    continue
                seen.add(m.group(0))
                d = self.docs / t
                in_archive = "/archive/" in m.group(0)
                if not (d / ("archive" if in_archive else "") / name).exists():
                    where = " (it moved to archive/: update the path)" if not in_archive and (d / "archive" / name).exists() else ""
                    self.add(9, rel, f"mentions `{self.dn}/{t}/{'archive/' if in_archive else ''}{name}`, which does not exist{where}")

    def check_templates(self):  # 12
        tdir = self.root / "plugins" / "kms" / "templates"
        if not tdir.is_dir():
            tdir = Path(__file__).resolve().parent.parent / "templates"
        if not tdir.is_dir():
            return
        for sub in sorted(p for p in tdir.iterdir() if p.is_dir()):
            tmpl = {}
            for p in sorted(sub.glob("*.md")):
                fm, _ = split_frontmatter(read(p))
                if fm and "id" in fm:
                    tmpl[str(fm["id"])] = fm.get("template-version", 1)
            have = {
                str(a["fm"]["id"]): a
                for a in self.arts
                if a["type"] == sub.name and not a["archived"] and a["fm"] and "id" in a["fm"]
            }
            for tid, ver in tmpl.items():
                if tid not in have:
                    self.add(12, f"{self.dn}/{sub.name}/", f"template `{tid}` has no file here")
                elif have[tid]["fm"].get("kms-seeded") is True:
                    try:
                        cur, want = int(have[tid]["fm"].get("kms-template-version", 0)), int(ver)
                    except (TypeError, ValueError):
                        self.add(12, have[tid]["rel"], f"`kms-template-version` is `{have[tid]['fm'].get('kms-template-version')}`, not a number")
                        continue
                    if cur < want:
                        self.add(12, have[tid]["rel"], f"seeded from template version {cur}, template is at {want}")
            for hid, a in have.items():
                if a["fm"].get("kms-seeded") is True and hid not in tmpl:
                    self.add(12, a["rel"], f"`kms-seeded` but template `{hid}` no longer exists")

    def check_index(self):  # 19
        for t in TYPES:
            for archived in (False, True):
                d = self.docs / t / ("archive" if archived else "")
                idx = d / "INDEX.md"
                if not d.is_dir() or not idx.exists():
                    continue
                rel = self.rel(idx)
                rows = {}
                lines = read(idx).splitlines()
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
                    if rid not in files and (t, archived, rid) not in self.broken:
                        self.add(19, rel, f"row `{rid}` has no file in this directory")

    def check_dates(self):  # 4, 17, 18
        for a in self.arts:
            fm, rel = a["fm"], a["rel"]
            if not fm or a["archived"]:
                continue
            exp = as_date(fm.get("expires")) if "expires" in fm else None
            if exp is not None and exp < self.today:
                self.add(4, rel, f"`expires: {exp}` has passed")
            open_question = fm.get("status") == "draft" and "expires-when" in fm  # not an abandoned stub: exempt from 17 only
            tbd = [f for f in EDGE_FIELDS if fm.get(f) == "TBD" or (isinstance(fm.get(f), list) and "TBD" in fm[f])]
            n = self.age(fm.get("date"))
            if not open_question and (tbd or fm.get("status") == "draft") and n is not None and n > self.stale_days:
                what = ", ".join(f"`{f}: TBD`" for f in tbd) or "`status: draft`"
                self.add(17, rel, f"{what} unresolved for {n} days (threshold {self.stale_days})")
            ff = fm.get("fitness-functions")
            if ff is not None and not isinstance(ff, list):
                self.add(2, rel, "`fitness-functions` must be a YAML list")
                ff = []
            for e in ff or []:
                if isinstance(e, dict):
                    n = self.age(e.get("last-verified")) if "last-verified" in e else None
                    if "last-verified" not in e or n is None:
                        self.add(18, rel, f"fitness function `{str(e.get('check'))[:40]}` has no `last-verified` date")
                    elif n > self.stale_days:
                        self.add(18, rel, f"fitness function `{str(e.get('check'))[:40]}` last verified {n} days ago (threshold {self.stale_days})")

    def check_plans(self):  # 24
        plans = self.docs / "plans"
        for p in sorted(plans.glob("*.md")) if plans.is_dir() else []:
            states = ["partial" if "except" in m.group(2) else m.group(1) for m in STEP.finditer(read(p))]
            if states and all(x == "done" for x in states):
                self.add(24, self.rel(p), "every step is `done`, but the plan is not under plans/archive/")

    def refs(self, target):
        """Files that cite TARGET in an edge field or in prose."""
        self.load()
        pat = re.compile(r"(?<![\w\-])" + re.escape(target) + r"(?![\w\-])")
        out = []
        for a in self.arts:
            own = str((a["fm"] or {}).get("id", a["path"].stem))
            if own != target and pat.search(a["text"]):
                out.append(str(a["rel"]))
        return sorted(out)

    def check_unpinned(self):  # advisory
        for a in self.arts:
            fm = a["fm"] or {}
            if a["type"] == "guardrails" and not a["archived"] and edge_ids(fm) and not fm.get("pinned"):
                self.warnings.append(f"unpinned: {a['rel']}: run `--pin`")

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
                    self.add(21, a["rel"], f"tag `{tag}` is not in {self.dn}/skills/tags.md")

    def run(self):
        self.load()
        for c in (
            self.check_fields,
            self.check_dangling,
            self.check_pins,
            self.check_dates,
            self.check_plans,
            self.check_unpinned,
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
        for rel in sorted(self.legacy_files):
            self.warnings.append(f"older shape: {rel}: " + "; ".join(self.legacy_files[rel]))
        return self.findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--docs", metavar="DIR", help="knowledge directory (default: docs/, else the first root-level directory holding decisions/)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--pin", metavar="FILE", help="record the current revision of FILE's edge targets")
    ap.add_argument("--refs", metavar="ID", help="list the files that cite ID")
    ap.add_argument("--strict", action="store_true", help="report older-shape fields as findings")
    ap.add_argument("--stale-days", type=int, default=STALE_DAYS)
    ap.add_argument("--today", metavar="DATE", help="override today's date (YYYY-MM-DD), for tests")
    ap.add_argument("--version", action="store_true", help="print the schema version and exit")
    args = ap.parse_args()
    if args.version:
        print(SCHEMA_VERSION)
        return
    if args.refs and args.pin:
        ap.error("--refs and --pin cannot be combined")
    if args.refs:
        for r in Linter(args.root, args.docs).refs(args.refs):
            print(r)
        return
    if args.pin:
        Linter(args.root, args.docs).pin(args.pin)
        return
    linter = Linter(args.root, args.docs, args.strict, args.stale_days, args.today)
    findings = linter.run()
    for w in linter.warnings:
        print("warning: " + w, file=sys.stderr)
    if args.json:
        print(json.dumps([dict(check=c, file=f, message=m) for c, f, m in findings], indent=1))
    else:
        for c, f, m in findings:
            print(f"check {c}: {f}: {m}")
    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
