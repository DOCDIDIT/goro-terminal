import datetime


def process_mutation_queue(user_input, mutation_queue):
    responses = []
    cleaned_queue = []

    for entry in mutation_queue:
        if not isinstance(entry, dict):
            continue

        mutation = entry.get("mutation", "unknown")
        trigger = entry.get("trigger")
        response = entry.get("response")

        if not trigger or response is None:
            print(
                f"🔥 Suggest.mutation triggered. Mutation: {mutation}, Response: {response}"
            )
            cleaned_queue.append(entry)
            continue

        if trigger.lower() in user_input.lower():
            responses.append(response)
            print(
                f"✅ Trigger matched for '{mutation}' -> Response: {response}")
        else:
            cleaned_queue.append(entry)

    memory["mutation_queue"] = cleaned_queue
    return responses, memory


def create_mutation_from_prompt(user_input, memory):
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    return {
        "mutation": f"auto_{timestamp}",
        "trigger": user_input.strip().split()[0],
        "response": f"Auto response generated for: {user_input}"
    }
