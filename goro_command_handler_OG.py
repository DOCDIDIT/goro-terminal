import subprocess
import sys


def handle_command(command):
    if command.startswith("inject.ui.darkmode"):
        subprocess.run(["python3", "goro_ui_mutator.py"])
        return "Darkmode UI mutation injected."

    elif command.startswith("inject.ui.chatgpt.clone"):
        subprocess.run(["python3", "goro_ui_chatgpt_clone.py"])
        return "ChatGPT UI clone mutation injected."

    elif command.lower() == "trigger.phase44":
        return "Phase 44 acknowledged. Neural behavior expansion queued. Introspective mutation logic now activating."

    else:
        return f"Unknown command: {command}"


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERROR] No command provided.")
    else:
        cmd = sys.argv[1]
        result = handle_command(cmd)
        print(result)
