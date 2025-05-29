import json
from mutation_executor import create_mutation_from_prompt


def process_command(user_input, memory):
    import json

    if "show.atlas" in user_input:
        return json.dumps(memory.get("flame_atlas", {}), indent=2)

    if "show.directives" in user_input:
        return json.dumps(memory.get("evolution_directives", []), indent=2)

    if "suggest.mutation" in user_input:
        mutation = create_mutation_from_prompt(user_input, memory)
        if "mutation_queue" not in memory:
            memory["mutation_queue"] = []
        memory["mutation_queue"].append(mutation)
        return json.dumps(mutation, indent=2)

    if "inject.ui" in user_input:
        return "✨ UI injection requested. Feature not yet implemented."

    if "last_triggered_response" in memory:
        return memory.pop("last_triggered_response")

    return f"Goro heard: {user_input}"
