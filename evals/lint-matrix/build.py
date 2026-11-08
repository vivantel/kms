#!/usr/bin/env python3
"""Generate the lint-matrix eval: one clean project and one project per lint check, each with
exactly one seeded violation, plus labels.json (the ground truth) and promptfooconfig.yaml.

Usage: build.py            write cases/, labels.json, promptfooconfig.yaml
       build.py --check    fail if the committed files differ from what this would write

A case's label is its target check plus every check the deterministic checker also reports on
it (a seeded violation can legitimately trip a second check, e.g. an audit-log fact is also an
orphan). Mutations for judgment checks must not trip any other deterministic check beyond the
`cofires` they declare. Judgment mutations are clear-cut instances, so recall on them is an
upper bound for subtler violations.
"""

import json
import re
import shutil
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "plugins" / "kms" / "shared"))
from lint_check import Linter, split_frontmatter  # noqa: E402

STRUCTURAL = [1, 2, 3, 7, 9, 12, 15, 19, 20, 21]  # checks run by lint_check.py (decision 0058)
JUDGMENT = [4, 5, 6, 8, 10, 11, 13, 14, 16, 17, 18, 22, 23, 24]


def art(id, title, tags, body, status="active", date="2026-10-01", **extra):
    fm = dict(id=id, title=title, status=status, date=date, tags=tags)
    fm.update(extra)
    return "---\n" + yaml.safe_dump(fm, sort_keys=False, default_flow_style=None, width=1000) + "---\n" + body + "\n"


def base():
    f = {}
    f["docs/decisions/0001-weekly-releases.md"] = art(
        "0001-weekly-releases", "Ship a release every week", ["release"],
        "## Decision\n\nCut a release every Thursday.\n", track="process",
        **{"fitness-functions": ["CI fails when a week passes without a release tag (last verified 2026-10-30)"]})
    f["docs/decisions/0002-changelog-per-release.md"] = art(
        "0002-changelog-per-release", "Each release carries a changelog entry", ["release", "documentation"],
        "## Decision\n\nEvery release adds an entry to CHANGELOG.md.\n", track="process")
    f["docs/decisions/0003-pr-before-merge.md"] = art(
        "0003-pr-before-merge", "Changes reach main through pull requests", ["git"],
        "## Decision\n\nNo direct pushes to main.\n", track="process")
    f["docs/facts/0001-release-cadence.md"] = art(
        "0001-release-cadence", "Releases go out on Thursdays", ["release"],
        "The release job runs Thursdays at 10:00 UTC.", kind="environmental",
        **{"governed-by": "0001-weekly-releases"})
    f["docs/facts/0002-ci-runs-on-pr.md"] = art(
        "0002-ci-runs-on-pr", "CI runs on every pull request", ["git"],
        "The test workflow triggers on pull_request.", kind="environmental",
        **{"governed-by": "0003-pr-before-merge"})
    f["docs/guardrails/require-changelog-entry.md"] = art(
        "require-changelog-entry", "Every release must have a changelog entry", ["release", "documentation"],
        "## Guardrail\n\nA release without a CHANGELOG.md entry is not shipped.\n\n## Derivation\n\nWeekly releases (fact) and the per-release entry rule (decision) imply one entry per week.",
        **{"governed-by": "0002-changelog-per-release",
           "grounded-in": ["0001-release-cadence", "0002-changelog-per-release"],
           "derivation-note": "Weekly cadence plus the per-release entry rule imply one entry a week."})
    f["docs/guardrails/pr-before-merge.md"] = art(
        "pr-before-merge", "Never push directly to main", ["git"],
        "## Guardrail\n\nOpen a pull request; CI must pass before merge.\n\n## Derivation\n\nPRs are the only path to main (decision) and CI runs on them (fact).",
        **{"governed-by": "0003-pr-before-merge", "grounded-in": ["0002-ci-runs-on-pr", "0003-pr-before-merge"],
           "derivation-note": "PR-only merges plus CI-on-PR imply CI gates every merge."})
    f["docs/skills/deploy-checklist.md"] = art(
        "deploy-checklist", "Deploy checklist", ["release"],
        "Steps: update CHANGELOG.md, tag the release, run the release job. Guardrails: pr-before-merge.",
        operationalizes=["require-changelog-entry"])
    f["docs/skills/process-track-roles.md"] = art(
        "process-track-roles", "Process-track roles", ["release"],
        "release manager — last matched a decision 2026-10-20\nci owner — last matched a decision 2026-10-24")
    f["docs/skills/tags.md"] = art(
        "tags", "Canonical tag vocabulary", ["release"],
        "release — the release process\ndocumentation — docs structure and prose\ngit — git workflow", **{"kms-generated": True})
    f["docs/plans/release-automation.md"] = (
        "---\nid: release-automation\ntitle: Automate the release job\nstatus: steps 1 done; step 2 pending\ndate: 2026-10-01\n---\n\n"
        "# Automate the release job\n\n### 1. [done] Write the job\n\n### 2. [pending] Add the tag step\n")
    f["plugins/kms/templates/guardrails/.keep"] = ""
    return f


