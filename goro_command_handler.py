import json
from mutation_executor import create_mutation_from_prompt


def process_command(user_input, memory):
    for entry in memory.get("mutation_queue", []):
        if entry["trigger"].lower() in user_input.lower():
            response = entry["response"]
            return f"Goro heard: {response}"

    def handle_command(user_input, memory):
        return {
            "type": "trigger_response",
            "response": f"Goro heard: {user_input}"
        }

    return "Goro heard: (no matching mutation)"
