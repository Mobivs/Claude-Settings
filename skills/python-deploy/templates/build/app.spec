# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for {{APP_NAME}}.
Run with: pyinstaller build/{{APP_SLUG_LOWER}}.spec
"""

import os

PROJ_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(SPEC)))

# Read version from version.py
version_info = {}
with open(os.path.join(PROJ_ROOT, 'version.py'), 'r') as f:
    exec(f.read(), version_info)
VERSION = version_info['VERSION']

# Bundled data files — edit this list per app.
datas_list = [
    # Example: (os.path.join(PROJ_ROOT, 'assets'), 'assets'),
    # Example: (os.path.join(PROJ_ROOT, 'templates', 'report.svg'), 'templates'),
]

a = Analysis(
    [os.path.join(PROJ_ROOT, '{{ENTRY_SCRIPT}}')],
    pathex=[PROJ_ROOT],
    binaries=[],
    datas=datas_list,
    hiddenimports=[
        # Project-specific — add modules PyInstaller can't trace (dynamic imports, plugin loaders,
        # DB drivers, keyring backends, etc.). Smoke-test the build; if it fails at runtime with
        # ModuleNotFoundError, add the missing module here.
        'version',
        'updater',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter.test',
        'pydoc',
        'doctest',
        'test',
        'tests',
        # NOTE: do NOT exclude 'unittest' — pyparsing.testing imports it at module level.
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{{APP_SLUG}}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,            # False for GUI apps; True for server/console apps (yellow-pine uses True)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    # icon=os.path.join(PROJ_ROOT, 'assets', 'icon.ico'),
    version=os.path.join(PROJ_ROOT, 'build', 'version_info.txt'),
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{{APP_SLUG}}',
)
