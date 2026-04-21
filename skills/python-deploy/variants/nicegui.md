# Variant: NiceGUI + PyWebView native window

Apps like NEC Inspection App. NiceGUI serves a web UI over a local
uvicorn server; PyWebView wraps it in a native Windows window so the user
sees a desktop app, not a browser.

This variant fought every failure mode we knew about and a few new ones.
Every item below was a real bug we shipped and chased. Apply them as a
set — they combine.

## PyInstaller spec tweaks

```python
hiddenimports = [
    'nicegui',
    'webview', 'webview.dom', 'webview.window',
    'webview.platforms.winforms',
    'clr_loader', 'pythonnet',
    'uvicorn', 'uvicorn.logging', 'uvicorn.lifespan',
    'uvicorn.lifespan.on', 'uvicorn.protocols',
    'uvicorn.protocols.http', 'uvicorn.protocols.http.auto',
    'uvicorn.protocols.websockets', 'uvicorn.protocols.websockets.auto',
    'uvicorn.loops', 'uvicorn.loops.auto',
    'starlette', 'fastapi', 'pydantic',

    # DB drivers etc.
    'psycopg2', 'psycopg2.extensions', 'psycopg2.extras',
    'keyring', 'keyring.backends', 'keyring.backends.Windows',
]

# console=False — windowed. This choice is what triggers every pitfall
# in this file. See "PyInstaller windowed-mode hardening" below.
```

## Python version

Native window requires **Python 3.12 + pythonnet 3.0.5**. Python 3.11
hits a race in `webview/dom/element.py::__generate_events` —
`TypeError: 'NoneType' object is not iterable` — during DOM bind, and the
window stays blank. Python 3.13+ hits other pythonnet ABI breakage.

