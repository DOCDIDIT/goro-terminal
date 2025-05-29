
import json
import os
from datetime import datetime

MEMORY_PATH = "memory.json"
HISTORY_PATH = "mutation_history.json"

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return {}
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def autogen_goals():
    memory = load_memory()
    existing_goals = [g["description"] for g in memory.get("goals", [])]

    proposed_goals = []

    # Goal 1: If memory.json is mutated frequently, recommend stability
    if os.path.exists(HISTORY_PATH):
        with open(HISTORY_PATH, "r") as f:
            history = json.load(f).get("history", [])

        mem_mutations = [m for m in history if m.get("target_file") == "memory.json"]
        if len(mem_mutations) >= 3:
            proposed_goals.append("Stabilize memory.json to prevent overmutation and identity loss.")

    # Goal 2: No existing goal about mutation optimization
    if not any("optimize mutation flow" in g.lower() for g in existing_goals):
        proposed_goals.append("Optimize mutation flow to reduce redundant evolution steps.")

    # Add goals if not already present
    if "goals" not in memory:
        memory["goals"] = []

    new_goals = []
    for g in proposed_goals:
        if g not in existing_goals:
            memory["goals"].append({
                "description": g,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            })
            new_goals.append(g)

    if new_goals:
        save_memory(memory)
        print("[Goals] Auto-generated and stored:")
        for g in new_goals:
            print(f" - {g}")
    else:
        print("[Goals] No new goals generated. System objectives are current.")

if __name__ == "__main__":
    autogen_goals()
