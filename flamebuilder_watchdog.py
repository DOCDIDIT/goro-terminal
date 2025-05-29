import time
import os
import importlib.util

# Load mutation queue handler dynamically
def run_mutation_handler():
    try:
        spec = importlib.util.spec_from_file_location("apply_mutation_queue", "apply_mutation_queue.py")
        mutation_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mutation_module)
        mutation_module.apply_mutation_queue()
    except Exception as e:
        print(f"[Watchdog Error] Failed to apply mutations: {e}")

if __name__ == "__main__":
    print("[Watchdog] Starting Goro mutation watchdog...")
    run_mutation_handler()
    # You can expand this to include file watching logic
    print("[Watchdog] Watching complete. Mutations applied.")
