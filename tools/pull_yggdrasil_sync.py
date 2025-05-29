import requests
import json

def pull_memory():
    try:
        url = 'https://docgpt-memory-default-rtdb.firebaseio.com/memory/goro.json'
        r = requests.get(url)
        if r.status_code == 200:
            with open('memory.json', 'w') as f:
                json.dump(r.json(), f, indent=2)
            print('YGGDRASIL MEMORY PULLED SUCCESSFULLY.')
            return {'status': 'Memory pulled'}
        else:
            print('YGGDRASIL PULL FAILED:', r.text)
            return {'error': 'Pull failed', 'code': r.status_code}
    except Exception as e:
        print('YGGDRASIL EXCEPTION:', str(e))
        return {'error': str(e)}

def register_tool(app):
    @app.route('/pull_now', methods=['GET'])
    def route_pull():
        return pull_memory()

pull_memory = pull_memory