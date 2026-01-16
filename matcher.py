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

def calculate_ats_score(resume_text, job_keywords=None):
    """Estimate an ATS compatibility score (0-100) for a resume.

    Components:
    - keyword_score (50%): fraction of job keywords found in resume skills
    - section_score (20%): presence of standard sections (Experience, Education, Skills, Contact)
    - parseability_score (20%): based on length of extracted text (proxy for successful OCR/parsing)
    - experience_score (10%): presence of years of experience and magnitude
    - formatting_penalty (subtract up to 10 points): short resumes or likely images-only PDFs

    Returns:
        float: ATS score between 0 and 100 (clipped)
    """
    if not resume_text or not isinstance(resume_text, str):
        return 0.0

    text = resume_text.lower()
    words = text.split()

    # Keyword score
    if job_keywords:
        try:
            jd_kw = set(k.lower() for k in job_keywords)
        except Exception:
            jd_kw = set()
    else:
        jd_kw = set()

    resume_skills = set(s.lower() for s in extract_skills(resume_text))
    if jd_kw:
        common = jd_kw.intersection(resume_skills)
        keyword_score = len(common) / max(1, len(jd_kw))
    else:
        # No job keywords provided -> fallback to fraction of recognized skills found (capped)
        keyword_score = min(1.0, len(resume_skills) / 6.0)

    # Section score
    sections = ['experience', 'education', 'skills', 'contact', 'projects']
    present = sum(1 for sec in sections if sec in text)
    section_score = present / len(sections)

    # Parseability score (proxy: word count)
    wc = len(words)
    parseability_score = min(1.0, wc / 400.0)  # 400+ words is considered fully parseable

    # Experience score: scaled from extracted experience years
    exp_list = extract_experience(resume_text)
    max_years = 0.0
    for e in exp_list:
        # clean digits from match like '5+' or '5-7' or 'five'
        m = re.search(r"(\d+(?:\.\d+)?)", e)
        if m:
            try:
                v = float(m.group(1))
                if v > max_years:
                    max_years = v
            except Exception:
                continue
    experience_score = min(1.0, max_years / 10.0)  # 10+ years -> full score

    # Formatting penalty: short text or few lines -> penalize
    penalty = 0.0
    if wc < 150:
        penalty += 0.05  # small penalty
    if wc < 50:
        penalty += 0.1   # larger penalty for extremely short / likely image PDF

    # Combine with weights
    raw_score = (
        0.5 * keyword_score +
        0.2 * section_score +
        0.2 * parseability_score +
        0.1 * experience_score
    )

    # Convert to 0-100 and subtract penalty (scaled to 0-10 points)
    score = raw_score * 100 - (penalty * 100)
    score = max(0.0, min(100.0, round(score, 2)))

    return score

