## Admission

Before drafting a fact, decision, guardrail or procedure, decide whether the change is worth a record at all. Reject if a hard gate fails; say which gate failed, in one line.

Hard gates:
- **Not already carried**: not stated in code, tests, config, tooling, history or a sibling record, and not a mechanical repeat of an enforced check. "Carried" means recoverable by one grep of the fact's own `source` path or of one file the reader would find first. A fact that aggregates two or more sources, or locates something not greppable (an external system, a vault path, a dashboard, a vendor limit), is admissible uncited. A decision is carried only if the sources also state its reason and the rejected alternative. A fact cited by a decision is not carried by its citer.
- **Right shape**: one claim; no contact details or secret. Name a role or system, not a person; `accepted-by` is the one field that may name a person, because it records accountability, and may hold a role or team instead.
- **Recurrence (guardrails)**: applies to every future occurrence of a kind of change. A prohibition from one incident is admitted only with a stated cause that generalises.

Then estimate **shelf life** (how long it stays true; a decision is valid until superseded), **recurrence** (how likely a different future task meets the same question) and **rediscovery cost** (tool calls, minutes, or asking another actor). Admit when shelf life times recurrence clearly exceeds rediscovery cost and a future agent would act differently knowing it. If the knowledge base already holds a record the change contradicts or supersedes, update it instead of adding one.

A raw reading, run result, status or timestamped event is rejected, except an incident-grounded fact that a guardrail cites in `grounded-in`, which retires with that guardrail. A scoped claim with a source (a contract term, a vendor limit, a permanent state change) can be a fact. Legacy records predating this test are not split retroactively; the one-claim gate applies to new and re-derived records.

Typical rejections: a rename or move visible in the diff, a one-line config or hygiene change, a CI result, who did what when, a meeting or on-call entry, "be careful" or "write tests" rules, a rule a lint or test already enforces. A risk that changes behaviour becomes a guardrail; an assumption a decision rests on becomes a fact with `source`; an open question or hypothesis is a `status: draft` decision with `expires-when` and the tag `question`.

Type for a pointer: a required path through another actor is a procedure; a static location is a fact; a standing consent before an action is a guardrail.

## Economy

A fact, guardrail or procedure uses the shortest phrasing that preserves meaning. Before calling a new one done, re-read it for restatement of a point made earlier in the file or in a sibling from the same pass, and for length; tighten before finishing.
