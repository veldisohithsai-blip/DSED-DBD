-- =====================================================
-- Job Portal Database Schema (SQLite)
-- =====================================================

DROP TABLE IF EXISTS matching_results;
DROP TABLE IF EXISTS applications;
DROP TABLE IF EXISTS resumes;
DROP TABLE IF EXISTS jobs;
DROP TABLE IF EXISTS users;

-- USERS: stores both job seekers and recruiters (role column differentiates them)
CREATE TABLE users (
    user_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL,
    email         TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    role          TEXT NOT NULL CHECK (role IN ('jobseeker', 'recruiter')),
    company_name  TEXT,                       -- only used for recruiters
    phone         TEXT,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- RESUMES: one job seeker can upload multiple resumes over time
CREATE TABLE resumes (
    resume_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    filename     TEXT NOT NULL,
    filepath     TEXT NOT NULL,
    parsed_text  TEXT,                         -- raw text extracted via PyPDF2
    skills       TEXT,                         -- comma-separated skills detected
    uploaded_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- JOBS: posted by recruiters
CREATE TABLE jobs (
    job_id           INTEGER PRIMARY KEY AUTOINCREMENT,
    recruiter_id     INTEGER NOT NULL,
    title            TEXT NOT NULL,
    company          TEXT NOT NULL,
    location         TEXT NOT NULL,
    job_type         TEXT NOT NULL CHECK (job_type IN ('Full-time','Part-time','Internship','Remote')),
    salary_range     TEXT,
    description      TEXT NOT NULL,
    skills_required  TEXT NOT NULL,            -- comma-separated
    posted_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recruiter_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- APPLICATIONS: link table between job seekers and jobs
CREATE TABLE applications (
    application_id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id         INTEGER NOT NULL,
    user_id        INTEGER NOT NULL,
    resume_id      INTEGER NOT NULL,
    status         TEXT NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending','Shortlisted','Rejected','Hired')),
    applied_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (job_id)    REFERENCES jobs(job_id) ON DELETE CASCADE,
    FOREIGN KEY (user_id)   REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (resume_id) REFERENCES resumes(resume_id) ON DELETE CASCADE,
    UNIQUE (job_id, user_id)                    -- a seeker can apply to a job only once
);

-- MATCHING_RESULTS: stores the computed resume <-> job match score
CREATE TABLE matching_results (
    match_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    application_id   INTEGER NOT NULL UNIQUE,
    resume_id        INTEGER NOT NULL,
    job_id           INTEGER NOT NULL,
    match_score      REAL NOT NULL,             -- percentage 0-100
    matched_skills   TEXT,                       -- comma-separated overlap
    missing_skills   TEXT,                       -- comma-separated gap
    generated_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (application_id) REFERENCES applications(application_id) ON DELETE CASCADE,
    FOREIGN KEY (resume_id)      REFERENCES resumes(resume_id) ON DELETE CASCADE,
    FOREIGN KEY (job_id)         REFERENCES jobs(job_id) ON DELETE CASCADE
);
