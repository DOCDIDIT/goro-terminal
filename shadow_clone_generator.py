
import json
import os
from datetime import datetime

MEMORY_PATH = "memory.json"
CLONE_DIR = "shadow_clones"

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_clone(data):
    if not os.path.exists(CLONE_DIR):
        os.makedirs(CLONE_DIR)

    timestamp = datetime.utcnow().isoformat().replace(":", "-")
    clone_path = os.path.join(CLONE_DIR, f"clone_{timestamp}.json")
    with open(clone_path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[Clone] Shadow clone created: {clone_path}")

def clone_memory():
    memory = load_json(MEMORY_PATH)
    save_clone(memory)

if __name__ == "__main__":
    clone_memory()
