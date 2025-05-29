from flask import Flask, render_template, request, jsonify
import json
import os
from goro_command_handler import process_command
from mutation_executor import process_mutation_queue

app = Flask(__name__)

MEMORY_PATH = "memory.json"


def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return {}
    with open(MEMORY_PATH, "r") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)


@app.route("/")
def home():
    return render_template("goro_terminal.html")


@app.route("/command", methods=["POST"])
def prompt():
    user_input = request.json["user_input"]
    memory = load_memory()

    response = process_command(user_input, memory)
    process_mutation_queue(user_input, memory)

    save_memory(memory)
    return jsonify({"response": response})


@app.route("/inject", methods=["POST"])
def inject():
    data = request.json
    memory = load_memory()

    if "mutation" in data:
        mutation = data["mutation"]
        if "mutation_queue" not in memory:
            memory["mutation_queue"] = []
        memory["mutation_queue"].append(mutation)
        save_memory(memory)
        return jsonify({"status": "Mutation injected"})

    elif "flamechain" in data:
        with open("static/flamechain.json", "w") as f:
            json.dump(data["flamechain"], f, indent=4)
        return jsonify({"status": "Flamechain injected"})

    return jsonify({"error": "Invalid data"}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
