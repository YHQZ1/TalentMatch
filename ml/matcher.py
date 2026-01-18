import re
from datetime import datetime

from dateutil import parser as date_parser
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================
# SKILLS DATABASE
# =========================

SKILLS_DB = [
    "Python", "Java", "C++", "C", "C#", "JavaScript", "TypeScript", "Go",
    "Rust", "Swift", "Kotlin", "PHP", "Ruby", "Scala", "R", "Matlab",
    "Dart", "Lua", "Perl", "Shell", "Bash", "HTML", "CSS", "React",
    "Angular", "Vue", "Next.js", "Node.js", "Django", "Flask", "FastAPI",
    "Spring Boot", "ASP.NET", "Laravel", "Ruby on Rails", "Tailwind",
    "Bootstrap", "jQuery", "GraphQL", "REST API", "Machine Learning",
    "Deep Learning", "Data Science", "NLP", "Computer Vision",
    "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy",
    "Matplotlib", "Seaborn", "OpenCV", "Hugging Face", "LLM",
    "Generative AI", "NLTK", "Spacy", "Jupyter", "AWS", "Azure", "GCP",
    "Docker", "Kubernetes", "Terraform", "Ansible", "Jenkins", "Git",
    "GitHub", "GitLab", "CI/CD", "Linux", "Unix", "Nginx", "Apache",
    "Heroku", "Vercel", "Netlify", "SQL", "NoSQL", "MongoDB",
    "PostgreSQL", "MySQL", "Oracle", "Redis", "Cassandra",
    "Elasticsearch", "DynamoDB", "Firebase", "Snowflake", "Databricks",
    "Algorithms", "Data Structures", "System Design", "OOP",
    "Functional Programming", "Agile", "Scrum", "Jira", "Trello",
    "Unit Testing", "Selenium", "Postman", "Swagger",
]


# =========================
# SKILL EXTRACTION
# =========================

def extract_skills(text):
    found = set()
    text_lower = text.lower()

    for skill in SKILLS_DB:
        s = skill.lower()
        if len(s) <= 3:
            pattern = rf"(?:^|\s){re.escape(s)}(?:$|[\s,./])"
        else:
            pattern = rf"\b{re.escape(s)}\b"

        if re.search(pattern, text_lower):
            found.add(skill)

    return list(found)


# =========================
# DATE PARSING
# =========================

def parse_date(date_str):
    date_str = date_str.strip().lower()

    if date_str in {"present", "current", "now", "today", "till date"}:
        return datetime.now()

    if re.fullmatch(r"\d{4}", date_str):
        return datetime(int(date_str), 1, 1)

    try:
        return date_parser.parse(
            date_str,
            default=datetime(datetime.now().year, 1, 1)
        )
    except Exception:
        return None


# =========================
# EXPERIENCE PARSING (FIXED)
# =========================

EXPERIENCE_HEADERS = [
    "work experience",
    "professional experience",
    "experience",
    "employment",
    "employment history",
    "work history",
]

STOP_HEADERS = [
    "education",
    "projects",
    "skills",
    "certifications",
    "achievements",
    "leadership",
    "interests",
    "hobbies",
    "languages",
    "summary",
]

