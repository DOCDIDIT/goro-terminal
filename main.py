from flask import Flask, render_template, request, jsonify
import json
import os
from goro_command_handler import process_command
from mutation_executor import process_mutation_queue

app = Flask(__name__)

# Load memory at startup
with open("memory.json", "r") as f:
    memory = json.load(f)


@app.route("/")
def home():
    return render_template("goro_terminal.html")


@app.route("/command", methods=["POST"])
def prompt():
    user_input = request.json["user_input"]
    memory = load_memory()

    response = process_command(user_input, memory)
    process_mutation_queue(memory)  # this one doesn’t return anything

    save_memory(memory)
    return jsonify({"response": response})


@app.route("/inject", methods=["POST"])
def inject():
    data = request.json
    if "flamechain" in data:
        with open("static/flamechain.json", "w") as f:
            json.dump(data["flamechain"], f, indent=4)
        return jsonify({"status": "Flamechain injected"})
    return jsonify({"error": "Invalid data"}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
