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

            # 🔥 Default behavior: return response
            if mutation_type == "response":
                response = mutation.get("response", "")
                memory["last_triggered_response"] = response

            # 🧠 Inject a memory key:value pair
            elif mutation_type == "memory":
                key = mutation.get("key")
                value = mutation.get("value")
                if key:
                    memory[key] = value
                    memory[
                        "last_triggered_response"] = f"Memory key '{key}' set."

            # 🧭 Add to flame_atlas
            elif mutation_type == "flameatlas":
                entry = mutation.get("entry")
                if isinstance(entry, dict):
                    if "flame_atlas" not in memory:
                        memory["flame_atlas"] = {}
                    memory["flame_atlas"].update(entry)
                    memory["last_triggered_response"] = f"Flame Atlas updated."

            # 📜 Add to evolution_directives
            elif mutation_type == "directive":
                directive = mutation.get("directive")
                if directive:
                    if "evolution_directives" not in memory:
                        memory["evolution_directives"] = []
                    memory["evolution_directives"].append(directive)
                    memory["last_triggered_response"] = "Directive added."

            # 🧾 Chain log
            memory["mutation_log"].append(trigger)
            memory["flamechain_history"].append({
                "trigger":
                trigger,
                "type":
                mutation_type,
                "timestamp":
                datetime.datetime.utcnow().isoformat() + "Z"
            })

            matched = True
        else:
            cleaned_queue.append(mutation)

    memory["mutation_queue"] = cleaned_queue


def create_mutation_from_prompt(user_input, memory):
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    return {
        "mutation": f"auto_{timestamp}",
        "trigger": user_input.strip().split()[0],
        "type": "response",
        "response": f"Auto response generated for: {user_input}"
    }
