# Design Thinking & Data Model — Course Content Manager

## 1. Problem Statement

Students often manage their course materials and notes in scattered, unorganized ways,
making it hard to track what they've completed and what's due. Mentors overseeing
multiple students have no centralized way to monitor engagement or spot overdue work,
since progress and consistency aren't visible anywhere outside informal check-ins.

The Course Content Manager solves this with a mentor-first dashboard that tracks not
just completion, but consistency — helping mentors identify students who need support —
while giving students a single organized space for their courses, content, and
deadlines, with visible alerts for upcoming or overdue work.

**What makes this different from a generic LMS (e.g., Google Classroom):**
- Mentor-first design: the mentor's oversight dashboard is a core feature, not an
  afterthought.
- Tracks *consistency*, not just completion — via a visual streak calendar showing
  daily engagement.

---

## 2. Design Thinking

### 2.1 Empathize — User Personas

**Persona 1: The Mentor (Mr. Rao)**
- Role: Oversees 5–15 students across one or more courses
- Goal: Wants to know who's falling behind before it becomes a problem, without
  manually messaging every student
- Frustration: No visibility into student activity between check-ins; can't tell if
  a quiet student is doing fine or silently struggling
- Needs: A quick dashboard view — who's active, who's stalled, what's overdue

**Persona 2: The Student (Priya)**
- Role: Enrolled in multiple courses, juggling notes/content across each
- Goal: Wants one place to see all their course content and know what's pending
- Frustration: Notes/materials scattered across apps; loses track of deadlines; no
  clear sense of their own progress
- Needs: An organized content view per course, with clear status and deadline
  visibility, and a motivating sense of their own progress

### 2.2 Define — Point of View Statements

> Mentors need a way to **see student engagement and consistency at a glance**
> because **manually checking in with each student doesn't scale and hides quiet
> students who are silently falling behind.**

> Students need a way to **organize their course content in one place with clear
> status and deadlines** because **scattered materials make it hard to know what's
> done, what's pending, and what's overdue.**

### 2.3 Ideate — Feature Table

| Feature | Solves whose need | Classification | Complexity/Time |
|---|---|---|---|
| Course CRUD (create/edit/delete courses) | Student | REQUIRED | Low |
| Content/notes CRUD under a course | Student | REQUIRED | Low |
| Status field (Not Started / In Progress / Completed) | Student + Mentor | REQUIRED | Low |
| Due date field on content items | Student | REQUIRED | Low |
| Search/filter courses & content | Student | REQUIRED | Medium |
| Mentor dashboard (per-student overview) | Mentor | REQUIRED | Medium |
| Deadline banner (overdue/upcoming alert) | Student + Mentor | RECOMMENDED | Low |
| Streak calendar (consistency heatmap) | Student (motivation) + Mentor (oversight) | RECOMMENDED | Low-Medium |
| Dashboard charts (completion % bar/pie) | Mentor | OPTIONAL | Medium |
| Email/SMS notifications | Student | OPTIONAL (deferred) | High |

---

## 3. Data Model

Hierarchy: **Mentor (1) → Student (many) → Course (many) → Content (many)**

Every relationship is one-to-many; no junction/association tables are needed.

### Mentor
- id (PK)
- name
- email

### Student
- id (PK)
- name
- email
- mentor_id (FK → Mentor.id)

### Course
- id (PK)
- title
- description
- student_id (FK → Student.id)

### Content
- id (PK)
- title
- notes
- status (Not Started / In Progress / Completed)
- due_date
- updated_at (used for streak calendar + consistency tracking)
- course_id (FK → Course.id)