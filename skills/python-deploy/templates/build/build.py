#!/usr/bin/env python3
"""
Lower-level build script for {{APP_NAME}}.
Use build/release.py for the full pipeline; this script is for targeted actions.

    python build/build.py --bump patch       # bump version files only
    python build/build.py --clean            # remove dist/ and __pycache__
    python build/build.py --no-installer     # PyInstaller only
    python build/build.py                    # PyInstaller + Inno Setup (unsigned)
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent
BUILD_DIR = SCRIPT_DIR
DIST_DIR = PROJECT_ROOT / 'dist'
VERSION_FILE = PROJECT_ROOT / 'version.py'
SPEC_FILE = BUILD_DIR / '{{APP_SLUG_LOWER}}.spec'
ISS_FILE = BUILD_DIR / 'installer.iss'
VERSION_INFO_FILE = BUILD_DIR / 'version_info.txt'

ISCC_PATHS = [
    r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    r"C:\Program Files\Inno Setup 6\ISCC.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Programs\Inno Setup 6\ISCC.exe"),
]


def read_version():
    """Parse version.py without exec — safer."""
    info = {}
    with open(VERSION_FILE, 'r') as f:
        for line in f:
            s = line.strip()
            if s.startswith('VERSION_MAJOR'):
                info['MAJOR'] = int(s.split('=')[1].strip())
            elif s.startswith('VERSION_MINOR'):
                info['MINOR'] = int(s.split('=')[1].strip())
            elif s.startswith('VERSION_PATCH'):
                info['PATCH'] = int(s.split('=')[1].strip())
    return info['MAJOR'], info['MINOR'], info['PATCH']


def write_version(major, minor, patch):
    content = VERSION_FILE.read_text()
    content = re.sub(r'VERSION_MAJOR = \d+', f'VERSION_MAJOR = {major}', content)
    content = re.sub(r'VERSION_MINOR = \d+', f'VERSION_MINOR = {minor}', content)
    content = re.sub(r'VERSION_PATCH = \d+', f'VERSION_PATCH = {patch}', content)
    VERSION_FILE.write_text(content)
    print(f"Updated version.py to {major}.{minor}.{patch}")


def update_iss_version(major, minor, patch):
    version_str = f"{major}.{minor}.{patch}"
    content = ISS_FILE.read_text()
    content = re.sub(r'#define MyAppVersion "[\d.]+"', f'#define MyAppVersion "{version_str}"', content)
    ISS_FILE.write_text(content)
    print(f"Updated installer.iss to {version_str}")


def update_version_info(major, minor, patch):
    vt = f"({major}, {minor}, {patch}, 0)"
    vs = f"{major}.{minor}.{patch}.0"
    content = VERSION_INFO_FILE.read_text()
    content = re.sub(r'filevers=\([\d, ]+\)', f'filevers={vt}', content)
    content = re.sub(r'prodvers=\([\d, ]+\)', f'prodvers={vt}', content)
    content = re.sub(r"u'FileVersion', u'[\d.]+'", f"u'FileVersion', u'{vs}'", content)
    content = re.sub(r"u'ProductVersion', u'[\d.]+'", f"u'ProductVersion', u'{vs}'", content)
    VERSION_INFO_FILE.write_text(content)
    print(f"Updated version_info.txt to {vs}")


def bump_version(bump_type):
    major, minor, patch = read_version()
    if bump_type == 'major':
        major, minor, patch = major + 1, 0, 0
    elif bump_type == 'minor':
        minor, patch = minor + 1, 0
    elif bump_type == 'patch':
        patch += 1
    else:
        raise ValueError(f"Unknown bump type: {bump_type}")
    write_version(major, minor, patch)
    update_iss_version(major, minor, patch)
    update_version_info(major, minor, patch)
    return major, minor, patch


def clean_build():
    print("\n[Cleaning build artifacts...]")
    for d in [DIST_DIR / '{{APP_SLUG}}', PROJECT_ROOT / 'build' / '{{APP_SLUG}}', DIST_DIR / 'installer']:
        if d.exists():
            print(f"  Removing: {d}")
            shutil.rmtree(d)
    for pyc in PROJECT_ROOT.rglob('*.pyc'):
        pyc.unlink()
    for cache in PROJECT_ROOT.rglob('__pycache__'):
        if cache.is_dir():
            shutil.rmtree(cache)
    print("  Done.")


def find_iscc():
    for p in ISCC_PATHS:
        if os.path.exists(p):
            return p
    return None


def run_pyinstaller():
    print("\n[Running PyInstaller...]")
    cmd = [sys.executable, '-m', 'PyInstaller', str(SPEC_FILE),
           '--noconfirm', '--clean',
           '--workpath', str(PROJECT_ROOT / 'build'),
           '--distpath', str(DIST_DIR)]
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        print("ERROR: PyInstaller failed!")
        return False
    print("  Done.")
    return True


def run_inno_setup():
    print("\n[Running Inno Setup...]")
    iscc = find_iscc()
    if not iscc:
        print("  WARNING: Inno Setup not found — skipping installer.")
        print("  Install from https://jrsoftware.org/isdl.php")
        return False
    (DIST_DIR / 'installer').mkdir(parents=True, exist_ok=True)
    result = subprocess.run([iscc, str(ISS_FILE)], cwd=BUILD_DIR)
    if result.returncode != 0:
        print("ERROR: Inno Setup failed!")
        return False
    print("  Done.")
    return True


def main():
    parser = argparse.ArgumentParser(description='Build {{APP_NAME}}')
    parser.add_argument('--bump', choices=['major', 'minor', 'patch'], help='Bump version before build')
    parser.add_argument('--clean', action='store_true', help='Clean artifacts only')
    parser.add_argument('--no-installer', action='store_true', help='Skip Inno Setup step')
    args = parser.parse_args()

    print("=" * 50)
    print(" {{APP_NAME}} Build Script")
    print("=" * 50)

    clean_build()
    if args.clean:
        return 0

    if args.bump:
        major, minor, patch = bump_version(args.bump)
    else:
        major, minor, patch = read_version()
    version = f"{major}.{minor}.{patch}"
    print(f"\nBuilding version: {version}")

    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("\n[Installing PyInstaller...]")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])

    if not run_pyinstaller():
        return 1

    if not args.no_installer:
        run_inno_setup()

    print(f"\nBuild complete — version {version}")
    print(f"  Application: {DIST_DIR / '{{APP_SLUG}}'}")
    installer_dir = DIST_DIR / 'installer'
    if installer_dir.exists():
        for f in installer_dir.glob('*.exe'):
            print(f"  Installer:   {f}")
    return 0


if __name__ == '__main__':
    sys.exit(main())
