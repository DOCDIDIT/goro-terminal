import json

def load_memory():
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_memory(memory):
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=2)

def get_next_ui_version():
    memory = load_memory()
    current_version = memory.get("ui_version", "2.8")
    try:
        major, minor = map(int, current_version.split('.'))
        minor += 1
        new_version = f"{major}.{minor}"
    except:
        new_version = "2.9"
    memory["ui_version"] = new_version
    save_memory(memory)
    return new_version

def run():
    version = get_next_ui_version()
    html = f"""<!DOCTYPE html>
<html>
<head>
  <title>DOC GPT Chat</title>
  <link rel=\"stylesheet\" href=\"/static/style.css\">
</head>
<body>
  <div class=\"chat-container\">
    <div class=\"chat-header\">DOC GPT — v{version}</div>
    <div id=\"output\" class=\"chat-box\"></div>
    <form id=\"command-form\" class=\"input-form\">
      <input type=\"text\" id=\"command\" placeholder=\"Type your message...\" />
      <button type=\"submit\">Send</button>
    </form>
  </div>
</body>
</html>"""

    css = """body {
  background-color: #f7f7f8;
  font-family: sans-serif;
  margin: 0;
  padding: 0;
}
.chat-container {
  max-width: 800px;
  margin: auto;
  display: flex;
  flex-direction: column;
  height: 100vh;
}
.chat-header {
  background-color: #343541;
  color: white;
  padding: 16px;
  font-size: 18px;
  font-weight: bold;
  text-align: center;
}
.chat-box {
  flex-grow: 1;
  padding: 16px;
  overflow-y: auto;
  background-color: white;
  border-top: 1px solid #ccc;
  border-bottom: 1px solid #ccc;
}
.input-form {
  display: flex;
  border-top: 1px solid #ccc;
  padding: 16px;
  background-color: #f7f7f8;
}
.input-form input {
  flex-grow: 1;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
}
.input-form button {
  margin-left: 10px;
  padding: 10px 16px;
  font-size: 16px;
  background-color: #10a37f;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.input-form button:hover {
  background-color: #0e8c6c;
}"""

    mutation = {
        "mutations": [
            {"file": "templates/goro_terminal.html", "content": html},
            {"file": "static/style.css", "content": css}
        ]
    }

    with open("mutation.json", "w") as f:
        json.dump(mutation, f, indent=2)
    print(f"[ChatGPT Clone] UI mutation written with version {version}")
