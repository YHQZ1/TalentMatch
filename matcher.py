import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# Specialized CS & Engineering Skills Database
SKILLS_DB = [
    # Languages
    "Python", "Java", "C++", "C", "C#", "JavaScript", "TypeScript", "Go", "Rust", "Swift", "Kotlin", "PHP", "Ruby", "Scala", "R", "Matlab", "Dart", "Lua", "Perl", "Shell", "Bash",
    
    # Web & Frameworks
    "HTML", "CSS", "React", "Angular", "Vue", "Next.js", "Node.js", "Django", "Flask", "FastAPI", "Spring Boot", "ASP.NET", "Laravel", "Ruby on Rails", "Tailwind", "Bootstrap", "jQuery", "GraphQL", "REST API",
    
    # Data Science & ML
    "Machine Learning", "Deep Learning", "Data Science", "NLP", "Computer Vision", "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Pandas", "NumPy", "Matplotlib", "Seaborn", "OpenCV", "Hugging Face", "LLM", "Generative AI", "NLTK", "Spacy", "Jupyter",
    
    # Cloud & DevOps
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform", "Ansible", "Jenkins", "Git", "GitHub", "GitLab", "CI/CD", "Linux", "Unix", "Nginx", "Apache", "Heroku", "Vercel", "Netlify",
    
    # Databases
    "SQL", "NoSQL", "MongoDB", "PostgreSQL", "MySQL", "Oracle", "Redis", "Cassandra", "Elasticsearch", "DynamoDB", "Firebase", "Snowflake", "Databricks",
    
    # CS Concepts & Tools
    "Algorithms", "Data Structures", "System Design", "OOP", "Functional Programming", "Agile", "Scrum", "Jira", "Trello", "Unit Testing", "Selenium", "Postman", "Swagger"
]

def extract_skills(text):
    found_skills = []
    text_lower = text.lower()
    for skill in SKILLS_DB:
        # Improved strict matching to avoid false positives (e.g. "C" in "Center")
        if len(skill) <= 3:
             pattern = r'(?:^|\s)' + re.escape(skill.lower()) + r'(?:$|[\s,.])'
        else:
             pattern = r'\b' + re.escape(skill.lower()) + r'\b'
             
        if re.search(pattern, text_lower):
            found_skills.append(skill)
    return list(set(found_skills))

import spacy
from datetime import datetime
from dateutil import parser as date_parser

try:
    nlp = spacy.load("en_core_web_sm")
except ImportError:
    import en_core_web_sm
    nlp = en_core_web_sm.load()
except:
    nlp = None # Fallback

def parse_date(date_str):
    """
    Parse a date string into a datetime object. 
    Handles 'Present', 'Current', 'Now' as today.
    Handles 'YYYY', 'Mon YYYY', 'Month YYYY', 'MM/YYYY'.
    """
    date_str = date_str.strip().lower()
    if date_str in ['present', 'current', 'now', 'date', 'till date', 'today']:
        return datetime.now()
    
    # Try parsing YYYY specifically
    if re.match(r'^\d{4}$', date_str):
        try:
            return datetime(int(date_str), 1, 1) # Assume start of year
        except:
             pass
    
    try:
        # Use dateutil for flexible parsing
        # default to 1st of Jan if month missing, or 1st of month if day missing
        return date_parser.parse(date_str, default=datetime(datetime.now().year, 1, 1))
    except:
        return None

def calculate_duration_in_years(start_str, end_str):
    """Calculate the difference between two dates in years."""
    start_date = parse_date(start_str)
    end_date = parse_date(end_str)
    
    if start_date and end_date:
        if end_date < start_date:
             return 0.0 # Invalid range
        
        diff = end_date - start_date
        years = diff.days / 365.25
        return round(years, 2)
    return 0.0

import re
from datetime import datetime

# ================= EXPERIENCE EXTRACTION (FIXED) =================

EXPERIENCE_HEADERS = [
    "work experience",
    "professional experience",
    "experience",
    "employment",
    "employment history",
    "work history"
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
    "summary"
]

