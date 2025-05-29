
import json
import os
from datetime import datetime

MEMORY_PATH = "memory.json"
CLONE_DIR = "shadow_clones"
MERGE_LOG = "merge_log.json"

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def merge_shadow_clone(clone_filename, overwrite=False):
    clone_path = os.path.join(CLONE_DIR, clone_filename)
    if not os.path.exists(clone_path):
        print(f"[Merge] Clone file not found: {clone_path}")
        return

    memory = load_json(MEMORY_PATH)
    clone = load_json(clone_path)

    merged = dict(memory)  # Start with current memory

    for key, value in clone.items():
        if key not in merged or overwrite:
            merged[key] = value

    save_json(MEMORY_PATH, merged)

    # Log merge event
    log = load_json(MERGE_LOG)
    if "merges" not in log:
        log["merges"] = []
    log["merges"].append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": clone_filename,
        "overwrite": overwrite
    })
    save_json(MERGE_LOG, log)

    print(f"[Merge] Memory selectively merged from: {clone_filename} (overwrite: {overwrite})")

if __name__ == "__main__":
    print("[Usage] Call merge_shadow_clone('filename.json', overwrite=True|False) from another script.")
