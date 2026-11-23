# Course Content Manager

An individual e-learning web application for organizing courses and their learning content
(notes, links, PDF references and assignment resources), with search, filters and a progress dashboard.

> This is **not** a task manager. "Status" here means how far a learner is with a piece of learning content
> (Not started, In progress, Completed). The Excel project tracker and the Git history are separate project records.

Built for a college project (PRJ-B058) that practises programming fundamentals, OOP, SQL/DBMS, CRUD, search/filter,
validation, exception handling, Git/GitHub, testing and documentation.

## Features
- One profile (name and email), no login
- Courses: add, view, edit, delete
- Learning content under each course: add, edit, delete, with type and status
- Keyword search across course titles and content titles (not case-sensitive)
- Filter a course's content by type and status
- Dashboard with totals and per-course progress
- Input validation with clear messages, and friendly 404 and 500 pages

## Technology
Python 3, Flask, SQLite, HTML/CSS (server-rendered Jinja pages). See `docs/decisions.md` for the reasons.

## Quick start (Windows PowerShell)
```powershell
git clone https://github.com/tushita386/course-content-manager.git
cd course-content-manager
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
python -m flask --app backend.app run
```
Open http://127.0.0.1:5000 in a browser. The database file is created automatically on first use.
Full instructions and troubleshooting: `docs/installation_guide.md`.

## Run the tests
```powershell
python tests/run_tests.py
```
Results are saved to `docs/test_results.txt`. The tests use temporary databases and never touch your real data.

## Project structure
```text
backend/        Flask app (app.py), validation, models and database code
frontend/       HTML templates and CSS
tests/          Automated tests and the test runner
docs/           Decision log, testing, user manual, installation guide, test results
PROJECT_MASTER_DOCUMENT.md   The complete engineering record of the project
```

## Documentation
| File | Contents |
|---|---|
| `PROJECT_MASTER_DOCUMENT.md` | Requirements, design, architecture, development log, bug log, testing log, requirements traceability, demo notes, viva preparation |
| `docs/decisions.md` | The decision log |
| `docs/testing.md` | Test approach and coverage |
| `docs/test_results.txt` | Output of the latest test run |
| `docs/user_manual.md` | How to use the application |
| `docs/installation_guide.md` | How to install and run it on Windows |

## Limitations
One profile and no login, search covers titles only, content types are a fixed list, and the app runs on
Flask's development server with a local SQLite file. See section 31 of the master document.


## Authentication and roles

The application has two roles:
- **Teacher:** can create student accounts and create, edit and delete courses and learning content.
- **Student:** can view courses and learning content and use search/filter. Students cannot modify records.

There is no public registration. Create the first teacher account from the project root:

```powershell
$env:FLASK_SECRET_KEY = "replace-with-a-long-random-secret"
flask --app backend.app create-teacher
flask --app backend.app run
```

The command prompts for a teacher username and password. The password is stored as a one-way hash. After logging in, the teacher can open **Students** and create student accounts. Share student credentials privately.

For a persistent local secret, set `FLASK_SECRET_KEY` in your environment before starting Flask. Do not use the development fallback in a deployed environment.
