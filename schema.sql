PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS skills (
    skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_abr TEXT NOT NULL UNIQUE,
    skill_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS job_postings (
    job_id INTEGER PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS job_skills (
    job_id INTEGER NOT NULL,
    skill_id INTEGER NOT NULL,
    PRIMARY KEY (job_id, skill_id),
    FOREIGN KEY (job_id) REFERENCES job_postings(job_id),
    FOREIGN KEY (skill_id) REFERENCES skills(skill_id)
);

CREATE TABLE IF NOT EXISTS salaries (
    salary_id INTEGER PRIMARY KEY,
    job_id INTEGER NOT NULL,
    max_salary REAL,
    med_salary REAL,
    min_salary REAL,
    pay_period TEXT,
    currency TEXT,
    compensation_type TEXT,
    FOREIGN KEY (job_id) REFERENCES job_postings(job_id)
);

CREATE TABLE IF NOT EXISTS radar_skills (
    radar_skill_id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS submissions (
    submission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    predicted_role TEXT NOT NULL,
    readiness_score REAL,
    tech_score REAL,
    label TEXT,
    ml_confidence REAL
);

CREATE TABLE IF NOT EXISTS submission_skills (
    submission_id INTEGER NOT NULL,
    radar_skill_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('matched', 'partial', 'missing')),
    PRIMARY KEY (submission_id, radar_skill_id),
    FOREIGN KEY (submission_id) REFERENCES submissions(submission_id),
    FOREIGN KEY (radar_skill_id) REFERENCES radar_skills(radar_skill_id)
);
