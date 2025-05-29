
import json
import os
from datetime import datetime

DELTA_LOG = "mutation_deltas.json"
MEMORY_PATH = "memory.json"

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def rewind_last_change():
    log = load_json(DELTA_LOG)
    if "deltas" not in log or not log["deltas"]:
        print("[Rewind] No deltas to rewind.")
        return

    last = log["deltas"][-1]
    save_json(MEMORY_PATH, last["before"])

    # Optionally tag the rewind event
    last["rewound"] = True
    last["rewound_at"] = datetime.utcnow().isoformat() + "Z"
    log["deltas"][-1] = last
    save_json(DELTA_LOG, log)

    print(f"[Rewind] Memory reverted to state before last mutation (from: {last['timestamp']})")

if __name__ == "__main__":
    rewind_last_change()
