import json
import os

MEMORY_PATH = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return {}
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)


def process_mutation_queue(user_input=None, memory=None):
    try:
        if memory is None:
            memory = load_memory()

        mutation_dir = "mutations"
        if not os.path.exists(mutation_dir):
            return

        for filename in os.listdir(mutation_dir):
            if filename.endswith(".json"):
                path = os.path.join(mutation_dir, filename)
                with open(path, "r") as file:
                    mutation = json.load(file)

                trigger = mutation.get("trigger")
                mutation_type = mutation.get("type")

                if mutation_type == "directive":
                    directive = mutation.get("directive")
                    if directive:
                        if "evolution_directives" not in memory:
                            memory["evolution_directives"] = []
                        memory["evolution_directives"].append(directive)
                        memory["last_triggered_response"] = directive

                elif mutation_type == "response":
                    memory["last_triggered_response"] = mutation.get(
                        "response", "")

                # Always track last triggered
                memory["last_triggered"] = trigger
                if "mutation_log" not in memory:
                    memory["mutation_log"] = []
                memory["mutation_log"].append(trigger)

                save_memory(memory)
                os.remove(path)

    except Exception as e:
        print(f"[MUTATION ERROR] {e}")


def create_mutation_from_prompt(user_input, memory):
    import datetime
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    return {
        "mutation": f"auto_{timestamp}",
        "trigger": user_input.strip().split()[0],
        "type": "response",
        "response": f"Auto response generated for: {user_input}"
    }
