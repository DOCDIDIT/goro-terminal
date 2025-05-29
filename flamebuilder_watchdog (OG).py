import time
import subprocess
from flamebuilder_injector import apply_mutations

CHECK_INTERVAL = 10  # seconds

def has_pending_mutations():
    try:
        with open("mutation.json", "r") as f:
            return "mutations" in f.read()
    except:
        return False

def git_push():
    try:
        subprocess.run(["git", "add", "."], check=True)
        # Check if there are staged changes
        status = subprocess.run(["git", "diff", "--cached", "--quiet"])
        if status.returncode == 0:
            print("No changes to commit.")
            return

        subprocess.run(["git", "commit", "-m", "FlameBuilder: auto-mutation"], check=True)
        subprocess.run(["git", "push"], check=True)
        print("Pushed to GitHub.")
    except Exception as e:
        print(f"Git push failed: {e}")

while True:
    if has_pending_mutations():
        print("Detected mutation. Applying...")
        apply_mutations()
        git_push()
    time.sleep(CHECK_INTERVAL)
