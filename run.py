import os
from app import create_app

app = create_app()

if __name__ == '__main__':
    # Debug mode is now controlled by an environment variable rather than
    # hardcoded to True. Flask's debug mode auto-reloads on save and shows
    # detailed tracebacks in the browser — great while developing, but it
    # leaks source code and file paths, so it should never be on for a demo
    # or anything resembling a "real" run.
    #
    # Default: OFF (safe). To develop with auto-reload, run instead:
    #   Windows (PowerShell): $env:FLASK_DEBUG="1"; python run.py
    #   Mac/Linux:             FLASK_DEBUG=1 python run.py
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    app.run(debug=debug_mode)
