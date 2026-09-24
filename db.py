import os
import sqlite3

import psycopg2


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


def save_submission(result):
    conn = get_connection()

    try:
        if is_postgres():
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO submissions (
                    predicted_role,
                    readiness_score,
                    tech_score,
                    label,
                    ml_confidence
                )
                VALUES (%s, %s, %s, %s, %s)
                RETURNING submission_id
                """,
                (
                    result["job_role"],
                    result["readiness_score"],
                    result["tech_score"],
                    result["label"],
                    result.get("ml_confidence"),
                ),
            )

            submission_id = cursor.fetchone()[0]

            cursor.execute(
                "SELECT skill_name, radar_skill_id FROM radar_skills"
            )

            skill_lookup = dict(cursor.fetchall())

            rows = _build_submission_skill_rows(
                result,
                submission_id,
                skill_lookup
            )

            cursor.executemany(
                """
                INSERT INTO submission_skills (
                    submission_id,
                    radar_skill_id,
                    status
                )
                VALUES (%s, %s, %s)
                """,
                rows,
            )

        else:
            cursor = conn.execute(
                """
                INSERT INTO submissions (
                    predicted_role,
                    readiness_score,
                    tech_score,
                    label,
                    ml_confidence
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    result["job_role"],
                    result["readiness_score"],
                    result["tech_score"],
                    result["label"],
                    result.get("ml_confidence"),
                ),
            )

            submission_id = cursor.lastrowid

            skill_lookup = dict(
                conn.execute(
                    "SELECT skill_name, radar_skill_id FROM radar_skills"
                ).fetchall()
            )

            rows = _build_submission_skill_rows(
                result,
                submission_id,
                skill_lookup
            )

            conn.executemany(
                """
                INSERT INTO submission_skills (
                    submission_id,
                    radar_skill_id,
                    status
                )
                VALUES (?, ?, ?)
                """,
                rows,
            )

        conn.commit()
        return submission_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()


def _build_submission_skill_rows(result, submission_id, skill_lookup):
    rows = []

    for item in result["matched"]:
        radar_skill_id = skill_lookup.get(item["skill"])

        if radar_skill_id is not None:
            rows.append(
                (submission_id, radar_skill_id, "matched")
            )

    for item in result["partial"]:
        radar_skill_id = skill_lookup.get(item["skill"])

        if radar_skill_id is not None:
            rows.append(
                (submission_id, radar_skill_id, "partial")
            )

    for item in result["missing"]:
        radar_skill_id = skill_lookup.get(item["skill"])

        if radar_skill_id is not None:
            rows.append(
                (submission_id, radar_skill_id, "missing")
            )

    return rows


def get_top_missing_skills(limit=10):
    conn = get_connection()

    try:
        if is_postgres():
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    rs.skill_name,
                    COUNT(*) AS missing_count
                FROM submission_skills ss
                JOIN radar_skills rs
                    ON ss.radar_skill_id = rs.radar_skill_id
                WHERE ss.status = 'missing'
                GROUP BY rs.radar_skill_id, rs.skill_name
                ORDER BY missing_count DESC
                LIMIT %s
                """,
                (limit,),
            )

            return cursor.fetchall()

        return conn.execute(
            """
            SELECT
                rs.skill_name,
                COUNT(*) AS missing_count
            FROM submission_skills ss
            JOIN radar_skills rs
                ON ss.radar_skill_id = rs.radar_skill_id
            WHERE ss.status = 'missing'
            GROUP BY rs.radar_skill_id, rs.skill_name
            ORDER BY missing_count DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    finally:
        conn.close()


def get_analysis_count_by_role():
    conn = get_connection()

    try:
        if is_postgres():
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    predicted_role,
                    COUNT(*) AS analysis_count
                FROM submissions
                GROUP BY predicted_role
                ORDER BY analysis_count DESC
                """
            )

            return cursor.fetchall()

        return conn.execute(
            """
            SELECT
                predicted_role,
                COUNT(*) AS analysis_count
            FROM submissions
            GROUP BY predicted_role
            ORDER BY analysis_count DESC
            """
        ).fetchall()

    finally:
        conn.close()


def get_average_readiness_by_role():
    conn = get_connection()

    try:
        if is_postgres():
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT
                    predicted_role,
                    ROUND(AVG(readiness_score)::numeric, 1)
                        AS average_readiness
                FROM submissions
                GROUP BY predicted_role
                ORDER BY average_readiness DESC
                """
            )

            return cursor.fetchall()

        return conn.execute(
            """
            SELECT
                predicted_role,
                ROUND(AVG(readiness_score), 1) AS average_readiness
            FROM submissions
            GROUP BY predicted_role
            ORDER BY average_readiness DESC
            """
        ).fetchall()

    finally:
        conn.close()