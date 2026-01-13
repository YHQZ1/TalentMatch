# TalentMatch 🎯
### Elevating Tech Recruitment with Data-Driven Intelligence

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B)
![Spacy](https://img.shields.io/badge/NLP-Spacy-09A3D5)

**TalentMatch** is an advanced, **NLP-driven CV Scanner** and ranking system designed specifically for the nuances of **Computer Science and Engineering** recruitment. 

Unlike generic keyword counters, TalentMatch uses a robust NLP pipeline to understand technical context, measure experience accurately, and allow recruiters to fine-tune ranking priorities based on the specific role (e.g., prioritizing "Skills" over "Education" for a Senior Dev role).

---

## 🚀 Key Features

### 🧠 Intelligent Parsing
- **Universal CS Role Support**: tuned for specific terminologies in Software Engineering, Data Science, Cybersecurity, DevOps, QA, and Research.
- **Section-Aware Extraction**: Smartly distinguishes between "Work Experience" and "Projects" or "Hobbies" to prevent false positives.
- **Natural Date Understanding**: Parses complex date formats ("Jan 2020 - Current", "2018-2022") and textual durations ("five years experience").

### ⚖️ Weighted Ranking Engine
- **Recruiter Control**: Interactive sliders (Ignore/Low/Medium/High/Critical) to adjust the weight of:
    - 🧠 **Skills Match**: Overlap with critical job keywords.
    - 📅 **Experience**: Total years of relevant professional history.
    - 🎓 **Education**: Academic background relevance.
    - 📝 **Content Similarity**: Semantic text similarity score.
- **Normalized Scoring**: A proprietary scoring algorithm ensures a balanced 0-100% match score regardless of weight configuration.

### 👁️ Instant Resume Preview
- **Interactive Results**: Click on any candidate in the ranking table to instantly render their original PDF resume within the application.
- **No Downloads Needed**: Screen candidates efficiently without cluttering your downloads folder.

### 📊 Visual Analytics
- **Interactive Charts**: Compare top candidates side-by-side using dynamic Plotly bar charts.
- **ATS Insights**: See estimated ATS visibility scores and median cohort performance.
- **CSV Export**: Download full detailed reports for offline analysis or sharing with hiring managers.

---

## 🛠️ Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/AaravKashyap12/TalentMatch.git
   cd TalentMatch
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Run the Application**
   ```bash
   streamlit run app.py
   ```

4. **Access the Dashboard**
   - Open your browser to `http://localhost:8501`

---

## 📂 Project Structure

- **`app.py`**: The main application entry point. Handles UI rendering, session state management, and interaction logic.
- **`matcher.py`**: The core intelligence engine. Contains algorithms for TF-IDF similarity, skill extraction, experience calculation, and weighted scoring.
- **`resume_parser.py`**: Utilities for extracting raw text from PDF files using `PyPDF2`.
- **`nlp_utils.py`**: Text preprocessing pipelines (cleaning, lemmatization, stopword removal).
- **`create_samples.py`**: A helper script to generate realistic dummy resumes for testing and demonstration purposes.

---

## 👨‍💻 Author

**Aarav**  
*Built with Python, Streamlit, and Passion for NLP.*

---

## 🛡️ License

This project is open-source and available under the MIT License.
