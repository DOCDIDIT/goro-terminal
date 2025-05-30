from flask import Flask, request, jsonify, render_template
import os
from memory_handler import load_memory, save_memory
from mutation_executor import process_mutation_queue
from command_cognition import interpret_command

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("goro_terminal.html")


@app.route("/command", methods=["POST"])
def prompt():
    try:
        user_input = request.json.get("prompt", "")
        memory = load_memory()

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
        return jsonify(
            {"response": response or "⚠️ No valid response generated."})

    except Exception as e:
        return jsonify({"response": f"❌ Internal Error: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
