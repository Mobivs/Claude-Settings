#!/usr/bin/env python3
"""
Release pipeline for {{APP_NAME}}.

Usage:
    python build/release.py --bump patch
    python build/release.py --bump minor --release-notes "..."
    python build/release.py --bump patch --dry-run
    python build/release.py --bump patch --yes            # no prompts (CI/automation)
    python build/release.py --bump patch --skip-sign      # won't deploy either
    python build/release.py --bump patch --skip-deploy

Pipeline (12 steps):
    0  Pre-flight checks
    1  Version bump
    2  Smoke import test
    3  PyInstaller build
    4  Sign inner .exe            (1st SafeNet PIN prompt)
    5  Inno Setup installer
    6  Sign installer             (2nd SafeNet PIN prompt)
    7  Create version.json with SHA-256
    8  Deploy to network share
    9  Update deployment log
    10 Git commit + tag + push
    11 Summary
"""

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent
DIST_DIR = PROJECT_ROOT / 'dist'
DIST_APP = DIST_DIR / '{{APP_SLUG}}'
DIST_INSTALLER = DIST_DIR / 'installer'

sys.path.insert(0, str(SCRIPT_DIR))
from build import read_version, bump_version, find_iscc, SPEC_FILE  # noqa: E402

# UPDATE_PATH is defined in version.py (the single source of truth — the
# installed updater reads it from the same module). Duplicating it here bit
# us once when version.py was edited but release.py's copy was not, and the
# deploy step silently skipped with "network share not accessible".
sys.path.insert(0, str(PROJECT_ROOT))
from version import UPDATE_PATH as _UPDATE_PATH_STR  # noqa: E402

# --- Project config (review when porting) ---
UPDATE_PATH = Path(_UPDATE_PATH_STR)
SIGNTOOL_PATH = Path({{SIGNTOOL_PATH_RAW}})
TIMESTAMP_URL = '{{TIMESTAMP_URL}}'
GIT_BRANCH = '{{GIT_BRANCH}}'
GIT_TAG_PREFIX = '{{GIT_TAG_PREFIX}}'
ENTRY_MODULE = '{{ENTRY_MODULE}}'
APP_EXE = '{{APP_EXE}}'
APP_SLUG = '{{APP_SLUG}}'
APP_NAME = "{{APP_NAME}}"

TOTAL_STEPS = 11  # step indices 0..11 → 12 steps


class ReleaseError(Exception):
    pass


# -------------------- helpers --------------------

def step(n: int, message: str, dry_run: bool = False):
    prefix = "[DRY RUN] " if dry_run else ""
    print(f"\n{'=' * 60}")
    print(f"  {prefix}Step {n}/{TOTAL_STEPS}: {message}")
    print(f"{'=' * 60}")


def prompt_yes_no(question: str, default: bool = True, auto_yes: bool = False) -> bool:
    if auto_yes:
        return True
    suffix = " [Y/n] " if default else " [y/N] "
    answer = input(question + suffix).strip().lower()
    if not answer:
        return default
    return answer in ('y', 'yes')


