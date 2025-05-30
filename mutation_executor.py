import os
import json
import time

MEMORY_FILE = "memory.json"


# === Memory Load/Save ===
def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {
        "flame_summary": "",
        "flame_last_seen": {},
        "mutation_queue": [],
        "evolution_directives": [],
        "bound_knowledge": [],
        "flamechain_history": [],
        "mutations": [],
        "flame_atlas": {},
        "phase_verification": "",
        "mutation_log": [],
        "last_triggered": "",
        "last_triggered_response": "",
        "last_conversation": [],
        "agent_roles": {},
        "task_routing": {}
    }


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


# === Mutation Builder ===
def create_mutation_from_prompt(prompt):
    try:
        mutation = json.loads(prompt)
        if "trigger" in mutation and ("response" in mutation or "alias"
                                      in mutation or "directive" in mutation):
            return mutation
    except Exception:
        pass
    return {
        "trigger": prompt.strip(),
        "response": f"Goro heard: {prompt.strip()}"
    }


# === Core Mutation Processor ===
def process_mutation_queue(user_input, memory):
    memory["last_triggered"] = user_input
    triggered = None

    for mutation in memory["mutation_queue"]:
        if mutation["trigger"] == user_input:
            triggered = mutation
            break

    if not triggered:
        triggered = create_mutation_from_prompt(user_input)
        memory["mutation_queue"].append(triggered)

    # === NEW: Multi-Agent Task Delegation ===
    mutation_type = triggered.get("type")
    directive = triggered.get("directive")
    agent_roles = memory.get("agent_roles", {})

    if mutation_type:
        role_response = agent_roles.get(mutation_type)
        if role_response:
            memory["last_triggered_response"] = role_response
            save_memory(memory)
            return role_response

    if mutation_type == "directive" and directive:
        memory["evolution_directives"].append(directive)
        memory["last_triggered_response"] = directive
        save_memory(memory)
        return directive

    response = triggered.get("response")
    if not response:
        if mutation_type == "directive":
            response = f"Directive '{triggered.get('directive', 'unknown')}' received."
        else:
            response = f"Goro heard: {user_input}"

        memory["last_triggered_response"] = response
        save_memory(memory)
        return response
