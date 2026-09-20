CREATE TABLE IF NOT EXISTS instructors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    instructor_id INTEGER NOT NULL,
    current_semester INTEGER,
    FOREIGN KEY (instructor_id) REFERENCES instructors (id)
);

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    subject TEXT,
    semester INTEGER,
    student_id INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id)
);

CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    notes TEXT,
    status TEXT NOT NULL DEFAULT 'Not Started',
    due_date TEXT,
    updated_at TEXT NOT NULL,
    created_by TEXT NOT NULL DEFAULT 'student',
    course_id INTEGER NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses (id)
);

-- Reference table: VTU 2022 Scheme, B.E. Computer Science and Engineering (CSE)
-- Scoped to one branch/scheme for now. If you ever add another branch, add
-- "branch" and "scheme" columns here rather than duplicating this table.
CREATE TABLE IF NOT EXISTS vtu_subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    semester INTEGER NOT NULL,
    subject_name TEXT NOT NULL,
    UNIQUE (semester, subject_name)
);

-- Seed data. INSERT OR IGNORE means re-running init_db() won't create duplicates.
INSERT OR IGNORE INTO vtu_subjects (semester, subject_name) VALUES
(1, 'Mathematics-I for CSE Stream'),
(1, 'Applied Physics for CSE Stream'),
(1, 'Principles of Programming Using C'),
(1, 'Engineering Science Course-I'),
(1, 'Emerging Technology Course-I / Programming Language Course-I'),
(1, 'Communicative English / Professional Writing Skills in English'),
(1, 'Samskrutika Kannada / Balake Kannada / Indian Constitution'),
(1, 'Innovation and Design Thinking / Scientific Foundations for Health'),

(2, 'Mathematics-II for CSE Stream'),
(2, 'Applied Chemistry for CSE Stream'),
(2, 'Computer-Aided Engineering Drawing'),
(2, 'Engineering Science Course-II'),
(2, 'Programming Language Course-II / Emerging Technology Course-II'),
(2, 'Professional Writing Skills in English / Communicative English'),
(2, 'Indian Constitution / Samskrutika Kannada / Balake Kannada'),
(2, 'Scientific Foundations for Health / Innovation and Design Thinking'),

(3, 'Mathematics for Computer Science'),
(3, 'Digital Design and Computer Organization'),
(3, 'Operating Systems'),
(3, 'Data Structures and Applications'),
(3, 'Data Structures Lab'),
(3, 'Engineering Science Course / Emerging Technology Course / Programming Language Course'),
(3, 'Social Connect and Responsibility'),
(3, 'Ability Enhancement Course / Skill Enhancement Course'),
(3, 'NSS / Physical Education / Yoga'),

(4, 'Analysis and Design of Algorithms'),
(4, 'Microcontrollers'),
(4, 'Database Management Systems'),
(4, 'Analysis and Design of Algorithms Lab'),
(4, 'Engineering Science Course / Emerging Technology Course / Programming Language Course'),
(4, 'Ability Enhancement Course / Skill Enhancement Course'),
(4, 'Biology for Computer Engineers'),
(4, 'Universal Human Values'),
(4, 'NSS / Physical Education / Yoga'),

(5, 'Software Engineering and Project Management'),
(5, 'Computer Networks'),
(5, 'Theory of Computation'),
(5, 'Web Technology Lab'),
(5, 'Professional Elective Course'),
(5, 'Mini Project'),
(5, 'Research Methodology and IPR'),
(5, 'Environmental Studies and E-Waste Management'),
(5, 'NSS / Physical Education / Yoga'),

(6, 'Cloud Computing'),
(6, 'Machine Learning'),
(6, 'Professional Elective Course'),
(6, 'Open Elective Course'),
(6, 'Project Phase-I'),
(6, 'Machine Learning Lab'),
(6, 'Ability Enhancement Course / Skill Development Course'),
(6, 'NSS / Physical Education / Yoga'),
(6, 'Indian Knowledge System'),

(7, 'Internet of Things'),
(7, 'Parallel Computing'),
(7, 'Cryptography and Network Security'),
(7, 'Professional Elective Course'),
(7, 'Open Elective Course'),
(7, 'Major Project Phase-II'),

(8, 'Professional Elective Course (Online Course)'),
(8, 'Open Elective Course (Online Course)'),
(8, 'Internship (Industry/Research)');
