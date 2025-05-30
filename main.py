import os
from flask import Flask, render_template, request, jsonify
from mutation_executor import process_mutation_queue, load_memory, save_memory
from goro_command_handler import process_command
from command_cognition import interpret_command
import time

app = Flask(__name__)

memory = load_memory()
memory.setdefault("flamekeeper_state", "stable")
memory.setdefault("flame_last_seen", {})
memory.setdefault("last_conversation", "")


@app.route("/")
def index():
    return render_template("goro_terminal.html")


@app.route("/command", methods=["POST"])
def prompt():
    user_input = request.json.get("prompt", "")
    memory = load_memory()

    # Try to interpret the input via cognition engine
    interpreted = interpret_command(user_input, memory)

    if interpreted:
        if interpreted["type"] == "trigger_response":
            return jsonify({"response": interpreted["response"]})
        if interpreted["type"] == "route":
            return jsonify({
                "response":
                f"Routing to {interpreted['agent']} for: {interpreted['context']}"
            })

    # Fallback to mutation executor
    response = process_mutation_queue(user_input, memory)
    return jsonify({"response": response})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
