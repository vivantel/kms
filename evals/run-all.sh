#!/bin/sh
# Runs every CI skill eval case; arguments (e.g. --repeat 3) are passed to each `promptfoo eval`.
for c in attribute bootstrap capture conform decide lint lint-clean query roadmap uninstall; do
  echo "=== evals/$c ==="
  npx promptfoo eval -c "evals/$c/promptfooconfig.yaml" "$@" || exit 1
done
