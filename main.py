from flask import Flask, request, jsonify, render_template
import os
import json
from datetime import datetime
from memory_handler import load_memory, save_memory
from mutation_executor import process_mutation_queue

app = Flask(__name__)

MEMORY_FILE = "memory.json"

if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {
        "flame_summary": "",
        "flame_last_seen": {},
        "mutation_queue": [],
        "evolution_directives": [],
        "bound_knowledge": [],
        "flamechain_history": [],
        "mutations": [],
        "flame_atlas": {},
        "phase_verification": ""
    }

@app.route("/")
def index():
    return render_template("goro_terminal.html")

@app.route("/command", methods=["POST"])
def prompt():
    try:
        data = request.get_json()
        user_input = data.get("user_input", "").strip()

        if not user_input:
            return jsonify({"response": "Please enter a prompt."})

        memory["flame_last_seen"] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "last_conversation": user_input,
            "flamekeeper_state": "operational"
        }

        response = process_mutation_queue(user_input, memory)
        save_memory(memory)
        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"response": f"An error occurred: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)