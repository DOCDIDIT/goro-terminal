
import json
import os
from datetime import datetime

MEMORY_PATH = "memory.json"
QUEUE_PATH = "mutation_queue.json"

def generate_self_mutations():
    print("[Genesis] Starting mutation genesis scan...")

    # Load memory.json
    if not os.path.exists(MEMORY_PATH):
        print("[Genesis] memory.json not found.")
        return

    with open(MEMORY_PATH, "r") as f:
        memory = json.load(f)

    flame_summary = memory.get("flame_summary", "")
    known_systems = memory.get("known_systems", [])

    # Example logic: If 'Terminal Goro' is not in known systems, propose adding it
    proposed_mutations = []
    if "Terminal Goro" not in known_systems:
        patch = "# Mutation: Add Terminal Goro to known systems\nmemory['known_systems'].append('Terminal Goro')"
        mutation = {
            "mutation_name": "add_terminal_goro",
            "target_file": "memory.json",
            "patch": patch
        }
        proposed_mutations.append(mutation)

    # Load or initialize the queue
    queue = {"mutations": [], "last_applied": None}
    if os.path.exists(QUEUE_PATH):
        with open(QUEUE_PATH, "r") as f:
            queue = json.load(f)

    # Inject new mutations if not already queued
    existing = [m.get("mutation_name") for m in queue.get("mutations", [])]
    for m in proposed_mutations:
        if m["mutation_name"] not in existing:
            queue["mutations"].append(m)
            print(f"[Genesis] Queued: {m['mutation_name']}")

    # Save updated queue
    with open(QUEUE_PATH, "w") as f:
        json.dump(queue, f, indent=2)

    print("[Genesis] Mutation generation complete.")

if __name__ == "__main__":
    generate_self_mutations()
