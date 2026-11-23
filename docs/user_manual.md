# User Manual - Course Content Manager

Course Content Manager helps you keep your courses and the learning material for each course in one place,
see what you have finished, and find things quickly.

## Starting the application
See `docs/installation_guide.md`. Then open http://127.0.0.1:5000 in your browser.

## Finding your way around
The bar at the top of every page has:
- **Dashboard** - totals and progress
- **Courses** - all your courses
- **Profile** - your name and email
- **Search box** - search course and content titles from any page

## Profile
1. Click **Profile**.
2. Enter your name and email and click **Save profile**.
3. Your name appears in the greeting on the dashboard. You can change the details at any time.

There is one profile and no password. A message appears next to a field if something is missing or the email is not valid.

## Courses
- **Add a course:** Courses > **+ Add course**. Only the title is required. After saving you land on the course page.
- **See a course:** click its title in the list. The page shows the details, your progress and its learning content.
- **Edit a course:** open the course and click **Edit course**.
- **Delete a course:** open the course and click **Delete course**, then confirm. This also deletes all content in that course.

## Learning content
Each course holds learning content of four types: **Note**, **Link**, **PDF reference** and **Assignment resource**.
Each item has a status:

| Status | Meaning |
|---|---|
| Not started | You have not begun it (shown in yellow) |
| In progress | You are working on it (shown in blue) |
| Completed | You are done (shown in grey) |

Not started and In progress items are called **pending**.

- **Add content:** open a course, click **+ Add content**, fill in the title, type, an optional link or description, and the status.
  A link that starts with http:// or https:// becomes clickable on the course page.
- **Change the status:** click **Edit** on the item, choose the new status and save.
- **Delete content:** click **Delete** on the item and confirm.

## Filtering a course's content
On a course page, choose a **Type** and/or a **Status** above the table and click **Filter**.
You can combine both. Choose **All** or click **Clear** to see everything again.
To see everything still to do, filter by Not started and then by In progress.

## Searching
Type a word in the search box at the top and click **Search**. The results show matching courses and matching
content items, and for each content item the course it belongs to. Search ignores upper and lower case.
If nothing matches, the page says so. Searching with an empty box asks you to enter a keyword.

## Dashboard
The dashboard shows how many courses and content items you have, how many are completed and how many are pending,
plus a progress bar for every course. The numbers update as you change statuses.

## Messages and error pages
- A red message next to a field tells you what to correct. What you typed is kept.
- If you open a page or record that does not exist (for example one you deleted), a "Page not found" page appears with a link back.
- If something unexpected goes wrong, a "Something went wrong" page appears. Go back to the dashboard and try again.

## Good to know
- Deleting a course cannot be undone.
- Your data is stored on your own computer in a local database file.


## Login and role permissions

### First-time teacher setup
1. Open PowerShell in the project root and activate the virtual environment.
2. Set a local secret: `$env:FLASK_SECRET_KEY = "your-long-random-secret"`.
3. Run `flask --app backend.app create-teacher`.
4. Enter a teacher username and password when prompted.
5. Start the app with `flask --app backend.app run` and log in.

### Teacher workflow
1. Log in with the teacher account.
2. Open **Students** to create student accounts.
3. Give each student their username and password privately.
4. Use Courses to create and maintain course material.

### Student workflow
1. Log in with the credentials supplied by the teacher.
2. View the dashboard and courses.
3. Open a course to read notes and resources.
4. Use search and filters to find content.

Students have read-only access. Attempts to access teacher-only pages or write endpoints are rejected by the server. There is no public student registration.
