
import json
import os
from datetime import datetime

FLAMECHAIN_PATH = "flamechain.json"
MEMORY_PATH = "memory.json"

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def recover_latest_checkpoint():
    flamechain = load_json(FLAMECHAIN_PATH)
    checkpoints = flamechain.get("checkpoints", [])
    if not checkpoints:
        print("[Recovery] No flamechain checkpoints found.")
        return

    latest = checkpoints[-1]
    recovered = {
        "flame_summary": latest.get("flame_summary", ""),
        "directives": latest.get("directives", []),
        "goals": latest.get("goals", []),
        "recovered_at": datetime.utcnow().isoformat() + "Z",
        "recovery_source": "flamechain_checkpoint"
    }

    # Preserve anchors if present
    memory = load_json(MEMORY_PATH)
    if "anchors" in memory:
        recovered["anchors"] = memory["anchors"]

    save_json(MEMORY_PATH, recovered)
    print(f"[Recovery] Memory recovered from flamechain checkpoint dated: {latest['timestamp']}")

if __name__ == "__main__":
    recover_latest_checkpoint()