# Matches:
# 2018 - 2020
# 2022 - current
# Jan 2018 - May 2021
# 2018-current Euclid, OH
DATE_RANGE_REGEX = re.compile(
    r"""
    (?P<start>
        (?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\s*\d{4}
    )
    \s*[-–]\s*
    (?P<end>
        present|current|now|
        (?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)?\s*\d{4}
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)


def extract_experience(text):
    text_lower = text.lower()

    # 1️⃣ Find experience section (loose, PDF-safe)
    start_idx = None
    for header in EXPERIENCE_HEADERS:
        m = re.search(re.escape(header), text_lower)
        if m:
            start_idx = m.end()
            break

    if start_idx is None:
        return ["0 Years"]

    # 2️⃣ Cut off at next section
    end_idx = len(text_lower)
    for header in STOP_HEADERS:
        m = re.search(re.escape(header), text_lower[start_idx:])
        if m:
            end_idx = start_idx + m.start()
            break

    experience_text = text_lower[start_idx:end_idx]

    total_years = 0.0

    # 3️⃣ Extract ALL date ranges
    for match in DATE_RANGE_REGEX.finditer(experience_text):
        start = parse_date(match.group("start"))
        end = parse_date(match.group("end"))

        if not start or not end or end < start:
            continue

        total_years += (end - start).days / 365.25

    if total_years < 0.3:
        return ["0 Years"]

    return [f"{round(min(total_years, 40), 2)} Years"]


# =========================
# SIMILARITY
# =========================

def calculate_similarity(job_desc, resumes_texts):
    if not job_desc or not resumes_texts:
        return []

    docs = [job_desc] + resumes_texts
    tfidf = TfidfVectorizer(stop_words="english")
    mat = tfidf.fit_transform(docs)

    sims = cosine_similarity(mat[0:1], mat[1:])
    return sims[0].tolist()


# =========================
# COMPONENT SCORING
# =========================

def calculate_component_scores(
    job_desc,
    resumes_texts,
    job_desc_raw,
    resumes_raw,
    weights,
):
    if not job_desc or not resumes_texts:
        return []

    similarity_scores = calculate_similarity(job_desc, resumes_texts)
    jd_skills = set(extract_skills(job_desc_raw))
    results = []

    for i, resume_raw in enumerate(resumes_raw):
        resume_skills = set(extract_skills(resume_raw))

        skills_score = (
            len(jd_skills & resume_skills) / len(jd_skills)
            if jd_skills else min(1.0, len(resume_skills) / 20.0)
        )

        exp_years = 0.0
        for e in extract_experience(resume_raw):
            m = re.search(r"(\d+(?:\.\d+)?)", e)
            if m:
                exp_years = max(exp_years, float(m.group(1)))

        exp_score = min(1.0, exp_years / 10.0)

        text_lower = resume_raw.lower()
        edu_score = (
            1.0 if any(k in text_lower for k in ["master", "phd", "m.tech", "ms"])
            else 0.5 if any(k in text_lower for k in ["bachelor", "degree", "college"])
            else 0.3 if "education" in text_lower
            else 0.0
        )

        raw = (
            weights["skills"] * skills_score
            + weights["experience"] * exp_score
            + weights["education"] * edu_score
            + weights["relevance"] * similarity_scores[i]
        )

        final = raw / sum(weights.values())

        results.append({
            "final_score": round(final * 100, 2),
            "skills_score": round(skills_score * 100, 1),
            "exp_score": round(exp_score * 100, 1),
            "edu_score": round(edu_score * 100, 1),
            "relevance_score": round(similarity_scores[i] * 100, 1),
        })

    return results


# =========================
# ATS SCORE
# =========================

def calculate_ats_score(resume_text, job_keywords=None):
    if not resume_text:
        return 0.0

    text = resume_text.lower()
    wc = len(text.split())
    resume_skills = {s.lower() for s in extract_skills(resume_text)}

    if job_keywords:
        jd = {k.lower() for k in job_keywords}
        skill_score = len(resume_skills & jd) / max(1, len(jd))
    else:
        skill_score = min(1.0, len(resume_skills) / 8.0)

    section_score = sum(
        s in text
        for s in ["experience", "education", "skills", "projects", "summary"]
    ) / 5

    years = 0.0
    for e in extract_experience(resume_text):
        m = re.search(r"(\d+(?:\.\d+)?)", e)
        if m:
            years = max(years, float(m.group(1)))

    exp_score = (
        0.6 if years == 0 else
        0.7 if years <= 2 else
        0.85 if years <= 5 else
        1.0
    )

    parse_score = (
        0.3 if wc < 80 else
        0.6 if wc < 150 else
        0.85 if wc < 300 else
        1.0
    )

    final = (
        0.40 * skill_score
        + 0.20 * section_score
        + 0.15 * exp_score
        + 0.15 * parse_score
    )

    return round(min(1.0, final) * 100, 2)
