"""
seed_data.py
------------
Populates the freshly-created database with realistic sample data so the
site looks populated for a demo: recruiters, job seekers, jobs, resumes
(real generated PDFs, parsed with the same PyPDF2 pipeline as a real
upload), applications and matching results.

This file is only ever called once, from app.py, when job_portal.db
does not yet exist.
"""

import os
from werkzeug.security import generate_password_hash
from fpdf import FPDF

from matcher import extract_text_from_pdf, detect_skills, compute_match_score

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")


def make_resume_pdf(filename, name, email, phone, summary, skills, experience):
    """Generate a simple, real PDF resume file using fpdf2."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, name, ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"{email}  |  {phone}", ln=True)
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Summary", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, summary)
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Skills", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, ", ".join(skills))
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(0, 8, "Experience", ln=True)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, experience)

    filepath = os.path.join(UPLOAD_FOLDER, filename)
    pdf.output(filepath)
    return filepath


def run(conn):
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    cur = conn.cursor()

    # ---------------- Users: recruiters ----------------
    recruiters = [
        ("Ananya Rao", "ananya.rao@technova.com", "TechNova Inc", "9876543210"),
        ("Rahul Nair", "rahul.nair@cloudify.com", "Cloudify Systems", "9876543211"),
    ]
    recruiter_ids = []
    for name, email, company, phone in recruiters:
        cur.execute(
            "INSERT INTO users (name, email, password_hash, role, company_name, phone) VALUES (?, ?, ?, 'recruiter', ?, ?)",
            (name, email, generate_password_hash("password123"), company, phone),
        )
        recruiter_ids.append(cur.lastrowid)

    # ---------------- Users: job seekers ----------------
    seekers = [
        ("John Doe", "john.doe@example.com", "9000000001"),
        ("Priya Sharma", "priya.sharma@example.com", "9000000002"),
        ("Arjun Mehta", "arjun.mehta@example.com", "9000000003"),
    ]
    seeker_ids = []
    for name, email, phone in seekers:
        cur.execute(
            "INSERT INTO users (name, email, password_hash, role, phone) VALUES (?, ?, ?, 'jobseeker', ?)",
            (name, email, generate_password_hash("password123"), phone),
        )
        seeker_ids.append(cur.lastrowid)

    # ---------------- Jobs ----------------
    jobs = [
        (recruiter_ids[0], "Python Developer", "TechNova Inc", "Hyderabad", "Full-time", "6-9 LPA",
         "We are looking for a Python developer to build and maintain backend services using Flask and SQL databases.",
         "Python, Flask, SQL, REST API, Git"),
        (recruiter_ids[1], "Frontend Developer", "Cloudify Systems", "Bangalore", "Full-time", "5-8 LPA",
         "Build responsive, accessible web interfaces and collaborate closely with designers and backend engineers.",
         "HTML, CSS, JavaScript, React, UI/UX"),
        (recruiter_ids[0], "Data Analyst", "TechNova Inc", "Remote", "Full-time", "5-7 LPA",
         "Analyze business data, build dashboards and present insights to stakeholders across the company.",
         "Python, SQL, Excel, Power BI, Statistics"),
        (recruiter_ids[1], "Java Backend Developer", "Cloudify Systems", "Pune", "Full-time", "7-10 LPA",
         "Design and maintain scalable backend microservices using Java and Spring Boot.",
         "Java, Spring Boot, MySQL, REST API"),
        (recruiter_ids[0], "Machine Learning Engineer", "TechNova Inc", "Hyderabad", "Full-time", "10-14 LPA",
         "Work on ML pipelines for recommendation systems, from data preparation to model deployment.",
         "Python, Machine Learning, TensorFlow, NumPy, Pandas"),
        (recruiter_ids[1], "UI/UX Design Intern", "Cloudify Systems", "Remote", "Internship", "15k/month",
         "Assist the design team with wireframes, prototypes and usability research for our web products.",
         "Figma, Adobe XD, Wireframing, CSS"),
        (recruiter_ids[0], "Python Teaching Assistant", "TechNova Inc", "Hyderabad", "Part-time", "25k/month",
         "Support students in Python programming labs, debugging exercises and basic data structures.",
         "Python, Communication, Data Structures, Algorithms"),
        (recruiter_ids[1], "SQL Data Intern", "Cloudify Systems", "Pune", "Part-time", "20k/month",
         "Help the analytics team prepare reports and clean relational data using SQL and Excel.",
         "SQL, MySQL, Excel, Statistics"),
    ]
    job_ids = []
    for j in jobs:
        cur.execute(
            """INSERT INTO jobs (recruiter_id, title, company, location, job_type, salary_range, description, skills_required)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            j,
        )
        job_ids.append(cur.lastrowid)

    # ---------------- Resumes (real generated PDFs, parsed like a live upload) ----------------
    resume_specs = [
        {
            "user_id": seeker_ids[0], "filename": "john_doe_resume.pdf",
            "name": "John Doe", "email": "john.doe@example.com", "phone": "9000000001",
            "summary": "Aspiring backend developer with hands-on project experience in Python and Flask, "
                       "comfortable working with relational databases and REST APIs.",
            "skills": ["Python", "Flask", "SQL", "Git", "REST API", "Data Structures"],
            "experience": "Built a college project management system using Flask and SQLite. "
                          "Completed a summer internship maintaining internal REST APIs.",
        },
        {
            "user_id": seeker_ids[1], "filename": "priya_sharma_resume.pdf",
            "name": "Priya Sharma", "email": "priya.sharma@example.com", "phone": "9000000002",
            "summary": "Frontend-focused developer who enjoys building clean, accessible user interfaces "
                       "and collaborating on design systems.",
            "skills": ["HTML", "CSS", "JavaScript", "React", "UI/UX", "Figma"],
            "experience": "Developed the frontend for a campus event portal using React. "
                          "Freelanced on small business landing pages using HTML, CSS and JavaScript.",
        },
        {
            "user_id": seeker_ids[2], "filename": "arjun_mehta_resume.pdf",
            "name": "Arjun Mehta", "email": "arjun.mehta@example.com", "phone": "9000000003",
            "summary": "Data enthusiast with a strong foundation in Python and statistics, interested in "
                       "analytics and machine learning roles.",
            "skills": ["Python", "SQL", "Pandas", "NumPy", "Statistics", "Power BI", "Machine Learning"],
            "experience": "Final-year project on predictive analytics using Python and Pandas. "
                          "Built dashboards in Power BI for a student analytics club.",
        },
    ]

    resume_ids = {}
    for spec in resume_specs:
        filepath = make_resume_pdf(
            spec["filename"], spec["name"], spec["email"], spec["phone"],
            spec["summary"], spec["skills"], spec["experience"],
        )
        parsed_text = extract_text_from_pdf(filepath)
        detected_skills = detect_skills(parsed_text)
        cur.execute(
            """INSERT INTO resumes (user_id, filename, filepath, parsed_text, skills)
               VALUES (?, ?, ?, ?, ?)""",
            (spec["user_id"], spec["filename"], f"uploads/{spec['filename']}",
             parsed_text, ", ".join(detected_skills)),
        )
        resume_ids[spec["user_id"]] = cur.lastrowid

    # ---------------- Applications + Matching Results ----------------
    # (seeker_id, job_id, status)
    sample_applications = [
        (seeker_ids[0], job_ids[0], "Shortlisted"),  # John -> Python Developer
        (seeker_ids[0], job_ids[2], "Pending"),      # John -> Data Analyst
        (seeker_ids[1], job_ids[1], "Shortlisted"),  # Priya -> Frontend Developer
        (seeker_ids[1], job_ids[5], "Pending"),      # Priya -> UI/UX Intern
        (seeker_ids[2], job_ids[2], "Hired"),        # Arjun -> Data Analyst
        (seeker_ids[2], job_ids[4], "Pending"),      # Arjun -> ML Engineer
    ]

    for user_id, job_id, status in sample_applications:
        resume_id = resume_ids[user_id]
        resume_row = cur.execute(
            "SELECT skills FROM resumes WHERE resume_id = ?", (resume_id,)
        ).fetchone()
        job_row = cur.execute(
            "SELECT skills_required FROM jobs WHERE job_id = ?", (job_id,)
        ).fetchone()

        resume_skills = [s.strip() for s in (resume_row["skills"] or "").split(",") if s.strip()]
        score, matched, missing = compute_match_score(resume_skills, job_row["skills_required"])

        cur.execute(
            "INSERT INTO applications (job_id, user_id, resume_id, status) VALUES (?, ?, ?, ?)",
            (job_id, user_id, resume_id, status),
        )
        application_id = cur.lastrowid

        cur.execute(
            """INSERT INTO matching_results
               (application_id, resume_id, job_id, match_score, matched_skills, missing_skills)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (application_id, resume_id, job_id, score, ", ".join(matched), ", ".join(missing)),
        )

    conn.commit()
    conn.close()
