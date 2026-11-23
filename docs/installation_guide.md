# Installation Guide (Windows PowerShell)

## What you need
- Windows 10 or 11
- Python 3.9 or newer (check with `python --version`; install from https://www.python.org if needed and tick "Add python.exe to PATH")
- Git (only if you are downloading the project from GitHub)

## 1. Get the project
If you already have the project folder, open PowerShell in it. Otherwise:
```powershell
git clone https://github.com/tushita386/course-content-manager.git
cd course-content-manager
```

## 2. Create and activate a virtual environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```
`(venv)` appears at the start of the prompt when it is active.

If PowerShell says that running scripts is disabled, run this once for the current window and activate again:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

## 3. Install the requirements
```powershell
pip install -r backend/requirements.txt
```

## 4. Start the application
```powershell
python -m flask --app backend.app run
```
Open http://127.0.0.1:5000 in your browser. Stop the server with Ctrl+C.
The database file is created automatically the first time the app is used.

To use another port (for example if 5000 is busy):
```powershell
python -m flask --app backend.app run --port 5001
```

## 5. Run the tests
```powershell
python tests/run_tests.py
```
The tests use temporary databases, so your own data is not touched. Results are saved to `docs/test_results.txt`.

## Troubleshooting
| Problem | What to do |
|---|---|
| `python` is not recognised | Reinstall Python and tick "Add python.exe to PATH", or try `py` instead of `python` |
| `No module named flask` | The virtual environment is not active. Run `.\venv\Scripts\Activate.ps1`, then step 3 again |
| `No module named backend` | Run the commands from the project's main folder (the one that contains `backend` and `frontend`) |
| Port already in use | Use `--port 5001` as shown above |
| I want an empty database | Stop the server and delete `backend/database/course_content.db`. It is created again on the next start |
