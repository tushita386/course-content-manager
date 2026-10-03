# Course Content Manager - Project Master Document

> This document is maintained throughout the project and is the central engineering record.

## 1. Project Overview
Course Content Manager is an individual e-learning application that manages courses and learning content. It is a college project built to demonstrate programming fundamentals, OOP, collections, SQL/DBMS, CRUD, search/filter, validation, exception handling, reports/dashboard, Git/GitHub, testing and documentation.

It is NOT a task manager. The Excel tracker is the development-management record and is separate from the application.

## 2. Problem Statement
Learners and instructors often keep course information and learning material scattered across files, folders and chats. This makes it hard to keep records current, to find specific content quickly, and to see what is still incomplete. There is no single, simple place to create, update and search courses and their learning content. Course Content Manager is a web application that lets a user manage their profile, create and maintain courses and learning content, search and filter records, and view simple reports of the current state.

Note: this is a problem framing, not the result of user research.
## 3. Objectives
1. Let a user create, view, update and delete their profile, courses and learning content.
2. Let a user search and filter courses and content.
3. Validate all input and handle errors without crashing.
4. Provide a simple dashboard and reports for the Mentor/Admin.
5. Store data in a relational database (SQLite) with a clear schema.
6. Provide a simple web UI, with frontend and backend separated.
7. Keep a traceable engineering record: Git history, tests, decision log, documentation.

## 4. Scope
- User/profile management
- Course records with CRUD
- Learning content records with CRUD
- Search and filter
- Input validation and exception handling
- Simple reports/dashboard
- Basic test cases
- README (written at the end, per the project guide)

## 5. Out of Scope
- Complex authentication or role permissions
- Payments
- Video or file hosting
- AI features
- Cloud deployment
- Mobile app
- Microservices
## 6. Users / Stakeholders

| Stakeholder | Role | Needs from the app |
|---|---|---|
| User | Primary user. Creates and manages their own profile, courses and learning content. | Create and update records, search and filter, keep information current. |
| Mentor/Admin | Reviews activity. | Simple reports and a dashboard showing activity and pending work. |
| Project guide / evaluator | Not an app user. Assesses the project. | A working demo, clear documentation, a traceable Git history. |

The User and Mentor/Admin roles come from the college's suggested user stories. The project guide / evaluator is a project stakeholder, not an application user. This analysis is not based on interviews or surveys.
## 7. Design Thinking

### 7.1 Empathize
**Method:** Self-observation by the developer, who is also a learner and the first user. No survey or interviews were conducted.

**Observations (in the developer's own words):**
- I usually keep my course notes and study material in different places, such as folders on my laptop, PDFs, and online documents.
- Important links for assignments, resources, and course material are often saved separately, so I have to search through different places when I need something.
- Sometimes it takes time to find a particular note, assignment, or learning resource because the material is not organized in one place.
- I may also have difficulty keeping track of which course content has been completed and what still needs to be done.
- I would find it useful to have one simple place where my courses and related learning content could be organized, updated, and searched.
### 7.2 Define
**Pain points (from the Empathize observations):**
1. Notes and material are spread across laptop folders, PDFs and online documents.
2. Assignment and resource links are saved separately from the material.
3. Finding one specific note, assignment or resource takes time.
4. It is hard to track which content is completed and what is still pending.

**Point-of-view statement:**
> A learner who keeps course notes, links and resources in many separate places needs one simple place to organize, update and search their courses and learning content, because looking through scattered locations wastes time and makes it hard to see what is still incomplete.

**How Might We questions:**
1. How might we keep courses and their learning content in one place?
2. How might we let a learner find any item quickly?
3. How might we show which content is completed and which is pending?

**Boundary note:** HMW 3 concerns learning progress on content (for example not started / in progress / completed). It does not mean due dates, priorities or Kanban, which belong to the development tracker. Whether the app has a completion-status field is decided in the Functional Requirements task.
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


### DL-05 - User and stakeholder analysis (Tracker T-05)
- **Date:** 2026-10-03
- **Work performed:** Added the stakeholder table as section 6.
- **Result:** Committed and pushed.
- **Evidence:** `git log --oneline --all` output.
- **Branch / Commit:** `feature/project-architecture` 633406b (docs: add user and stakeholder analysis)


### DL-06 - Project objectives and scope (Tracker T-06)
- **Date:** 2026-10-03
- **Work performed:** Added objectives, scope and out-of-scope as sections 3-5.
- **Result:** Committed and pushed.
- **Evidence:** `git log --oneline --all` output.
- **Branch / Commit:** `feature/project-architecture` 9c6f811 (docs: add project objectives, scope and out-of-scope)


### DL-07 - Design Thinking: Empathize stage (Tracker T-07, stage 1 of 5)
- **Date:** 2026-10-03
- **Work performed:** Recorded the developer's self-observation as section 7.1. No survey or interviews were conducted.
- **Result:** Committed and pushed.
- **Evidence:** `git log --oneline --all` output.
- **Branch / Commit:** `feature/project-architecture` 11020cc (docs: add design thinking empathize stage)