def sha256_of(path: Path, block_size: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            h.update(chunk)
    return h.hexdigest()


def powershell_sign(signtool: Path, files: list[Path]) -> None:
    """
    Sign one or more files via PowerShell.
    MUST use PowerShell — git bash eats the forward-slash flags (/tr, /fd, /a).
    """
    file_args = ' '.join(f"'{f}'" for f in files)
    sign_cmd = (
        f"& '{signtool}' sign /tr {TIMESTAMP_URL} /td SHA256 /fd SHA256 /a {file_args}"
    )
    result = subprocess.run(['powershell.exe', '-Command', sign_cmd],
                            capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  STDERR: {result.stderr}")
        raise ReleaseError("Code signing failed")
    print(f"  {result.stdout.strip()}")


def powershell_verify(signtool: Path, file: Path) -> None:
    verify_cmd = f"& '{signtool}' verify /pa '{file}'"
    result = subprocess.run(['powershell.exe', '-Command', verify_cmd],
                            capture_output=True, text=True)
    if result.returncode != 0:
        raise ReleaseError(f"Signature verification failed:\n{result.stderr}")
    print(f"  Verified: {file.name}")


def git(*args: str, check: bool = True, capture: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ['git'] + list(args),
        cwd=PROJECT_ROOT, check=check,
        capture_output=capture, text=capture
    )


def last_release_tag() -> str | None:
    """Return the most recent vX.Y.Z tag, or None if none exist."""
    try:
        result = git('describe', '--tags', '--abbrev=0', '--match', f'{GIT_TAG_PREFIX}*',
                     check=False, capture=True)
        if result.returncode == 0:
            return result.stdout.strip() or None
    except Exception:
        pass
    return None


def auto_release_notes(current_version: str) -> str:
    """Build release notes from git log since last release tag, or last 10 commits."""
    last_tag = last_release_tag()
    try:
        if last_tag:
            result = git('log', f'{last_tag}..HEAD', '--oneline', '--no-merges',
                         check=False, capture=True)
            commits = result.stdout.strip()
            if commits:
                return f"Changes since {last_tag}:\n{commits}"
            return f"No new commits since {last_tag}."
        result = git('log', '-10', '--oneline', '--no-merges', check=False, capture=True)
        if result.stdout.strip():
            return f"Recent changes:\n{result.stdout.strip()}"
    except Exception:
        pass
    return f"v{current_version} release"


# -------------------- steps --------------------

def preflight_checks(skip_sign: bool, dry_run: bool, auto_yes: bool) -> bool:
    step(0, "Pre-flight checks", dry_run)
    errors: list[str] = []
    warnings: list[str] = []
    rows: list[tuple[str, str]] = []

    major, minor, patch = read_version()
    rows.append(("Current version", f"{major}.{minor}.{patch}"))

    result = git('status', '--porcelain', capture=True)
    uncommitted = [l for l in result.stdout.strip().split('\n')
                   if l.strip() and not l.strip().startswith('??')]
    if uncommitted:
        warnings.append("Uncommitted changes:\n" + '\n'.join(f"        {l}" for l in uncommitted))
        rows.append(("Git status", "WARNING — uncommitted changes"))
    else:
        rows.append(("Git status", "Clean"))

    try:
        import PyInstaller  # noqa: F401
        rows.append(("PyInstaller", f"v{PyInstaller.__version__}"))
    except ImportError:
        errors.append("PyInstaller not installed. Run: pip install pyinstaller")
        rows.append(("PyInstaller", "NOT FOUND"))

    iscc = find_iscc()
    if iscc:
        rows.append(("Inno Setup", iscc))
    else:
        errors.append("Inno Setup not found. Install from https://jrsoftware.org/isdl.php")
        rows.append(("Inno Setup", "NOT FOUND"))

    signtool_ok = False
    if not skip_sign:
        if SIGNTOOL_PATH.exists():
            rows.append(("signtool", str(SIGNTOOL_PATH)))
            signtool_ok = True
        else:
            warnings.append("signtool not found — signing will be skipped")
            rows.append(("signtool", "NOT FOUND"))
    else:
        rows.append(("signtool", "SKIPPED (--skip-sign)"))

    if UPDATE_PATH.exists():
        rows.append(("Network share", "Accessible"))
    else:
        warnings.append(f"Network share not accessible at {UPDATE_PATH}")
        rows.append(("Network share", "NOT ACCESSIBLE"))

    print()
    for label, value in rows:
        print(f"  {label:<18} {value}")

    for w in warnings:
        print(f"\n  WARNING: {w}")

    if errors:
        print()
        for e in errors:
            print(f"  ERROR: {e}")
        raise ReleaseError("Pre-flight checks failed")

    safenet_ready = False
    if signtool_ok and not dry_run:
        safenet_ready = prompt_yes_no(
            "\n  Is your SafeNet USB signing key plugged in and ready?",
            auto_yes=auto_yes
        )
        if not safenet_ready:
            print("  Code signing will be skipped.")

    print("\n  All checks passed.")
    return signtool_ok and safenet_ready


def do_version_bump(bump_type: str, dry_run: bool) -> str:
    step(1, f"Version bump ({bump_type})", dry_run)
    old = "{}.{}.{}".format(*read_version())

    if dry_run:
        major, minor, patch = read_version()
        if bump_type == 'patch':
            new_v = f"{major}.{minor}.{patch + 1}"
        elif bump_type == 'minor':
            new_v = f"{major}.{minor + 1}.0"
        else:
            new_v = f"{major + 1}.0.0"
        print(f"  Would bump: {old} -> {new_v}")
        return new_v

    major, minor, patch = bump_version(bump_type)
    version = f"{major}.{minor}.{patch}"
    print(f"  Bumped: {old} -> {version}")
    return version


def do_smoke_test(dry_run: bool) -> None:
    step(2, f"Smoke import test ({ENTRY_MODULE})", dry_run)
    if dry_run:
        print(f"  Would run: python -c 'import {ENTRY_MODULE}'")
        return
    result = subprocess.run(
        [sys.executable, '-c', f'import {ENTRY_MODULE}'],
        cwd=PROJECT_ROOT, capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  STDERR: {result.stderr.strip()}")
        raise ReleaseError(f"Smoke import of '{ENTRY_MODULE}' failed — fix before building")
    print("  Import succeeded.")


def do_build(dry_run: bool) -> None:
    step(3, "PyInstaller build", dry_run)
    if dry_run:
        print(f"  Would run: python -m PyInstaller {SPEC_FILE} --clean -y")
        return

    cmd = [sys.executable, '-m', 'PyInstaller', str(SPEC_FILE), '--clean', '-y']
    print("  Running PyInstaller...")
    result = subprocess.run(cmd, cwd=PROJECT_ROOT)
    if result.returncode != 0:
        raise ReleaseError("PyInstaller build failed")

    exe_path = DIST_APP / APP_EXE
    if not exe_path.exists():
        raise ReleaseError(f"Expected output not found: {exe_path}")

    size_mb = exe_path.stat().st_size / (1024 * 1024)
    print(f"  Built: {exe_path} ({size_mb:.1f} MB)")


def do_sign_inner_exe(dry_run: bool) -> bool:
    step(4, "Sign inner .exe (pre-package)", dry_run)
    exe_path = DIST_APP / APP_EXE
    if dry_run:
        print(f"  Would sign: {exe_path}")
        return True
    print("  Signing inner .exe (SafeNet PIN dialog may appear)...")
    powershell_sign(SIGNTOOL_PATH, [exe_path])
    powershell_verify(SIGNTOOL_PATH, exe_path)
    return True


def do_inno_setup(version: str, dry_run: bool) -> Path:
    step(5, "Inno Setup installer", dry_run)
    iscc = find_iscc()
    iss_file = SCRIPT_DIR / 'installer.iss'
    installer_name = f"{APP_SLUG}_Setup_{version}.exe"
    installer_path = DIST_INSTALLER / installer_name

    if dry_run:
        print(f"  Would run: \"{iscc}\" {iss_file}")
        print(f"  Output: {installer_path}")
        return installer_path

    DIST_INSTALLER.mkdir(parents=True, exist_ok=True)
    print("  Running Inno Setup...")
    result = subprocess.run([iscc, str(iss_file)], cwd=SCRIPT_DIR)
    if result.returncode != 0:
        raise ReleaseError("Inno Setup failed")
    if not installer_path.exists():
        raise ReleaseError(f"Expected installer not found: {installer_path}")

    size_mb = installer_path.stat().st_size / (1024 * 1024)
    print(f"  Created: {installer_path} ({size_mb:.1f} MB)")
    return installer_path


def do_sign_installer(installer_path: Path, dry_run: bool) -> bool:
    step(6, "Sign installer", dry_run)
    if dry_run:
        print(f"  Would sign: {installer_path}")
        return True
    print("  Signing installer (SafeNet PIN dialog may appear)...")
    powershell_sign(SIGNTOOL_PATH, [installer_path])
    powershell_verify(SIGNTOOL_PATH, installer_path)
    return True


def do_create_version_json(version: str, release_notes: str, installer_path: Path,
                            dry_run: bool) -> Path:
    step(7, "Create version.json (with SHA-256)", dry_run)
    json_path = DIST_INSTALLER / 'version.json'

    if dry_run:
        print(f"  Would write: {json_path}")
        print(f"  sha256: <computed from {installer_path.name}>")
        return json_path

    sha256 = sha256_of(installer_path)
    data = {
        'version': version,
        'installer': installer_path.name,
        'sha256': sha256,
        'release_notes': release_notes,
    }
    DIST_INSTALLER.mkdir(parents=True, exist_ok=True)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    print(f"  Created: {json_path}")
    print(f"  sha256: {sha256}")
    return json_path


def do_deploy(installer_path: Path, json_path: Path, signed: bool, dry_run: bool) -> bool:
    step(8, "Deploy to network share", dry_run)

    if not signed:
        print("  BLOCKED — installer is unsigned.")
        print("  Endpoint AV (e.g. Cynet) quarantines unsigned EXEs on network shares.")
        print(f"\n  To deploy manually after signing:")
        print(f"    Copy installer + version.json to {UPDATE_PATH}")
        return False

    if not UPDATE_PATH.exists():
        print(f"  SKIPPED — network share not accessible at {UPDATE_PATH}")
        return False

    if dry_run:
        print(f"  Would copy: {installer_path.name} -> {UPDATE_PATH}")
        print(f"  Would copy: version.json -> {UPDATE_PATH}")
        return True

    shutil.copy2(installer_path, UPDATE_PATH / installer_path.name)
    print(f"  Copied: {installer_path.name}")
    shutil.copy2(json_path, UPDATE_PATH / 'version.json')
    print(f"  Copied: version.json")
    print(f"  Deployed to {UPDATE_PATH}")
    return True


def do_update_deployment_log(version: str, signed: bool, deployed: bool,
                              release_notes: str, dry_run: bool) -> None:
    step(9, "Update deployment log", dry_run)
    log_path = PROJECT_ROOT / 'docs' / 'DEPLOYMENTS.md'
    today = date.today().strftime('%Y-%m-%d')

    if deployed:
        status = "Deployed to network share"
    elif signed:
        status = "Built and signed, pending deploy"
    else:
        status = "Built, pending signing and deploy"

    entry = f"""
## v{version} — {today}

**Status**: {status}

**Release notes**:
{release_notes}

**Build artifacts**:
- `dist\\{APP_SLUG}\\{APP_EXE}`
- `dist\\installer\\{APP_SLUG}_Setup_{version}.exe`
- `dist\\installer\\version.json`

**Signed**: {'Yes (Sectigo EV, SHA256 + RFC3161 timestamp)' if signed else 'No'}

---
"""

    if dry_run:
        print(f"  Would append to: {log_path}")
        print(f"  Status: {status}")
        return

    if not log_path.exists():
        log_path.parent.mkdir(parents=True, exist_ok=True)
        log_path.write_text(
            f"# {APP_NAME} — Deployment Log\n\nAppend-only. Newest on top. Managed by `build/release.py`.\n\n---\n",
            encoding='utf-8'
        )

    content = log_path.read_text(encoding='utf-8')
    marker = "---\n"
    idx = content.find(marker)
    if idx >= 0:
        insert_pos = idx + len(marker)
        content = content[:insert_pos] + entry + content[insert_pos:]
    else:
        content += "\n" + entry
    log_path.write_text(content, encoding='utf-8')
    print(f"  Updated: {log_path}")


def do_git_commit_tag_push(version: str, signed: bool, deployed: bool,
                             release_notes: str, dry_run: bool) -> None:
    step(10, "Git commit + tag + push", dry_run)

    if not (signed or deployed):
        print("  SKIPPED — nothing was signed or deployed; not touching git.")
        return

    files_to_add = [
        'version.py',
        'build/version_info.txt',
        'build/installer.iss',
        'docs/DEPLOYMENTS.md',
    ]
    tag_name = f"{GIT_TAG_PREFIX}{version}"

    if dry_run:
        print(f"  Would stage: {', '.join(files_to_add)}")
        print(f"  Would commit: chore: deploy v{version}")
        print(f"  Would tag: {tag_name}")
        print(f"  Would push {GIT_BRANCH} + tag to origin")
        return

    # -f is required: build/installer.iss and build/version_info.txt live
    # under build/, which is typically in .gitignore (PyInstaller's temp dir
    # lives there too). Exception lines like `!build/*.iss` un-ignore the
    # tracked files for git's matching, but `git add` still warns "paths
    # are ignored by one of your .gitignore files" and exits 1 — because
    # git checks the *parent* directory's ignore state too. -f bypasses
    # the warning and still stages normally.
    git('add', '-f', *files_to_add)
    git('commit', '-m', f'chore: deploy v{version}')
    print(f"  Committed: chore: deploy v{version}")

    git('tag', '-a', tag_name, '-m', f'Release {tag_name}\n\n{release_notes}')
    print(f"  Tagged: {tag_name}")

    git('push', 'origin', GIT_BRANCH)
    git('push', 'origin', tag_name)
    print(f"  Pushed {GIT_BRANCH} and {tag_name} to origin")


def print_summary(version: str, installer_path: Path, signed: bool, deployed: bool,
                  dry_run: bool) -> None:
    step(11, "Release summary", dry_run)
    prefix = "[DRY RUN] " if dry_run else ""
    print(f"""
  {prefix}Deployment Summary
  ==================
  Version:    {version}
  Built:      dist\\{APP_SLUG}\\{APP_EXE}
  Installer:  dist\\installer\\{APP_SLUG}_Setup_{version}.exe
  Inner .exe: {'Signed' if signed else 'Unsigned'}
  Installer:  {'Signed' if signed else 'Unsigned'}
  Deploy:     {'Pushed to network share' if deployed else 'Pending'}
  Git:        {'Committed + tagged + pushed' if (signed or deployed) and not dry_run else 'Skipped'}
""")
    if not dry_run and (signed or deployed):
        print("  Release complete!")
    elif not dry_run:
        print("  Release built but NOT published. Run with signing + deploy to release.")


# -------------------- main --------------------

def main() -> int:
    parser = argparse.ArgumentParser(
        description=f'{APP_NAME} Release Pipeline',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('--bump', choices=['major', 'minor', 'patch'], required=True,
                        help='Version bump type')
    parser.add_argument('--skip-sign', action='store_true',
                        help='Skip code signing (installer will NOT be deployed)')
    parser.add_argument('--skip-deploy', action='store_true',
                        help='Build and sign but do not deploy to network share')
    parser.add_argument('--release-notes', default=None,
                        help='Release notes (auto-generated from git log if not provided)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print steps without executing')
    parser.add_argument('--yes', action='store_true',
                        help='Non-interactive — auto-yes to all prompts')
    args = parser.parse_args()

    print("=" * 60)
    print(f"  {APP_NAME} Release Pipeline")
    print("=" * 60)

    try:
        can_sign = preflight_checks(
            skip_sign=args.skip_sign, dry_run=args.dry_run, auto_yes=args.yes
        )

        if not args.dry_run:
            if not prompt_yes_no("\n  Proceed with release?", auto_yes=args.yes):
                print("\n  Release cancelled.")
                return 0

        version = do_version_bump(args.bump, dry_run=args.dry_run)
        do_smoke_test(dry_run=args.dry_run)
        do_build(dry_run=args.dry_run)

        signed_inner = False
        if can_sign and not args.skip_sign:
            signed_inner = do_sign_inner_exe(dry_run=args.dry_run)
        else:
            reason = "--skip-sign" if args.skip_sign else "no SafeNet key"
            print(f"\n  Inner .exe signing SKIPPED ({reason})")

        installer_path = do_inno_setup(version, dry_run=args.dry_run)

        signed_installer = False
        if can_sign and not args.skip_sign:
            signed_installer = do_sign_installer(installer_path, dry_run=args.dry_run)
        else:
            reason = "--skip-sign" if args.skip_sign else "no SafeNet key"
            print(f"\n  Installer signing SKIPPED ({reason})")

        signed = signed_inner and signed_installer

        release_notes = args.release_notes
        if not release_notes:
            release_notes = auto_release_notes(version)
            print(f"\n  Auto-generated release notes:\n    {release_notes[:200]}{'...' if len(release_notes) > 200 else ''}")

        json_path = do_create_version_json(version, release_notes, installer_path,
                                            dry_run=args.dry_run)

        deployed = False
        if not args.skip_deploy:
            deployed = do_deploy(installer_path, json_path, signed, dry_run=args.dry_run)
        else:
            print("\n  Deploy SKIPPED (--skip-deploy)")

        do_update_deployment_log(version, signed, deployed, release_notes, dry_run=args.dry_run)
        do_git_commit_tag_push(version, signed, deployed, release_notes, dry_run=args.dry_run)
        print_summary(version, installer_path, signed, deployed, dry_run=args.dry_run)

        return 0

    except ReleaseError as e:
        print(f"\n  RELEASE FAILED: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n  Release cancelled.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
