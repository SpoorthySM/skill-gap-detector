import sqlite3
import pandas as pd
from data.job_roles import JOB_ROLES

DB_PATH = "skillradar.db"


def import_skills(conn):
    skills = pd.read_csv("data/skills.csv")

    rows = list(
        skills[["skill_abr", "skill_name"]].itertuples(index=False, name=None)
    )

    conn.executemany(
        """
        INSERT OR IGNORE INTO skills (skill_abr, skill_name)
        VALUES (?, ?)
        """,
        rows
    )

    print(f"Skills loaded: {len(rows)}")


def import_jobs(conn):
    jobs = pd.read_csv("data/job_skills.csv")

    # Get all unique job IDs.
    job_ids = jobs["job_id"].drop_duplicates().tolist()

    conn.executemany(
        """
        INSERT OR IGNORE INTO job_postings (job_id)
        VALUES (?)
        """,
        [(job_id,) for job_id in job_ids]
    )

    # Build a lookup:
    # skill abbreviation -> database skill_id
    skill_lookup = dict(
        conn.execute(
            "SELECT skill_abr, skill_id FROM skills"
        ).fetchall()
    )

    job_skill_rows = []

    for row in jobs.itertuples(index=False):
        skill_id = skill_lookup.get(row.skill_abr)

        if skill_id is not None:
            job_skill_rows.append((row.job_id, skill_id))

    conn.executemany(
        """
        INSERT OR IGNORE INTO job_skills (job_id, skill_id)
        VALUES (?, ?)
        """,
        job_skill_rows
    )

    print(f"Unique jobs loaded: {len(job_ids)}")
    print(f"Job-skill relationships loaded: {len(job_skill_rows)}")


def import_salaries(conn):
    salaries = pd.read_csv("data/salaries.csv")

    # Some salary records belong to jobs that were not
    # present in job_skills.csv. Add those jobs first.
    salary_job_ids = salaries["job_id"].drop_duplicates().tolist()

    conn.executemany(
        """
        INSERT OR IGNORE INTO job_postings (job_id)
        VALUES (?)
        """,
        [(job_id,) for job_id in salary_job_ids]
    )

    rows = [
        (
            row.salary_id,
            row.job_id,
            row.max_salary,
            row.med_salary,
            row.min_salary,
            row.pay_period,
            row.currency,
            row.compensation_type
        )
        for row in salaries.itertuples(index=False)
    ]

    conn.executemany(
        """
        INSERT OR IGNORE INTO salaries (
            salary_id,
            job_id,
            max_salary,
            med_salary,
            min_salary,
            pay_period,
            currency,
            compensation_type
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows
    )

    print(f"Salary records loaded: {len(rows)}")
def import_radar_skills(conn):
    skill_names = set()

    for role_data in JOB_ROLES.values():
        skill_names.update(role_data["technical"])
        skill_names.update(role_data["soft"])
        skill_names.update(role_data["tools"])

    rows = [(skill.lower().strip(),) for skill in skill_names]

    conn.executemany(
        """
        INSERT OR IGNORE INTO radar_skills (skill_name)
        VALUES (?)
        """,
        rows
    )

    print(f"SkillRadar skills loaded: {len(rows)}")

def main():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    import_skills(conn)
    import_jobs(conn)
    import_salaries(conn)
    import_radar_skills(conn)

    conn.commit()
    print("\nDatabase counts:")

    print(
        "skills:",
        conn.execute("SELECT COUNT(*) FROM skills").fetchone()[0]
    )

    print(
        "job_postings:",
        conn.execute("SELECT COUNT(*) FROM job_postings").fetchone()[0]
    )

    print(
        "job_skills:",
        conn.execute("SELECT COUNT(*) FROM job_skills").fetchone()[0]
    )

    print(
       "salaries:",
        conn.execute("SELECT COUNT(*) FROM salaries").fetchone()[0]
    )

    conn.close()


if __name__ == "__main__":
    main()
