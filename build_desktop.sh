#!/usr/bin/env bash
# Build desktop executable for Activos Fijos Etiquetas 2.0.
# Requires: Python env with streamlit, reportlab, svglib, pillow, pyinstaller installed.
# Run from project root: ./build_desktop.sh

set -e
cd "$(dirname "$0")"

echo "Checking app files..."
test -f app.py || { echo "app.py not found"; exit 1; }
test -f Logo.svg || { echo "Logo.svg not found"; exit 1; }
test -f desktop_launcher.py || { echo "desktop_launcher.py not found"; exit 1; }

echo "Installing PyInstaller if needed..."
pip install -q pyinstaller

echo "Building (this may take a few minutes)..."
pyinstaller --noconfirm ActivosFijos2_desktop.spec

echo "Done. Executable: dist/ActivosFijos2"
echo "Send the file dist/ActivosFijos2 to run the app (no Python needed)."
ls -la dist/ActivosFijos2 2>/dev/null || true
