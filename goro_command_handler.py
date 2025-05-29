import json
from mutation_executor import create_mutation_from_prompt


def process_command(user_prompt, memory):
    if "show.atlas" in prompt:
        return json.dumps(memory.get("flame_atlas", {}), indent=2)

    if "show.directives" in prompt:
        return json.dumps(memory.get("evolution_directives", []), indent=2)

    if "suggest.mutation" in prompt:
        mutation = create_mutation_from_prompt(prompt, memory)
        return json.dumps(mutation, indent=2)

    if "inject.ui" in prompt:
        return "🧩 UI injection requested. Feature not yet implemented."

    return f"Goro heard: {prompt}"
