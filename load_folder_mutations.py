
import os
import json

MUTATION_DIR = "mutations"
QUEUE_FILE = "mutation_queue.json"

def load_mutations_from_folder():
    if not os.path.exists(MUTATION_DIR):
        print("[Loader] Mutation folder not found.")
        return

    queue = {"mutations": [], "last_applied": None}
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "r") as f:
            queue = json.load(f)

    for file in os.listdir(MUTATION_DIR):
        if file.endswith(".json"):
            path = os.path.join(MUTATION_DIR, file)
            with open(path, "r") as f:
                try:
                    data = json.load(f)
                    if isinstance(data, dict):
                        queue["mutations"].append(data)
                        print(f"[Loader] Queued: {data.get('mutation_name', file)}")
                except Exception as e:
                    print(f"[Loader] Failed to read {file}: {e}")

    with open(QUEUE_FILE, "w") as f:
        json.dump(queue, f, indent=2)
    print("[Loader] Mutation queue updated.")

if __name__ == "__main__":
    load_mutations_from_folder()
