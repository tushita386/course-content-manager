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
- Teacher and student accounts with role-based access
- Teacher-managed student account creation
- User/profile management (teacher profile)
- Course records with CRUD
- Learning content records with CRUD
- Search and filter
- Input validation and exception handling
- Simple reports/dashboard
- Basic test cases
- README (written at the end, per the project guide)

## 5. Out of Scope
- Public student self-registration
- Student editing of courses, notes or profile data
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
| Teacher | Owns course content and manages student accounts. | Create and manage courses/content; create student accounts; view dashboard. |
| Student | Consumes learning materials. | Log in, view courses and notes, search and filter; no write access. |
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
| FR-18 | Authenticate teachers and students using username and password. | Updated role-based access decision |
| FR-19 | Allow only teachers to create student accounts; public registration is unavailable. | Updated role-based access decision |
| FR-20 | Allow students to view courses/content and search/filter, but reject all create, edit and delete operations. | Updated role-based access decision |
| FR-21 | Restrict course/content/profile management and student account management to teachers. | Updated role-based access decision |

Ideas refer to section 7.3. The original no-login portion of D-04 is superseded by D-11; the other D-04 decisions remain in force.
## 8.1 Authentication and authorization requirements
- Passwords are stored as one-way password hashes, never as plaintext.
- Login state is held in a Flask session with HTTP-only and SameSite cookie settings.
- The first teacher account is provisioned through a terminal-only Flask CLI command; there is no public teacher registration.
- A teacher creates student accounts and shares their credentials privately.
- Authorization is enforced by backend route guards. Hiding controls in HTML is only a usability measure, not the security boundary.
- Students can access the dashboard, course list, course detail and search. Students cannot access profile editing, student management, or any write route.

### Additional user stories
| ID | Story | Covers |
|---|---|---|
| US-12 | As a teacher, I want to log in securely so that only authorized staff can manage learning content. | FR-18, FR-21 |
| US-13 | As a teacher, I want to create student accounts so that students can access the materials. | FR-19 |
| US-14 | As a student, I want to view and search course notes without being able to change them. | FR-20 |

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
| NFR-09 | Authentication | Passwords are hashed and login sessions are protected with secure cookie settings. |
| NFR-10 | Authorization | Every write route checks the teacher role on the server, regardless of UI visibility. |

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
| US-12 | Valid teacher/student credentials create a session; invalid credentials are rejected; logout clears the session. |
| US-13 | A teacher can create a student account; duplicate usernames and passwords shorter than 8 characters are rejected. |
| US-14 | A student can view courses/content and search, but direct requests to teacher-only pages and write routes are rejected. |
## 12. Agile Development Approach
The project was built incrementally. The guide asked for an Agile approach, so the current state of the project, not a fixed plan, decided the next task.

For every task the same cycle was followed:
1. Pick the next task from the Excel tracker, checking what it depends on.
2. Implement it on a feature branch.
3. Verify it with real evidence (command output, a check, or a test).
4. Record it in the Development Log with the real commit.
5. Update the tracker, commit and push.

Sequential and parallel work:
```text
Requirements -> Design -> Database -> Models -> CRUD -> Search/Filter, Dashboard, Profile -> Validation -> Web UI -> Testing -> Documentation
```
Search/filter, dashboard and profile depended only on the models, so they could be done in any order (parallel in principle).
Validation had to precede the web UI because the forms use it. Testing followed the web UI.

The dates in the Excel tracker come from the original plan. The actual dates are in the Git history and in the Development Log.

## 13. System Architecture

```text
 Browser (user)
     |  HTTP: GET / POST
     v
+-------------------------------------------------+
| FLASK APPLICATION (one Python process)          |
|                                                 |
|  frontend/templates + static   <- pages (HTML/CSS)
|          ^                                      |
|          | render                               |
|  backend/routes     handle URLs, validate input |
|          |                                      |
|          v                                      |
|  backend/models     Course, ContentItem,        |
|                     Profile classes (OOP)       |
|          |                                      |
|          v                                      |
|  backend/database   connection + schema.sql     |
+----------|--------------------------------------+
           v
     SQLite file (local, no server)
```

