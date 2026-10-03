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

## D-03 - Technology stack
- **Date:** 2026-10-03
- **Decision:** Use Python + Flask + SQLite + HTML/CSS.
- **Options considered:** The college allows Option A (Python + PostgreSQL/SQLite + simple web UI) or Option B (Java + PostgreSQL + simple web UI).
- **Selected approach:** Python with Flask for the backend, SQLite for the database, HTML/CSS for the frontend.
- **Reason:** It is allowed by the college, simple, and easy to explain in a viva.
- **Consequences:** The database is a single file with no server to install. `*.db` is in `.gitignore`, so the schema is kept in `backend/database/schema.sql`.

## D-04 - Functional requirement decisions
- **Date:** 2026-10-03
- **Decision:** Four decisions that shape the functional requirements.
  1. Search (FR-12) covers both course titles and content titles.
  2. After saving a new course, the user lands on that course's detail page.
  3. "Pending" means status Not started or In progress.
  4. The app has a single profile and no login. The Mentor/Admin sees the same dashboard.
- **Options considered:** Not recorded. The proposals were accepted as written.
- **Reason:** (1) resolves the open question from the prototype test in 7.5; (2) resolves test finding 1; (3) defines the dashboard counts; (4) follows the out-of-scope list, which excludes complex authentication.
- **Consequences:** The dashboard and search must apply these rules. There is no user table for login, so profile data is a single record.

## D-05 - Server-rendered pages
- **Date:** 2026-10-03
- **Decision:** Flask renders HTML templates directly. There is no separate JSON API and no JavaScript frontend that calls it.
- **Options considered:** (a) server-rendered Flask pages; (b) a separate REST API plus a JavaScript frontend.
- **Selected approach:** (a). Routes use standard HTTP methods (GET, POST).
- **Reason:** Simpler, fits the college's "simple web UI" requirement, and is easier to build and defend within the deadline.
- **Consequences:** Frontend/backend separation is by folders and responsibilities inside one Flask app, not two servers. Flask must load templates and static files from `frontend/`.