On a managed machine where the MSI installer is blocked by group policy
(exit code 1625), install Python 3.12 user-scope with
[uv](https://github.com/astral-sh/uv). If AV blocks uv's trampoline
`.exe` writes during `uv pip install`, fall back to stdlib pip:
`venv/Scripts/python.exe -m ensurepip --upgrade`, then use the venv's pip.

## The big one: `ui.run(native=True)` silently fails in a windowed build

NiceGUI's native mode launches PyWebView in a **multiprocessing
subprocess** (see `nicegui/native/native_mode.py::_open_window`). In a
PyInstaller windowed bundle the subprocess spawn silently fails —
`webview.start()` in the child never creates a window, no exception
reaches the parent, and `ui.run()` returns as if the user had closed the
window. NiceGUI gracefully shuts uvicorn down. Exit code 0. No crash
dump. No Event Viewer entry.

**Drive PyWebView from the main thread yourself:**

```python
import threading, time, socket, webview
from nicegui import ui

def _run_server():
    try:
        ui.run(
            host="127.0.0.1",
            port=8080,
            reload=False,
            show=False,
            native=False,
        )
    except BaseException:
        logger.exception("ui.run (server thread) raised")

server_thread = threading.Thread(target=_run_server, daemon=True,
                                  name="nicegui-server")
server_thread.start()

# Wait for uvicorn to actually bind before pointing PyWebView at the URL.
deadline = time.time() + 30
while time.time() < deadline:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("127.0.0.1", 8080)) == 0:
            break
    time.sleep(0.1)

webview.create_window(
    title="Your App",
    url="http://127.0.0.1:8080",
    width=1400, height=900,
)
webview.start()
# webview.start() blocks until the user closes the window. The server
# thread is a daemon so it dies with the process.
```

Main-thread PyWebView is the supported path on Windows and avoids the
fragile multiprocessing-spawn-from-a-bundled-exe pattern.

## 3-second page-handler budget

NiceGUI's client uses a 3s handshake timeout. Any `@ui.page("/")` handler
that awaits longer than that — even through `await run.io_bound(...)` —
causes the client to be torn down. Downstream `run.io_bound` calls then
return `None`, `ui` element creation warns
`"Client has been deleted but is still being used"`, and you get cryptic
`TypeError: cannot unpack non-iterable NoneType object` tracebacks from
PyWebView's `bind_drop` as the DOM half-initializes.

Concretely: a remote-DB `DatabaseManager().__init__()` can spend ~6s in
the connection-pool / schema init on first use. Call that from a page
handler and you'll blow the budget on every initial load.

Three patterns that work:

1. **Prime heavy singletons in `_bootstrap()` before `ui.run()`** — pay
   the one-time cost pre-UI where there's no client to time out.
2. **Defer panel data loads** with `ui.timer(0.1, once=True, callback=...)`
   inside each panel — render empty widgets first, populate after the
   HTML is sent.
3. **Never await DB/network inline in the page handler**. If you need
   per-request DB state, ensure the singleton is already hot so the call
   is <100ms.

## Credential dialog + page-handler closure pitfall

Common pattern: `@ui.page("/")` captures `db_error` from `_bootstrap()`
in its closure and routes to a credential dialog if set. The dialog
writes `.env`, calls `ui.navigate.to("/")` to reload. The page handler
runs again — **but the closure still holds the old `db_error`**. The
dialog reopens with the same "Could not connect" message. Looks stuck.

Fix:
- Page handler calls the DB check fresh on every request, not the
  closure.
- Dialog primes the app's DB pool (`DatabaseManager().health_check()`)
  **before** navigating, so the next page handler's check hits a primed
  pool and completes inside the 3s budget.

## PyInstaller windowed-mode hardening

Windowed builds (`console=False`) have no console attached. That breaks
things in ways that produce total silence on crash. Apply all of these
early in the entry script, guarded by `sys.frozen`:

```python
import sys, os, faulthandler
from pathlib import Path

# sys.stdout / sys.stderr are None in a windowed build. Guard before
# anyone calls .reconfigure() / .write() on them.
if sys.platform == "win32":
    if sys.stdout is not None:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if sys.stderr is not None:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

if getattr(sys, "frozen", False):
    try:
        from utils.config import get_user_data_root  # %LOCALAPPDATA%\AppName
        _data_root = get_user_data_root()

        # Redirect sys.stdout/stderr to a log file so Python-level output
        # isn't lost.
        _diag_dir = _data_root / "data" / "logs"
        _diag_dir.mkdir(parents=True, exist_ok=True)
        _diag_log = open(_diag_dir / "app.stderr.log", "a",
                         encoding="utf-8", buffering=1)
        _diag_log.write(f"\n--- startup {__import__('datetime').datetime.now().isoformat()} ---\n")
        sys.stdout = _diag_log
        sys.stderr = _diag_log

        # OS-level fd 1 and 2 don't exist in a windowed build. Native
        # libs (pythonnet, pywebview, uvicorn C extensions) that call
        # fprintf(stderr) or WriteFile(GetStdHandle) directly crash
        # silently. Point both fds at the log too.
        try:
            os.dup2(_diag_log.fileno(), 1)
            os.dup2(_diag_log.fileno(), 2)
        except (OSError, AttributeError):
            pass

        # Installed cwd is Program Files (x86), read-only for non-admin.
        # Libs writing relative to cwd (WebView2 user-data dir, tempfile
        # fallbacks, etc.) silently fail there.
        try:
            os.chdir(str(_data_root))
        except OSError:
            pass

        # Native crashes (SIGSEGV / access violation) dump a Python-level
        # stack to the diag log instead of vanishing. Must run AFTER
        # stderr is pointed at the log.
        try:
            faulthandler.enable(_diag_log)
        except (OSError, RuntimeError):
            pass

        # PyWebView's DEBUG logger is the only place its internal errors
        # surface. Route it (and nicegui, clr_loader) into the diag log
        # so the next silent failure leaves a trace.
        import logging as _diag_logging
        _handler = _diag_logging.StreamHandler(_diag_log)
        _handler.setFormatter(_diag_logging.Formatter(
            "%(asctime)s %(name)s %(levelname)s %(message)s"
        ))
        for name in ("pywebview", "webview", "nicegui", "clr_loader"):
            lg = _diag_logging.getLogger(name)
            lg.setLevel(_diag_logging.INFO)
            lg.addHandler(_handler)
            lg.propagate = False
    except Exception:
        pass  # never crash startup because diagnostic setup failed
```

`get_user_data_root()` pattern (put this in `utils/config.py` or similar):

```python
def get_user_data_root() -> Path:
    if getattr(sys, "frozen", False):
        root = Path(os.environ["LOCALAPPDATA"]) / APP_NAME
        root.mkdir(parents=True, exist_ok=True)
        return root
    return Path(__file__).resolve().parent.parent.parent  # project root
```

Write **everything user-generated** (logs, `.env`, caches, DBs) under
that root. Writing to the install dir will work in dev and fail on every
non-admin install.

## Diagnosing a silent-exit frozen build

If the app is still vanishing after all of the above, don't guess:

1. Clear `%LOCALAPPDATA%\AppName\data\logs\app.stderr.log` and relaunch.
2. Wrap your `ui.run` / `webview.start` in `try/except BaseException`
   and log both branches. If you see "ui.run returned normally" a few
   hundred ms after start, you're in nicegui's native-subprocess silent
   fail (see the main-thread PyWebView fix above).
3. Test PyWebView standalone against the bundled interpreter:

   ```python
   import webview
   webview.create_window("test", html="<h1>ok</h1>")
   webview.start(debug=True)
   ```

   If the window opens, the bundle is fine — the issue is your
   framework's multiprocessing/subprocess approach.
4. Check `Get-WinEvent -LogName Application` for a `1000` Application
   Error. Absence of an entry means the process exited cleanly — look
   for silent early returns, not crashes.

## Common pitfalls

1. **DB credentials in the install dir** — `.env` next to the exe is
   read-only for non-admin. Read from `get_user_data_root() / ".env"`.
2. **Keeping `native=True` because it worked in dev** — it worked in
   dev, not in the bundle. Use the main-thread PyWebView pattern.
3. **Long-running awaits in the page handler** — see the 3s budget
   section. Always defer.
4. **Trusting that `ui.run()` blocks** — it only blocks when the server
   is running happily. A silent early return looks identical to "the
   window was closed." Always log before AND after.
