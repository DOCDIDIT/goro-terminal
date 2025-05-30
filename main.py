from flask import Flask, render_template, request, jsonify
import os
from mutation_executor import (load_memory, save_memory,
                               create_mutation_from_prompt,
                               process_mutation_queue)

app = Flask(__name__, static_folder="static")

memory = load_memory()


@app.route("/")
def index():
    return render_template("goro_terminal.html")


@app.route("/command", methods=["POST"])
def prompt():
    user_input = request.get_json()["user_input"]
    response = process_mutation_queue(user_input, memory)
    save_memory(memory)
    return jsonify({"response": response})


@app.route("/memory", methods=["GET"])
def memory_dump():
    return jsonify(memory)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
