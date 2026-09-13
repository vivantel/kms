---
id: confirming-party-acceptable-for-checkpoint-gates
title: A confirmation gate must accept a human or an authorized reviewing subagent, never assume human-only
status: active
date: 2026-09-13
tags: [kms, knowledge-management, automation, guardrail]
governed-by: [0057-confirming-party-generalizes-human-checkpoint]
grounded-in: [0057-confirming-party-generalizes-human-checkpoint]
derivation-note: 0057 commits to generalizing lint's "wait for human confirmation" gate to "wait for a
  confirming party." This guardrail is the resulting normative rule lint's gate must satisfy now, and any
  future gate (new or reworded) must satisfy going forward.
---

## Guardrail

`lint`'s confirmation gate must address "a confirming party" — not assume that party is necessarily
human. Any new confirmation gate this plugin adds, or any existing one reworded going forward, must do
the same. kms itself must not define or ship an authority-configuration mechanism for a reviewing
subagent; that remains the deploying environment's concern. This does not yet require rewording every
other skill's existing human-phrased gate (`roadmap`, `clarify`, `capture`, `attribute`, `refactor-plan`,
`uninstall`) — that generalization is deliberately deferred, per `0057-...`'s own scope note.
