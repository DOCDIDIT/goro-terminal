import json
from mutation_executor import create_mutation_from_prompt


def process_command(user_input, memory):
    # 🔥 Respond with memory-stored mutation response if available
    if "last_triggered_response" in memory:
        return memory.pop("last_triggered_response")

    # 🌍 Flame Atlas viewer
    if "show.atlas" in user_input:
        return json.dumps(memory.get("flame_atlas", {}), indent=2)

    # 📜 Evolution directive viewer
    if "show.directives" in user_input:
        return json.dumps(memory.get("evolution_directives", []), indent=2)

    # 💡 Auto-suggested mutation creation
    if "suggest.mutation" in user_input:
        mutation = create_mutation_from_prompt(user_input, memory)
        if "mutation_queue" not in memory:
            memory["mutation_queue"] = []
        memory["mutation_queue"].append(mutation)
        return json.dumps(mutation, indent=2)

    # 🔥 Inject mutation via prompt
    if "inject.mutation" in user_input:
        try:
            start = user_input.index("{")
            json_str = user_input[start:]
            mutation = json.loads(json_str)
            if "trigger" in mutation and "response" in mutation:
                if "mutation_queue" not in memory:
                    memory["mutation_queue"] = []
                memory["mutation_queue"].append(mutation)
                return f"✅ Mutation injected: {mutation['trigger']}"
            else:
                return "❌ Invalid mutation: missing 'trigger' or 'response'"
        except Exception as e:
            return f"❌ Failed to parse mutation: {str(e)}"

    # 🎨 Placeholder
    if "inject.ui" in user_input:
        return "✨ UI injection requested. Feature not yet implemented."

    # 🗣️ Default echo
    return f"Goro heard: {user_input}"
