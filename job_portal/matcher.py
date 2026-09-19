"""
matcher.py
----------
Small helper module that handles:
1. Extracting raw text from an uploaded PDF resume (PyPDF2)
2. Detecting which known skills appear in that text
3. Comparing a resume's skills against a job's required skills
   to produce a match score (used for the "Matching Results" table)

This keeps the matching logic simple and explainable for a
college project: it is a keyword-overlap score, not a full NLP model.
"""

from PyPDF2 import PdfReader

# A master skill list used to scan resume text. In a bigger system this
# would live in its own table; here a flat list keeps things simple.
KNOWN_SKILLS = [
    "python", "java", "c++", "javascript", "html", "css", "sql", "mysql",
    "sqlite", "flask", "django", "react", "node.js", "spring boot",
    "machine learning", "deep learning", "tensorflow", "pandas", "numpy",
    "power bi", "excel", "statistics", "rest api", "git", "docker",
    "figma", "adobe xd", "wireframing", "ui/ux", "communication",
    "project management", "data structures", "algorithms", "aws",
    "linux", "agile", "testing", "kubernetes"
]


def extract_text_from_pdf(filepath):
    """Read a PDF file from disk and return its plain text content."""
    text = ""
    try:
        reader = PdfReader(filepath)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"
    except Exception as e:
        text = ""
        print(f"[matcher] Could not parse PDF {filepath}: {e}")
    return text.strip()


def detect_skills(text):
    """Scan free text and return the subset of KNOWN_SKILLS found in it."""
    text_lower = text.lower()
    found = [skill for skill in KNOWN_SKILLS if skill in text_lower]
    return found


def compute_match_score(resume_skills, job_skills_csv):
    """
    Compare a list of resume skills against a job's required skills
    (comma-separated string) and return:
        score (0-100), matched_skills (list), missing_skills (list)
    """
    job_skills = [s.strip().lower() for s in job_skills_csv.split(",") if s.strip()]
    resume_skills_lower = [s.strip().lower() for s in resume_skills]

    if not job_skills:
        return 0.0, [], []

    matched = [s for s in job_skills if s in resume_skills_lower]
    missing = [s for s in job_skills if s not in resume_skills_lower]

    score = round((len(matched) / len(job_skills)) * 100, 1)
    return score, matched, missing
