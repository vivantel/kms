<!-- kms-generated: true -->
# Decisions index (TOON)

id,title,tags,status
0001-knowledge-artifact-storage-convention,"Knowledge artifacts live under docs/{facts,decisions,guardrails,skills}/","kms, roadmap, knowledge-management",active
0002-commit-pr-attribution-skill-design,"Split commit/PR/changelog work into two skills, added to the kms plugin","kms, git, commit-messages, pull-requests",active
0003-commit-trailer-traceability,"Use a \"Refs:\" git trailer to link commits to knowledge artifacts, one-directionally","kms, git, traceability",active
0004-conventional-commits-adoption,"Adopt Conventional Commits type prefixes, applied only when the attribute skill is invoked","kms, git, commit-messages",active
0005-changelog-generation-design,"Thin, on-demand changelog skill reading from commit trailers","kms, git, changelog",active
0007-claude-md-agents-md-symlink,"Rewrite CLAUDE.md as AGENTS.md, keep CLAUDE.md as a symlink","kms, agent-agnostic, claude-md, agents-md",active
0008-native-codex-plugin-support,"Ship a native Codex plugin manifest for the kms skill set; keep the current directory layout; defer Cursor","kms, agent-agnostic, codex, packaging",active
0009-bootstrap-and-steward-skills,"Add bootstrap and steward as two skills, not one combined skill","kms, knowledge-management",active
0010-decision-track-field,"Add a track field (product | process) to decisions","kms, knowledge-management",active
0011-kms-domain-agnostic-beyond-software,"Generalize clarify/roadmap/bootstrap/steward beyond software projects","kms, knowledge-management, agent-agnostic",active
0012-no-redundant-guardrails,"A guardrail must not be a pure restatement of one skill's own procedure","kms, knowledge-management",active
0013-ai-agent-role-lists-per-track,"bootstrap creates, steward maintains, product/process role lists for reviewing decisions","kms, knowledge-management",active
0014-decision-scope-and-expires-fields,"Add optional scope and expires fields to decisions","kms, knowledge-management",active
0015-facts-must-not-be-audit-log-records,"Facts must not be audit-log records","kms, knowledge-management",active
0016-lint-skill,"Add lint — an on-demand, full-repo validation skill, separate from steward","kms, knowledge-management",active
0017-query-skill,"Add query — an on-demand skill that answers questions from the knowledge base with citations","kms, knowledge-management",active
0018-per-skill-examples-convention,"Every skill ships a colocated examples.md with 2-3 worked usage examples","kms, packaging, documentation",active
0019-brainstorm-skill,"Add brainstorm — a generative, write-nothing ideation skill","kms, ideation",active
0020-onboard-skill,"Add onboard — a role-tailored, read-only onboarding-plan skill","kms, knowledge-management",active
0021-refactor-plan-skill,"Add refactor-plan — a phased, guardrail-respecting refactor-planning skill","kms, knowledge-management",active
0022-vivantel-kms-display-name,"Display name becomes \"Vivantel KMS\", technical identifiers stay \"kms\"","kms, naming, branding",active
0023-quickstart-skill,"Add quickstart — bootstrap plus one real decision captured live","kms, onboarding, knowledge-management",active
0024-automate-steward-nudge-hook,"Ship a Claude Code SessionStart hook that nudges toward steward after a recent commit","kms, automation, claude-code, hooks",active
0025-discoverability-improvements,"Improve discoverability — README badges, GitHub topics and description sync","kms, discoverability, marketing",active
0026-token-economy-guardrail,"Promote token economy from unenforced steward prose to a governed, checked guardrail","kms, knowledge-management, guardrail",active
0027-baseline-guardrail-seeding,"Ship kms's four Global Principles as templated, synced baseline guardrails","kms, knowledge-management, guardrail, packaging",active
0028-generalize-templates-sync-scope,"Generalize the templates sync mechanism from guardrails-only to any artifact type","kms, knowledge-management, packaging",active
0029-bootstrap-full-traceability,"Make every bootstrap output traceable back to kms, and wire a pointer into the project's own agent-instructions file","kms, knowledge-management, packaging",active
0030-uninstall-skill,"Add uninstall — a manual pre-uninstall step that reverses everything bootstrap adds","kms, knowledge-management, packaging",active
0031-consolidate-kb-checks-rename-capture,"Permanently move duplicated KB checks into lint; narrow and rename steward to capture","kms, knowledge-management, packaging",active
0032-conform-skill,"Add conform — validates a pending changeset against existing decisions and guardrails","kms, knowledge-management",active
0033-kms-architecture-doc,"Add a single reference doc synthesizing kms's own layers and marker conventions","kms, knowledge-management, documentation",active
0034-shared-artifact-model,"Extract the shared artifact-type model into one file, read by sibling reference","kms, knowledge-management, packaging",active
0035-native-kilo-code-support,"Ship a self-hosted Kilo remote-skills index; list on kilo-marketplace; no directory restructuring","kms, agent-agnostic, kilo, packaging",active
0036-standalone-installing-doc,"Extract per-agent install steps into a standalone INSTALLING.md","kms, discoverability, packaging",active
0037-plans-not-a-governed-artifact-type,"Plans are not a 5th governed artifact type","kms, knowledge-management, taxonomy",active
0038-track-field-mutual-exclusivity,"track values are mutually exclusive; \"both\"/\"mixed\" is never stored","kms, knowledge-management, taxonomy",active
0039-unify-lifecycle-and-drop-scope,"Unify status and expires across all four artifact types; add superseded-by; drop scope","kms, knowledge-management, taxonomy",active
0040-lint-contradiction-and-staleness-checks,"Add lint checks for cross-artifact contradiction, stale debt, and stale fitness-functions","kms, knowledge-management, taxonomy",active
0041-index-and-archive-for-scale,"Add a per-type TOON index and an archive mechanism for superseded/deprecated artifacts","kms, knowledge-management, scale",active
0042-tag-vocabulary-and-scoped-contradiction-check,"Add a canonical tag vocabulary; scope the contradiction check to tag overlap","kms, knowledge-management, scale",active
