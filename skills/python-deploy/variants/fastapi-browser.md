# Variant: FastAPI + browser UI apps

Apps like yellow-pine. The "app" is a local FastAPI server bound to `127.0.0.1` that serves static HTML/JS + JSON API; users interact through their browser.

## Key differences from GUI variant

1. **Two processes at runtime** — the server, and the browser (opened via `webbrowser.open`)
2. **Console window is OK** — users benefit from seeing server logs. `console=True` in the spec.
3. **Static assets are large** — `dashboard/static/` must be in `datas_list`
4. **Auto-update UX** — can't show a tkinter dialog; either push update notification into the served UI, or prompt in console

## PyInstaller spec tweaks

```python
# Entry point is the server script
a = Analysis(
    [os.path.join(PROJ_ROOT, 'dashboard', 'server.py')],
    ...
    datas=[
        # ALL static UI assets
        (os.path.join(PROJ_ROOT, 'dashboard', 'static'), 'dashboard/static'),
        # Templates if you use Jinja
        # (os.path.join(PROJ_ROOT, 'dashboard', 'templates'), 'dashboard/templates'),
    ],
    hiddenimports=[
        'fastapi', 'uvicorn', 'uvicorn.logging', 'uvicorn.lifespan',
        'uvicorn.lifespan.on', 'uvicorn.protocols',
        'uvicorn.protocols.http', 'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets', 'uvicorn.protocols.websockets.auto',
        'uvicorn.loops', 'uvicorn.loops.auto',
        'starlette', 'pydantic',
        'psycopg2', 'pynvml',
        # Your routers / deps
    ],
    ...
)

# console=True — keep terminal visible for server logs
exe = EXE(..., console=True, ...)
```

## Startup flow

In `server.py`:

```python
import webbrowser, threading, time

def open_browser():
    time.sleep(2)  # let uvicorn bind before browser hits it
    webbrowser.open('http://127.0.0.1:8000')

if __name__ == '__main__':
    threading.Thread(target=open_browser, daemon=True).start()
    uvicorn.run(app, host='127.0.0.1', port=8000)
```

The installer's `[Run]` section launches the bundled `.exe` the same as a GUI app; user sees a console window and their browser opens.

## Inno Setup tweaks

Add a firewall exception for the bound port (though binding to `127.0.0.1` means no WAN exposure and typically no firewall prompt — verify on a fresh machine):

```
[Run]
Filename: "netsh"; Parameters: "advfirewall firewall add rule name=""{#MyAppName}"" dir=in action=allow protocol=TCP localport=8000"; Flags: runhidden; StatusMsg: "Adding firewall rule..."
```

## Auto-update integration

Two options:

### Option A: Console-only prompt on startup (simplest)
Before starting uvicorn, run the update check. If an update is available, print to console and ask user to press `Y` to install:

```python
from updater import UpdateChecker

def check_for_updates_console():
    checker = UpdateChecker()
    available, version, installer_path, notes = checker.check_for_update()
    if available:
        print(f"\n  Update available: {version}")
        print(f"  Notes: {notes}\n")
        if input("  Install now? [y/N] ").strip().lower() == 'y':
            local = checker.copy_installer(installer_path)
            if local:
                checker.install_update(local)
                sys.exit(0)

if getattr(sys, 'frozen', False):
    check_for_updates_console()
```

### Option B: UI banner (better UX)
Add a `/api/updates` endpoint that calls `UpdateChecker.check_for_update()`. The HTML dashboard polls it on load and shows a banner: "Update X.Y.Z available. [Install] [Later]". `[Install]` POSTs to `/api/install-update` which stops uvicorn and launches the installer with `/SILENT /CLOSEAPPLICATIONS`.

Option B requires a UI change but gives users a native-feeling experience.

## Common pitfalls

1. **Uvicorn hidden imports** — miss one and the server crashes on startup with a cryptic ASGI error. The hiddenimports list above is the known-good set for FastAPI + uvicorn.
2. **Static files path** — use `Path(__file__).parent / 'static'` or the PyInstaller-bundled path (`sys._MEIPASS` at runtime). FastAPI's `StaticFiles(directory=...)` must resolve correctly both in dev and bundled.

   ```python
   if getattr(sys, 'frozen', False):
       STATIC_DIR = Path(sys._MEIPASS) / 'dashboard' / 'static'
   else:
       STATIC_DIR = Path(__file__).parent / 'static'
   ```
3. **Port conflict** — user already has something on 8000. Either pick an uncommon port (18000) or detect and increment.
4. **Browser opens before server is ready** — 2s sleep is usually enough; for slow machines, poll `http://127.0.0.1:<port>/health` until it returns 200.
5. **`/CLOSEAPPLICATIONS` during install** — Inno Setup uses window-class matching. A console-mode PyInstaller exe usually closes on signal; test the upgrade path explicitly.