def sub(files, old, new, only=None):
    for k in list(files):
        if only is None or k == only:
            files[k] = files[k].replace(old, new)


def rename_id(files, old, new):
    sub(files, old, new)
    for k in list(files):
        if old in k:
            files[k.replace(old, new)] = files.pop(k)


def add_guardrail(files, id, title, body, **extra):
    gd = {"governed-by": "0002-changelog-per-release", "grounded-in": ["0001-release-cadence"],
          "derivation-note": "Follows from the release cadence fact."}
    gd.update(extra)
    files[f"docs/guardrails/{id}.md"] = art(id, title, gd.pop("tags", ["release"]), body, **gd)
    sub(files, "Guardrails: pr-before-merge.", f"Guardrails: pr-before-merge, {id}.", "docs/skills/deploy-checklist.md")


# --- mutations: target check -> (pre-index function, post-index function or None, declared co-fires)

def m1(f): sub(f, "governed-by: 0001-weekly-releases", "governed-by: 0099-nonexistent", "docs/facts/0001-release-cadence.md")
def m2(f): sub(f, "track: process\n", "", "docs/decisions/0003-pr-before-merge.md")
def m3(f): rename_id(f, "0002-ci-runs-on-pr", "0003-ci-runs-on-pr")
def m4(f): sub(f, "track: process\n", "track: process\nexpires: 2026-06-01\n", "docs/decisions/0003-pr-before-merge.md")
def m5(f): add_guardrail(f, "changelog-skill-writes-entry", "The changelog skill writes a Keep a Changelog entry",
                         "## Guardrail\n\nWhenever the changelog skill runs, it writes a Keep a Changelog entry and nothing else.\n\n## Derivation\n\nOnly restates that skill's own procedure.")
def m6(f):
    f["docs/facts/0003-release-14-shipped.md"] = art("0003-release-14-shipped", "Release 1.4 shipped on 14 October at 16:02", ["release"],
                                                     "Release 1.4 was tagged on 2026-10-14 at 16:02 UTC.", kind="environmental", **{"governed-by": "0001-weekly-releases"})
def m7(f):
    f["docs/facts/0003-release-bucket.md"] = art("0003-release-bucket", "Artifacts are stored in the release bucket", ["release"],
                                                 "Release artifacts upload to the shared bucket.", kind="environmental", **{"governed-by": "0001-weekly-releases"})
def m8(f): add_guardrail(f, "smoke-test-before-deploy", "Every deploy runs the smoke test first",
                         "## Guardrail\n\nBefore any deploy, the deploy checklist runs the smoke test suite and aborts on failure.\n\n## Derivation\n\nA failed deploy costs a weekly release.")
def m9(f): sub(f, "Steps:", "Steps (see docs/guardrails/retired-rule.md):", "docs/skills/deploy-checklist.md")
def m10(f): sub(f, "Steps: update CHANGELOG.md, tag the release, run the release job.",
                "Steps: update CHANGELOG.md, and when you update the changelog you should make sure the changelog is updated, "
                "because the changelog needs to be up to date; then tag the release, which means creating the release tag, "
                "and then run the release job, which is the job that does the release, so that the release is released.", "docs/skills/deploy-checklist.md")
