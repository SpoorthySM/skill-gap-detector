# SkillRadar — Skill Gap Intelligence System

🚀 **Live Demo**: https://skill-gap-detector-gp3o.onrender.com

> AI + ML powered placement readiness analyzer for students

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.0-black?style=flat-square&logo=flask)
![ML](https://img.shields.io/badge/ML-RandomForest-green?style=flat-square)
![Gemini](https://img.shields.io/badge/AI-Gemini-orange?style=flat-square&logo=google)
![PostgreSQL](https://img.shields.io/badge/Database-PostgreSQL-336791?style=flat-square&logo=postgresql)

---

## What is this?

SkillRadar is an AI/ML-powered placement readiness and skill-gap analysis system designed for students and early-career developers.

Enter your skills or upload your resume — SkillRadar compares your profile against technical roles and real job-market data to identify what you already know, what you're missing, and what you should learn next.

The system combines **machine learning, NLP, generative AI, SQL, and full-stack development** into an end-to-end web application.

---

## Features

- **Skill Gap Analysis** — Matched, missing, and partial skill detection against 10 tech roles
- **Readiness Score** — Weighted score (0–100%) with labels: Job Ready / Almost There / Needs Work / Early Stage
- **ML Role Prediction** — Random Forest model trained on 3,579 real LinkedIn job postings
- **Resume Upload** — PDF/TXT upload with AI-powered skill extraction via Google Gemini
- **Learning Roadmap** — Personalized links to real learning platforms with time estimates
- **AI Recommendations** — Gemini-generated personalized advice based on identified skill gaps
- **Role Comparison** — Compare your profile across all 10 job roles at once
- **Interactive Dashboard** — Radar chart + Donut chart visualizations
- **SQL-Powered Insights** — Analyze historical submissions, frequently missing skills, role distributions, and average readiness
- **PostgreSQL Integration** — Persistent production database for job-market data and analysis history

---

## Supported Roles

SkillRadar currently supports analysis for 10 technical and business-oriented roles:

1. Software Development Engineer
2. Data Scientist
3. Data Analyst
4. Machine Learning Engineer
5. Frontend Developer
6. Backend Developer
7. DevOps Engineer
8. Quantitative Analyst
9. Product Manager
10. Cybersecurity Analyst

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Flask |
| ML Model | Scikit-learn — Random Forest + TF-IDF |
| AI | Google Gemini |
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Charts | Chart.js |
| PDF Parsing | PyPDF2 |
| Data Processing | Pandas |
| Local Database | SQLite |
| Production Database | PostgreSQL |
| Database Hosting | Aiven |
| Application Hosting | Render |
| Training Data | LinkedIn Job Postings Dataset (3.3M rows) |

---

## ML Model

SkillRadar uses a machine learning pipeline to predict the most relevant technical role from a user's profile.

### Training Data

- **Dataset:** LinkedIn Job Postings Dataset (Kaggle) — 3.3M job postings
- **Tech job postings used for ML:** 3,579 curated postings
- **Features:** TF-IDF on job descriptions
- **TF-IDF configuration:** 500 features with unigram and bigram features
- **Model:** Random Forest
- **Number of trees:** 200
- **Class balancing:** Balanced class weights
- **Accuracy:** 78.35% on the held-out test set

The **3,579 postings** form the curated machine-learning dataset used for role prediction. The larger job-postings dataset is also used as the source for the project's relational job-market database.

### Model Comparison

Five classification models were evaluated on the same dataset:

| Model | Accuracy |
|-------|----------|
| **SVM** | **80.31%** |
| **Random Forest** | **78.35%** ← selected |
| Logistic Regression | 71.37% |
| Decision Tree | 71.37% |
| KNN | 70.11% |

![Model Comparison](model_comparison.png)

> Although SVM achieved the highest accuracy (80.31%), **Random Forest was selected for deployment** due to its faster inference time, native probability estimation via `predict_proba()` which powers the confidence scores in the dashboard, and feature-importance capabilities. The accuracy difference was considered alongside the requirements of a real-time web application.

---

## Skill Gap Scoring

SkillRadar calculates a readiness score based on matched and partially matched skills.

### Readiness Score

```text
Readiness Score =
((Matched Skills + 0.5 × Partial Skills) / Total Required Skills) × 100
```

The resulting score is classified as:

| Score | Classification |
|-------|----------------|
| 80–100 | Job Ready |
| 60–79 | Almost There |
| 40–59 | Needs Work |
| 0–39 | Early Stage |

A separate **technical score** is also calculated for the technical skills required by the selected role.

---

## SQL & Database Architecture

SkillRadar includes a relational database layer for storing job-market information and analysis history.

### Database Architecture

The application uses:

- **SQLite** for local development
- **PostgreSQL** for production
- **Aiven** for hosted PostgreSQL
- Parameterized SQL queries for database operations
- Primary and foreign-key relationships
- Many-to-many relationships for job-to-skill mappings
- SQL aggregation queries for dashboard insights

### Database Tables

| Table | Purpose |
|-------|---------|
| `skills` | Stores job-market skill categories |
| `job_postings` | Stores job posting IDs |
| `job_skills` | Many-to-many relationship between jobs and skills |
| `salaries` | Stores salary information associated with jobs |
| `radar_skills` | Stores SkillRadar's supported skill vocabulary |
| `submissions` | Stores user analysis submissions |
| `submission_skills` | Stores matched, partial, and missing skills for each submission |

### Production Database Scale

The production PostgreSQL database currently contains approximately:

| Data | Records |
|------|---------:|
| Skills | 35 |
| Job Postings | 127,349 |
| Job-Skill Relationships | 213,768 |
| Salary Records | 40,785 |
| SkillRadar Skills | 137 |

The **3,579 ML training postings** and the **127,349 relational job records** serve different purposes:

- **3,579 postings** — curated dataset used to train the role-prediction model
- **127,349 job records** — broader job-market data imported into the relational database

---

## SQL-Powered Insights

SkillRadar stores analysis submissions and uses SQL queries to generate aggregated insights.

The Insights dashboard provides:

- **Most Frequently Missing Skills**
- **Analyses by Role**
- **Average Readiness by Role**

The application uses relational queries involving operations such as:

```sql
JOIN
GROUP BY
COUNT()
AVG()
ORDER BY
LIMIT
```

These queries allow SkillRadar to turn stored analysis history into useful aggregate insights.

---

## Project Architecture

```text
                    ┌─────────────────────┐
                    │    User / Resume    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Flask Backend    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
       │ ML Pipeline │  │ Gemini API  │  │ SQL Layer   │
       │ TF-IDF + RF │  │ Skill       │  │ PostgreSQL  │
       │             │  │ Extraction  │  │ / SQLite    │
       └─────────────┘  └─────────────┘  └─────────────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │   SkillRadar UI     │
                    │ Scores + Insights   │
                    └─────────────────────┘
```

---

## Project Structure

```text
skill-gap-detector/
│
├── app.py                  # Flask application
├── analyzer.py             # Skill-gap analysis and scoring
├── ml_predictor.py         # ML role prediction
├── db.py                   # Database connection and SQL queries
├── init_db.py              # Local database initialization
├── import_data.py          # Job-market data importer
├── schema.sql              # Relational database schema
│
├── skill_gap_model.pkl     # Trained Random Forest model
├── tfidf_vectorizer.pkl    # TF-IDF vectorizer
│
├── templates/
│   └── index.html          # Frontend interface
│
├── static/
│   └── ...                 # CSS, JavaScript and assets
│
├── model_comparison.png    # ML model comparison
├── requirements.txt
└── README.md
```

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main SkillRadar application |
| `/api/analyze` | POST | Analyze skills/resume |
| `/api/roles` | GET | Get supported roles |
| `/api/insights` | GET | Get aggregated database insights |

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/SpoorthySM/skill-gap-detector.git
cd skill-gap-detector
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**macOS/Linux**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key
```

For PostgreSQL development/production:

```env
DATABASE_URL=your_postgresql_connection_string
```

Do **not** commit `.env` or database credentials to GitHub.

### 5. Initialize the database

For local SQLite development:

```bash
python init_db.py
```

Import the job-market data:

```bash
python import_data.py
```

### 6. Run the application

```bash
python app.py
```

Open:

```text
http://localhost:5000
```

---

## Production Architecture

The deployed application uses:

```text
User
  │
  ▼
Render
  │
  ├── Flask Application
  │      ├── ML Model
  │      ├── Gemini API
  │      └── SQL Queries
  │
  ▼
Aiven PostgreSQL
```

Render hosts the Flask application, while Aiven PostgreSQL provides persistent production database storage.

---

## ML Notebook

The model development and comparison process is documented in the project's ML notebook.

The notebook covers:

- Data preprocessing
- Role filtering
- TF-IDF feature extraction
- Train/test split
- Model training
- Model comparison
- Accuracy evaluation
- Random Forest selection
- Model and vectorizer serialization

---

## Why SkillRadar?

SkillRadar combines several components that are often implemented separately:

**Machine Learning**  
→ Predicts relevant technical roles from job-description data.

**NLP**  
→ Converts job descriptions into TF-IDF feature representations.

**Generative AI**  
→ Extracts skills from uploaded resumes and generates personalized recommendations.

**SQL & Data Engineering**  
→ Stores job-market data and analysis history in a relational database and enables analytical queries.

**Full-Stack Development**  
→ Connects the ML, AI, database, backend, and frontend layers into a deployable web application.

---

## Future Improvements

- Expand the number of supported roles
- Improve model performance with larger curated datasets
- Add user accounts and personalized analysis history
- Add more advanced job-market analytics
- Add skill trend analysis
- Improve recommendation ranking
- Add automated resume feedback

---

## Built By

**Spoorthy Sree M**

Final-year Computer Science Engineering student specializing in Data Science.

Interested in **Machine Learning, Data Science, AI, and building end-to-end intelligent systems.**

---

## License

This project is developed for educational and portfolio purposes.