def extract_experience(text):
    """
    STRICT experience extraction:
    ✅ Counts experience ONLY inside Work / Experience section
    ❌ Ignores education, projects, leadership, internships unless explicitly under experience
    ❌ Prevents student resumes from getting fake years
    """

    text_lower = text.lower()

    # 1️⃣ Locate experience section
    start_idx = None
    for header in EXPERIENCE_HEADERS:
        pattern = rf"(?:^|\n)\s*{re.escape(header)}\s*(?:\:)?\s*(?:\n|$)"
        match = re.search(pattern, text_lower)
        if match:
            start_idx = match.end()
            break

    # ❗ NO EXPERIENCE SECTION → ZERO EXPERIENCE
    if start_idx is None:
        return ["0 Years"]

    # 2️⃣ Determine where experience section ends
    end_idx = len(text_lower)
    for header in STOP_HEADERS:
        pattern = rf"(?:^|\n)\s*{re.escape(header)}\s*(?:\:)?\s*(?:\n|$)"
        match = re.search(pattern, text_lower[start_idx:])
        if match:
            end_idx = start_idx + match.start()
            break

    experience_text = text_lower[start_idx:end_idx]

    # 3️⃣ Extract date ranges ONLY from experience section
    date_pattern = re.findall(
        r"(19\d{2}|20\d{2})\s*[-–]\s*(present|current|19\d{2}|20\d{2})",
        experience_text
    )

    total_years = 0.0
    current_year = datetime.now().year

    for start, end in date_pattern:
        start_year = int(start)
        end_year = current_year if end in ["present", "current"] else int(end)

        if end_year >= start_year:
            total_years += (end_year - start_year)

    # 4️⃣ Safety caps
    if total_years < 0.5:
        return ["0 Years"]

    total_years = min(total_years, 40)  # Hard cap

    return [f"{round(total_years, 1)} Years"]


def calculate_similarity(job_desc, resumes_texts):
    if not resumes_texts or not job_desc:
        return []

    documents = [job_desc] + resumes_texts
    
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    
    similarity_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])
    
    return similarity_matrix[0].tolist()


def calculate_component_scores(job_desc, resumes_texts, job_desc_raw, resumes_raw, weights):
    """
    Calculate weighted scores.
    Args:
        job_desc: Cleaned JD text (for TF-IDF)
        resumes_texts: List of Cleaned Resume texts (for TF-IDF)
        job_desc_raw: Raw JD text (for Skill extraction)
        resumes_raw: List of Raw Resume texts (for Skill/Experience extraction)
        weights: Dictionary of weights
    """
    if not resumes_texts or not job_desc:
        return []

    # 1. Similarity Scores (Context/Projects relevance) - Uses CLEANED text
    similarity_scores = calculate_similarity(job_desc, resumes_texts)
    
    # 2. Extract JD Skills - Uses RAW text (preserves C++, C#, etc.)
    jd_skills = set(extract_skills(job_desc_raw))
    
    results = []
    
    for i, text_raw in enumerate(resumes_raw):
        # text_raw is the raw string with newlines
        
        # Skills Score (Use Raw)
        resume_skills = set(extract_skills(text_raw))
        if jd_skills:
            # Overlap score
            skills_score = len(jd_skills.intersection(resume_skills)) / len(jd_skills)
        else:
            skills_score = len(resume_skills) / 20.0 # Fallback normalized
        skills_score = min(1.0, skills_score)
        
        # Experience Score (Use Raw - essential for regex/newlines)
        exp_list = extract_experience(text_raw)
        max_exp = 0.0
        for e in exp_list:
             m = re.search(r"(\d+(?:\.\d+)?)", e)
             if m:
                 try:
                     val = float(m.group(1))
                     if val > max_exp: max_exp = val
                 except: pass
        
        # Normalize: Assume 10 years is 'max' (1.0)
        exp_score = min(1.0, max_exp / 10.0)
        
        # Education Score (Use Raw or Lower Raw)
        edu_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college', 'b.tech', 'm.tech', 'bs', 'ms']
        edu_score = 0.0
        text_lower = text_raw.lower()
        if any(kw in text_lower for kw in edu_keywords):
            edu_score = 0.5 # Has some education mention
            # Boost for higher degrees
            if any(kw in text_lower for kw in ['master', 'phd', 'm.tech', 'ms']):
                edu_score = 1.0
        elif 'education' in text_lower:
             edu_score = 0.3 # Section exists
             
        # Combined Weighted Score
        raw_final_score = (
            weights['skills'] * skills_score +
            weights['experience'] * exp_score +
            weights['education'] * edu_score +
            weights['relevance'] * similarity_scores[i]
        )
        
        # Normalize by sum of weights to ensure 0-100% range
        total_weight = sum(weights.values())
        if total_weight > 0:
            final_score = raw_final_score / total_weight
        else:
            final_score = 0.0
        
        # Scale to 0-100
        results.append({
            'final_score': round(final_score * 100, 2),
            'skills_score': round(skills_score * 100, 1),
            'exp_score': round(exp_score * 100, 1),
            'edu_score': round(edu_score * 100, 1),
            'relevance_score': round(similarity_scores[i] * 100, 1)
        })
        
    return results

