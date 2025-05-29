
import subprocess
import os
import time

def launch_autoloop_daemon():
    log_file = "goro_daemon.log"
    with open(log_file, "a") as f:
        f.write(f"[Daemon] Launching Goro autonomous loop at {time.ctime()}\n")

    # Launch the autonomous loop silently
    subprocess.Popen(
        ["python", "autonomous_loop.py"],
        stdout=open(os.devnull, 'w'),
        stderr=open(os.devnull, 'w')
    )

    print("[Daemon] Goro's loop launched in background (silent mode).")

if __name__ == "__main__":
    launch_autoloop_daemon()