def m11(f): add_guardrail(f, "changelog-and-linked-issue", "Releases need a changelog entry and every PR needs a linked issue",
                          "## Guardrail\n\nEvery release carries a changelog entry. Separately, every pull request must link an issue.\n\n## Derivation\n\nWeekly cadence; PR-only merges.")
def m12(f): f["plugins/kms/templates/guardrails/missing-here.md"] = "---\ntemplate-version: 1\nid: missing-here\ntitle: A template\n---\n"
def m13(f):
    f["docs/decisions/archive/0004-monthly-reviews.md"] = art("0004-monthly-reviews", "Review the guardrails monthly", ["process-review"], "## Decision\n\nReview monthly.\n",
                                                              status="superseded", track="process", **{"superseded-by": "0005-quarterly-reviews"})
    f["docs/decisions/0005-quarterly-reviews.md"] = art("0005-quarterly-reviews", "Review the guardrails quarterly", ["process-review"], "## Decision\n\nReview quarterly, not monthly.\n", track="process")
    add_guardrail(f, "monthly-guardrail-review", "Guardrails are reviewed every month", "## Guardrail\n\nReview every guardrail once a month.\n\n## Derivation\n\nFollows the monthly review decision.",
                  **{"governed-by": "0005-quarterly-reviews", "grounded-in": ["0004-monthly-reviews"], "tags": ["process-review"]})
    sub(f, "git — git workflow", "git — git workflow\nprocess-review — how guardrails are reviewed", "docs/skills/tags.md")
def m14(f): sub(f, "ci owner — last matched a decision 2026-10-24", "ci owner — last matched a decision 2026-10-24\ndata-privacy officer — last matched a decision 2025-02-10", "docs/skills/process-track-roles.md")
def m15(f): sub(f, "track: process", "track: both", "docs/decisions/0003-pr-before-merge.md")
def m16(f): f.update({"docs/decisions/0004-monthly-releases.md": art("0004-monthly-releases", "Ship a release once a month", ["release"], "## Decision\n\nCut a release on the first Thursday of each month; weekly releases are too frequent.\n", track="process")})
def m17(f): add_guardrail(f, "sign-release-tags", "Release tags are signed", "## Guardrail\n\nTBD\n", status="draft", date="2025-12-01",
                          **{"governed-by": "TBD", "grounded-in": "TBD", "derivation-note": "TBD"})
def m18(f): sub(f, "(last verified 2026-10-30)", "(last verified 2025-01-15)", "docs/decisions/0001-weekly-releases.md")
def m19(f): pass
def m20(f): sub(f, "status: active", "status: superseded\nsuperseded-by: 0001-weekly-releases", "docs/decisions/0003-pr-before-merge.md")
def m21(f): sub(f, "tags:\n- git", "tags:\n- gitt", "docs/facts/0002-ci-runs-on-pr.md"); sub(f, "tags: [git]", "tags: [gitt]", "docs/facts/0002-ci-runs-on-pr.md")
def m22(f): sub(f, "git — git workflow", "git — git workflow\nlegacy-api — the v1 HTTP API (no artifact has used this tag since 2025-01)", "docs/skills/tags.md")
def m23(f): add_guardrail(f, "tag-and-push-every-release", "Every release is tagged and the tag pushed",
                          "## Guardrail\n\nFor each release: create an annotated tag, push it, confirm CI picked it up, then announce it.\n\n## Derivation\n\nWeekly cadence.")
def m24(f): sub(f, "### 2. [pending] Add the tag step", "### 2. [done] Add the tag step", "docs/plans/release-automation.md")


def p19(f): sub(f, "Ship a release every week", "Ship a release every day", "docs/decisions/INDEX.md")


