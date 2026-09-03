<!-- kms-generated: true -->
# Guardrails index (TOON)

id,title,tags,status
agent-agnostic-skill-content,"Skill instruction bodies must stay agent-neutral","kms, agent-agnostic, guardrail",active
decision-expires-must-be-reevaluated,"An artifact past its expires date or condition must be re-evaluated","kms, knowledge-management, guardrail",active
decision-track-field,"Every decision must declare its track","kms, knowledge-management, guardrail",active
every-skill-ships-examples,"Every skill must ship a colocated examples.md","kms, packaging, documentation, guardrail",active
fact-governance-fields,"Facts must declare their kind and governing decision","kms, knowledge-management, guardrail",active
fact-not-audit-log,"A fact must not be an ungrounded audit-log record","kms, knowledge-management, guardrail",active
guardrail-derivation-fields,"Guardrails must declare their derivation","kms, knowledge-management, guardrail",active
guardrail-re-derivation-on-source-change,"A guardrail must be re-derived when its governing decision or grounding fact changes","kms, knowledge-management, guardrail",active
lifecycle-status-values,"status must be draft, active, superseded, or deprecated — for any of the four artifact types","kms, knowledge-management, guardrail",active
no-redundant-guardrails,"A guardrail true only \"whenever skill X does Y\" belongs in skill X's own body","knowledge-management, guardrail",active
no-unenforced-guardrail,"A guardrail describing shipped behavior is incomplete until that behavior's own body says so too","knowledge-management, guardrail",active
one-statement-one-job,"A fact, guardrail, or derivation-note doing two things must be split","knowledge-management, guardrail",active
plugin-manifest-version-sync,"Every plugin manifest's version field must be bumped together","kms, agent-agnostic, codex, kilo, packaging, guardrail",active
superseded-decision-requires-pointer,"A decision marked superseded must name what superseded it","kms, knowledge-management, guardrail",active
tags-from-canonical-list,"Any artifact's tags must come from the canonical tag list, when one exists","kms, knowledge-management, guardrail",active
token-economy,"Every fact, guardrail, and procedure must be maximally economical","kms, knowledge-management, guardrail",active
