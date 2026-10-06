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

## D-06 - Database design decisions
- **Date:** 2026-10-03
- **Decision:** Three decisions about the data model.
  1. Courses are not linked to the profile.
  2. Content types are fixed to four values: Note, Link, PDF reference, Assignment resource.
  3. `created_at` is stored on courses and content items.
- **Options considered:** Not recorded. The proposals were accepted as written.
- **Reason:** (1) With one profile and no login (D-04), a link would add nothing. (2) Matches the content types chosen in Ideate and keeps validation simple. (3) Lets reports show recent activity.
- **Consequences:** Adding a new content type later needs a schema change. Profile is a single record.

## D-07 - UI and route conventions
- **Date:** 2026-10-03
- **Decision:** Three conventions.
  1. Forms use GET and POST only. Every state-changing action is a POST, and deletes are never GET.
  2. The search results page is grouped into Courses and Content.
  3. A failed validation saves nothing and re-shows the form with the user's input kept and a clear message.
- **Options considered:** Not recorded. The proposals were accepted as written.
- **Reason:** Browser forms only send GET and POST, so this keeps the implementation simple. Grouped results and kept input make the app easier to use.
- **Consequences:** Routes follow section 18. The length limits in section 18.1 are working values and can be revisited.

## D-08 - Branch for the development environment
- **Date:** 2026-10-03
- **Decision:** Development environment work is done on its own branch, `feature/dev-environment`, created from `feature/project-architecture`.
- **Options considered:** (a) keep working on `feature/project-architecture`; (b) branch from `main`; (c) a new branch from `feature/project-architecture`.
- **Selected approach:** (c).
- **Reason:** The `backend/` folders, the schema and the documentation exist only on `feature/project-architecture`, so a branch from `main` would not contain them. A separate branch keeps code work apart from the design documents.
- **Consequences:** Branches depend on each other. At final integration, they are merged into `main` in the order they were created. Nothing is merged before then (D-02).

## D-09 - Content status filter values
- **Date:** 2026-10-06
- **Decision:** The status filter on a course's content accepts only the three statuses (Not started, In progress, Completed) or All. There is no separate Pending filter value.
- **Options considered:** (a) the three statuses only; (b) add a fourth value, Pending, meaning Not started and In progress together.
- **Selected approach:** (a).
- **Reason:** Keeps the filter matching the sketched dropdown and the stored values. Pending is still defined in D-04 and is used for the dashboard counts.
- **Consequences:** To see everything pending, the user filters by Not started and by In progress separately. This can be revisited if it proves awkward.