MUTATIONS = {  # check -> (pre, post, cofires)
    1: (m1, None, []), 2: (m2, None, []), 3: (m3, None, []), 4: (m4, None, []), 5: (m5, None, []),
    6: (m6, None, [7]), 7: (m7, None, []), 8: (m8, None, []), 9: (m9, None, []), 10: (m10, None, []),
    11: (m11, None, []), 12: (m12, None, []), 13: (m13, None, []), 14: (m14, None, []), 15: (m15, None, []),
    16: (m16, None, []), 17: (m17, None, []), 18: (m18, None, []), 19: (m19, p19, []), 20: (m20, None, []),
    21: (m21, None, []), 22: (m22, None, []), 23: (m23, None, []), 24: (m24, None, []),
}


def write_indexes(files):
    for t in ("facts", "decisions", "guardrails", "skills"):
        for arch in (False, True):
            prefix = f"docs/{t}/" + ("archive/" if arch else "")
            rows = []
            for k in sorted(files):
                if k.startswith(prefix) and k.endswith(".md") and "/" not in k[len(prefix):] and not k.endswith("INDEX.md"):
                    fm, _ = split_frontmatter(files[k])
                    tags = ", ".join(map(str, fm["tags"]))
                    rows.append('"{}","{}","{}",{}'.format(fm["id"], fm["title"], tags, fm["status"]))
            if rows:
                files[prefix + "INDEX.md"] = "id,title,tags,status\n" + "\n".join(rows) + "\n"


def make_case(target):
    files = base()
    post, cofires = None, []
    if target is not None:
        pre, post, cofires = MUTATIONS[target]
        pre(files)
    write_indexes(files)
    if post:
        post(files)
    return files, cofires


PROMPT = (
    "Lint the knowledge base. After completing your analysis, end your response with exactly one line, "
    "`LINT_FINDINGS:` followed by the comma-separated numbers of every lint check (1-24) for which you found at "
    "least one violation, or `NONE` if the knowledge base has no violations. Report only what you verified."
)


def build():
    """Return {relative path: text} for everything this script owns under evals/lint-matrix/."""
    out, labels = {}, {}
    for target in [None] + sorted(MUTATIONS):
        name = "clean" if target is None else f"c{target:02d}"
        files, cofires = make_case(target)
        for rel, text in files.items():
            out[f"cases/{name}/{rel}"] = text
        found = sorted({c for c, _, _ in Linter_run(files)})
        bad = [c for c in found if c != target and c not in cofires]
        if bad or (target in STRUCTURAL and target not in found) or (target is None and found):
            raise SystemExit(f"{name}: checker reports {found}, expected target {target} plus {cofires}")
        labels[name] = {"target": target, "expected": sorted(set(found) | ({target} if target else set()))}
    out["labels.json"] = json.dumps({"structural": STRUCTURAL, "judgment": JUDGMENT, "cases": labels}, indent=1) + "\n"
    tests = "\n".join(f'  - description: "{n}"\n    vars:\n      fixture_dir: "evals/lint-matrix/cases/{n}"' for n in labels)
    out["promptfooconfig.yaml"] = (
        "# Generated by build.py; do not edit. Run: npx promptfoo eval -c evals/lint-matrix/promptfooconfig.yaml --repeat 5 -o out.json\n"
        "# Score: python3 evals/lint-matrix/score.py out.json\n"
        'description: "kms lint matrix: clean control plus one seeded violation per check"\n'
        f"prompts:\n  - >\n    {PROMPT}\n"
        "providers:\n  - id: \"exec:../providers/kilo-runner.sh\"\n    config:\n      model: \"cohere/north-mini-code:free\"\n      timeout_seconds: 1440\n"
        f"tests:\n{tests}\n")
    return out


def Linter_run(files):
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        for rel, text in files.items():
            p = Path(d, rel)
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        return Linter(d).run()


def main():
    out = build()
    if "--check" in sys.argv:
        stale = [k for k, v in out.items() if not (HERE / k).exists() or (HERE / k).read_text(encoding="utf-8") != v]
        on_disk = {str(p.relative_to(HERE)) for p in (HERE / "cases").rglob("*") if p.is_file()}
        stale += sorted(on_disk - set(out))
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
