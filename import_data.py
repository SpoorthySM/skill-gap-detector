import os
import io
import sqlite3

import pandas as pd
import psycopg2

from data.job_roles import JOB_ROLES


DB_PATH = "skillradar.db"


def is_postgres():
    return bool(os.getenv("DATABASE_URL"))


def get_connection():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg2.connect(database_url)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def postgres_copy(conn, table, columns, rows):
    """
    Bulk insert rows into PostgreSQL using COPY.
    This is much faster than executemany() for large datasets.
    """
    buffer = io.StringIO()

    for row in rows:
        values = []

        for value in row:
            if value is None:
                values.append("\\N")
            else:
                value = str(value)
                value = value.replace("\\", "\\\\")
                value = value.replace("\t", "\\t")
                value = value.replace("\n", "\\n")
                values.append(value)

        buffer.write("\t".join(values) + "\n")

    buffer.seek(0)

    cursor = conn.cursor()

    cursor.copy_from(
        buffer,
        table,
        columns=columns,
        null="\\N"
    )

    cursor.close()


def import_skills(conn):
    skills = pd.read_csv("data/skills.csv")

    rows = list(
        skills[
            ["skill_abr", "skill_name"]
        ].itertuples(index=False, name=None)
    )

    if is_postgres():
        cursor = conn.cursor()

        # Empty the table so the import is deterministic.
        cursor.execute("TRUNCATE TABLE skills RESTART IDENTITY CASCADE")

        postgres_copy(
            conn,
            "skills",
            ["skill_abr", "skill_name"],
            rows
        )

    else:
        conn.execute("DELETE FROM skills")

        conn.executemany(
            """
            INSERT OR IGNORE INTO skills (
                skill_abr,
                skill_name
            )
            VALUES (?, ?)
            """,
            rows
        )

    print(f"Skills loaded: {len(rows)}")


def import_jobs(conn):
    jobs = pd.read_csv("data/job_skills.csv")

    job_ids = (
        jobs["job_id"]
        .drop_duplicates()
        .astype(int)
        .tolist()
    )

    if is_postgres():
        cursor = conn.cursor()

        cursor.execute(
            "TRUNCATE TABLE job_skills, job_postings CASCADE"
        )

        postgres_copy(
            conn,
            "job_postings",
            ["job_id"],
            [(job_id,) for job_id in job_ids]
        )

        cursor.execute(
            """
            SELECT skill_abr, skill_id
            FROM skills
            """
        )

        skill_lookup = dict(cursor.fetchall())

    else:
        conn.execute("DELETE FROM job_skills")
        conn.execute("DELETE FROM job_postings")

        conn.executemany(
            """
            INSERT OR IGNORE INTO job_postings (job_id)
            VALUES (?)
            """,
            [(job_id,) for job_id in job_ids]
        )

        skill_lookup = dict(
            conn.execute(
                """
                SELECT skill_abr, skill_id
                FROM skills
                """
            ).fetchall()
        )

    job_skill_rows = []

    for row in jobs.itertuples(index=False):
        skill_id = skill_lookup.get(row.skill_abr)

        if skill_id is not None:
            job_skill_rows.append(
                (int(row.job_id), skill_id)
            )

    if is_postgres():
        postgres_copy(
            conn,
            "job_skills",
            ["job_id", "skill_id"],
            job_skill_rows
        )

    else:
        conn.executemany(
            """
            INSERT OR IGNORE INTO job_skills (
                job_id,
                skill_id
            )
            VALUES (?, ?)
            """,
            job_skill_rows
        )

    print(f"Unique jobs loaded: {len(job_ids)}")
    print(
        f"Job-skill relationships loaded: "
        f"{len(job_skill_rows)}"
    )


def import_salaries(conn):
    salaries = pd.read_csv("data/salaries.csv")

    salary_job_ids = (
        salaries["job_id"]
        .drop_duplicates()
        .astype(int)
        .tolist()
    )

    if is_postgres():
        cursor = conn.cursor()

        # Salary jobs may include jobs not present in job_skills.
        # Add only the missing job IDs.
        cursor.execute(
            """
            INSERT INTO job_postings (job_id)
            SELECT job_id
            FROM unnest(%s::bigint[]) AS t(job_id)
            ON CONFLICT (job_id) DO NOTHING
            """,
            (salary_job_ids,)
        )

    else:
        conn.executemany(
            """
            INSERT OR IGNORE INTO job_postings (job_id)
            VALUES (?)
            """,
            [(job_id,) for job_id in salary_job_ids]
        )

    rows = [
        (
            int(row.salary_id),
            int(row.job_id),
            row.max_salary,
            row.med_salary,
            row.min_salary,
            row.pay_period,
            row.currency,
            row.compensation_type
        )
        for row in salaries.itertuples(index=False)
    ]

    if is_postgres():
        cursor = conn.cursor()

        cursor.execute("TRUNCATE TABLE salaries")

        postgres_copy(
            conn,
            "salaries",
            [
                "salary_id",
                "job_id",
                "max_salary",
                "med_salary",
                "min_salary",
                "pay_period",
                "currency",
                "compensation_type"
            ],
            rows
        )

    else:
        conn.execute("DELETE FROM salaries")

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

    rows = [
        (skill.lower().strip(),)
        for skill in skill_names
    ]

    if is_postgres():
        cursor = conn.cursor()

        cursor.execute(
            "TRUNCATE TABLE radar_skills RESTART IDENTITY CASCADE"
        )

        postgres_copy(
            conn,
            "radar_skills",
            ["skill_name"],
            rows
        )

    else:
        conn.execute("DELETE FROM radar_skills")

        conn.executemany(
            """
            INSERT OR IGNORE INTO radar_skills (skill_name)
            VALUES (?)
            """,
            rows
        )

    print(f"SkillRadar skills loaded: {len(rows)}")


def print_database_counts(conn):
    tables = [
        "skills",
        "job_postings",
        "job_skills",
        "salaries",
        "radar_skills",
    ]

    print("\nDatabase counts:")

    for table in tables:
        if is_postgres():
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT COUNT(*) FROM {table}"
            )
            count = cursor.fetchone()[0]
        else:
            count = conn.execute(
                f"SELECT COUNT(*) FROM {table}"
            ).fetchone()[0]

        print(f"{table}: {count}")


def main():
    if is_postgres():
        print("Using PostgreSQL database.")
    else:
        print("Using local SQLite database.")

    conn = get_connection()

    try:
        import_skills(conn)
        conn.commit()

        import_jobs(conn)
        conn.commit()

        import_salaries(conn)
        conn.commit()

        import_radar_skills(conn)
        conn.commit()

        print_database_counts(conn)

        print("\nImport completed successfully.")

    except Exception as e:
        conn.rollback()
        print("\nImport failed:")
        print(e)
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    main()