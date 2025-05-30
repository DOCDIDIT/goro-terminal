import json
import re


def interpret_command(user_input, memory):
    """
    This function processes the user_input string and checks if it matches
    any command, mutation trigger, or system directive in memory.json.

    Returns:
        - 'response': if a trigger matches
        - 'route': for routed agent
        - None: if no matches found
    """

    if not user_input or not memory:
        return None

    user_input = user_input.strip().lower()

    # Check direct mutation triggers
    for entry in memory.get("mutation_queue", []):
        if user_input == entry.get("trigger", "").lower():
            return {
                "type": "trigger_response",
                "response": entry.get("response", "")
            }

    # Check fusion being agent routing
    if memory.get("fusion_agents"):
        for agent in memory["fusion_agents"]:
            if agent["name"].lower() in user_input:
                return {
                    "type": "route",
                    "agent": agent["name"],
                    "context": user_input
                }

    # Fallback
    return None
