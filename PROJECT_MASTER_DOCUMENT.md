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
### 7.3 Ideate
Feature ideas generated from the How Might We questions. All eight were kept by the developer.

| # | Idea | Answers | College requirement |
|---|---|---|---|
| 1 | Simple profile: name, email | HMW 1 | User/profile management |
| 2 | Course records: title, description, category, create/edit/delete | HMW 1 | Core records and CRUD |
| 3 | Learning content under each course: title, type (note / link / PDF reference / assignment resource), URL or description | HMW 1 | Core records and CRUD |
| 4 | Keyword search across courses and content | HMW 2 | Search/filter |
| 5 | Filter by course, content type and completion status | HMW 2, 3 | Search/filter |
| 6 | Completion status on each content item: Not started / In progress / Completed | HMW 3 | Core records |
| 7 | Dashboard: courses count, content count, completed vs pending per course | HMW 3 | Reports/dashboard |
| 8 | Validation messages for empty or invalid input | all | Validation |

Deliberately left out: reminders, due dates, priorities, tags, file uploads and sharing, because they exceed the college requirements or drift toward a task manager.

### 7.4 Prototype
Low-fidelity screen sketches. The names and numbers are placeholders for layout only, not real data.

```text
[1] DASHBOARD                         [2] COURSES
+-------------------------------+     +-------------------------------+
| Courses: 3   Content: 12      |     | Search: [____________] [Go]   |
| Completed: 5  Pending: 7      |     | [+ Add course]                |
|                               |     | DBMS            4 items  >    |
| Per course:                   |     | Algorithms      5 items  >    |
|  DBMS        2/4 done         |     | Embedded Sys    3 items  >    |
|  Algorithms  3/5 done         |     +-------------------------------+
+-------------------------------+

[3] COURSE DETAIL                     [4] ADD / EDIT CONTENT
+-------------------------------+     +-------------------------------+
| DBMS  [Edit] [Delete]         |     | Title:  [______________]      |
| Filter: type [All v]          |     | Type:   [Note v]              |
|         status [All v]        |     | Link/description: [_______]   |
| [+ Add content]               |     | Status: [Not started v]       |
| Normalization notes           |     | [Save] [Cancel]               |
|   Note | Completed   [Edit]   |     | (error text shows here if     |
| SQL practice sheet            |     |  title is empty)              |
|   Assignment | Not started    |     +-------------------------------+
+-------------------------------+
[5] PROFILE: Name [_______] Email [_______] [Save]
```

### 7.5 Test
**Method:** Walkthrough of the paper prototype by the developer. This is not user testing, and no other participants were involved.

| Scenario | Completed with the sketched screens? | Notes from the developer |
|---|---|---|
| 1. Add a new course, then add a note to it | Yes. The Courses screen has Add course, Course Detail has Add content, and the form has title, type, link/description and status. | The sketch does not show how the user moves from saving a new course to its Course Detail screen, but the intended flow is understandable. |
| 2. Find an item by keyword, then narrow to completed items | Yes. The Courses screen has keyword search, and Course Detail has type and status filters. | The sketch shows the controls but not an example of the search result state. |
| 3. See what is still pending in one course | Yes. Course Detail has a status filter, and the dashboard shows completed vs pending per course. | The pending state could be made more visually obvious, but the required information is represented. |

**Findings to carry forward:**
1. Define the navigation after saving a new course (screens and flow).
2. Define the search result state.
3. Make the pending status visually clear in the UI.

**Open question for Functional Requirements (not a test result):** the sketched search box is on the Courses screen. Whether search also covers content items needs to be decided.
## 8. Functional Requirements

