# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Activos Fijos Etiquetas 2.0 desktop app.
# Build: pyinstaller ActivosFijos2_desktop.spec
# Output: dist/ActivosFijos2/ folder — zip it and send; run ActivosFijos2.exe (Windows) or ActivosFijos2 (Linux/macOS).

import os

block_cipher = None

# App files that must sit next to the executable at runtime
app_datas = [
    ('app.py', '.'),
    ('Logo.svg', '.'),
]

# Include Streamlit's package data (static files, etc.) so the UI works
try:
    from PyInstaller.utils.hooks import collect_data_files
    streamlit_datas = collect_data_files('streamlit')
except Exception:
    streamlit_datas = []

a = Analysis(
    ['desktop_launcher.py'],
    pathex=[],
    binaries=[],
    datas=app_datas + streamlit_datas,
    hiddenimports=[
        'streamlit',
        'streamlit.web',
        'streamlit.web.cli',
        'streamlit.runtime',
        'streamlit.runtime.scriptrunner',
        'streamlit.runtime.state',
        'streamlit.runtime.uploaded_file_manager',
        'streamlit.case_converters',
        'streamlit.elements',
        'streamlit.proto',
        'streamlit.delta_generator',
        'streamlit.components',
        'streamlit.logger',
        'streamlit.config',
        'streamlit.in_memory_file_manager',
        'reportlab',
        'reportlab.pdfgen',
        'reportlab.graphics.barcode',
        'reportlab.graphics.barcode.code128',
        'reportlab.graphics',
        'reportlab.graphics.renderPDF',
        'svglib',
        'svglib.svglib',
        'PIL',
        'PIL._tkinter_finder',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ActivosFijos2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Keep console so user sees logs and can close the app cleanly
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
