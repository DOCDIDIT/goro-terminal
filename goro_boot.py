from inject_ui_optimization import inject_ui_optimization
from blueprint_loader import load_ui_blueprint
from inject_terminal_theme import inject_terminal_theme
from template_binder import bind_template_to_memory


def goro_boot_init():
    print("[Goro Boot] Starting initialization...")

    try:
        inject_ui_optimization()
        print("[Goro Boot] UI optimization injected.")
    except Exception as e:
        print("[Goro Boot] UI injection failed:", str(e))

    try:
        blueprint = load_ui_blueprint("terminal_base")
        print("[Goro Boot] Loaded terminal_base blueprint.")
    except Exception as e:
        print("[Goro Boot] Failed to load UI blueprint:", str(e))

    try:
        with open("templates/goro_terminal.html", "r") as f:
            html = f.read()
        bind_template_to_memory("terminal_v2", html)
        print("[Theme Inject] Applied goro_terminal theme.")
    except Exception as e:
        print("[Theme Inject] Failed to apply theme:", str(e))
