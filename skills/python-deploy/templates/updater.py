"""
Auto-update client for {{APP_NAME}}.
Checks the network share for a newer version; copies + SHA-256 verifies the installer;
launches it with /SILENT /CLOSEAPPLICATIONS and exits the app.

Safe to call from any thread — UI integration uses `after(...)` to marshal to the main thread.
"""

import hashlib
import json
import logging
import os
import shutil
import subprocess
import sys
import tempfile
import threading
import zipfile
from typing import Callable, Optional, Tuple

from version import UPDATE_PATH, VERSION, compare_versions

logger = logging.getLogger(__name__)


def _sha256_of_file(path: str, block_size: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            h.update(chunk)
    return h.hexdigest()


class UpdateChecker:
    """Headless update client — no UI dependencies."""

    def __init__(self):
        self.update_path = UPDATE_PATH
        self.current_version = VERSION
        self.version_file = os.path.join(self.update_path, 'version.json')
        self._temp_dirs: list[str] = []  # track for cleanup

    def check_for_update(self) -> Tuple[bool, Optional[str], Optional[str], Optional[str], Optional[str]]:
        """
        Returns (update_available, latest_version, installer_path, release_notes, expected_sha256).
        All-None tuple on any error or when share isn't accessible.
        """
        try:
            if not os.path.exists(self.update_path):
                logger.debug(f"Update path not accessible: {self.update_path}")
                return (False, None, None, None, None)
            if not os.path.exists(self.version_file):
                logger.debug(f"Version file not found: {self.version_file}")
                return (False, None, None, None, None)

            with open(self.version_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            latest = data.get('version', '')
            installer_name = data.get('installer', '')
            notes = data.get('release_notes', '')
            sha256 = data.get('sha256')  # optional — older version.json files won't have it

            if not latest or not installer_name:
                logger.warning("Invalid version.json — missing version or installer")
                return (False, None, None, None, None)

            if compare_versions(latest, self.current_version) > 0:
                installer_path = os.path.join(self.update_path, installer_name)
                if not os.path.exists(installer_path):
                    logger.warning(f"Installer not found: {installer_path}")
                    return (False, latest, None, notes, None)
                return (True, latest, installer_path, notes, sha256)

            return (False, latest, None, None, None)

        except json.JSONDecodeError as e:
            logger.error(f"Invalid version.json: {e}")
            return (False, None, None, None, None)
        except Exception as e:
            logger.error(f"Error checking for updates: {e}")
            return (False, None, None, None, None)

    def copy_installer(self,
                       installer_path: str,
                       expected_sha256: Optional[str] = None,
                       progress_callback: Optional[Callable[[int, int, str], None]] = None
                       ) -> Optional[str]:
        """
        Copy installer from network share to local temp dir. SHA-256 verifies if expected_sha256 given.
        Handles both .exe (direct) and .zip (extract) formats.

        Returns path to the local .exe on success, None on failure.
        On failure, the tempdir is cleaned up.
        """
        temp_dir = None
        try:
            if not os.path.exists(installer_path):
                logger.error(f"Update package not found: {installer_path}")
                return None

            total_size = os.path.getsize(installer_path)
            temp_dir = tempfile.mkdtemp(prefix='{{APP_SLUG}}_Update_')
            self._temp_dirs.append(temp_dir)

            filename = os.path.basename(installer_path)
            local_path = os.path.join(temp_dir, filename)

            if progress_callback:
                progress_callback(0, total_size, "Copying installer...")

            copied = 0
            block_size = 1 << 20
            with open(installer_path, 'rb') as src, open(local_path, 'wb') as dst:
                while True:
                    chunk = src.read(block_size)
                    if not chunk:
                        break
                    dst.write(chunk)
                    copied += len(chunk)
                    if progress_callback:
                        progress_callback(copied, total_size, "Copying installer...")

            logger.info(f"Copied to: {local_path}")

            # Extract if zip (legacy format — current pipeline ships .exe directly)
            if filename.lower().endswith('.zip'):
                if progress_callback:
                    progress_callback(total_size, total_size, "Extracting installer...")
                try:
                    with zipfile.ZipFile(local_path, 'r') as zf:
                        exe_files = [f for f in zf.namelist() if f.lower().endswith('.exe')]
                        if not exe_files:
                            logger.error("No .exe file found in update package")
                            self._cleanup_tempdir(temp_dir)
                            return None
                        exe_name = exe_files[0]
                        zf.extract(exe_name, temp_dir)
                    os.remove(local_path)  # delete zip AFTER closing it (Windows file lock)
                    local_path = os.path.join(temp_dir, exe_name)
                except zipfile.BadZipFile:
                    logger.error(f"Invalid zip file: {installer_path}")
                    self._cleanup_tempdir(temp_dir)
                    return None

            # Integrity check
            if expected_sha256:
                if progress_callback:
                    progress_callback(total_size, total_size, "Verifying installer...")
                actual = _sha256_of_file(local_path)
                if actual.lower() != expected_sha256.lower():
                    logger.error(f"SHA-256 mismatch! Expected {expected_sha256}, got {actual}")
                    self._cleanup_tempdir(temp_dir)
                    return None
                logger.info("SHA-256 verified.")
            else:
                logger.warning("No SHA-256 provided — skipping integrity check.")

            logger.info(f"Installer ready: {local_path}")
            return local_path

        except Exception as e:
            logger.error(f"Error preparing update: {e}")
            if temp_dir:
                self._cleanup_tempdir(temp_dir)
            return None

    # Backwards-compat alias
    copy_and_extract = copy_installer

    def _cleanup_tempdir(self, temp_dir: str):
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
            if temp_dir in self._temp_dirs:
                self._temp_dirs.remove(temp_dir)
            logger.debug(f"Cleaned up tempdir: {temp_dir}")
        except Exception as e:
            logger.warning(f"Failed to clean tempdir {temp_dir}: {e}")

    def install_update(self, installer_path: str) -> bool:
        """Launch installer with /SILENT /CLOSEAPPLICATIONS. Caller should exit after this returns True."""
        try:
            if not os.path.exists(installer_path):
                logger.error(f"Installer not found: {installer_path}")
                return False
            subprocess.Popen([installer_path, '/SILENT', '/CLOSEAPPLICATIONS'],
                             creationflags=subprocess.DETACHED_PROCESS)
            logger.info("Installer launched, exiting application")
            return True
        except Exception as e:
            logger.error(f"Error launching installer: {e}")
            return False


class UpdateCheckerUI:
    """customtkinter integration. For FastAPI apps see variants/fastapi-browser.md."""

    def __init__(self, parent_window):
        self.parent = parent_window
        self.checker = UpdateChecker()
        self._check_thread: Optional[threading.Thread] = None

    def check_for_updates_async(self, show_no_update_message: bool = False):
        def _check():
            available, version, path, notes, sha256 = self.checker.check_for_update()
            self.parent.after(0, lambda: self._show_update_result(
                available, version, path, notes, sha256, show_no_update_message
            ))
        self._check_thread = threading.Thread(target=_check, daemon=True)
        self._check_thread.start()

    def _show_update_result(self, available, version, installer_path, notes, sha256, show_no_update):
        try:
            from tkinter import messagebox

            if available and installer_path:
                message = f"A new version ({version}) is available!\n\n"
                if notes:
                    truncated = notes[:500] + "..." if len(notes) > 500 else notes
                    message += f"What's new:\n{truncated}\n\n"
                message += "Would you like to install the update now?"

                if messagebox.askyesno("Update Available", message, parent=self.parent):
                    self._copy_and_install(installer_path, sha256)

            elif show_no_update:
                messagebox.showinfo(
                    "No Updates",
                    f"You are running the latest version ({VERSION}).",
                    parent=self.parent
                )
        except Exception as e:
            logger.error(f"Error showing update dialog: {e}")

    def _copy_and_install(self, installer_path: str, expected_sha256: Optional[str]):
        try:
            import customtkinter as ctk

            progress_window = ctk.CTkToplevel(self.parent)
            progress_window.title("Preparing Update")
            progress_window.geometry("420x160")
            progress_window.transient(self.parent)
            progress_window.grab_set()
            progress_window.resizable(False, False)

            # Center on parent
            progress_window.update_idletasks()
            px = self.parent.winfo_x() + (self.parent.winfo_width() - 420) // 2
            py = self.parent.winfo_y() + (self.parent.winfo_height() - 160) // 2
            progress_window.geometry(f"+{px}+{py}")

            label = ctk.CTkLabel(progress_window, text="Preparing update...")
            label.pack(pady=15)
            bar = ctk.CTkProgressBar(progress_window, width=360)
            bar.pack(pady=8)
            bar.set(0)
            status = ctk.CTkLabel(progress_window, text="0%")
            status.pack(pady=8)

            def on_progress(current, total, text):
                if total > 0:
                    pct = current / total
                    self.parent.after(0, lambda: self._update_progress_ui(
                        label, bar, status, pct, current, total, text
                    ))

            def worker():
                local_path = self.checker.copy_installer(installer_path, expected_sha256, on_progress)
                self.parent.after(0, lambda: self._finish(progress_window, local_path))

            threading.Thread(target=worker, daemon=True).start()

        except Exception as e:
            logger.error(f"Error starting update: {e}")

    def _update_progress_ui(self, label, bar, status, pct, current, total, text):
        try:
            label.configure(text=text)
            bar.set(pct)
            mb_c = current / (1 << 20)
            mb_t = total / (1 << 20)
            status.configure(text=f"{pct*100:.0f}% ({mb_c:.1f} / {mb_t:.1f} MB)")
        except Exception:
            pass

    def _finish(self, progress_window, installer_path: Optional[str]):
        try:
            progress_window.destroy()
            from tkinter import messagebox

            if installer_path:
                if messagebox.askyesno(
                    "Install Update",
                    "Ready to install. The application will close.\n\nInstall now?",
                    parent=self.parent
                ):
                    if self.checker.install_update(installer_path):
                        self.parent.quit()
                        sys.exit(0)
            else:
                messagebox.showerror(
                    "Update Failed",
                    "Failed to prepare the update. Please try again or install manually.",
                    parent=self.parent
                )
        except Exception as e:
            logger.error(f"Error finishing update: {e}")


def check_for_updates_on_startup(parent_window):
    """
    Call once from your app's main window after UI is ready.
    Skips the check when running from source (not bundled) — easier dev workflow.
    """
    if not getattr(sys, 'frozen', False):
        logger.debug("Running from source — skipping update check")
        return None
    ui = UpdateCheckerUI(parent_window)
    ui.check_for_updates_async(show_no_update_message=False)
    return ui
