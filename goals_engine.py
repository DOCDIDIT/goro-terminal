
import json
import os
from datetime import datetime

MEMORY_PATH = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return {}
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)

def save_memory(memory):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def show_goals():
    memory = load_memory()
    goals = memory.get("goals", [])
    if not goals:
        print("[Goals] No active goals.")
        return
    print("\n[Goals] Active System Goals:")
    for i, goal in enumerate(goals, 1):
        print(f" {i}. {goal['description']} (Set: {goal['timestamp']})")

def set_goal(description):
    memory = load_memory()
    if "goals" not in memory:
        memory["goals"] = []
    goal = {
        "description": description,
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    memory["goals"].append(goal)
    save_memory(memory)
    print(f"[Goals] Goal set: "{description}"")

def purge_goals():
    memory = load_memory()
    memory["goals"] = []
    save_memory(memory)
    print("[Goals] All goals purged.")

if __name__ == "__main__":
    print("[Goals] Use as module. To set, show, or purge goals:")
    print(" set_goal("Description")")
    print(" show_goals()")
    print(" purge_goals()")
