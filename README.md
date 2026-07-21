# 🤖 AI Resume Screening System

An AI-powered Resume Screening and ATS Analysis platform that automatically analyzes resumes against job descriptions, calculates match scores, identifies skill gaps, and provides actionable recommendations.

Built using **Python, Streamlit, NLP, and Machine Learning**.

---

## 🚀 Project Overview

Recruiters often spend a lot of time manually reviewing resumes. This project helps automate the initial screening process by comparing candidate resumes with job descriptions.

The system extracts resume information, analyzes required skills, calculates ATS compatibility, and highlights matching and missing skills.

---

## ✨ Features

### 📄 Resume Parsing
- Upload resume in PDF format
- Extract candidate information automatically
- Process resume text using NLP techniques

### 📊 ATS Resume Matching
- Compare resume content with job description
- Calculate resume-job compatibility score
- Evaluate candidate suitability

### 🎯 Skill Analysis
- Identify matched skills
- Detect missing skills
- Provide improvement suggestions

### 📈 AI Screening Dashboard
- Interactive Streamlit interface
- Resume analysis dashboard
- Easy-to-understand results visualization

### 📥 Report Generation
- Download ATS analysis report
- Save screening results for future reference

---

# 🏗️ System Architecture

## 📂 Project Structure

```text
AI-Resume-Screening-System/

│
├── main.py                 # Streamlit application
│
├── config.py               # Configuration settings
│
├── requirements.txt        # Required libraries
│
├── README.md               # Documentation
│
└── .gitignore              # Ignored files

```

---

# ⚙️ Installation & Setup

## 1. Clone Repository

```bash
git clone https://github.com/aravindsai2202/ai-resume-screening-system.git
```

---

## 2. Navigate to Project

```bash
cd ai-resume-screening-system
```

---

## 3. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Run Application

```bash
streamlit run main.py
```

Application will open in your browser:

```text
http://localhost:8501
```

---

# 📸 Application Workflow

### Step 1:
Upload candidate resume PDF

### Step 2:
Paste job description

### Step 3:

Click:

```text
🚀 Analyze Resume
```

### Step 4:

View:

- ✅ ATS Score
- ✅ Matched Skills
- ✅ Missing Skills
- ✅ Resume Analysis

---

# 📊 Example Analysis

## Input:

```text
Resume:
Python, SQL, Machine Learning, AWS

Job Description:
Python, SQL, AI, Cloud
```

## Output:

```text
ATS Score: 78%

Matched Skills:
✓ Python
✓ SQL

Missing Skills:
✗ Cloud
```

---

# 🔮 Future Improvements

Planned upgrades:

- Sentence Transformer based semantic matching
- LLM powered resume feedback
- AI generated improvement suggestions
- Resume ranking system
- Multiple resume comparison
- Recruiter dashboard
- Cloud deployment

---

# 🎯 Use Cases

- Resume screening automation
- Recruitment assistance
- Career guidance platforms
- ATS optimization
- HR automation

---

# 👨‍💻 Author

**Venkata Aravind Sai Thanneru**

B.Tech Electronics and Communication Engineering (2025)

AI/ML Engineer | Generative AI Enthusiast

GitHub:

https://github.com/aravindsai2202

LinkedIn:

https://www.linkedin.com/
