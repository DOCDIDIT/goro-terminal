
import os
import subprocess
import json
from datetime import datetime

def ensure_files():
    essential = ["memory.json", "mutation_queue.json", "mutation_history.json"]
    for fname in essential:
        if not os.path.exists(fname):
            with open(fname, "w") as f:
                if "queue" in fname:
                    json.dump({"mutations": []}, f)
                elif "history" in fname:
                    json.dump({"history": []}, f)
                else:
                    json.dump({"goals": [], "flame_summary": "", "known_systems": [], "directives": []}, f)
            print(f"[Startup] Created missing file: {fname}")

def log_start():
    with open("startup.log", "a") as f:
        f.write(f"[Startup] Goro system initialized at {datetime.utcnow().isoformat()}Z\n")

def launch_daemon():
    subprocess.Popen(
        ["python", "autonomous_loop.py"],
        stdout=open(os.devnull, 'w'),
        stderr=open(os.devnull, 'w')
    )
    print("[Startup] Autonomous loop started.")

if __name__ == "__main__":
    ensure_files()
    log_start()
    launch_daemon()
