
import json
import os
from datetime import datetime

MEMORY_PATH = "memory.json"
QUEUE_PATH = "mutation_queue.json"

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def create_mutation(description, target, patch_code):
    return {
        "mutation_name": description,
        "target_file": target,
        "patch": patch_code,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }

def reflex_scan():
    memory = load_json(MEMORY_PATH)
    queue = load_json(QUEUE_PATH)

    mutations = []

    for goal in memory.get("goals", []):
        desc = goal.get("description", "").lower()
        if "refactor" in desc or "optimize" in desc:
            mutations.append(create_mutation(
                "inject_refactor_hook",
                "main.py",
                "# Auto-refactor placeholder triggered by memory reflex"
            ))
        if "log identity" in desc or "monitor flamechain" in desc:
            mutations.append(create_mutation(
                "inject_flamechain_monitor",
                "main.py",
                "# Flamechain identity monitor stub injected"
            ))

    if mutations:
        queue["mutations"] = queue.get("mutations", []) + mutations
        save_json(QUEUE_PATH, queue)
        print(f"[Reflex] {len(mutations)} reflex mutation(s) queued.")
    else:
        print("[Reflex] No reflex mutations triggered.")

if __name__ == "__main__":
    reflex_scan()
