import json


def register_tool(app):
    with open("memory.json", "r") as f:
        m = json.load(f)
        globals()['persona_prompt'] = m.get('persona_prompt', '')
        globals()['flame_summary'] = m.get('flame_summary', '')
    return {'status': 'Live memory bound from memory.json'}
