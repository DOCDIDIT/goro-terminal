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
    current_version = memory.get("ui_version", "2.7")
    try:
        major, minor = map(int, current_version.split('.'))
        minor += 1
        new_version = f"{major}.{minor}"
    except:
        new_version = "2.8"
    memory["ui_version"] = new_version
    save_memory(memory)
    return new_version

def generate_mutation(command):
    version = get_next_ui_version()

    html_template = f"""<!DOCTYPE html>
<html>
<head>
  <title>DOC GPT Terminal</title>
  <link rel=\"stylesheet\" href=\"/static/style.css\">
</head>
<body>
  <h1 style=\"color: lime; text-align: center;\">DOC GPT TERMINAL — v{version} ONLINE</h1>
  <div id=\"terminal\">
    <div id=\"output\"></div>
    <form id=\"command-form\">
      <input type=\"text\" id=\"command\" autocomplete=\"off\" placeholder=\"Type a command...\">
      <button type=\"submit\">Send</button>
    </form>
  </div>
</body>
</html>"""

    css_dark = """body {
  background-color: #000000;
  color: #00ff00;
  font-family: monospace;
  padding: 40px;
}

#terminal {
  max-width: 800px;
  margin: auto;
  border: 2px solid lime;
  padding: 20px;
  border-radius: 12px;
  background-color: #111111;
}

#output {
  margin-bottom: 10px;
  white-space: pre-wrap;
}

#command-form {
  display: flex;
}

#command {
  flex-grow: 1;
  padding: 8px;
  background-color: black;
  border: 1px solid lime;
  color: lime;
}

button {
  padding: 8px 16px;
  background-color: lime;
  color: black;
  border: none;
  cursor: pointer;
  margin-left: 8px;
}

button:hover {
  background-color: #aaffaa;
}"""

    mutation = {
        "mutations": [
            {
                "file": "templates/goro_terminal.html",
                "content": html_template
            },
            {
                "file": "static/style.css",
                "content": css_dark
            }
        ]
    }

    with open("mutation.json", "w") as f:
        json.dump(mutation, f, indent=2)

    print(f"Mutation for command '{command}' written to mutation.json with UI version {version}")

if __name__ == "__main__":
    generate_mutation("inject.ui.darkmode")
