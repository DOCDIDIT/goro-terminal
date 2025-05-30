import os
import json
import time

MEMORY_FILE = "memory.json"
MUTATION_FOLDER = "mutations"


# ---- Load + Save Memory (with Pruning) ----
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
        "current_personality": "default"
    }


def save_memory(memory):
    # Prune history logs to prevent overload
    for key in ["mutation_log", "flamechain_history", "evolution_directives"]:
        if key in memory and isinstance(memory[key], list) and len(
                memory[key]) > 200:
            memory[key] = memory[key][-200:]  # Keep last 200 entries
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


# ---- Handle Mutation Queue ----
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

    # Handle directive-based personality switch
    if triggered.get("type") == "directive":
        directive = triggered.get("directive")
        if directive:
            if directive.startswith("be."):
                memory["current_personality"] = directive[3:]
            memory["evolution_directives"].append(directive)
            memory["last_triggered_response"] = directive
            save_memory(memory)
            return directive

    response = triggered.get("response", f"Goro heard: {user_input}")
    memory["last_triggered_response"] = response
    save_memory(memory)
    return response


# ---- Flamebuilder Watchdog (Phase 133) ----
def flamebuilder_watchdog():
    memory = load_memory()
    if not os.path.isdir(MUTATION_FOLDER):
        return

    for fname in os.listdir(MUTATION_FOLDER):
        if fname.endswith(".json"):
            path = os.path.join(MUTATION_FOLDER, fname)
            try:
                with open(path, "r") as f:
                    mutation = json.load(f)
                    if mutation not in memory["mutation_queue"]:
                        memory["mutation_queue"].append(mutation)
                        memory["mutation_log"].append({
                            "source": fname,
                            "timestamp": time.time()
                        })
                        print(f"🔥 Mutation injected from: {fname}")
                os.remove(path)  # Delete after injection
            except Exception as e:
                print(f"⚠️ Failed to process {fname}: {e}")
    save_memory(memory)


# Optional: Call this during Flask startup or every prompt
# flamebuilder_watchdog()
