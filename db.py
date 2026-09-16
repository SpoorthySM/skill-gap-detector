import sqlite3

DB_PATH = "skillradar.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def save_submission(result):
    conn = get_connection()

    try:
        # 1. Save the main analysis
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
                result.get("ml_confidence")
            )
        )

        submission_id = cursor.lastrowid

        # 2. Collect all skills and their statuses
        skill_statuses = []

        for item in result["matched"]:
            skill_statuses.append((item["skill"], "matched"))

        for item in result["partial"]:
            skill_statuses.append((item["skill"], "partial"))

        for item in result["missing"]:
            skill_statuses.append((item["skill"], "missing"))

        # 3. Find the database ID for each SkillRadar skill
        skill_lookup = dict(
            conn.execute(
                "SELECT skill_name, radar_skill_id FROM radar_skills"
            ).fetchall()
        )

        # 4. Save each skill's status
        rows = []

        for skill_name, status in skill_statuses:
            radar_skill_id = skill_lookup.get(skill_name)

            if radar_skill_id is not None:
                rows.append(
                    (submission_id, radar_skill_id, status)
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
            rows
        )

        conn.commit()

        return submission_id

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()
def get_top_missing_skills(limit=10):
    conn = get_connection()

    rows = conn.execute(
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
        (limit,)
    ).fetchall()

    conn.close()
    return rows


def get_analysis_count_by_role():
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            predicted_role,
            COUNT(*) AS analysis_count
        FROM submissions
        GROUP BY predicted_role
        ORDER BY analysis_count DESC
        """
    ).fetchall()

    conn.close()
    return rows


def get_average_readiness_by_role():
    conn = get_connection()

    rows = conn.execute(
        """
        SELECT
            predicted_role,
            ROUND(AVG(readiness_score), 1) AS average_readiness
        FROM submissions
        GROUP BY predicted_role
        ORDER BY average_readiness DESC
        """
    ).fetchall()

    conn.close()
    return rows
