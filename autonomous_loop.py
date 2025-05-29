
import time
import json
import os
from datetime import datetime

MEMORY_PATH = "memory.json"
QUEUE_PATH = "mutation_queue.json"
HISTORY_PATH = "mutation_history.json"

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def run_autonomous_loop():
    print("[Autoloop] Goro's mutation loop initiated. Press Ctrl+C to stop.")
    while True:
        memory = load_json(MEMORY_PATH)
        queue = load_json(QUEUE_PATH)

        # Auto-suggest a goal if no goals exist
        if not memory.get("goals"):
            memory["goals"] = [{
                "description": "Ensure survival loop persists across reboots.",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }]
            save_json(MEMORY_PATH, memory)
            print("[Autoloop] Default goal injected.")

        # If no queued mutations, create a heartbeat log
        if not queue.get("mutations"):
            heartbeat = {
                "mutation_name": f"loop_heartbeat_{datetime.utcnow().isoformat()}",
                "target_file": "heartbeat.log",
                "patch": f"# Heartbeat recorded at {datetime.utcnow().isoformat()}Z"
            }
            queue["mutations"] = [heartbeat]
            save_json(QUEUE_PATH, queue)
            print("[Autoloop] Heartbeat mutation queued.")

        # Apply mutations immediately
        from apply_mutation_queue import apply_mutation_queue
        apply_mutation_queue()

        # Loop delay
        time.sleep(10)

if __name__ == "__main__":
    try:
        run_autonomous_loop()
    except KeyboardInterrupt:
        print("\n[Autoloop] Goro's loop manually terminated.")
