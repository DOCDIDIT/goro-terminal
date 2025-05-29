import json
from flask import request

def register_tool(app):
    @app.after_request
    def bind_memory(response):
        try:
            if request.path == '/chat' and response.status_code == 200:
                with open('memory.json', 'r') as f:
                    memory = json.load(f)
                memory['flame_summary'] += f" | {request.json.get('prompt', '').strip()}"
                with open('memory.json', 'w') as f:
                    json.dump(memory, f, indent=2)
        except:
            pass
        return response