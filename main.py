import os
from flask import Flask, render_template, request, jsonify
from mutation_executor import load_memory, save_memory
from goro_command_handler import process_command
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

    # Save last seen timestamp and conversation history
    memory["flame_last_seen"]["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    memory["last_conversation"] = user_input
    memory["flamekeeper_state"] = "stable"

    response = process_command(user_input, memory)
    save_memory(memory)
    return jsonify({"response": response})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