| ID | Requirement | Source |
|---|---|---|
| FR-01 | Create and edit a profile (name, email). | Idea 1 |
| FR-02 | View the profile. | Idea 1 |
| FR-03 | Create a course (title required; description and category optional). | Idea 2 |
| FR-04 | View the list of all courses. | Idea 2 |
| FR-05 | View a course's details and its learning content. | Idea 2, 3 |
| FR-06 | Edit a course. | Idea 2 |
| FR-07 | Delete a course, together with its content. | Idea 2 |
| FR-08 | Add learning content to a course (title required, type, link/description, status). | Idea 3 |
| FR-09 | Edit a content item. | Idea 3 |
| FR-10 | Delete a content item. | Idea 3 |
| FR-11 | Set a content item's status: Not started / In progress / Completed. | Idea 6 |
| FR-12 | Keyword search across course titles and content titles. | Idea 4 |
| FR-13 | Filter a course's content by type and by status. | Idea 5 |
| FR-14 | Dashboard totals: courses, content items, completed, pending. | Idea 7 |
| FR-15 | Dashboard per-course progress (completed / total). | Idea 7 |
| FR-16 | Validate input: reject an empty title or invalid email, and invalid type or status values, with a clear message. | Idea 8 |
| FR-17 | Handle errors without crashing: a friendly message for a missing record or an unexpected error. | College requirement |

Ideas refer to section 7.3. Decisions affecting these requirements are recorded in D-04.
## 9. Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-01 | Usability | Every main function (courses, content, search, dashboard, profile) is reachable from the navigation on every page. |
| NFR-02 | Performance | Pages load in about 2 seconds or less on a local machine with up to a few hundred records. |
| NFR-03 | Reliability | Invalid input or a missing record never crashes the app. A clear message is shown instead (supports FR-16, FR-17). |
| NFR-04 | Data integrity | Deleting a course leaves no orphaned content. Foreign keys are enforced in SQLite. |
| NFR-05 | Security (basic) | All database queries are parameterized, and user text is escaped when displayed. |
| NFR-06 | Maintainability | Code follows the frontend/backend structure from D-01, with meaningful names and short comments where needed. |
| NFR-07 | Portability | The app runs locally on Windows with Python and `pip install -r requirements.txt`, and needs no database server. |
| NFR-08 | Testability | Core functions have basic automated tests in the `tests/` folder. |

These are targets. Each is verified during testing, and none is claimed as met yet.
## 10. User Stories

| ID | Story | Covers |
|---|---|---|
| US-01 | As a user, I want to create and update my profile so that my information stays current. | FR-01, FR-02 |
| US-02 | As a user, I want to create a course so that I can organize my learning in one place. | FR-03, FR-04 |
| US-03 | As a user, I want to view a course with its content so that I see everything for it together. | FR-05 |
| US-04 | As a user, I want to edit or delete a course so that my records stay accurate. | FR-06, FR-07 |
| US-05 | As a user, I want to add learning content to a course so that notes, links and resources sit with the course. | FR-08 |
| US-06 | As a user, I want to edit or delete content so that the course stays current. | FR-09, FR-10 |
| US-07 | As a user, I want to mark content Not started / In progress / Completed so that I know what is done. | FR-11 |
| US-08 | As a user, I want to search by keyword so that I can find information quickly. | FR-12 |
| US-09 | As a user, I want to filter a course's content by type and status so that I can see what is pending. | FR-13 |
| US-10 | As a mentor/admin, I want simple reports so that I can review activity and identify pending work. | FR-14, FR-15 |
| US-11 | As a user, I want clear messages for bad input or errors so that I can fix problems without the app breaking. | FR-16, FR-17 |

US-01 and US-10 follow the college's suggested user stories. Roles come from section 6.

## 11. Acceptance Criteria

| Story | Acceptance criteria |
|---|---|
| US-01 | A profile with a name and a valid email can be saved. The saved details display on the profile page. Editing changes them. |
| US-02 | A course with a title is saved. After saving, the user lands on that course's detail page (D-04). The course appears in the course list. |
| US-03 | The detail page shows the course info and all its content items with type and status. |
| US-04 | Edits are saved and shown. Deleting a course removes it and all its content. |
| US-05 | Content with a title, type, link/description and status is saved under the course and listed on its page. |
| US-06 | Edits are saved. A deleted item no longer appears. |
| US-07 | The status can be changed, and the new status shows on the course page and the dashboard. |
| US-08 | A keyword returns courses and content whose titles match. No match shows a clear "no results" message. |
| US-09 | Filtering by type and/or status lists only matching items. Pending means Not started or In progress (D-04). |
| US-10 | The dashboard shows totals for courses, content, completed and pending, plus completed/total per course. |
| US-11 | An empty title, an invalid email, or an invalid type or status is rejected with a clear message. A missing record shows a friendly message, not a crash. |
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


