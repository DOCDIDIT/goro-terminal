
import json
import os
from datetime import datetime

QUEUE_PATH = "mutation_queue.json"
HISTORY_PATH = "mutation_history.json"

def log_applied_mutations():
    if not os.path.exists(QUEUE_PATH):
        print("[Logger] Mutation queue not found.")
        return

    if not os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "w") as f:
            json.dump({"history": []}, f, indent=2)

    with open(QUEUE_PATH, "r") as qf:
        queue = json.load(qf)

    with open(HISTORY_PATH, "r") as hf:
        history_data = json.load(hf)

    for mutation in queue.get("mutations", []):
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

if __name__ == "__main__":
    log_applied_mutations()
