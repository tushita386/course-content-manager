# Decision Log

## D-01 - Frontend/backend separation
- **Date:** 2026-10-03
- **Decision:** Keep frontend and backend in separate top-level folders.
- **Options considered:** Not recorded. The project guide required frontend/backend separation, and the structure was proposed and approved on this date.
- **Selected approach:** `backend/` holds the Flask app, routes, models and database code. `frontend/` holds the HTML templates and static files (CSS/JS).
- **Reason:** Clear separation of concerns, and easy to explain in a viva.
- **Consequences:** Flask must be configured to load templates and static files from `frontend/`. This is handled in the development environment setup task.

## D-02 - Git branching strategy
- **Date:** 2026-10-03
- **Decision:** Development happens on feature branches. Nothing is merged into `main` until final integration.
- **Options considered:** Not recorded. This is the project guide's rule.
- **Selected approach:** `main` holds only an initial `.gitignore` commit. All work lives on `feature/*` branches, which are committed and pushed.
- **Reason:** `main` represents the final integrated version.
- **Consequences:** Git cannot branch from a repository with no commits, so one initial commit on `main` was required (8b55163).
