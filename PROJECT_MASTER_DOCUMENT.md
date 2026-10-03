# Course Content Manager - Project Master Document

> This document is maintained throughout the project and is the central engineering record.

## 1. Project Overview
Course Content Manager is an individual e-learning application that manages courses and learning content. It is a college project built to demonstrate programming fundamentals, OOP, collections, SQL/DBMS, CRUD, search/filter, validation, exception handling, reports/dashboard, Git/GitHub, testing and documentation.

It is NOT a task manager. The Excel tracker is the development-management record and is separate from the application.

## 2. Problem Statement
Learners and instructors often keep course information and learning material scattered across files, folders and chats. This makes it hard to keep records current, to find specific content quickly, and to see what is still incomplete. There is no single, simple place to create, update and search courses and their learning content. Course Content Manager is a web application that lets a user manage their profile, create and maintain courses and learning content, search and filter records, and view simple reports of the current state.

Note: this is a problem framing, not the result of user research.
## 6. Users / Stakeholders

| Stakeholder | Role | Needs from the app |
|---|---|---|
| User | Primary user. Creates and manages their own profile, courses and learning content. | Create and update records, search and filter, keep information current. |
| Mentor/Admin | Reviews activity. | Simple reports and a dashboard showing activity and pending work. |
| Project guide / evaluator | Not an app user. Assesses the project. | A working demo, clear documentation, a traceable Git history. |

The User and Mentor/Admin roles come from the college's suggested user stories. The project guide / evaluator is a project stakeholder, not an application user. This analysis is not based on interviews or surveys.
## 17. Folder Structure
```text
course-content-manager/
+-- backend/        (app.py, routes/, models/, database/, requirements.txt)
+-- frontend/       (templates/, static/)
+-- tests/
+-- docs/           (decisions.md)
+-- PROJECT_MASTER_DOCUMENT.md
+-- .gitignore
```
See D-01 in `docs/decisions.md`.

## 20. Development Log

### DL-01 - GitHub repository setup (Tracker T-01)
- **Date:** 2026-10-03
- **Work performed:** Created the public repo and cloned it locally. Git identity was already configured.
- **Result:** The clone reported an empty repository. `git status` showed `main` with no commits.
- **Evidence:** Terminal output from clone and `git status`.
- **Branch / Commit:** none

### DL-02 - Initial project structure (Tracker T-02)
- **Date:** 2026-10-03
- **Work performed:** Added `.gitignore` on `main`. Created the frontend/backend/tests/docs structure on `feature/project-architecture`. `.gitkeep` files are placeholders so Git tracks empty folders.
- **Result:** Both branches pushed. `main` was not merged into.
- **Evidence:** `tree /F` and `git log --oneline --all` output.
- **Branch / Commit:** `main` 8b55163 (chore: add .gitignore); `feature/project-architecture` 27e4f62 (feat: add frontend/backend project structure)


### DL-03 - Documentation setup (Tracker T-03)
- **Date:** 2026-10-03
- **Work performed:** Added the decision log (D-01, D-02) and the master document skeleton.
- **Result:** Both files committed and pushed.
- **Evidence:** `git log --oneline --all` output.
- **Branch / Commit:** `feature/project-architecture` fcd1e5b (docs: add decision log and master project document)


### DL-04 - Problem statement and technology decision (Tracker T-04)
- **Date:** 2026-10-03
- **Work performed:** Wrote the problem statement as section 2. Recorded D-03 (Python + Flask + SQLite + HTML/CSS) in the decision log.
- **Result:** Committed and pushed.
- **Evidence:** `git log --oneline --all` output.
- **Branch / Commit:** `feature/project-architecture` 438858b (docs: add problem statement and record technology decision)
