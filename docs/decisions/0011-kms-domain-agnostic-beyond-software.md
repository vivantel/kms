---
id: 0011-kms-domain-agnostic-beyond-software
title: Generalize clarify/roadmap/bootstrap/steward beyond software projects
status: accepted
date: 2026-08-30
tags: [kms, knowledge-management, agent-agnostic]
track: product
---

## Decision

`clarify`, `roadmap`, `bootstrap`, and `steward` are generalized to work
for any git-based project, not only software ones — their instructions
should read as naturally for a research paper or a business plan as for
a codebase.

`attribute` and `changelog` stay scoped to git commit history as they
are today: both require a commit history to act on at all, so there's
nothing to generalize away from — a project with no commits has nothing
for either skill to do, software or not.

The storage substrate — a git repository with Markdown files under
`docs/{facts,decisions,guardrails,skills}/` — is unchanged. This is not
a move to a storage-agnostic knowledge system; git-plus-Markdown remains
the one supported mechanism.

`bootstrap` is the only skill with actual software-specific language
today (`clarify`/`roadmap`/`steward` already have none — confirmed by
grepping all four bodies for software/git terms): git-log-only phrasing
in its intent-extraction step, a CI/build-only framing in its
fitness-function step, and a skill-gap-detection table with exclusively
software rows. See
`docs/plans/product-process-track-and-domain-agnostic-scope.md` for the
specific wording changes.

## Why

The user has already used this exact toolchain for scientific articles,
git-versioned like a software project — real evidence the underlying
mechanism (facts/decisions/guardrails, interviewed and maintained across
sessions) isn't actually software-specific, only some of `bootstrap`'s
example wording is. Fixing the wording, not the mechanism, is the
accurate scope of this change.

Keeping the storage substrate as git+Markdown, rather than abstracting
over other backends, keeps this cheap to bootstrap and maintain — the
explicit design goal stated alongside this request — instead of taking
on a much larger, differently-scoped project.

`attribute`/`changelog` are the two skills whose entire function is
reading/writing git commit history; generalizing "beyond software"
doesn't change what a commit is, so there's no version of these two
skills that isn't git-shaped.

## Tradeoffs considered

- **Generalize attribute/changelog too**, e.g. some abstract "change
  record" concept: rejected — unclear what a "commit" even generalizes
  to outside git, and no concrete need surfaced for it; deferred rather
  than speculatively designed.
- **Abstract the storage substrate away from git+Markdown**: rejected —
  much larger scope, works against the "cheap to bootstrap and maintain"
  goal this same request stated.
- **Chosen: generalize bootstrap's wording** (the only skill that needed
  it); leave the git+Markdown substrate and the two git-native skills as
  they are.
