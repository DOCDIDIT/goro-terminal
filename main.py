from flask import Flask, request, jsonify, render_template
import os
from memory_handler import load_memory, save_memory
from mutation_executor import process_mutation_queue
from command_cognition import interpret_command

app = Flask(__name__)

MEMORY_FILE = "memory.json"

# Load memory
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

# Save memory


def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


# Home route
@app.route("/")
def index():
    return render_template("goro_terminal.html")


# Command route
@app.route("/command", methods=["POST"])
def prompt():
    try:
        data = request.get_json()
        user_input = data.get("user_input", "").strip()

        if not user_input:
            return jsonify({"response": "Please enter a prompt."})

        # Update last seen state
        memory["flame_last_seen"] = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "last_conversation": user_input,
            "flamekeeper_state": "operational"
        }

        # Process the command
        response = handle_command(user_input, memory)
        save_memory()

        return jsonify({"response": response})

    except Exception as e:
        return jsonify({"response": f"An error occurred: {str(e)}"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
