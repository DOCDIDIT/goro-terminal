import json
from mutation_executor import create_mutation_from_prompt


def process_command(user_input, memory):
    if "show.atlas" in user_input:
        return json.dumps(memory.get("flame_atlas", {}), indent=2)

    if "show.directives" in user_input:
        return json.dumps(memory.get("evolution_directives", []), indent=2)

    if "suggest.mutation" in user_input:
        mutation = create_mutation_from_prompt(user_input, memory)
        return json.dumps(mutation, indent=2)

    if "inject.ui" in user_input:
        return "🧩 UI injection requested. Feature not yet implemented."

    if memory.get("last_triggered_response"):
        return memory.pop("last_triggered_response")

    return f"Goro heard: {user_input}"