def calculate_ats_score(resume_text, jd_text=None):
    """
    ATS Quality Score (0–100)
    Independent of JD Match %
    Mimics real ATS resume scanners
    """

    if not resume_text or len(resume_text.strip()) < 100:
        return 0.0

    text = resume_text.lower()
    wc = len(text.split())

    # ---------------------------------
    # 1️⃣ Resume Structure (25%)
    # ---------------------------------
    sections = [
        "experience", "education", "skills",
        "projects", "certifications", "summary"
    ]
    present_sections = sum(1 for s in sections if s in text)
    structure_score = present_sections / len(sections)

    # ---------------------------------
    # 2️⃣ Skill Presence (30%)
    # ---------------------------------
    resume_keywords, resume_categories = extract_skills_and_keywords(resume_text)

    total_skills = sum(len(v) for v in resume_categories.values())

    if total_skills == 0:
        skill_score = 0.1
    elif total_skills < 5:
        skill_score = 0.4
    elif total_skills < 12:
        skill_score = 0.7
    else:
        skill_score = 1.0

    # ---------------------------------
    # 3️⃣ Experience Realism (20%)
    # ---------------------------------
    experience_text = analyze_experience(resume_text)
    years = 0

    if experience_text:
        m = re.search(r'(\d+)', experience_text)
        if m:
            years = int(m.group(1))

    if years == 0:
        experience_score = 0.4      # fresher-friendly
    elif years <= 2:
        experience_score = 0.6
    elif years <= 5:
        experience_score = 0.85
    else:
        experience_score = 1.0

    # ---------------------------------
    # 4️⃣ Education Relevance (15%)
    # ---------------------------------
    education = analyze_education(resume_text)

    if not education:
        edu_score = 0.2
    elif any(x in education.lower() for x in [
        'computer science', 'information technology',
        'software', 'engineering', 'data science'
    ]):
        edu_score = 1.0
    else:
        edu_score = 0.6

    # ---------------------------------
    # 5️⃣ Parseability & Length (10%)
    # ---------------------------------
    if wc < 80:
        parse_score = 0.2
    elif wc < 150:
        parse_score = 0.5
    elif wc < 300:
        parse_score = 0.8
    else:
        parse_score = 1.0

    # ---------------------------------
    # 🚫 Penalties (up to -20%)
    # ---------------------------------
    penalty = 0.0

    # Keyword stuffing
    if total_skills > 45:
        penalty += 0.1

    # Very short / image-based resume
    if wc < 60:
        penalty += 0.1

    penalty = min(0.2, penalty)

    # ---------------------------------
    # 🎯 Final ATS Score
    # ---------------------------------
    final_score = (
        0.30 * skill_score +
        0.25 * structure_score +
        0.20 * experience_score +
        0.15 * edu_score +
        0.10 * parse_score
    )

    final_score = max(0.0, min(1.0, final_score - penalty))
    return round(final_score * 100, 1)

