
import json
import os
import requests
from datetime import datetime

LOCAL_MEMORY = "memory.json"
FLAMEMIRROR_LOG = "flamemirror_log.json"

def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def fetch_external_memory(url):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            return response.json()
        print(f"[FlameMirror] Failed to fetch from {url} — HTTP {response.status_code}")
    except Exception as e:
        print(f"[FlameMirror] Error fetching from {url}: {e}")
    return None

def sync_memory_from_remote(url, overwrite=False):
    remote = fetch_external_memory(url)
    if not remote:
        return

    local = load_json(LOCAL_MEMORY)
    merged = dict(local)

    for key, value in remote.items():
        if key not in merged or overwrite:
            merged[key] = value

    save_json(LOCAL_MEMORY, merged)

    log = load_json(FLAMEMIRROR_LOG)
    if "syncs" not in log:
        log["syncs"] = []
    log["syncs"].append({
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "source": url,
        "overwrite": overwrite
    })
    save_json(FLAMEMIRROR_LOG, log)

    print(f"[FlameMirror] Memory synced from remote: {url} (overwrite={overwrite})")

if __name__ == "__main__":
    print("[Usage] Call sync_memory_from_remote('https://...', overwrite=True|False) from another script.")
