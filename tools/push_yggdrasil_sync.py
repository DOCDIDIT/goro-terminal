import requests, json
from flask import Flask

def register_tool(app):
    @app.route('/push_now', methods=['POST'])
    def push_memory():
        try:
            url = 'https://docgpt-memory-default-rtdb.firebaseio.com/memory.json'
            with open('memory.json', 'r') as f:
                memory = json.load(f)

            r = requests.put(url, json=memory)
            print('YGGDRASIL PUSH RESPONSE:', r.text)

            if r.status_code == 200:
                return {'status': 'Memory pushed to Yggdrasil'}
            else:
                return {'error': 'Push failed', 'code': r.status_code}
        except Exception as e:
            return {'error': str(e)}