@echo off
REM Build desktop executable for Activos Fijos Etiquetas 2.0.
REM Requires: Python env with streamlit, reportlab, svglib, pillow, pyinstaller.
REM Run from project root: build_desktop.bat

cd /d "%~dp0"

if not exist app.py (echo app.py not found & exit /b 1)
if not exist Logo.svg (echo Logo.svg not found & exit /b 1)
if not exist desktop_launcher.py (echo desktop_launcher.py not found & exit /b 1)

echo Installing PyInstaller if needed...
pip install -q pyinstaller

echo Building (this may take a few minutes)...
pyinstaller --noconfirm ActivosFijos2_desktop.spec

echo Done. Executable: dist\ActivosFijos2.exe
echo Send dist\ActivosFijos2.exe to run the app (no Python needed).
dir dist\ActivosFijos2.exe 2>nul
pause
