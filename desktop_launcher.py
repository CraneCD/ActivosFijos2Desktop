#!/usr/bin/env python3
"""
Desktop launcher for Activos Fijos Etiquetas 2.0.
Runs the Streamlit app and opens the default browser.
When built with PyInstaller, app.py and Logo.svg are next to the executable.
"""
import os
import sys
import threading
import webbrowser
import time

# When frozen with PyInstaller: one-file uses _MEIPASS (unpacked files), one-folder uses exe dir
if getattr(sys, "frozen", False):
    app_dir = getattr(sys, "_MEIPASS", os.path.dirname(sys.executable))
else:
    app_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(app_dir)
sys.path.insert(0, app_dir)

APP_SCRIPT = os.path.join(app_dir, "app.py")
URL = "http://localhost:8501"


def open_browser():
    time.sleep(2.0)
    webbrowser.open(URL)


def main():
    if not os.path.isfile(APP_SCRIPT):
        print(f"Error: app.py not found in {app_dir}")
        input("Press Enter to exit...")
        sys.exit(1)

    # Open browser after a short delay so Streamlit has time to start
    threading.Thread(target=open_browser, daemon=True).start()

    import streamlit.web.cli as stcli
    sys.argv = ["streamlit", "run", APP_SCRIPT, "--server.headless", "true", "--browser.gatherUsageStats", "false"]
    stcli.main()


if __name__ == "__main__":
    main()
