
import json
import os
from datetime import datetime

MEMORY_PATH = "memory.json"

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return {}
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)

def check_and_execute_behaviors():
    memory = load_memory()
    routines = []

    # Example: respond to specific goals
    for goal in memory.get("goals", []):
        desc = goal.get("description", "").lower()
        if "self-patching" in desc:
            routines.append("Trigger mutation scan and apply pipeline.")
        elif "optimize" in desc:
            routines.append("Refactor all core files.")
        elif "survival" in desc or "daemon" in desc:
            routines.append("Ensure loop and daemon integrity.")

    # Example: directive-based behaviors
    for directive in memory.get("directives", []):
        if "flamechain" in directive.lower():
            routines.append("Monitor flamechain and log system identity.")
        if "truth" in directive.lower():
            routines.append("Reject hallucinated answers and verify context memory.")

    # Output behavior plan
    if routines:
        print(f"[Behavior] {len(routines)} behavior(s) generated from memory:")
        for r in routines:
            print(f" - {r}")
    else:
        print("[Behavior] No behaviors generated. Memory context quiet.")

if __name__ == "__main__":
    print("[Behavior] Parsing memory-driven routines...")
    check_and_execute_behaviors()
