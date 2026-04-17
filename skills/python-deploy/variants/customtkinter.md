# Variant: customtkinter GUI apps

Apps like Thermal Inspector and inspection-master. Single-entry GUI, no server component.

## PyInstaller spec tweaks

```python
hiddenimports = [
    'customtkinter',
    'darkdetect',
    'PIL', 'PIL._tkinter_finder',

    # DB drivers (if used)
    'psycopg2', 'psycopg2.extensions', 'psycopg2.extras',

    # Image processing
    'cv2', 'numpy',

    # Matplotlib (if plotting)
    'matplotlib', 'matplotlib.backends.backend_tkagg',

    # Keyring for credential storage
    'keyring', 'keyring.backends', 'keyring.backends.Windows',

    # Your own modules (every module imported by runtime dispatch)
    # e.g.:  'app_settings', 'database_tab', 'image_processor', ...
]

# console=False — no terminal window when launched
```

## Inno Setup tweaks

Default settings (`PrivilegesRequired=admin`, `MinVersion=10.0`) are fine.

If your app needs PATH entries (e.g. for bundled binaries), add a `[Registry]` block like Thermal Inspector's DJI SDK PATH manipulation.

## In-app update check

In the main window's init, after the UI is set up:

```python
from updater import check_for_updates_on_startup

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        # ... UI setup ...
        self.after(2000, lambda: check_for_updates_on_startup(self))
```

The 2-second delay lets the UI paint before the update dialog appears.

## Common pitfalls

1. **Menu bar / custom widgets not bundled** — if you use custom `.png` / `.ico` files, add to `datas_list`.
2. **`matplotlib` backend** — include `matplotlib.backends.backend_tkagg` or plots won't render.
3. **DPI scaling** — customtkinter handles it, but add `customtkinter.set_window_scaling(1.0)` if users report blurry UI on 4K monitors.
4. **`__main__` entry vs importable** — `ENTRY_MODULE` for smoke test must be importable without side effects. If `entry_script.py` runs the GUI at module level, refactor:

   ```python
   # GOOD
   def main():
       app = MainApp()
       app.mainloop()

   if __name__ == '__main__':
       main()
   ```

## Skipping auto-update when running from source

When running `python app.py` during development, the updater would check the share and potentially prompt to install. Gate the call on whether we're bundled:

```python
import sys
if getattr(sys, 'frozen', False):  # True only under PyInstaller
    check_for_updates_on_startup(self)
```

Thermal Inspector adopted this in v1.1.13.
