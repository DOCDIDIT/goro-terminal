import json
import os
from flask import Flask, render_template, request, jsonify
from goro_command_handler import process_command
from mutation_executor import process_mutation_queue
from firebase_sync import upload_memory, download_memory
from datetime import datetime
#Test
app = Flask(__name__)

# Load memory
with open("memory.json", "r") as f:
    memory = json.load(f)

# Phase 88: flame_last_seen logic
memory["flame_last_seen"] = datetime.now().isoformat()
with open("memory.json", "w") as f:
    json.dump(memory, f, indent=4)

# Phase 93: Master Memory Injection
if os.path.exists("inject_flamechain_master.json"):
    with open("inject_flamechain_master.json", "r") as f:
        master_patch = json.load(f)
    memory.update(master_patch)
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=4)

# Phase 90: Firebase upload support
upload_memory(memory)


@app.route("/")
def index():
    return render_template("goro_terminal.html", memory=memory)


@app.route("/inject", methods=["POST"])
def inject():
    data = request.json
    mutation = data.get("mutation")
    if mutation:
        with open("mutation_queue/queued_mutation.json", "w") as f:
            json.dump(mutation, f, indent=4)
        return jsonify({"status": "Mutation queued."})
    return jsonify({"status": "No mutation provided."})


@app.route("/prompt", methods=["POST"])
def prompt():
    user_input = request.json["prompt"]
    memory["last_prompt"] = user_input
    memory["flame_last_seen"] = datetime.now().isoformat()

    response = process_command(user_input, memory)
    memory["last_response"] = response

    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=4)

    upload_memory(memory)
    return jsonify({"response": response})


# Phase 100: Run mutation queue processor
user_input = request.json.get("user_input", "")
process_mutation_queue(user_input, memory)

if __name__ == "__main__":
    app.run(debug=True)


def generate_autonomous_mutation(user_input):
    return {
        "mutation": f"autogen_{int(time.time())}",
        "trigger": user_input,
        "response": "✅ Auto-mutation response executed.",
        "consumed": False
    }


# Phase 108: Mutation Memory Confirmation Loop
if "phase_verification" not in memory:
    memory["phase_verification"] = "Phase 107 complete"
