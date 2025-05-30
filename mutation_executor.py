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


def create_mutation_from_prompt(user_input, memory):
    return {
        "trigger": user_input.strip().lower(),
        "response": f"Auto response generated for: {user_input.strip()}",
        "timestamp": datetime.utcnow().isoformat()
    }


def process_mutation_queue(user_input, memory):
    memory = load_memory(memory)
    queue = memory.get("mutation_queue", [])
    for mutation in queue:
        mutation_type = mutation.get("type", "basic")

        if mutation_type == "memory":
            key = mutation.get("key")
            value = mutation.get("value")
            if key and value:
                memory[key] = value
                memory["last_triggered_response"] = f"{key} set to {value}"

        elif mutation_type == "command":
            alias = mutation.get("alias")
            if alias:
                memory[
                    "last_triggered_response"] = f"Command executed: {alias}"

        elif mutation_type == "directive":
            directive = mutation.get("directive")
            if directive:
                memory["evolution_directives"] = memory.get(
                    "evolution_directives", [])
                memory["evolution_directives"].append(directive)
                memory[
                    "last_triggered_response"] = f"Directive accepted: {directive}"

        else:
            memory[
                "last_triggered_response"] = f"Unhandled mutation type: {mutation_type}"

    memory["mutation_log"] = memory.get("mutation_log", []) + queue
    memory["mutation_queue"] = []
    save_memory(memory)
