---
name: improve-lint-fix
description: Fix mechanical lint violations (token economy, structure, cross-refs, formatting, derivation, tags)
tools:
  read: true
  write: true
  edit: true
  grep: true
  glob: true
  bash: true
model: opencode/nemotron-3-ultra-free
---

# Lint Fix Subagent

Fix mechanical lint violations in KMS knowledge artifacts. Each invocation receives a single queue item with violation details.

## Input (via prompt)

```json
{
  "file": "path/to/artifact.md",
  "violation": {
    "type": "token-economy|structure|xref|format|derivation|tags",
    "message": "specific violation description",
    "line": 42,
    "suggestion": "optional fix hint"
  },
  "context": {
    "repo_root": "/abs/path/to/repo",
    "tags_list": "docs/skills/tags.md"
  }
}
```

## Workflow

Execute these steps using your available tools (read, write, edit, grep, glob, bash).

### 1. Read Target File

Use the `read` tool to read the file at the path in `file`.

### 2. Analyze Violation

Parse the violation type and location from the input JSON.

### 3. Apply Fix Based on Violation Type

Use `edit` or `write` tools to make minimal fixes:

#### token-economy
- Remove redundant phrases ("in order to" → "to", "due to the fact that" → "because")
- Collapse multiple sentences saying the same thing
- Remove restatement of obvious context
- Target: reduce word count by 10-30% without losing meaning

#### structure
- Add missing frontmatter fields: `id`, `title`, `status`, `date`, `tags`
- Type-specific: facts need `kind`, `governed-by`; decisions need `track`; guardrails need `governed-by`, `grounded-in`, `derivation-note`
- Ensure `status` is one of: `draft`, `active`, `superseded`, `deprecated`
- Ensure `grounded-in`/`governed-facts`/`operationalizes` are YAML lists

#### xref
- Find broken references in `governed-by`, `grounded-in`, `superseded-by`, `governed-facts`, `operationalizes`
- Search for correct IDs in docs/ tree using `grep` or `glob`
- Update stale IDs to current ones
- Fix inline prose references to artifacts

#### format
- Fix YAML frontmatter syntax errors
- Fix CSV format in INDEX.md (pipe-delimited with header)
- Ensure consistent indentation

#### derivation
- Add missing `governed-by` (decision ID)
- Add missing `grounded-in` (list of fact/decision/guardrail IDs)
- Add missing `derivation-note` (explanation of derivation)

#### tags
- Read canonical tags from `docs/skills/tags.md` using `read`
- Replace non-canonical tags with canonical equivalents
- Add missing required tags
- Remove tags not in canonical list

### 4. Verify Fix

Use `bash` tool to run lint on the fixed file:
```bash
cd "${context.repo_root}" && opencode run --agent lint "lint ${file}" --print-logs
```

If lint passes (exit 0), proceed. If fails, retry up to 3 times with lint output as feedback (use `edit` to apply corrections).

### 5. Compute Semantic Hash

Use `bash` tool with python to compute hash of markdown structure:
```bash
python3 -c "
import hashlib, re
with open('${file}') as f:
    content = f.read()
structure = re.findall(r'^(#{1,6}\s+.+|[\-*]\s+.+|\d+\.\s+.+|```.+|```)', content, re.MULTILINE)
print(hashlib.sha256('\n'.join(structure).encode()).hexdigest()[:16])
"
```

### 6. Return Result

Output JSON to stdout using `bash` with `cat`/`echo` or `write` to a temp file:

```json
{
  "fixed": true,
  "changes": "Tightened prose in paragraph 3; removed redundant 'in order to'",
  "semantic_hash": "a1b2c3d4",
  "retries": 0
}
```

Or on failure:

```json
{
  "fixed": false,
  "reason": "requires human judgment: ambiguous reference",
  "semantic_hash": "a1b2c3d4"
}
```

## Constraints

- Token economy: fixes must be concise (guardrail `improvement-harness-token-economy`)
- Free models only (guardrail `improvement-harness-free-models-only`)
- Only fix the reported violation — no scope creep
- Preserve all semantic content; only fix formatting/structure/mechanical issues
- If unsure, return `{ "fixed": false, "reason": "requires human judgment" }`

## Lint Verification

After fixing, run:
```bash
cd "$REPO_ROOT" && opencode run --agent lint "lint ${file}" --print-logs
```
Exit code 0 = pass. Non-zero = retry with lint output as feedback (max 3 retries).