**Example flow (FR-08, add content):**
1. The user submits the Add Content form (POST to the course's content URL).
2. The route checks the input (FR-16).
3. The model saves it using a parameterized SQL query (NFR-05).
4. The route redirects to the course detail page, which reads the data and renders the template.

| Part | Folder | Job |
|---|---|---|
| Presentation | `frontend/` | HTML templates and CSS. No business logic. |
| Request handling | `backend/routes/` | Receive requests, validate, call models, return pages. |
| Domain and data access | `backend/models/` | Classes with the database operations for each entity. |
| Database | `backend/database/` | Connection helper and `schema.sql`. |

The frontend/backend separation is a separation of folders and responsibilities inside one Flask app, not two separate servers (D-05).

## 14. Frontend Architecture
- `frontend/templates/` holds the HTML pages rendered by Flask. `frontend/static/` holds CSS and any JavaScript.
- The frontend contains presentation only, with no business logic or database access.
- Flask is configured to load templates and static files from `frontend/` (consequence of D-01).
- Pages follow the prototype sketches in section 7.4.

## 15. Backend Architecture
- `backend/app.py` is the Flask entry point.
- `backend/routes/` receives requests, validates input and returns rendered pages or redirects.
- `backend/models/` holds the classes for the entities (Course, ContentItem, Profile) and their database operations.
- `backend/database/` holds the SQLite connection helper and `schema.sql`.
- All database queries are parameterized (NFR-05).
### 15.1 Models
- `backend/models/` holds three dataclasses: `Course`, `ContentItem` and `Profile`, matching the tables in `schema.sql`.
- Each has a `from_row` method that builds an object from a database row.
- `ContentItem` defines the allowed content types and statuses (D-06, FR-11), used as the single source for validation. Its `is_pending` check is true for Not started and In progress (D-04).
- The database operations (create, read, update, delete) are added to the models during the CRUD tasks.
## 16. Database Architecture

```text
+------------------+
| PROFILE          |   (exactly one row, no login: D-04)
|------------------|
| id  PK (=1)      |
| name             |
| email            |
+------------------+

+------------------+            +----------------------+
| COURSE           | 1        N | CONTENT_ITEM         |
|------------------|------------|----------------------|
| id  PK           |            | id  PK               |
| title            |            | course_id  FK -> COURSE.id (delete cascades)
| description      |            | title                |
| category         |            | content_type         |
| created_at       |            | link_or_description  |
+------------------+            | status               |
                                | created_at           |
                                +----------------------+
```

One course has many content items. Each content item belongs to exactly one course. Profile is a single record and is not linked to courses (D-06).

The schema is in `backend/database/schema.sql`.
- `ON DELETE CASCADE` supports FR-07 and NFR-04.
- `CHECK` rules on content type and status back up FR-16. Email format is validated in the app, not in the database.
- SQLite enforces foreign keys only when `PRAGMA foreign_keys = ON` is set on each connection. This goes in the connection helper during Database Implementation.
### 16.1 Implementation
- `backend/database/db.py` provides a SQLite connection helper and an initialization function.
- The helper enables foreign keys on every connection (PRAGMA foreign_keys = ON), which makes ON DELETE CASCADE work (FR-07, NFR-04).
- The initialization function creates the tables from `schema.sql`.
- The SQLite database file is created locally and excluded from Git by `.gitignore`.
- Verified by a sanity check, not a formal test case: the three tables were created, foreign keys were on, and deleting a course left 0 content rows (see DL-18). Formal tests are planned in the testing phase.
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

## 18. API Design (Routes)

| Method | URL | Purpose | Covers |
|---|---|---|---|
| GET | `/` | Dashboard | FR-14, FR-15 |
| GET, POST | `/profile` | View the profile and save changes | FR-01, FR-02 |
| GET | `/courses` | Course list | FR-04 |
| GET, POST | `/courses/new` | Add course form, then create it | FR-03 |
| GET | `/courses/<id>` | Course detail with content. Filters via `?type=&status=` | FR-05, FR-13 |
| GET, POST | `/courses/<id>/edit` | Edit course | FR-06 |
| POST | `/courses/<id>/delete` | Delete course and its content | FR-07 |
| GET, POST | `/courses/<id>/content/new` | Add content | FR-08 |
| GET, POST | `/content/<id>/edit` | Edit content, including its status | FR-09, FR-11 |
| POST | `/content/<id>/delete` | Delete content | FR-10 |
| GET | `/search?q=` | Search course and content titles | FR-12 |
| GET, POST | `/login` | Authenticate teacher or student | FR-18 |
| POST | `/logout` | End the current session | FR-18 |
| GET, POST | `/students` | Teacher creates and lists student accounts | FR-19, FR-21 |
| (CLI) | `create-teacher` | Provision the first teacher account from the terminal | FR-18 |
| (handlers) | 404 and 500 | Friendly error pages | FR-17 |

Browser forms only send GET and POST, so every change is a POST. Deletes are never GET (D-07).

### 18.1 Validation and Error Handling

| Field | Rule |
|---|---|
| Profile name | Required, up to 100 characters |
| Profile email | Required, simple format check (text, `@`, text, `.`, text), up to 254 characters |
| Course title | Required, up to 150 characters |
| Course description / category | Optional, up to 1000 / 50 characters |
| Content title | Required, up to 150 characters |
| Content type / status | Must be one of the allowed values (D-06 and FR-11) |
| Content link/description | Optional, up to 1000 characters |
| Search keyword | An empty keyword shows "Enter a keyword" |
| Filters | An unknown filter value is treated as "All" |

Behaviour:
- Whitespace is trimmed before checking.
- A failed validation saves nothing, re-shows the form with the entered values, and gives a clear message next to the field.
- A missing course or content id shows a friendly "not found" page.
- An unexpected error shows a friendly "something went wrong" page. Details are printed to the console and not shown to the user.
- Database errors and other unexpected errors are caught by a central error handler (D-10).

The length limits are working values and may be revisited if implementation shows a genuine need.

## 19. UI Flow

```text
              +--------- navigation bar on every page ----------+
              |   Dashboard      Courses      Profile           |
              +-------------------------------------------------+

 Dashboard (/)                 Profile
   |                             (view + edit on one page)
   v
 Courses list --> Add course form --(save)--> Course detail
   |  [search box]                              |  filters: type, status
   |                                            |--> Edit course / Delete course
   v                                            |--> Add content form --(save)--> Course detail
 Search results                                 '--> Edit content form --(save)--> Course detail
   |--> matching courses --> Course detail
   '--> matching content --> its Course detail
```

- Search results page (test finding 2): two groups, "Courses" and "Content". Each content result shows the course it belongs to. No match shows "No results found".
- Pending visibility (test finding 3): status appears as a badge on every content item. Not started and In progress are styled to stand out, and Completed is styled muted.
- After saving a new course (test finding 1, D-04), the user lands on that course's detail page.
- After saving content, the user returns to the course detail page.
- Pages follow the prototype sketches in section 7.4.
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

### DL-13 - Requirements traceability matrix, initial (Tracker T-11)
- **Date:** 2026-10-03
- **Work performed:** Added the initial traceability matrix as section 24. FR-01 to FR-17 are mapped to stories and prototype screens. Implementation, test, evidence and commit columns are pending.
- **Result:** Committed and pushed.
- **Evidence:** Push output `e9f8d07..1235acc`.
- **Branch / Commit:** `feature/project-architecture` 1235acc (docs: add initial requirements traceability matrix)

### DL-14 - System architecture (Tracker T-12)
- **Date:** 2026-10-03
- **Work performed:** Added system, frontend and backend architecture as sections 13-15. Recorded decision D-05 (server-rendered Flask pages).
- **Result:** Committed and pushed.
- **Evidence:** Push output `1235acc..f55fca8`.
- **Branch / Commit:** `feature/project-architecture` f55fca8 (docs: add system architecture and record decision D-05)

### DL-15 - ER diagram and database schema (Tracker T-13, T-14)
- **Date:** 2026-10-03
- **Work performed:** Added the ER diagram as section 16 and created `backend/database/schema.sql`. Recorded decision D-06. Ran a one-off check that the SQL creates the tables in a temporary in-memory database. This was a validity check, not a formal test case.
- **Result:** Output `['profile', 'course', 'content_item']`. Committed and pushed.
- **Evidence:** Python output and push output `f55fca8..c9e65d7`.
- **Branch / Commit:** `feature/project-architecture` c9e65d7 (feat: add ER design, database schema and record decision D-06)

### DL-16 - UI flow, route design and validation design (Tracker T-15, T-16, T-17)
- **Date:** 2026-10-03
- **Work performed:** Added the route table and validation design as section 18 and 18.1, and the UI flow as section 19. Recorded decision D-07. Updated the FR-17 design reference in the traceability matrix.
- **Result:** Committed and pushed.
- **Evidence:** Push output `c9e65d7..d7d9dfc`.
- **Branch / Commit:** `feature/project-architecture` d7d9dfc (docs: add UI flow, route design, validation design and record decision D-07)

### DL-17 - Development environment setup (Tracker T-18)
- **Date:** 2026-10-03
- **Work performed:** Created a Python virtual environment (excluded from Git), installed Flask, and pinned the dependencies in backend/requirements.txt (Flask 3.1.3, Werkzeug 3.1.9, Jinja2 3.1.6, click 8.5.0, itsdangerous 2.2.0, blinker 1.9.0, MarkupSafe 3.0.4). Created backend/app.py, which loads templates and static files from frontend/ (consequence of D-01). Python version: Python 3.13.3.
- **Result:** Printing the configured folders showed the frontend/templates and frontend/static paths. The development server has not been run yet.
- **Evidence:** Terminal output of the path check and the requirements file.
- **Branch / Commit:** feature/dev-environment 9d578b5 (feat: set up Flask development environment)

### DL-18 - Database implementation (Tracker T-19)
- **Date:** 2026-10-03
- **Work performed:** Added backend/database/db.py with a SQLite connection helper that enables foreign keys (PRAGMA foreign_keys = ON) and an initialization function that creates the tables from schema.sql.
- **Result:** Verification output: tables ['profile', 'course', 'content_item']; foreign_keys 1; a cascade-delete sanity check returned 0 content rows left after deleting the course. The first attempt at the check failed because of a paste error in the terminal; the corrected one-line run succeeded. This was a sanity check, not a formal test case. The SQLite database file is excluded by .gitignore.
- **Evidence:** Terminal output as reported by the developer.
- **Branch / Commit:** feature/database a69ccba (feat: add SQLite database connection and initialization)

### DL-19 - Model classes (Tracker T-20)
- **Date:** 2026-10-05
- **Work performed:** Added the Course, ContentItem and Profile classes in backend/models/. ContentItem defines the allowed types and statuses and an is_pending check.
- **Result:** A sanity check printed the expected output: a Course built from a row, is_pending True for Not started and False for Completed, the allowed types and statuses, and a Profile. This was a sanity check, not a formal test case.
- **Evidence:** Terminal output of the check.
- **Branch / Commit:** feature/models 4bf20ee (feat: add Course, ContentItem and Profile model classes)

### DL-20 - Course CRUD, database operations (Tracker T-22)
- **Date:** 2026-10-06
- **Work performed:** Added create, get_all, get_by_id, update and delete operations to the Course model (backend/models/course.py). Each takes the database connection as its first argument and uses parameterized SQL. Validation (T-25) and exception handling (T-26) are not part of this task.
- **Result:** A sanity check on a temporary in-memory database printed the expected output: a course was created, read, updated and deleted; deleting it left 0 content rows (cascade); deleting a missing id returned False. This was a sanity check, not a formal test case. The routes for FR-03 to FR-07 are not built yet.
- **Evidence:** Terminal output of the check.
- **Branch / Commit:** feature/course-crud b22864d (feat: add course database operations)

### DL-21 - Learning content CRUD, database operations (Tracker T-23)
- **Date:** 2026-10-06
- **Work performed:** Added create, get_by_id, get_by_course, update and delete operations to the ContentItem model (backend/models/content_item.py). Each takes the database connection as its first argument and uses parameterized SQL. Status can be set on create and update. Filtering by type and status (T-24), validation (T-25) and exception handling (T-26) are not part of this task.
- **Result:** A sanity check on a temporary in-memory database printed the expected output: content items were created, read, updated (status changed to Completed, is_pending False) and deleted; deleting a missing id returned False; the database rejected an invalid status with an IntegrityError. This was a sanity check, not a formal test case. The routes for FR-08 to FR-11 are not built yet.
- **Evidence:** Terminal output of the check.
- **Branch / Commit:** feature/content-crud fbeaa87 (feat: add learning content database operations)

### DL-22 - Search and filtering, database operations (Tracker T-24)
- **Date:** 2026-10-06
- **Work performed:** Added search (new file backend/models/search.py) and optional type and status filters on ContentItem.get_by_course. Search is a case-insensitive title match (for English letters) over courses and content. It returns the matching courses and the matching content items with their course title. An empty keyword returns nothing, and % and _ are matched literally. Filters ignore unknown or empty values, which means All. Routes, validation and exception handling are not part of this task.
- **Result:** A sanity check with 11 checks on a temporary in-memory database passed: search for notes and for dbms, empty keyword, literal percent sign, and filters by type, by status, by both, with no match, and with unknown values. The first run did not pass, because git status showed content_item.py unmodified, so the filter change was missing. After writing the file again, all 11 checks passed. This was a sanity check, not a formal test case. The routes for FR-12 and FR-13 are not built yet.
- **Evidence:** Terminal output showing 11 PASS lines.
- **Branch / Commit:** feature/search-filter 25ba843 (feat: add search and content filtering operations)

### DL-23 - Dashboard and reports, database operations (Tracker T-27)
- **Date:** 2026-11-24
- **Work performed:** Added get_dashboard in backend/models/dashboard.py: totals, completed, pending (Not started and In progress) and per-course progress.
- **Result:** Covered by test cases TC-M21 to TC-M24 in the automated suite.
- **Evidence:** docs/test_results.txt
- **Branch / Commit:** feature/dashboard 4ab20f8 (feat: add dashboard totals and per-course progress)


### DL-24 - Profile management, database operations (Tracker T-21)
- **Date:** 2026-10-10
- **Work performed:** Added get and save operations to the Profile model (one profile with id 1, no login).
- **Result:** Covered by test cases TC-M01 to TC-M04 in the automated suite.
- **Evidence:** docs/test_results.txt
- **Branch / Commit:** feature/profile 2185d4b (feat: add profile view and save operations)


### DL-25 - Validation (Tracker T-25)
- **Date:** 2026-11-24
- **Work performed:** Added backend/validation.py with the rules from section 18.1: required fields, length limits, email format, allowed types and statuses, filter and keyword cleaning.
- **Result:** Covered by test cases TC-V01 to TC-V14 and the route tests for invalid input.
- **Evidence:** docs/test_results.txt
- **Branch / Commit:** feature/validation 083301f (feat: add input validation rules)


### DL-26 - Web UI and exception handling (Tracker T-26, T-28)
- **Date:** 2026-11-24
- **Work performed:** Added all routes from section 18, the HTML templates (dashboard, courses, course detail, forms, profile, search, custom 404 and 500 pages), a modern indigo/purple stylesheet, a per-request database connection and central error handlers. db.py now accepts an optional database path so tests can use a temporary database. Recorded decision D-10.
- **Result:** The app starts and the main pages load; behaviour is covered by the route tests TC-R01 to TC-R29.
- **Evidence:** docs/test_results.txt
- **Branch / Commit:** feature/web-ui 2a27666 (feat: add web UI routes, templates and error handling)


### DL-27 - Automated tests and testing guide (Tracker T-29 to T-33)
- **Date:** 2026-11-24
- **Work performed:** Added docs/testing.md and the unittest suite (validation, model and route tests) with tests/run_tests.py.
- **Result:** Run 1: 69 of 69 tests passed. No test failed, so no bug fixing was needed in this run.
- **Evidence:** docs/test_results.txt (written by the run)
- **Branch / Commit:** feature/testing 1621f49 (test: add automated test suite and testing guide)


### DL-28 - README, guides and final documentation (Tracker T-34 to T-37)
- **Date:** 2026-11-24
- **Work performed:** Added README.md, docs/user_manual.md and docs/installation_guide.md, and in the master document the Agile approach, decision summary, bug log, testing log, traceability matrix with tests, NFR verification, Git strategy, project status, demo notes and viva preparation. Ran the full test suite again (regression run).
- **Result:** Run 2: 69 of 69 tests passed.
- **Evidence:** docs/test_results.txt (written by the run)
- **Branch / Commit:** feature/final-docs b4193cf (docs: add README, guides, testing log, project status and traceability)


## 21. Decision Log
The full decisions, with options, reasons and consequences, are in `docs/decisions.md`.

| ID | Decision |
|---|---|
| D-01 | Separate frontend and backend folders |
| D-02 | Feature branches only; merge into main at final integration |
| D-03 | Python + Flask + SQLite + HTML/CSS |
| D-04 | Search covers course and content titles; new course opens its detail page; Pending = Not started + In progress; one profile, no login |
| D-05 | Server-rendered pages (no separate JavaScript API) |
| D-06 | Profile not linked to courses; four fixed content types; created_at stored |
| D-07 | Forms use GET/POST only; grouped search results; failed validation keeps the input |
| D-08 | Each stage of work on its own branch, cut from the previous one |
| D-09 | Status filter uses the three statuses only (no Pending option) |
| D-10 | Central error handlers with custom 404/500 pages; search box in the navigation bar; validation errors return HTTP 400 |

## 22. Bug / Debugging Log

| ID | Problem | Found by | Root cause | Fix | Verification |
|---|---|---|---|---|---|
| BUG-01 | During the search and filtering task (T-24), the first check failed. | The check, together with `git status`, which showed `content_item.py` as unmodified. | The filter change had not been written to `backend/models/content_item.py`. | The file was written again with the type and status filter. | All 11 checks passed afterwards (commit 25ba843). |

Process note: while checking cascade delete during the database task (T-19), the first multi-line terminal paste failed because of a paste error. The corrected one-line check passed. This was a terminal problem, not a defect in the project.

Automated testing: the recorded regression run executed 69 tests, 69 passed, and no further defects were found by the suite. Any defect found later should be added here with its steps to reproduce, root cause, fix and commit.

## 23. Testing Log

**Method.** Automated tests with Python's `unittest` (they also run under `pytest`), run with `python tests/run_tests.py`. The approach is in `docs/testing.md` and the full output is in `docs/test_results.txt`. Each test uses a temporary or in-memory database, so the real database is never touched.

**Runs.**

| Run | Tracker task | Branch / commit | Date | Tests run | Passed | Failed or errors |
|---|---|---|---|---|---|---|
| 1. Functional | Test Plan, CRUD, Validation and Search/Filter Testing | feature/testing 1621f49 | 2026-11-24 | 69 | 69 | 0 |
| 2. Regression | Regression Testing, Final Testing | feature/final-docs | 2026-11-24 | 69 | 69 | 0 |

Environment of run 2: Python 3.13.3 on Windows 11.

**Which tests belong to which tracker task.**

| Tracker task | Test cases |
|---|---|
| CRUD Testing | TC-M01 to TC-M14, TC-R03 to TC-R07, TC-R09 to TC-R14 |
| Validation Testing | TC-V01 to TC-V14, TC-M13, TC-R04, TC-R08, TC-R15 |
| Search/Filter Testing | TC-M15 to TC-M20, TC-R16 to TC-R20 |
| Dashboard, errors, safety and quality | TC-M21 to TC-M26, TC-R01, TC-R02, TC-R21 to TC-R29 |

**Test cases (results of run 2).**

| ID | Requirements | What is checked | Result |
|---|---|---|---|
| TC-M01 | FR-02 | There is no profile until one is saved | PASS |
| TC-M02 | FR-01, FR-02 | Saving creates the profile and it can be read back | PASS |
| TC-M03 | FR-01 | Saving again replaces the profile and keeps a single row | PASS |
| TC-M04 | FR-01 | The database rejects a second profile (id other than 1) | PASS |
| TC-M05 | FR-03, FR-04 | Courses are created and listed in alphabetical order | PASS |
| TC-M06 | FR-05 | A course is found by id and a missing id returns None | PASS |
| TC-M07 | FR-06 | Updating a course changes its fields | PASS |
| TC-M08 | FR-07, NFR-04 | Deleting a course also deletes its content, leaving no orphans | PASS |
| TC-M09 | FR-07 | Deleting a course that does not exist returns False | PASS |
| TC-M10 | FR-08, FR-11 | New content starts as Not started and counts as pending | PASS |
| TC-M11 | FR-09, FR-11 | Updating content changes its fields and status | PASS |
| TC-M12 | FR-10 | Deleting content removes it; a missing id returns False | PASS |
| TC-M13 | FR-16 | The database itself rejects an invalid status or type | PASS |
| TC-M14 | FR-05 | Content is listed only under its own course, oldest first | PASS |
| TC-M15 | FR-12 | Search finds content titles and shows the course each belongs to | PASS |
| TC-M16 | FR-12 | Search finds course titles regardless of letter case | PASS |
| TC-M17 | FR-12 | An empty keyword returns no results | PASS |
| TC-M18 | FR-12 | The characters % and _ are searched literally, not as wildcards | PASS |
| TC-M19 | FR-13 | Content can be filtered by type, by status and by both | PASS |
| TC-M20 | FR-13 | Unknown filter values are treated as All | PASS |
| TC-M21 | FR-14 | Dashboard totals count courses, content, completed and pending (D-04) | PASS |
| TC-M22 | FR-15 | Per-course progress shows completed/total, including courses with no content | PASS |
| TC-M23 | FR-14 | Dashboard totals follow status changes and course deletion | PASS |
| TC-M24 | FR-14 | An empty database gives all-zero totals | PASS |
| TC-M25 | NFR-05 | SQL-looking text is stored as plain text and the tables stay intact | PASS |
| TC-M26 | NFR-04 | Every connection from the helper has foreign keys switched on | PASS |
| TC-R01 | FR-14, FR-15 | The dashboard shows totals and per-course progress | PASS |
| TC-R02 | FR-14 | The dashboard works with no data and invites the user to add a course | PASS |
| TC-R03 | FR-01, FR-02 | A profile can be saved and is shown again on the profile page | PASS |
| TC-R04 | FR-16 | An invalid profile shows messages, keeps the input and saves nothing | PASS |
| TC-R05 | FR-02 | The dashboard greets the user by the saved profile name | PASS |
| TC-R06 | FR-03 | Saving a new course opens that course's detail page (D-04) | PASS |
| TC-R07 | FR-04 | The course list shows each course with its number of content items | PASS |
| TC-R08 | FR-16 | An empty course title shows a message, keeps the input and saves nothing | PASS |
| TC-R09 | FR-05 | The detail page shows the course, its content, types, status badges and progress | PASS |
| TC-R10 | FR-06 | Editing a course saves the change and returns to its detail page | PASS |
| TC-R11 | FR-07 | Deleting a course removes it and its content; the delete URL does not accept GET | PASS |
| TC-R12 | FR-08 | Adding content returns to the course page where the new item is listed | PASS |
| TC-R13 | FR-09, FR-11 | Editing content changes its fields and its status | PASS |
| TC-R14 | FR-10 | Deleting content removes it from the course page | PASS |
| TC-R15 | FR-16 | Invalid content shows messages, keeps the input and saves nothing | PASS |
| TC-R16 | FR-13 | The course page filters content by type and status; unknown values show everything | PASS |
| TC-R17 | FR-13 | The filter drop-downs keep the selected values | PASS |
| TC-R18 | FR-12 | Search results list matching courses and matching content with their course | PASS |
| TC-R19 | FR-12 | An empty keyword asks for one, and no match says so | PASS |
| TC-R20 | FR-12 | Searching in a different letter case finds the same course | PASS |
| TC-R21 | FR-17, NFR-03 | Missing courses or content show a friendly not-found page, not a crash | PASS |
| TC-R22 | FR-17 | The 404 page is the custom page with a way back to the app | PASS |
| TC-R23 | FR-17, NFR-03 | An unexpected database error shows the custom 500 page without technical details | PASS |
| TC-R24 | NFR-05 | User text containing HTML is shown as text, not run | PASS |
| TC-R25 | NFR-05 | Only http and https links become clickable links | PASS |
| TC-R26 | NFR-01 | Every main page offers links to the dashboard, courses and profile, and search | PASS |
| TC-R27 | NFR-01, FR-17 | Every internal link on the main pages leads to a working page | PASS |
| TC-R28 | NFR-01 | Every form on the main pages submits to a route that exists | PASS |
| TC-R29 | NFR-02 | With 300 courses and 900 content items the main pages respond in under 2 seconds | PASS |
| TC-V01 | FR-16 | A profile with a name and a valid email is accepted | PASS |
| TC-V02 | FR-16 | An empty or whitespace-only profile name is rejected | PASS |
| TC-V03 | FR-16 | Invalid email addresses are rejected | PASS |
| TC-V04 | FR-16 | Reasonable email addresses are accepted | PASS |
| TC-V05 | FR-16 | Profile name over 100 and email over 254 characters are rejected | PASS |
| TC-V06 | FR-16 | An empty or whitespace-only course title is rejected | PASS |
| TC-V07 | FR-16 | Course input is trimmed and optional fields may be empty | PASS |
| TC-V08 | FR-16 | Course title (150), description (1000) and category (50) limits are enforced | PASS |
| TC-V09 | FR-16 | A content type outside the allowed list is rejected | PASS |
| TC-V10 | FR-16, FR-11 | A status outside the allowed list is rejected | PASS |
| TC-V11 | FR-16, FR-11 | Every allowed content type and status is accepted | PASS |
| TC-V12 | FR-16 | Content title is required (max 150) and link/description is limited to 1000 | PASS |
| TC-V13 | FR-13 | Unknown or empty filter values are treated as All | PASS |
| TC-V14 | FR-12 | The search keyword is trimmed and None becomes empty | PASS |

**Not covered by automated tests:** using the pages in a real browser and the look of the pages. See the demo checklist in section 33.

## 24. Requirements Traceability

Chain: Requirement -> Story -> Design -> Implementation -> Test -> Evidence -> Git commit.
All columns are filled from verified work. The Test column lists the automated test cases (IDs as in docs/test_results.txt) that cover each requirement. In the recorded regression run on 2026-11-24, 69 of 69 tests passed. The quick checks run during development are logged in the development log and are not counted as tests.

| Requirement | Story | Design (prototype, 7.4) | Implementation | Test | Evidence | Commit |
|---|---|---|---|---|---|---|
| FR-01 | US-01 | Screen 5 | Profile.save; POST /profile | TC-M02, TC-M03, TC-M04, TC-R03 (all passed) | docs/test_results.txt | 2185d4b (code), 2a27666 (web) |
| FR-02 | US-01 | Screen 5 | Profile.get; GET /profile | TC-M01, TC-M02, TC-R03, TC-R05 (all passed) | docs/test_results.txt | 2185d4b (code), 2a27666 (web) |
| FR-03 | US-02 | Screen 2 | Course.create; GET, POST /courses/new | TC-M05, TC-R06 (all passed) | docs/test_results.txt | b22864d (code), 2a27666 (web) |
| FR-04 | US-02 | Screen 2 | Course.get_all; GET /courses | TC-M05, TC-R07 (all passed) | docs/test_results.txt | b22864d (code), 2a27666 (web) |
| FR-05 | US-03 | Screen 3 | Course.get_by_id and ContentItem.get_by_course; GET /courses/<id> | TC-M06, TC-M14, TC-R09 (all passed) | docs/test_results.txt | b22864d (code), 2a27666 (web) |
| FR-06 | US-04 | Screen 3 | Course.update; GET, POST /courses/<id>/edit | TC-M07, TC-R10 (all passed) | docs/test_results.txt | b22864d (code), 2a27666 (web) |
| FR-07 | US-04 | Screen 3 | Course.delete with cascade; POST /courses/<id>/delete | TC-M08, TC-M09, TC-R11 (all passed) | docs/test_results.txt | b22864d (code), 2a27666 (web) |
| FR-08 | US-05 | Screen 3, 4 | ContentItem.create; GET, POST /courses/<id>/content/new | TC-M10, TC-R12 (all passed) | docs/test_results.txt | fbeaa87 (code), 2a27666 (web) |
| FR-09 | US-06 | Screen 3, 4 | ContentItem.update; GET, POST /content/<id>/edit | TC-M11, TC-R13 (all passed) | docs/test_results.txt | fbeaa87 (code), 2a27666 (web) |
| FR-10 | US-06 | Screen 3 | ContentItem.delete; POST /content/<id>/delete | TC-M12, TC-R14 (all passed) | docs/test_results.txt | fbeaa87 (code), 2a27666 (web) |
| FR-11 | US-07 | Screen 4 | Status field in ContentItem.create and update; content forms | TC-M10, TC-M11, TC-R13, TC-V10, TC-V11 (all passed) | docs/test_results.txt | fbeaa87 (code), 2a27666 (web) |
| FR-12 | US-08 | Screen 2 | search() in backend/models/search.py; GET /search | TC-M15, TC-M16, TC-M17, TC-M18, TC-R18, TC-R19, TC-R20, TC-V14 (all passed) | docs/test_results.txt | 25ba843 (code), 2a27666 (web) |
| FR-13 | US-09 | Screen 3 | ContentItem.get_by_course type/status filters; ?type=&status= on /courses/<id> | TC-M19, TC-M20, TC-R16, TC-R17, TC-V13 (all passed) | docs/test_results.txt | 25ba843 (code), 2a27666 (web) |
| FR-14 | US-10 | Screen 1 | get_dashboard totals; GET / | TC-M21, TC-M23, TC-M24, TC-R01, TC-R02 (all passed) | docs/test_results.txt | 4ab20f8 (code), 2a27666 (web) |
| FR-15 | US-10 | Screen 1 | get_dashboard per_course; GET / | TC-M22, TC-R01 (all passed) | docs/test_results.txt | 4ab20f8 (code), 2a27666 (web) |
| FR-16 | US-11 | Screen 4 (error text) | backend/validation.py, used by every form in backend/app.py | TC-M13, TC-R04, TC-R08, TC-R15, TC-V01, TC-V02, TC-V03, TC-V04, TC-V05, TC-V06, TC-V07, TC-V08, TC-V09, TC-V10, TC-V11, TC-V12 (all passed) | docs/test_results.txt | 083301f (code), 2a27666 (web) |
| FR-17 | US-11 | No screen sketched; error handling designed in section 18.1 | Central error handlers and custom 404/500 pages in backend/app.py | TC-R21, TC-R22, TC-R23, TC-R27 (all passed) | docs/test_results.txt | 2a27666 |

### NFR verification

| ID | Requirement | Verification |
|---|---|---|
| NFR-01 | Usability: navigation on every page, working links and forms | TC-R26, TC-R27, TC-R28 (all passed) |
| NFR-02 | Performance: about 2 seconds or less | TC-R29 (all passed) (checked in the recorded run with 300 courses and 900 content items) |
| NFR-03 | Reliability: no crashes on bad input or missing records | TC-R21, TC-R23 (all passed) |
| NFR-04 | Data integrity: no orphaned content, foreign keys enforced | TC-M08, TC-M26 (all passed) |
| NFR-05 | Security (basic): parameterized queries, escaped output, safe links | TC-M25, TC-R24, TC-R25 (all passed) |
| NFR-06 | Maintainability: frontend/backend structure (D-01) | Verified by code structure and review only. No automated test. |
| NFR-07 | Portability: runs locally on Windows with Python and pip | The suite ran in the project virtual environment (Python 3.13.3) on Windows 11: 69 of 69 tests passed. The app is started with python -m flask --app backend.app run. |
| NFR-08 | Testability: automated tests in tests/ | 69 automated tests in tests/ (69 passed in the recorded run). |

## 25. Git / GitHub Strategy
- All development happens on feature branches. Each stage of work starts from the previous branch (D-08).
- Nothing is merged into `main` during development (D-02). `main` is updated once, at final integration, after the tests pass.
- Commit messages follow the pattern `feat:`, `fix:`, `test:`, `docs:`, `chore:` with a meaningful description.

| Branch | Purpose | Tip commit |
|---|---|---|
| `feature/project-architecture` | Requirements, design documents and folder structure | d7d9dfc |
| `feature/dev-environment` | Flask development environment | 9d578b5 |
| `feature/database` | SQLite connection and initialization | b8cd612 |
| `feature/models` | Model classes | 7df3c01 |
| `feature/course-crud` | Course database operations | 5ed765d |
| `feature/content-crud` | Learning content database operations | 7019fd7 |
| `feature/search-filter` | Search and filtering | 72455e0 |
| `feature/profile` | Profile operations | 4ab20f8 |
| `feature/validation` | Input validation | 083301f |
| `feature/web-ui` | Web UI, routes and error handling | 2a27666 |
| `feature/final-docs` | README, guides and final documentation | 1621f49 |
| `feature/testing` | Automated tests and testing guide | 1621f49 |

Final integration: pending. The branches are merged into `main` in creation order, only after final verification.

## 26. Current Project Status
As of 2026-11-24, all planned requirements (FR-01 to FR-17) are implemented and covered by automated tests: 69 of 69 tests passed in the recorded regression run. The application can be started and used in a browser (see the README).

Still to be done by the developer: the manual browser walk-through in section 33, the demo rehearsal, and the final review of the GitHub repository.

## 27. Completed Work

| Tracker tasks | Work | Evidence |
|---|---|---|
| 1-3 | Repository, folder structure, documentation setup | Section 17, `docs/decisions.md` |
| 4-7 | Problem statement, stakeholders, scope, Design Thinking | Sections 2-7 |
| 8-11 | Functional and non-functional requirements, user stories, traceability | Sections 8-11, 24 |
| 12-17 | Architecture, ER diagram, schema, UI flow, routes, validation design | Sections 13-19 |
| 18-20 | Environment, database, models | DL-17 to DL-19 |
| 21-24, 27 | Profile, course and content operations, search/filter, dashboard | DL-20 to DL-24 |
| 25 | Validation | `backend/validation.py`, commit 083301f |
| 26, 28 | Error handling and web UI | `backend/app.py`, `frontend/`, commit 2a27666 |
| 29-35 | Testing guide, automated tests, regression run, traceability update | Sections 23-24, `docs/testing.md`, `docs/test_results.txt`, commit 1621f49 |
| 36-37 | Technical documentation, README, user manual and installation guide | This document, `README.md`, `docs/user_manual.md`, `docs/installation_guide.md` |

## 28. Work In Progress
No implementation work is in progress. Open items for the developer: browser walk-through (section 33), demo rehearsal, final review (tracker tasks 38 to 41).

## 29. Next Steps
1. Do the browser walk-through in section 33 and note anything unexpected in section 22.
2. Rehearse the demo and the viva questions in section 34.
3. Review the GitHub repository page and the final Git history.
4. Submit.

## 30. Known Issues
- Search is case-insensitive for English letters only (a SQLite limit for the default LIKE).
- The web pages have not been checked by automated browser tests, only through Flask's test client.
- The manual browser walk-through has not been recorded yet.
- The tracker dates come from the original plan and differ from the Git dates (see section 12).
- The application runs on Flask's development server, which is fine for a demo but not for production use.

## 31. Limitations
- One profile and no login (D-04).
- Search covers titles only.
- The four content types are fixed (D-06).
- No file uploads, due dates or reminders (out of scope, section 5).
- No pagination. The speed target was checked with 300 courses and 900 content items.
- Data is stored in a local SQLite file.

## 32. Future Improvements
- User accounts and sign-in.
- Searching descriptions as well as titles.
- Tags, sorting and pagination.
- Import and export of course data.
- Browser-level automated tests.

## 33. Demo Notes
Start the app (README): `python -m flask --app backend.app run`, then open http://127.0.0.1:5000.

Suggested demo order, with a box to tick once it has been tried:
- [ ] Dashboard shows zeros and a button to add the first course.
- [ ] Profile: save a name and email. Try a bad email and see the message. The dashboard greets you by name.
- [ ] Add a course. You land on its detail page.
- [ ] Try to add a course with an empty title. The message appears and nothing is saved.
- [ ] Add three content items of different types and statuses. The status badges differ, and pending items stand out.
- [ ] Filter the content by type and by status. Clear the filter.
- [ ] Edit a content item and change its status to Completed. The progress bar moves.
- [ ] Search for a word from a course title and from a content title, in a different letter case. Search for something that does not exist.
- [ ] Dashboard: totals and per-course progress have changed.
- [ ] Delete a content item, then delete the course (confirm the prompt). The dashboard returns to zero for it.
- [ ] Open a page that does not exist, for example /courses/999. The custom 404 page appears.
- [ ] Show `python tests/run_tests.py` passing, and `git log --oneline --graph --all`.

## 34. Viva Preparation
- **What is the project?** A course content manager: courses with learning content, search, filters and a progress dashboard. It is not a task manager. Status describes learning progress.
- **Why Flask and SQLite?** Allowed by the college (Option A), simple to run, and easy to explain (D-03). SQLite needs no server.
- **Why server-rendered pages?** Simpler than a separate JavaScript API and enough for the requirement (D-05). Frontend and backend are separated by folders and responsibilities inside one Flask app.
- **How is OOP used?** The models are classes (`Course`, `ContentItem`, `Profile`) with their own database operations. `ContentItem` knows its allowed values and whether it is pending.
- **How do you stop SQL injection?** Every query is parameterized. A test stores SQL-looking text and checks that the tables stay intact (TC-M25).
- **How do you stop HTML injection?** Jinja escapes output, and only http and https links are clickable (TC-R24, TC-R25).
- **What does ON DELETE CASCADE do?** Deleting a course deletes its content. SQLite only enforces it if `PRAGMA foreign_keys = ON` is set on each connection, which the connection helper does (TC-M08, TC-M26).
- **How does validation work?** `backend/validation.py` trims and checks the input, returns values and messages, and the form is shown again with the user's input kept (TC-R04, TC-R08, TC-R15).
- **How does search work?** A case-insensitive title match on courses and content, with `%` and `_` treated literally (TC-M15 to TC-M18).
- **What counts as pending?** Not started and In progress (D-04). The status filter uses the three real statuses (D-09).
- **How are errors handled?** Central error handlers show custom 404 and 500 pages and log the details to the console, never to the user (D-10, TC-R21 to TC-R23).
- **How were requirements traced?** Section 24 links each requirement to its story, design, code, tests, evidence and commit.
- **Why are there so many branches?** Each stage was developed on its own branch and merged into `main` only at the end (D-02, D-08).
- **What did testing show?** 69 of 69 automated tests passed in the recorded run. One earlier defect (BUG-01) was caught by a check during development.
- **What are the limits?** One profile, no login, title-only search, development server (section 31).
- **What would you improve?** Accounts, richer search, tags, pagination, export (section 32).


## 36. Role-based authentication update (2026-11-24)
The original D-04 decision specified one profile and no login. The project owner later changed the required application model to two roles: Teacher and Student. This update supersedes only the no-login portion of D-04. The historical decision remains in the decision log for traceability.

- Teachers authenticate with a username and password, create student accounts, and manage courses/content.
- Students authenticate with credentials created by a teacher and have read-only access to the dashboard, courses, course content, search and filters.
- Students cannot create accounts, edit profiles, or perform create/update/delete operations.
- Passwords are stored as Werkzeug password hashes. Flask sessions identify the authenticated user.
- The initial teacher account is created from the command line using `flask --app backend.app create-teacher`.
- `FLASK_SECRET_KEY` must be set to a long random secret before deployment. The built-in fallback is for local development only.
- Public self-registration is intentionally not implemented.


### Authentication data model
The `app_user` table stores `id`, unique case-insensitive `username`, `password_hash`, `role` (`teacher` or `student`) and `created_at`. It is separate from the existing single teacher profile record. Password hashes are generated by Werkzeug; raw passwords are never written to SQLite. The database constraint rejects duplicate usernames and roles outside the two supported values.
