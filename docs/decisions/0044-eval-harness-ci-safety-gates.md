---
id: 0044-eval-harness-ci-safety-gates
title: Wire the eval harness into CI with fork and comment safety gates
status: active
date: 2026-09-04
tags: [kms, eval-harness]
track: process
---

## Decision

- Full GitHub Actions workflow from day one — not a local-only-first phase — using `promptfoo-action`.
- Trigger: the `pull_request` event, restricted to `types: [opened]` (never `pull_request_target`, which exposes secrets to fork-originated PRs), targeting `master` only. `types: [opened]` is required, not optional decoration — GitHub's `pull_request` event defaults to firing on `opened`, `synchronize` (every push), and `reopened` when no `types:` filter is given, which would silently re-run on every push and defeat the frequency limit below.
- **Fork-guard**: the job is skipped entirely when `github.event.pull_request.head.repo.fork == true`. A fork PR gets neither the `OPENROUTER_API_KEY` secret nor an autonomous-agent run against its content at all — not even a secret-less one.
- **Path-filter**: only triggers on changes under `plugins/kms/skills/**` and `plugins/kms/shared/**`.
- **Frequency**: runs once when a same-repo PR targeting `master` opens; re-runs on demand via a PR comment (e.g. `/eval`) rather than on every push, given OpenRouter's 200-request/day free cap (`docs/facts/0010-openrouter-free-tier-terms.md`). The comment trigger requires **both** gates, not just one: the commenter's `author_association` must be `OWNER`, `MEMBER`, or `COLLABORATOR` (on a public repository, commenting doesn't require write access even when the underlying PR is same-repo, so an ungated comment trigger would reopen the "unknown party can trigger this" risk the fork-guard closes on the PR-open side) — **and** the PR being commented on must itself not be fork-originated, checked via an API call (`gh pr view <number> --json isCrossRepository` or equivalent), since `issue_comment` event payloads carry no `head.repo.fork` field the way `pull_request` payloads do. Without this second check, a legitimate collaborator commenting `/eval` on someone else's fork-originated PR would still trigger an autonomous run against that fork's content — exactly what the fork-guard exists to prevent on the PR-open path.
- `--max-cost-usd` is set as a defensive ceiling despite both models being free-tier, in case a free model's pricing status changes or a misconfiguration reaches a paid one.

`vivantel/kms` is a public repository, which is why this design — rather than one assuming a private repo's narrower audience — is necessary.

## Why

Built now rather than deferred to a later "local-only first" phase, because `promptfoo-action`'s actual value — native before/after PR comparison — only exists inside CI; deferring it indefinitely defers the value indefinitely too, the same failure mode that shelved this whole initiative once already (`docs/decisions/0040-lint-contradiction-and-staleness-checks.md`'s fitness-functions entry).

The security design answers a concrete, specific risk, not a generic one: an autonomous coding agent (Kilo, `--auto`, real tool access) executing against untrusted fork-PR content is a CI-abuse/supply-chain vector distinct from, and worse than, ordinary secret leakage. `pull_request_target` is the well-documented unsafe pattern that exposes secrets to fork PRs and must never be used here; `pull_request` alone already withholds secrets from forks, but the fork-guard goes further and prevents the autonomous run itself, since running arbitrary agent-driven tool calls against untrusted content carries real risk even with zero secrets in play. The comment-trigger gate closes a distinct gap the fork-guard doesn't touch: fork-blocking only protects the PR-*open* trigger, but a public repo lets anyone comment on anyone else's PR regardless of who opened it, so a re-run trigger with no `author_association` check would let an unrelated, unknown commenter fire the workflow against a legitimate collaborator's own PR.

## Tradeoffs considered

- **Local-only first, defer CI**: proves the harness before investing in automation, but the reason `promptfoo-action` exists at all never gets used without a concrete decision to eventually build it — indefinite deferral.
- **Every push re-triggers, no frequency limit**: freshest possible signal, but a single active afternoon of iterating on a PR could exhaust the entire daily free quota, leaving nothing for anything else that day.
- **Nightly on `master` only, no PR-time signal**: cheapest and simplest, but loses the actual "before/after this specific change" comparison that's the whole point of adopting this.
- **A trusted-fork allowlist instead of a blanket fork-block**: more useful if this repo expects external contributions worth evaluating, but adds a list to maintain for a repo with no evidence yet of needing it.
- **Chosen**: full CI now, `pull_request` only, fork-guard + path-filter + `author_association`-gated comment retrigger, defensive cost ceiling.

## Amendment (implementation-time, 2026-09-05)

`promptfoo` has no `--max-cost-usd` flag or equivalent cost-ceiling option (verified against its
current CLI reference) — this decision's "defensive cost ceiling" doesn't exist as a literal
flag to pass. The substitute, serving the same purpose (bound worst-case spend/runtime if a
free model's pricing status changes or a misconfiguration reaches a paid one): every case's
`promptfooconfig.yaml` pins an explicit `:free`-suffixed model id (visible in code review, not a
runtime default that can silently drift to a paid model), plus a `timeout-minutes: 20` ceiling
on each matrix job in `.github/workflows/eval-skills.yml`.

Also: the `permissions:` block needs no `models: read` scope — that was for GitHub Models
access, which `docs/decisions/0043-eval-harness-for-shipped-skill-changes.md`'s amendment
records as fully retired; the judge model is OpenRouter now, reached the same way the runner is.

## Amendment (implementation-time, 2026-09-10)

`docs/decisions/0043-...`'s 2026-09-10 amendment moved both the runner and judge off OpenRouter
entirely, onto Kilo's own built-in free gateway (no account, no API key). Consequence for this
decision: the CI workflow (`.github/workflows/eval-skills.yml`) needs **no secret at all** —
every `OPENROUTER_API_KEY` reference (`env:` blocks, the line above) is gone, and this repo
never provisions or stores an OpenRouter key. `npm install -g @kilocode/cli` replaces it as the
one thing each job installs before running. Every other gate in this decision (fork-guard,
path-filter, `author_association` + cross-repo check on the comment retrigger, the timeout
ceiling from the amendment above) is unaffected — none of them were about *which* model backend
was in use.

## Amendment (implementation-time, 2026-09-10)

"No secret at all," above, held only briefly: `PROMPTFOO_API_KEY` is now a CI secret after all
— see `docs/decisions/0043-...`'s matching amendment for why (promptfoo's own hosted "share"
feature is the only way to get a real, working results link in the PR comment instead of dead
text). Every safety gate this decision defines is orthogonal to that and still applies
unchanged: the fork-guard still withholds this secret (and every other) from fork-originated
PRs exactly as before — one more secret in the same `env:` block doesn't change what the
fork-guard's `if:` condition protects.

Separately, but discovered at the same time: `promptfoo-action`'s built-in PR comment never
named which matrix case (`bootstrap`/`roadmap`/`capture`/`lint`/`attribute`) it was reporting
on — running 5 cases in a matrix posted 5 byte-for-byte-identical comments, indistinguishable
from the PR itself. Disabled (`disable-comment: true`) in favor of
`evals/providers/post-eval-comment.py`, one clearly-labeled comment per case, run after the
export step this decision's earlier amendment already added.
