import json
import re
from datetime import datetime

MEMORY_PATH = "memory.json"

def load_memory():
    try:
        with open(MEMORY_PATH, "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(memory):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def parse_command(input_text):
    input_text = input_text.strip()

    goal_match = re.match(r"(set|add)_goal\s*\(\s*[\"'](.+?)[\"']\s*\)", input_text)
    if goal_match:
        return {
            "type": "goal",
            "description": goal_match.group(2)
        }

    inject_match = re.match(r"1031\.inject\s*\{(.+)\}", input_text)
    if inject_match:
        return {
            "type": "mutation",
            "raw": inject_match.group(1)
        }

    if input_text.startswith("inject.flame_summary"):
        return {
            "type": "persona_patch",
            "command": input_text
        }

    if "reset" in input_text.lower() and "memory" in input_text.lower():
        return {
            "type": "reset",
            "target": "memory"
        }

    return {
        "type": "general_prompt",
        "content": input_text
    }

def process_command(input_text):
    result = parse_command(input_text)
    print(f"[Command Parser] Type: {result['type']}")
    if result['type'] == "goal":
        print(f" -> New Goal: {result['description']}")
        memory = load_memory()
        if "goals" not in memory:
            memory["goals"] = []
        memory["goals"].append({
            "description": result['description'],
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
        save_memory(memory)
        print(" -> Goal stored in memory.")
    elif result['type'] == "mutation":
        print(" -> Detected raw mutation payload. Ready for parsing or queuing.")
    elif result['type'] == "persona_patch":
        print(" -> Detected flame_summary update.")
    elif result['type'] == "reset":
        print(" -> Memory reset requested (manual confirmation needed).")
    elif result['type'] == "general_prompt":
        print(" -> Treated as natural input or task for Goro to interpret.")

if __name__ == "__main__":
    print("[Command Parser] Awaiting input. Type 'exit' to quit.")
    while True:
        user_input = input(">> ")
        if user_input.lower() == "exit":
            break
        process_command(user_input)