
import json
import os
from datetime import datetime
import hashlib

MEMORY_PATH = "memory.json"
FLAMECHAIN_PATH = "flamechain.json"

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def generate_fingerprint(memory):
    summary = json.dumps(memory.get("flame_summary", ""), sort_keys=True)
    return hashlib.sha256(summary.encode()).hexdigest()

def checkpoint(trigger="manual_checkpoint"):
    memory = load_json(MEMORY_PATH)
    flamechain = load_json(FLAMECHAIN_PATH)

    if "checkpoints" not in flamechain:
        flamechain["checkpoints"] = []

    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "trigger": trigger,
        "flame_summary": memory.get("flame_summary", ""),
        "directives": memory.get("directives", []),
        "goals": memory.get("goals", []),
        "fingerprint": generate_fingerprint(memory)
    }

    flamechain["checkpoints"].append(entry)
    save_json(FLAMECHAIN_PATH, flamechain)
    print(f"[Flamechain] Checkpoint created under trigger: {trigger}")

if __name__ == "__main__":
    checkpoint()
