#!/bin/sh
# Nudges toward running the lint skill when enough recent commits have
# touched the knowledge base to make a full validation pass worthwhile —
# an approximation of "the KB has churned enough that drift may have
# accumulated." See docs/skills/automating-lint-nudge.md and
# docs/decisions/0055-automate-lint-nudge-hook.md for why this heuristic
# exists and its known imprecision.

window_days=14   # see docs/skills/automating-lint-nudge.md
threshold=5      # commits touching the KB in that window

# `git rev-parse --is-inside-work-tree` exits 0 even in a bare repo or a
# cwd inside .git, printing "false" in that case — check the printed
# value, not just the exit code (same guard as capture-nudge.sh).
inside_work_tree=$(git rev-parse --is-inside-work-tree 2>/dev/null)
[ "$inside_work_tree" = "true" ] || exit 0

# Knowledge directory, in the artifact model's order: `kms-dir:` in the
# AGENTS.md kms block, .vivantel/akasha/docs, docs/ holding decisions/,
# else the first top-level directory holding decisions/.
kb=
if [ -f AGENTS.md ]; then
  kb=$(sed -n '/<!-- kms:start -->/,/<!-- kms:end -->/{s/^[[:space:]]*kms-dir:[[:space:]]*\([^[:space:]]*\).*/\1/p;}' AGENTS.md | head -n 1)
  kb=${kb%/}
  case "$kb" in /*|*..*) kb= ;; esac
fi
if [ -z "$kb" ]; then
  if [ -d .vivantel/akasha/docs ]; then kb=.vivantel/akasha/docs
  elif [ -d docs/decisions ]; then kb=docs
  else
    kb=docs
    for d in */; do
      if [ -d "${d}decisions" ]; then kb=${d%/}; break; fi
    done
  fi
fi

count=$(git log --oneline --since="${window_days} days ago" -- \
  "$kb/facts" "$kb/decisions" "$kb/guardrails" "$kb/skills" 2>/dev/null \
  | wc -l | tr -d ' ')

if [ "$count" -ge "$threshold" ]; then
  echo "This knowledge base has had $count commit(s) touching $kb/{facts,decisions,guardrails,skills}/ in the last $window_days days. If relevant, mention to the user that running this plugin's lint skill would check the whole knowledge base for drift, contradictions, or stale debt that individual sessions wouldn't catch."
fi
