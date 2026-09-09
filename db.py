import sqlite3
import pandas as pd
from data.job_roles import JOB_ROLES

def init_db():
    """Load JOB_ROLES into SQLite for querying."""
    conn = sqlite3.connect(":memory:")
    
    rows = []
    for role, data in JOB_ROLES.items():
        for skill in data["technical"]:
            rows.append({"role": role, "skill": skill, "type": "technical"})
        for skill in data["tools"]:
            rows.append({"role": role, "skill": skill, "type": "tool"})
    
    df = pd.DataFrame(rows)
    df.to_sql("role_skills", conn, if_exists="replace", index=False)
    return conn

def get_top_skills_for_role(conn, role, limit=10):
    return pd.read_sql("""
        SELECT skill, type 
        FROM role_skills 
        WHERE role = ? AND type = 'technical'
        LIMIT ?
    """, conn, params=[role, limit])

def get_roles_requiring_skill(conn, skill):
    return pd.read_sql("""
        SELECT DISTINCT role 
        FROM role_skills 
        WHERE LOWER(skill) = LOWER(?)
    """, conn, params=[skill])

def get_skill_count_by_role(conn):
    return pd.read_sql("""
        SELECT role, COUNT(*) as skill_count
        FROM role_skills
        WHERE type = 'technical'
        GROUP BY role
        ORDER BY skill_count DESC
    """, conn)
