
import json
import os

MEMORY_PATH = os.path.join("static", "memory.json")

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return {}
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)

def save_memory(data):
    with open(MEMORY_PATH, "w") as f:
        json.dump(data, f, indent=2)

def bind_template_to_memory(name, html_content):
    memory = load_memory()
    if "ui_templates" not in memory:
        memory["ui_templates"] = {}
    memory["ui_templates"][name] = html_content
    save_memory(memory)
    print(f"[Template Binder] Bound template '{name}' to memory.")

def get_template_from_memory(name):
    memory = load_memory()
    return memory.get("ui_templates", {}).get(name, None)
