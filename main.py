from flask import Flask, request, jsonify, render_template
from mutation_executor import load_memory, save_memory, process_mutation_queue
from goro_command_handler import process_command

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("goro_terminal.html")


@app.route("/command", methods=["POST"])
def prompt():
    user_input = request.json["user_input"]
    memory = load_memory()

    # Default to command processing
    response = process_command(user_input, memory)

    # If mutation handled it, override response
    mutation_response = process_mutation_queue(user_input, memory)
    if mutation_response:
        response = mutation_response

    save_memory(memory)
    return jsonify({"response": response})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
