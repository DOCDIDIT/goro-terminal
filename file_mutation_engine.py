
import os
import json

def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"[FileEngine] File not found: {file_path}")
        return None
    with open(file_path, "r") as f:
        return f.read()

def write_file(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)
    print(f"[FileEngine] File written: {file_path}")

def append_to_file(file_path, patch_text):
    if not os.path.exists(file_path):
        print(f"[FileEngine] Cannot append. File not found: {file_path}")
        return
    with open(file_path, "a") as f:
        f.write(f"\n\n# Mutation Patch\n{patch_text}\n")
    print(f"[FileEngine] Patch appended to: {file_path}")

def replace_in_file(file_path, match_text, replacement):
    if not os.path.exists(file_path):
        print(f"[FileEngine] File not found: {file_path}")
        return False
    with open(file_path, "r") as f:
        content = f.read()
    if match_text not in content:
        print(f"[FileEngine] Match text not found in {file_path}")
        return False
    content = content.replace(match_text, replacement)
    with open(file_path, "w") as f:
        f.write(content)
    print(f"[FileEngine] Text replaced in: {file_path}")
    return True

def file_status(file_path):
    exists = os.path.exists(file_path)
    size = os.path.getsize(file_path) if exists else 0
    return {
        "path": file_path,
        "exists": exists,
        "size": size
    }

if __name__ == "__main__":
    print("[FileEngine] Sample run:")
    print(file_status("main.py"))
