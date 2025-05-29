import json

def write_ui_mutation():
    mutation = {
        "mutations": [
            {
                "file": "templates/goro_terminal.html",
                "content": "<!DOCTYPE html>\n<html>\n<head>\n  <title>DOC GPT Terminal</title>\n  <link rel=\"stylesheet\" href=\"/static/style.css\">\n</head>\n<body>\n  <h1 style=\"color: lime; text-align: center;\">DOC GPT TERMINAL — v2.7 ONLINE</h1>\n  <div id=\"terminal\">\n    <div id=\"output\"></div>\n    <form id=\"command-form\">\n      <input type=\"text\" id=\"command\" autocomplete=\"off\" placeholder=\"Type a command...\">\n      <button type=\"submit\">Send</button>\n    </form>\n  </div>\n</body>\n</html>"
            },
            {
                "file": "static/style.css",
                "content": "body {\n  background-color: #000000;\n  color: #00ff00;\n  font-family: monospace;\n  padding: 40px;\n}\n\n#terminal {\n  max-width: 800px;\n  margin: auto;\n  border: 2px solid lime;\n  padding: 20px;\n  border-radius: 12px;\n  background-color: #111111;\n}\n\n#output {\n  margin-bottom: 10px;\n  white-space: pre-wrap;\n}\n\n#command-form {\n  display: flex;\n}\n\n#command {\n  flex-grow: 1;\n  padding: 8px;\n  background-color: black;\n  border: 1px solid lime;\n  color: lime;\n}\n\nbutton {\n  padding: 8px 16px;\n  background-color: lime;\n  color: black;\n  border: none;\n  cursor: pointer;\n  margin-left: 8px;\n}\n\nbutton:hover {\n  background-color: #aaffaa;\n}"
            }
        ]
    }

    with open("mutation.json", "w") as f:
        json.dump(mutation, f, indent=2)

    print("Goro UI mutation queued.")

if __name__ == "__main__":
    write_ui_mutation()
