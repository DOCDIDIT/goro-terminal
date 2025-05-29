
import json
import os
from datetime import datetime

HISTORY_FILE = "mutation_history.json"

def analyze_mutation_history():
    if not os.path.exists(HISTORY_FILE):
        print("[Intel] mutation_history.json not found.")
        return

    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)

    history = data.get("history", [])
    if not history:
        print("[Intel] No mutation history found.")
        return

    mutation_count = len(history)
    print(f"[Intel] {mutation_count} mutations found. Analyzing...\n")

    seen_targets = {}
    suggestions = []

    for m in history:
        name = m.get("mutation_name")
        file = m.get("target_file")
        patch = m.get("patch")
        timestamp = m.get("timestamp")

        # Track how many times each file is mutated
        if file not in seen_targets:
            seen_targets[file] = []
        seen_targets[file].append((name, patch, timestamp))

    for file, entries in seen_targets.items():
        if len(entries) > 2:
            suggestions.append({
                "target_file": file,
                "issue": "High mutation frequency",
                "recommendation": "Consider rewriting or consolidating this file. Goro has evolved it multiple times."
            })

    if suggestions:
        print("[Intel] Recommendations:")
        for s in suggestions:
            print(f" - {s['target_file']}: {s['issue']} — {s['recommendation']}")
    else:
        print("[Intel] No issues found. Mutation history is clean and well-distributed.")

if __name__ == "__main__":
    analyze_mutation_history()
