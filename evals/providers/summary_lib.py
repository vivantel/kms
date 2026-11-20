"""Classification helpers for post-eval-summary.py (kept apart so they are unit-testable)."""

MARKER = "=== HARNESS ERROR"


def is_infra(result):
    """True when a failed promptfoo result is a harness failure, not a graded skill failure."""
    out = (result.get("response") or {}).get("output") or ""
    err = result.get("error") or (result.get("response") or {}).get("error") or ""
    return MARKER in str(out) or MARKER in str(err)


def split_failures(results):
    """(skill_failures, infra_failures) over the unsuccessful results."""
    bad = [r for r in results if not r.get("success")]
    infra = [r for r in bad if is_infra(r)]
    return [r for r in bad if not is_infra(r)], infra
