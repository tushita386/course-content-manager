# Testing - Course Content Manager

## Purpose
Show, with repeatable evidence, that the application meets the functional requirements (FR-01 to FR-17)
and the testable non-functional requirements (NFR-01 to NFR-05) in `PROJECT_MASTER_DOCUMENT.md`.

## Approach
- Automated tests written with Python's built-in `unittest`, so no extra package is needed.
  The same tests also run unchanged with `pytest` if you prefer it (`pip install pytest`, then `python -m pytest`).
- Three levels, one file each in `tests/`:

| File | What it checks | Test cases |
|---|---|---|
| `test_validation.py` | The input rules from section 18.1 | TC-V01 to TC-V14 |
| `test_models.py` | Database operations: profile, course, content, search, filters, dashboard, safety | TC-M01 to TC-M26 |
| `test_routes.py` | The web pages through Flask's test client: create, view, edit, delete, validation messages, error pages, escaping, links, forms and speed | TC-R01 to TC-R29 |

- Every test uses a temporary or in-memory database. The real development database is never touched or reset.
- Each test starts with a one-line description in the form `TC-ID | requirement IDs | what is checked`.
  The traceability matrix (section 24 of the master document) is built from these tags.

## How to run
From the project root, with the virtual environment active:
```powershell
python tests/run_tests.py
```
The results are printed and saved to `docs/test_results.txt`. To run a single file:
```powershell
python -m unittest tests.test_validation -v
```

## Coverage by area
| Area | Test cases |
|---|---|
| Profile | TC-M01 to TC-M04, TC-R03 to TC-R05 |
| Courses | TC-M05 to TC-M09, TC-R06 to TC-R11 |
| Learning content and status | TC-M10 to TC-M14, TC-R12 to TC-R14 |
| Search and filters | TC-M15 to TC-M20, TC-R16 to TC-R20 |
| Dashboard | TC-M21 to TC-M24, TC-R01, TC-R02 |
| Validation | TC-V01 to TC-V14, TC-R04, TC-R08, TC-R15 |
| Invalid IDs and error pages | TC-R21 to TC-R23 |
| Safety, links, forms, speed | TC-M25, TC-M26, TC-R24 to TC-R29 |

## Pass criteria
All tests pass. Any failure is investigated and fixed in the code (tests are not weakened to get a pass),
and the whole suite is then run again (regression run).

## Environment
Windows, Python virtual environment, Flask and the other pinned packages in `backend/requirements.txt`.
The date, Python version and operating system of each run are written at the top of `docs/test_results.txt`.

## What is not covered
- Looking at the pages in a real browser, and their visual appearance (see the demo checklist in section 33 of the master document).
- Different browsers and screen sizes.
- Security testing beyond the checks for escaping HTML, safe links and parameterized SQL.
