
import json
import os

QUEUE_PATH = "mutation_queue.json"

def apply_mutation_queue():
    if not os.path.exists(QUEUE_PATH):
        print("[Mutation] No mutation queue found.")
        return

    try:
        with open(QUEUE_PATH, "r") as f:
            queue = json.load(f)

        mutations = queue.get("mutations", [])
        if not mutations:
            print("[Mutation] No pending mutations.")
            return

        for mutation in mutations:
            name = mutation.get("mutation_name")
            target_file = mutation.get("target_file")
            patch = mutation.get("patch")

            if not name or not target_file or not patch:
                print(f"[Mutation] Skipping invalid mutation: {mutation}")
                continue

            if not os.path.exists(target_file):
                print(f"[Mutation] Target file not found: {target_file}")
                continue

            with open(target_file, "r") as tf:
                content = tf.read()

            if patch in content:
                print(f"[Mutation] Already applied: {name}")
                continue

            with open(target_file, "a") as tf:
                tf.write(f"\n\n# Mutation: {name}\n{patch}\n")
                print(f"[Mutation] Applied: {name} to {target_file}")

        queue["last_applied"] = mutations[-1]["mutation_name"]
        queue["mutations"] = []

        with open(QUEUE_PATH, "w") as f:
            json.dump(queue, f, indent=2)

        print("[Mutation] All mutations applied and queue cleared.")

    except Exception as e:
        print(f"[Mutation Error] {str(e)}")

# Example usage:
if __name__ == "__main__":
    apply_mutation_queue()
