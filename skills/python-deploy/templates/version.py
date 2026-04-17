"""
Version management for {{APP_NAME}}.
Single source of truth — build scripts sync installer.iss and version_info.txt from here.
"""

# Bump these for each release. build/build.py --bump {major|minor|patch} will do it for you.
VERSION_MAJOR = 1
VERSION_MINOR = 0
VERSION_PATCH = 0

VERSION = f"{VERSION_MAJOR}.{VERSION_MINOR}.{VERSION_PATCH}"
VERSION_TUPLE = (VERSION_MAJOR, VERSION_MINOR, VERSION_PATCH)

APP_NAME = "{{APP_NAME}}"
APP_AUTHOR = "{{APP_PUBLISHER}}"
APP_ID = "com.{{APP_PUBLISHER_LOWER}}.{{APP_SLUG_LOWER}}"

# Network share for auto-updates.
# Signed installer .exe + version.json live here.
UPDATE_PATH = {{UPDATE_PATH_RAW}}

# version.json format (written by build/release.py):
# {
#   "version": "1.0.1",
#   "installer": "{{APP_SLUG}}_Setup_1.0.1.exe",
#   "sha256": "<hex digest>",
#   "release_notes": "..."
# }


def get_version_string() -> str:
    return VERSION


def get_version_tuple() -> tuple:
    return VERSION_TUPLE


def compare_versions(v1: str, v2: str) -> int:
    """Return -1/0/1 for v1 < == > v2. Handles simple major.minor.patch only."""
    def parse(v):
        return tuple(int(x) for x in v.split('.'))
    t1, t2 = parse(v1), parse(v2)
    return -1 if t1 < t2 else (1 if t1 > t2 else 0)
