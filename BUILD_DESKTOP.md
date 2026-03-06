# Desktop build – Activos Fijos Etiquetas 2.0

You can build a **single executable** that someone can run without installing Python or Streamlit. When they run it, the app starts and their browser opens to the labels UI.

## What you need

- Python 3.8+ with the project dependencies installed:
  ```bash
  pip install -r requirements.txt
  ```
- PyInstaller (the build script installs it if missing).

## Build

**Linux / macOS (build for your current OS):**
```bash
./build_desktop.sh
```

**Windows (build on a Windows machine):**
```cmd
build_desktop.bat
```

### Building the Windows .exe from Linux (Fedora, etc.)

PyInstaller only builds for the OS you’re on, so on Linux you get a Linux binary, not a Windows .exe. To get a **Windows executable** from Fedora, use GitHub Actions (runs the build on Windows and gives you a downloadable .exe):

1. **Push your project to GitHub** (if it’s not already there):
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/activosfijos2.git
   git add .
   git commit -m "Add desktop build and Windows CI"
   git push -u origin main
   ```
   (Use your real repo URL and branch name.)

2. **Trigger the build**
   - Go to your repo on GitHub → **Actions**.
   - Click **“Build Windows desktop”** in the left sidebar.
   - Either wait for the workflow that runs on push, or click **“Run workflow”** and run it.

3. **Download the .exe**
   - When the run finishes (green check), open the run.
   - In **Artifacts**, download **ActivosFijos2-Windows** (a zip containing `ActivosFijos2.exe`).
   - Unzip and send `ActivosFijos2.exe` to Windows users.

The workflow file is `.github/workflows/build-windows-desktop.yml`; it uses a Windows runner, installs dependencies, runs PyInstaller, and uploads the exe as an artifact.

Or manually (on the OS you want the binary for):
```bash
pip install pyinstaller
pyinstaller --noconfirm ActivosFijos2_desktop.spec
```

## Output

- **One-file build:** `dist/ActivosFijos2` (Linux/macOS) or `dist/ActivosFijos2.exe` (Windows).
- Send that **single file** to the user. They double‑click it; a console window may appear, then the browser opens to the app. They do not need Python or anything else installed.

## For the person who receives it

1. Get the file `ActivosFijos2` (or `ActivosFijos2.exe` on Windows).
2. Double‑click it.
3. Wait a few seconds; the browser will open with the app.
4. To close the app, close the console window or press Ctrl+C in it.

## Notes

- The first run can be slow while the app unpacks.
- Antivirus may flag new executables; the recipient may need to allow it.
- If the build fails (e.g. missing Streamlit modules), run again with:
  `pyinstaller --log-level DEBUG ActivosFijos2_desktop.spec`
  and check the log for missing imports or data files.
