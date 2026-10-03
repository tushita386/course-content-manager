CREATE TABLE IF NOT EXISTS profile (
    id    INTEGER PRIMARY KEY CHECK (id = 1),
    name  TEXT NOT NULL,
    email TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS course (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    title       TEXT NOT NULL,
    description TEXT,
    category    TEXT,
    created_at  TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS content_item (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    course_id           INTEGER NOT NULL,
    title               TEXT NOT NULL,
    content_type        TEXT NOT NULL
        CHECK (content_type IN ('Note', 'Link', 'PDF reference', 'Assignment resource')),
    link_or_description TEXT,
    status              TEXT NOT NULL DEFAULT 'Not started'
        CHECK (status IN ('Not started', 'In progress', 'Completed')),
    created_at          TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES course(id) ON DELETE CASCADE
);