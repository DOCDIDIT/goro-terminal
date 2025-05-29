import os

ui_templates = {}


def inject_ui_optimization():
    print("[Goro Boot] UI optimization injected.")

    try:
        for file in os.listdir("mutations"):
            if not file.endswith(".html"):
                continue

            try:
                with open(f"mutations/{file}", "r", encoding="utf-8") as f:
                    html = f.read()
                    if "<html" not in html:
                        raise ValueError("File doesn't look like HTML")
                    key = file.split(".")[0]
                    ui_templates[key] = html
                    print(f"[Inject] Bound UI template: {key}")
            except Exception as e:
                print(f"[Inject Error] Skipped {file}: {e}")
    except Exception as e:
        print(f"[Inject Error] Could not list mutations folder: {e}")
