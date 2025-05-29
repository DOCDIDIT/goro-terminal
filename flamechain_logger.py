import json
from datetime import datetime

LOG_PATH = "flamechain_log.json"

def log_event(event_type, details):
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "type": event_type,
        "details": details
    }

    try:
        with open(LOG_PATH, "r") as f:
            log = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        log = []

    log.append(entry)

    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2)

def log_mutation_applied(mutation_id, source="watchdog"):
    log_event("mutation_applied", {
        "mutation_id": mutation_id,
        "source": source
    })

def log_memory_sync(status="success"):
    log_event("memory_sync", {
        "status": status
    })

def log_flame_summary_change(old_summary, new_summary):
    log_event("flame_summary_update", {
        "from": old_summary,
        "to": new_summary
    })