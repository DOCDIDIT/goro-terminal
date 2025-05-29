import json
import os

def apply_mutations():
    if not os.path.exists("mutation.json"):
        print("mutation.json not found.")
        return

    with open("mutation.json", "r") as f:
        data = json.load(f)

    if not data.get("mutations"):
        print("No mutations to apply.")
        return

    for mutation in data["mutations"]:
        file_path = mutation["file"]
        content = mutation["content"]

        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"Updated {file_path}")
        except Exception as e:
            print(f"Error writing {file_path}: {e}")

    # Clear the mutations after applying
    with open("mutation.json", "w") as f:
        json.dump({"mutations": []}, f)

    print("Mutations applied and cleared.")
