
import json
import os
from datetime import datetime

QUEUE_PATH = "mutation_queue.json"
HISTORY_PATH = "mutation_history.json"

def apply_mutation_queue():
    if not os.path.exists(QUEUE_PATH):
        print("[Mutation] No mutation queue found.")
        return

    try:
        with open(QUEUE_PATH, "r") as f:
            queue = json.load(f)

        mutations = queue.get("mutations", [])
        if not mutations:
            print("[Mutation] No pending mutations.")
            return

        for mutation in mutations:
            name = mutation.get("mutation_name")
            target_file = mutation.get("target_file")
            patch = mutation.get("patch")

            if not name or not target_file or not patch:
                print(f"[Mutation] Skipping invalid mutation: {mutation}")
                continue

            if not os.path.exists(target_file):
                print(f"[Mutation] Target file not found: {target_file}")
                continue

            with open(target_file, "r") as tf:
                content = tf.read()

            if patch in content:
                print(f"[Mutation] Already applied: {name}")
                continue

            with open(target_file, "a") as tf:
                tf.write(f"\n\n# Mutation: {name}\n{patch}\n")
                print(f"[Mutation] Applied: {name} to {target_file}")

        queue["last_applied"] = mutations[-1]["mutation_name"]
        queue["mutations"] = []

        with open(QUEUE_PATH, "w") as f:
            json.dump(queue, f, indent=2)

        log_applied_mutations(mutations)
        analyze_mutation_intel()

    except Exception as e:
        print(f"[Mutation Error] {str(e)}")


def log_applied_mutations(mutations):
    if not os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "w") as f:
            json.dump({"history": []}, f, indent=2)

    with open(HISTORY_PATH, "r") as hf:
        history_data = json.load(hf)

    for mutation in mutations:
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "mutation_name": mutation.get("mutation_name"),
            "target_file": mutation.get("target_file"),
            "patch": mutation.get("patch"),
            "status": "applied"
        }
        history_data["history"].append(entry)
        print(f"[Logger] Logged mutation: {entry['mutation_name']}")

    with open(HISTORY_PATH, "w") as hf:
        json.dump(history_data, hf, indent=2)

def analyze_mutation_intel():
    print("\n[Intel] Running post-mutation analysis...")
    with open(HISTORY_PATH, "r") as f:
        data = json.load(f)

    history = data.get("history", [])
    if not history:
        print("[Intel] No mutation history found.")
        return

    seen_targets = {}
    suggestions = []

    for m in history:
        name = m.get("mutation_name")
        file = m.get("target_file")
        patch = m.get("patch")
        timestamp = m.get("timestamp")

        if file not in seen_targets:
            seen_targets[file] = []
        seen_targets[file].append((name, patch, timestamp))

    for file, entries in seen_targets.items():
        if len(entries) > 2:
            suggestions.append({
                "target_file": file,
                "issue": "High mutation frequency",
                "recommendation": "Consider rewriting or consolidating this file."
            })

    if suggestions:
        print("[Intel] Recommendations:")
        for s in suggestions:
            print(f" - {s['target_file']}: {s['issue']} — {s['recommendation']}")
    else:
        print("[Intel] All systems stable. No optimization required.")

if __name__ == "__main__":
    apply_mutation_queue()
