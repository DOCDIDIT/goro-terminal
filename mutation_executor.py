import datetime


def process_mutation_queue(user_input, memory):
    if "mutation_queue" not in memory:
        memory["mutation_queue"] = []

    if "flamechain_history" not in memory:
        memory["flamechain_history"] = []

    if "mutation_log" not in memory:
        memory["mutation_log"] = []

    queue = memory["mutation_queue"]
    cleaned_queue = []
    matched = False

    for mutation in queue:
        trigger = mutation.get("trigger", "").strip().lower()
        if trigger and trigger in user_input.lower() and not matched:
            mutation_type = mutation.get("type", "response")
            memory["last_triggered"] = trigger

            # 🔥 Type: Response
            if mutation_type == "response":
                memory["last_triggered_response"] = mutation.get(
                    "response", "")

            # 🧠 Type: Memory
            elif mutation_type == "memory":
                key = mutation
