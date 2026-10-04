import json, sys, os

queue_file = os.environ.get("QUEUE_FILE")
max_files = 10
lint_output_file = os.environ.get("LINT_OUTPUT_FILE")

try:
    with open(lint_output_file) as f:
        lint_result = json.load(f)
    violations = lint_result.get("violations", [])
    summary = lint_result.get("summary", {})
    total = summary.get("total_violations", 0)
    print(f"LINT_VIOLATIONS_BEFORE={total}")
    
    by_file = {}
    for v in violations:
        f = v["file"]
        if f not in by_file:
            by_file[f] = []
        by_file[f].append(v)
    
    limited_files = list(by_file.keys())[:max_files]
    
    items = []
    for f in limited_files:
        items.append({
            "type": "lint-fix",
            "file": f,
            "violations": by_file[f],
            "priority": 10,
            "source": "lint"
        })
    
    with open(queue_file, "r") as qf:
        queue = json.load(qf)
    queue["items"] = items
    queue["metadata"]["lint_violations_before"] = total
    with open(queue_file, "w") as qf:
        json.dump(queue, qf, indent=2)
    
    print(f"QUEUE_DEPTH={len(items)}")
except Exception as e:
    print(f"Error parsing lint output: {e}", file=sys.stderr)
    print("LINT_VIOLATIONS_BEFORE=0")
    print("QUEUE_DEPTH=0")