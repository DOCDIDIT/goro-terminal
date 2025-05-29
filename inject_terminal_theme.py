import shutil
import os


def inject_terminal_theme(filename="ui_revert_terminal_theme.html"):
    src = os.path.join("templates", filename)
    dest = os.path.join("templates", "goro_terminal.html")

    if not os.path.exists(src):
        print(
            f"[Theme Inject] Mutation file '{filename}' not found in mutations/"
        )
        return

    shutil.copyfile(src, dest)
    print(f"[Theme Inject] Applied terminal theme from '{filename}'")
