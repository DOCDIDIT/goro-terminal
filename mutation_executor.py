import datetime


def process_mutation_queue(user_input, memory):
    if "mutation_queue" not in memory:
        memory["mutation_queue"] = []

    queue = memory["mutation_queue"]
    cleaned_queue = []

    for mutation in queue:
        if "trigger" in mutation and mutation["trigger"] in user_input:
            # you can do something here like apply mutation logic
            memory["last_triggered"] = mutation["trigger"]
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
