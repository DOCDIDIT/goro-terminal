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
    if memory is None:
        memory = load_memory()
    if not os.path.exists("queue"):
        os.makedirs("queue")

    for filename in os.listdir("queue"):
        if filename.endswith(".json"):
            path = os.path.join("queue", filename)
            try:
                with open(path, "r") as f:
                    mutation = json.load(f)

                trigger = mutation.get("trigger")
                mutation_type = mutation.get("type")

                if mutation_type == "summary":
                    new_summary = mutation.get("summary")
                    if new_summary:
                        memory["flame_summary"] = new_summary
                        memory[
                            "last_triggered_response"] = "Flame summary updated."

                elif mutation_type == "directive":
                    directive = mutation.get("directive")
                    if directive:
                        if "evolution_directives" not in memory:
                            memory["evolution_directives"] = []
                        memory["evolution_directives"].append(directive)
                        memory["last_triggered_response"] = "Directive added."

                elif mutation_type == "response":
                    response = mutation.get("response")
                    if response:
                        memory["last_triggered_response"] = response

                # Record trigger history
                if "trigger_history" not in memory:
                    memory["trigger_history"] = []
                memory["trigger_history"].append(trigger)

                save_memory(memory)
                os.remove(path)
            except Exception as e:
                print(f"Error processing {filename}: {e}")


def create_mutation_from_prompt(user_input, memory):
    import datetime
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    return {
        "mutation": f"auto_{timestamp}",
        "trigger": user_input.strip().split()[0],
        "type": "response",
        "response": f"Auto response generated for: {user_input}"
    }
