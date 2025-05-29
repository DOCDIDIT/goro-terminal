
import json
import os
import time
import hashlib
from datetime import datetime

MEMORY_PATH = "memory.json"
DELTA_LOG = "mutation_deltas.json"
POLL_INTERVAL = 2  # seconds

def hash_content(content):
    return hashlib.sha256(json.dumps(content, sort_keys=True).encode()).hexdigest()

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def record_delta(before, after):
    delta = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "change_detected": True,
        "before_hash": hash_content(before),
        "after_hash": hash_content(after),
        "before": before,
        "after": after
    }

    log = load_json(DELTA_LOG)
    if "deltas" not in log:
        log["deltas"] = []
    log["deltas"].append(delta)
    save_json(DELTA_LOG, log)
    print("[Debugger] Memory mutation detected and logged.")

def watch_memory():
    print("[Debugger] Watching memory.json for live mutations...")
    prev = load_json(MEMORY_PATH)
    prev_hash = hash_content(prev)

    while True:
        time.sleep(POLL_INTERVAL)
        current = load_json(MEMORY_PATH)
        current_hash = hash_content(current)
        if current_hash != prev_hash:
            record_delta(prev, current)
            prev = current
            prev_hash = current_hash
        else:
            print("[Debugger] No change.")

if __name__ == "__main__":
    watch_memory()
