
import json
import os

def load_ui_blueprint(name="terminal_base"):
    path = os.path.join("static", "ui_blueprints.json")
    if not os.path.exists(path):
        raise FileNotFoundError("Blueprint file not found at static/ui_blueprints.json")

    with open(path, "r") as f:
        data = json.load(f)

    if name not in data:
        raise ValueError(f"Blueprint '{name}' not found in ui_blueprints.json")

    return data[name]