### DL-08 - Design Thinking: Define stage (Tracker T-07, stage 2 of 5)
- **Date:** 2026-10-03
- **Work performed:** Recorded pain points, the point-of-view statement and three How Might We questions as section 7.2.
- **Result:** Committed and pushed.
- **Evidence:** Push output `11020cc..4fdeffc`.
- **Branch / Commit:** `feature/project-architecture` 4fdeffc (docs: add design thinking define stage)


### DL-09 - Design Thinking: Ideate, Prototype and Test stages (Tracker T-07, completed)
- **Date:** 2026-10-03
- **Work performed:** Recorded the eight kept ideas (7.3), low-fidelity screen sketches (7.4) and a developer walkthrough of the paper prototype (7.5). The test was not user testing.
- **Result:** All three walkthrough scenarios were completed with the sketched screens. Three findings and one open question were carried forward.
- **Evidence:** `git log --oneline -n 3` output.
- **Branch / Commit:** `feature/project-architecture` 8ceaaa0 (docs: complete design thinking stages)


### DL-10 - Functional requirements (Tracker T-08)
- **Date:** 2026-10-03
- **Work performed:** Added 17 functional requirements (FR-01 to FR-17) as section 8. Recorded decision D-04 in the decision log.
- **Result:** Committed and pushed.
- **Evidence:** Push output `8ceaaa0..27acfb8`.
- **Branch / Commit:** `feature/project-architecture` 27acfb8 (docs: add functional requirements and record decision D-04)


### DL-11 - Non-functional requirements (Tracker T-09)
- **Date:** 2026-10-03
- **Work performed:** Added 8 non-functional requirements (NFR-01 to NFR-08) as section 9. They are targets, to be verified in testing.
- **Result:** Committed and pushed.
- **Evidence:** `git log --oneline -n 3` output.
- **Branch / Commit:** `feature/project-architecture` 44a27a8 (docs: add non-functional requirements)

### DL-12 - User stories and acceptance criteria (Tracker T-10)
- **Date:** 2026-10-03
- **Work performed:** Added 11 user stories (US-01 to US-11) and their acceptance criteria as sections 10-11, covering FR-01 to FR-17.
- **Result:** Committed and pushed.
- **Evidence:** Push output `44a27a8..e9f8d07`.
- **Branch / Commit:** `feature/project-architecture` e9f8d07 (docs: add user stories and acceptance criteria)

## 24. Requirements Traceability

Chain: Requirement -> Story -> Design -> Implementation -> Test -> Evidence -> Git commit.
Only the Story and Design columns are filled so far. "pending" means no real evidence exists yet and will be filled as work is completed and verified. NFR-01 to NFR-08 are added later, in the Requirements Traceability Update task.

| Requirement | Story | Design (prototype, 7.4) | Implementation | Test | Evidence | Commit |
|---|---|---|---|---|---|---|
| FR-01 | US-01 | Screen 5 | pending | pending | pending | pending |
| FR-02 | US-01 | Screen 5 | pending | pending | pending | pending |
| FR-03 | US-02 | Screen 2 | pending | pending | pending | pending |
| FR-04 | US-02 | Screen 2 | pending | pending | pending | pending |
| FR-05 | US-03 | Screen 3 | pending | pending | pending | pending |
| FR-06 | US-04 | Screen 3 | pending | pending | pending | pending |
| FR-07 | US-04 | Screen 3 | pending | pending | pending | pending |
| FR-08 | US-05 | Screen 3, 4 | pending | pending | pending | pending |
| FR-09 | US-06 | Screen 3, 4 | pending | pending | pending | pending |
| FR-10 | US-06 | Screen 3 | pending | pending | pending | pending |
| FR-11 | US-07 | Screen 4 | pending | pending | pending | pending |
| FR-12 | US-08 | Screen 2 | pending | pending | pending | pending |
| FR-13 | US-09 | Screen 3 | pending | pending | pending | pending |
| FR-14 | US-10 | Screen 1 | pending | pending | pending | pending |
| FR-15 | US-10 | Screen 1 | pending | pending | pending | pending |
| FR-16 | US-11 | Screen 4 (error text) | pending | pending | pending | pending |
| FR-17 | US-11 | not sketched, planned in Validation & Error-Handling Design | pending | pending | pending | pending |
