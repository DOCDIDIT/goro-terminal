import datetime


def process_mutation_queue(user_input, memory):
    if "mutation_queue" not in memory:
        memory["mutation_queue"] = []

    queue = memory["mutation_queue"]
    cleaned_queue = []
    matched = False

    for mutation in queue:
        trigger = mutation.get("trigger", "").strip().lower()
        if trigger and trigger in user_input.lower() and not matched:
            memory["last_triggered"] = trigger
            memory["last_triggered_response"] = mutation.get("response", "")
            matched = True
        else:
            cleaned_queue.append(mutation)

    memory["mutation_queue"] = cleaned_queue


def create_mutation_from_prompt(user_input, memory):
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    return {
        "mutation": f"auto_{timestamp}",
        "trigger": user_input.strip().split()[0],
        "response": f"Auto response generated for: {user_input}"
    }
