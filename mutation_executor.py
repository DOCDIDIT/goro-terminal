import json
import os

MEMORY_FILE = "memory.json"


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
        "last_triggered": ""
    }


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def create_mutation_from_prompt(prompt):
    prompt = prompt.strip()
    try:
        mutation = json.loads(prompt)
        if ("trigger" in mutation
                and ("response" in mutation or "alias" in mutation
                     or "directive" in mutation)):
            return mutation
    except json.JSONDecodeError:
        pass

    return {"trigger": prompt, "response": f"Goro heard: {prompt}"}


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

    mutation_type = triggered.get("type")
    if mutation_type == "directive":
        directive = triggered.get("directive")
        if directive:
            memory["evolution_directives"].append(directive)
            memory["last_triggered_response"] = directive
            save_memory(memory)
            return directive

    response = triggered.get("response", f"Goro heard: {user_input}")
    memory["last_triggered_response"] = response
    save_memory(memory)
    return response
