import json
from mutation_executor import create_mutation_from_prompt


def process_command(user_input, memory):
    # 🧠 Return memory-stored mutation response
    if "last_triggered_response" in memory:
        return memory.pop("last_triggered_response")

    # 📜 Memory queries
    if "show.memory" in user_input:
        return json.dumps(memory, indent=2)

    if "show.mutations" in user_input:
        return json.dumps(memory.get("flamechain_history", []), indent=2)

    if "last.triggered" in user_input:
        return memory.get("last_triggered", "No mutation triggered yet.")

    if "mutation.count" in user_input:
        return str(len(memory.get("mutation_log", [])))

    # 🔭 Flame Atlas
    if "show.atlas" in user_input:
        return json.dumps(memory.get("flame_atlas", {}), indent=2)

    # 📘 Evolution Directives
    if "show.directives" in user_input:
        return json.dumps(memory.get("evolution_directives", []), indent=2)

    # 💡 Suggest mutation
    if "suggest.mutation" in user_input:
        mutation = create_mutation_from_prompt(user_input, memory)
        if "mutation_queue" not in memory:
            memory["mutation_queue"] = []
        memory["mutation_queue"].append(mutation)
        return json.dumps(mutation, indent=2)

    # 🔥 Inject custom mutation from prompt
    if "inject.mutation" in user_input:
        try:
            start = user_input.index("{")
            json_str = user_input[start:]
            mutation = json.loads(json_str)
            if "trigger" in mutation:
                if "mutation_queue" not in memory:
                    memory["mutation_queue"] = []
                memory["mutation_queue"].append(mutation)
                return f"✅ Mutation injected: {mutation['trigger']}"
            else:
                return "❌ Invalid mutation: missing 'trigger' or 'response'"
        except Exception as e:
            return f"❌ Failed to parse mutation: {str(e)}"

    # 🎨 Placeholder for UI
    if "inject.ui" in user_input:
        return "✨ UI injection requested. Feature not yet implemented."

    # 🔊 Default echo
    return f"Goro heard: {user_input}"
