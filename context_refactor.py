
import os
import re

def read_file(file_path):
    if not os.path.exists(file_path):
        print(f"[Refactor] File not found: {file_path}")
        return None
    with open(file_path, "r") as f:
        return f.read()

def write_file(file_path, content):
    with open(file_path, "w") as f:
        f.write(content)
    print(f"[Refactor] File written: {file_path}")

def simplify_redundant_comments(content):
    lines = content.splitlines()
    cleaned_lines = []
    for line in lines:
        if "# Mutation Patch" in line and line.strip().startswith("#"):
            continue  # Skip repeated mutation tags
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def consolidate_duplicate_imports(content):
    seen = set()
    result = []
    for line in content.splitlines():
        if line.strip().startswith("import") or line.strip().startswith("from"):
            if line in seen:
                continue
            seen.add(line)
        result.append(line)
    return "\n".join(result)

def refactor_file(file_path):
    original = read_file(file_path)
    if original is None:
        return

    print(f"[Refactor] Starting cleanup on {file_path}...")

    simplified = simplify_redundant_comments(original)
    optimized = consolidate_duplicate_imports(simplified)

    if optimized != original:
        write_file(file_path, optimized)
        print(f"[Refactor] {file_path} cleaned and optimized.")
    else:
        print(f"[Refactor] No changes needed in {file_path}.")

if __name__ == "__main__":
    test_target = "main.py"
    refactor_file(test_target)
