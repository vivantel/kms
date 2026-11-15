#!/usr/bin/env python3
"""Generate the conformance corpus for the knowledge-base core (docs/skills/core-contract.md).

Each case is a small project tree under cases/<name>/ plus cases/<name>.expected.json:
  {"args": [extra CLI args], "findings": [{"check": N, "file": "<repo-relative path>", "severity": "error"}]}
A checker conforms when `lint_check.py --root <case> --json --today 2026-11-08 <args>` reports exactly
those (check, file) pairs. Messages are not part of the contract.

Usage: build.py          write cases/
       build.py --check  fail if the committed files differ from what this would write
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "plugins" / "kms" / "shared"))
from lint_check import Linter, revision  # noqa: E402

TODAY = "2026-11-08"


def art(**fm):
    body = fm.pop("body", "Body.")
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, default_flow_style=None, width=1000) + "---\n" + body + "\n"


def base():
    f = {
        "docs/facts/0001-cadence.md": art(id="0001-cadence", title="Releases are weekly", status="active", date="2026-10-01", tags=["release"], source="CHANGELOG.md", body="Weekly."),
        "docs/decisions/0001-weekly.md": art(id="0001-weekly", title="Ship weekly", status="active", date="2026-10-01", tags=["release"], body="## Decision\n\nShip weekly."),
        "docs/guardrails/changelog.md": art(id="changelog", title="Every release has a changelog entry", status="active", date="2026-10-01", tags=["release"],
                                            **{"governed-by": ["0001-weekly"], "grounded-in": ["0001-cadence"], "derivation-note": "Given 0001-weekly and 0001-cadence, each release needs an entry."}, body="Guardrail."),
        "docs/skills/deploy.md": art(id="deploy", title="Deploy steps", status="active", date="2026-10-01", tags=["release"], body="See changelog."),
        "docs/skills/tags.md": art(id="tags", title="Tags", status="active", date="2026-10-01", tags=["release"], **{"kms-registry": "tags"}, body="release — release process"),
        "plugins/kms/templates/guardrails/.keep": "",
    }
    return f


def indexes(f):
    for t in ("facts", "decisions", "guardrails", "skills"):
        rows = []
        for k in sorted(f):
            if k.startswith(f"docs/{t}/") and k.endswith(".md") and k.count("/") == 3 and not k.endswith("INDEX.md"):
                fm = yaml.safe_load(f[k].split("---\n")[1])
                if "kms-registry" in fm:
                    continue
                rows.append('{},"{}","{}",{}'.format(fm["id"], fm["title"], ", ".join(fm["tags"]), fm["status"]))
        if rows:
            f[f"docs/{t}/INDEX.md"] = "<!-- kms-registry: index -->\nid,title,tags,status\n" + "\n".join(rows) + "\n"


def sub(f, path, old, new):
    assert old in f[path], (path, old)
    f[path] = f[path].replace(old, new, 1)


CASES = {}


def case(name, args=()):
    def deco(fn):
        CASES[name] = (fn, list(args))
        return fn
    return deco


@case("valid")
def _(f): pass
@case("valid-registry-and-open-question")
def _(f):
    f["docs/skills/roles.md"] = art(id="roles", title="Roles", status="active", date="2026-10-01", tags=["release"], **{"kms-registry": "roles"})
    f["docs/decisions/0002-open.md"] = art(id="0002-open", title="Does X hold?", status="draft", date="2026-01-01", tags=["release"], **{"expires-when": "the test closes"})
@case("older-shape-is-advisory")
def _(f): sub(f, "docs/facts/0001-cadence.md", "source: CHANGELOG.md\n", "kind: environmental\ngoverned-by: 0001-weekly\n")
@case("older-shape-strict", ["--strict"])
def _(f): sub(f, "docs/facts/0001-cadence.md", "source: CHANGELOG.md\n", "kind: environmental\ngoverned-by: 0001-weekly\n")
@case("c01-dangling-reference")
def _(f): sub(f, "docs/guardrails/changelog.md", "[0001-cadence]", "[0099-none]")
@case("c02-missing-field")
def _(f): sub(f, "docs/decisions/0001-weekly.md", "date: '2026-10-01'\n", "")
@case("c02-bad-status")
def _(f): sub(f, "docs/decisions/0001-weekly.md", "status: active", "status: accepted")
@case("c03-duplicate-number")
def _(f): f["docs/decisions/0001-twin.md"] = art(id="0001-twin", title="Twin", status="active", date="2026-10-01", tags=["release"])
@case("gap-is-advisory")
def _(f): f["docs/decisions/0003-gap.md"] = art(id="0003-gap", title="Gap", status="active", date="2026-10-01", tags=["release"])
@case("c07-enforced-guardrail-is-not-orphan")
def _(f): f["docs/guardrails/enforced.md"] = art(id="enforced", title="Enforced", status="active", date="2026-10-01", tags=["release"], **{"governed-by": ["0001-weekly"], "enforced-by": "ci job x", "derivation-note": "Given 0001-weekly, x."})
@case("c04-expired")
def _(f): sub(f, "docs/decisions/0001-weekly.md", "tags: [release]\n", "tags: [release]\nexpires: '2026-06-01'\n")
@case("c07-orphan-guardrail")
def _(f): f["docs/guardrails/lonely.md"] = art(id="lonely", title="Lonely", status="active", date="2026-10-01", tags=["release"], **{"governed-by": ["0001-weekly"], "derivation-note": "Given 0001-weekly, nothing."})
@case("c07-fact-with-source-is-not-orphan")
def _(f): sub(f, "docs/guardrails/changelog.md", "grounded-in: [0001-cadence]\n", "")
@case("c09-stale-prose-reference")
def _(f): sub(f, "docs/skills/deploy.md", "See changelog.", "See docs/guardrails/missing.md.")
@case("c12-template-missing")
def _(f): f["plugins/kms/templates/guardrails/seed.md"] = "---\ntemplate-version: 1\nid: seed\ntitle: Seed\n---\n"
@case("c13-pinned-edge-stale")
def _(f):
    g = f["docs/guardrails/changelog.md"]
    f["docs/guardrails/changelog.md"] = g.replace("---\nGuardrail.", 'pinned:\n  0001-weekly: "{}"\n  0001-cadence: "{}"\n---\nGuardrail.'.format(revision(f["docs/decisions/0001-weekly.md"]), revision(f["docs/facts/0001-cadence.md"])))
    sub(f, "docs/facts/0001-cadence.md", "Weekly.", "Monthly now.")
@case("c13-pin-ignores-lifecycle-fields")
def _(f):
    g = f["docs/guardrails/changelog.md"]
    f["docs/guardrails/changelog.md"] = g.replace("---\nGuardrail.", 'pinned:\n  0001-weekly: "{}"\n  0001-cadence: "{}"\n---\nGuardrail.'.format(revision(f["docs/decisions/0001-weekly.md"]), revision(f["docs/facts/0001-cadence.md"])))
    sub(f, "docs/facts/0001-cadence.md", "tags: [release]\n", "tags: [release]\nlast-verified: '2026-11-01'\n")
@case("c17-stale-draft")
def _(f): f["docs/decisions/0002-stale.md"] = art(id="0002-stale", title="Stale", status="draft", date="2026-01-01", tags=["release"])
@case("c18-stale-fitness-function")
def _(f): sub(f, "docs/decisions/0001-weekly.md", "tags: [release]\n", "tags: [release]\nfitness-functions:\n- {check: weekly tag, enforced-by: ci, last-verified: '2025-01-01'}\n")
@case("c19-index-row-missing")
def _(f): pass  # indexes are written, then a row is removed in post()
@case("c20-superseded-not-archived")
def _(f): sub(f, "docs/decisions/0001-weekly.md", "status: active", "status: superseded\nsuperseded-by: 0002-x")
@case("c21-tag-off-list")
def _(f): sub(f, "docs/skills/deploy.md", "tags: [release]", "tags: [shipping]")
@case("c24-completed-plan")
def _(f): f["docs/plans/p.md"] = "---\nid: p\ntitle: P\n---\n### 1. [done] A\n### 2. [done] B\n"


def post(name, f):
    if name == "c19-index-row-missing":
        f["docs/facts/INDEX.md"] = "<!-- kms-registry: index -->\nid,title,tags,status\n"


def render(name):
    fn, args = CASES[name]
    f = base()
    fn(f)
    indexes(f)
    post(name, f)
    with tempfile.TemporaryDirectory() as d:
        for rel, text in f.items():
            p = Path(d, rel)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        lin = Linter(d, strict="--strict" in args, today=TODAY)
        found = sorted({(c, fl) for c, fl, _ in lin.run()})
    exp = {"args": args, "findings": [{"check": c, "file": fl, "severity": "error"} for c, fl in found]}
    return f, json.dumps(exp, indent=1) + "\n"


def build():
    out = {}
    for name in CASES:
        f, exp = render(name)
        for rel, text in f.items():
            out[f"cases/{name}/{rel}"] = text
        out[f"cases/{name}.expected.json"] = exp
    return out


def main():
    out = build()
    if "--check" in sys.argv:
        on_disk = {str(p.relative_to(HERE)) for p in (HERE / "cases").rglob("*") if p.is_file()} if (HERE / "cases").exists() else set()
        stale = [k for k, v in out.items() if not (HERE / k).exists() or (HERE / k).read_text(encoding="utf-8") != v] + sorted(on_disk - set(out))
        if stale:
            raise SystemExit("out of date: " + ", ".join(stale[:5]))
        return
    shutil.rmtree(HERE / "cases", ignore_errors=True)
    for k, v in out.items():
        p = HERE / k
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(v, encoding="utf-8")


if __name__ == "__main__":
    main()
