# SkillBridge — Job Portal with Resume Parsing & Matching

A college project demonstrating a full-stack job portal: Flask backend,
SQLite relational database, and a resume parsing/matching pipeline built
with PyPDF2.

## Setup

```bash
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser. The database (`job_portal.db`)
and sample resume PDFs are generated automatically on first run.

## Demo accounts

| Role       | Email                          | Password    |
|------------|---------------------------------|-------------|
| Job seeker | john.doe@example.com            | password123 |
| Job seeker | priya.sharma@example.com        | password123 |
| Recruiter  | ananya.rao@technova.com         | password123 |
| Recruiter  | rahul.nair@cloudify.com         | password123 |

## Folder structure

```
job_portal/
├── app.py              Flask routes and application logic
├── matcher.py           PDF parsing + skill matching logic
├── seed_data.py          Generates sample users/jobs/resumes on first run
├── schema.sql            SQLite table definitions
├── requirements.txt
├── templates/            Jinja2 HTML templates
├── static/css/style.css   Design system + animations
├── static/js/script.js    Match-ring animation, dropzone, flash messages
└── static/uploads/        Uploaded/generated resume PDFs
```

## Database design

Five tables, connected by foreign keys:

- **users** — job seekers and recruiters (role column differentiates them)
- **resumes** — PDF resumes uploaded by a user, with parsed text and detected skills
- **jobs** — postings created by a recruiter
- **applications** — a job seeker applying to a job with a chosen resume
- **matching_results** — the computed match score for each application

See the full write-up in the project delivery message for an ER diagram
and how each relationship maps to a real user action.


## Demo notes
- Job search supports keyword, location, and job-type filtering.
- Recruiters can post, edit, delete jobs and update applicant status.
- A fresh database is seeded with Full-time, Part-time, Internship and Remote examples.
- If an older `job_portal.db` is present and you want the new demo data, stop Flask, delete `job_portal.db`, then run `python app.py` again.
