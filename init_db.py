import sqlite3

DB_PATH = "skillradar.db"
SCHEMA_PATH = "schema.sql"


def init_db():
    conn = sqlite3.connect(DB_PATH)

    # Enable foreign-key enforcement
    conn.execute("PRAGMA foreign_keys = ON")

    with open(SCHEMA_PATH, "r") as f:
        schema_sql = f.read()

    conn.executescript(schema_sql)
    conn.commit()
    conn.close()

    print(f"Database initialized at {DB_PATH}")


def show_tables():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name;
    """)

    tables = cursor.fetchall()

    print("\nTables:")
    for table in tables:
        print(" -", table[0])

    conn.close()


if __name__ == "__main__":
    init_db()
    show_tables()
