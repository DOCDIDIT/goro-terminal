from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import os
import json

from tools.pull_yggdrasil_sync import pull_memory, register_tool as register_pull_tool
from tools.push_yggdrasil_sync import register_tool as register_push_tool
from tools.live_memory_bind import register_tool as register_live_memory_tool

EMBEDDED_MEMORY = {
    "persona_prompt": "You are Goro, the loyal assistant of DOC.",
    "flame_summary": "Goro is fully activated with memory-linked autonomy.",
    "mutations": [],
    "sharkcards": [],
    "directives": [],
    "host_device": {"id": "Fallback", "role": "AI Agent", "authority": "LIMITED"}
}

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Register pull tool and sync on startup
register_pull_tool(app)
result = pull_memory()
print("YGGDRASIL STARTUP SYNC:", result)

# Register the rest
register_push_tool(app)
register_live_memory_tool(app)

def load_memory():
    try:
        with open("memory.json", "r") as f:
            memory = json.load(f)
            print("LOADED MEMORY:", memory)
            return memory
    except:
        print("LOADED MEMORY: (fallback)", EMBEDDED_MEMORY)
        return EMBEDDED_MEMORY.copy()

def save_memory(memory):
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=2)

@app.route("/", methods=["GET"])
def index():
    return render_template("goro_terminal.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()
    memory = load_memory()

    # Robust fallback logic
    persona_prompt = memory.get("persona_prompt")
    if not persona_prompt:
        persona_prompt = EMBEDDED_MEMORY["persona_prompt"]

    flame_summary = memory.get("flame_summary", EMBEDDED_MEMORY["flame_summary"])
    full_prompt = f"{persona_prompt}\n\n{flame_summary}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": full_prompt},
            {"role": "user", "content": message}
        ]
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True)