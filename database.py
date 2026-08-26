import sqlite3
from pathlib import Path

DB_PATH = Path("data/applications.db")

def create_database():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT NOT NULL,
            location TEXT,
            application_date TEXT,
            job_link TEXT,
            status TEXT,
            interview_date TEXT,
            notes TEXT
        )
    """)

    cursor.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS unique_application
        ON applications(company, role, application_date)
    """)

    conn.commit()
    conn.close()



def add_application(
    company,
    role,
    location,
    application_date,
    job_link,
    status,
    interview_date,
    notes
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO applications (
            company,
            role,
            location,
            application_date,
            job_link,
            status,
            interview_date,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        company,
        role,
        location,
        application_date,
        job_link,
        status,
        interview_date,
        notes
    ))

    conn.commit()
    conn.close()


def get_applications():
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM applications
        ORDER BY id DESC
    """)

    applications = cursor.fetchall()

    conn.close()

    return applications

def get_application_stats():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM applications")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'Applied'")
    applied = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'Interview'")
    interviews = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'Offer'")
    offers = cursor.fetchone()[0]

    conn.close()

    return total, applied, interviews, offers

def get_status_counts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT status, COUNT(*)
        FROM applications
        GROUP BY status
    """)

    results = cursor.fetchall()

    conn.close()

    return results

def update_application(
    app_id,
    company,
    role,
    location,
    application_date,
    job_link,
    status,
    interview_date,
    notes
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE applications
        SET company = ?,
            role = ?,
            location = ?,
            application_date = ?,
            job_link = ?,
            status = ?,
            interview_date = ?,
            notes = ?
        WHERE id = ?
    """, (
        company,
        role,
        location,
        application_date,
        job_link,
        status,
        interview_date,
        notes,
        app_id
    ))

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_database()
    print("Database created successfully!")


def delete_application(app_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE id = ?",
        (app_id,)
    )

    conn.commit()
    conn.close()

    def get_dashboard_metrics():
     conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM applications")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Interview'"
    )
    interviews = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Offer'"
    )
    offers = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Rejected'"
    )
    rejected = cursor.fetchone()[0]

    conn.close()

    interview_rate = (
        (interviews / total) * 100
        if total > 0
        else 0
    )

    success_rate = (
        (offers / total) * 100
        if total > 0
        else 0
    )

    return (
        total,
        interviews,
        offers,
        rejected,
        interview_rate,
        success_rate
    )


def get_dashboard_metrics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM applications")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Interview'"
    )
    interviews = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Offer'"
    )
    offers = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM applications WHERE status = 'Rejected'"
    )
    rejected = cursor.fetchone()[0]

    conn.close()

    interview_rate = (
        (interviews / total) * 100
        if total > 0
        else 0
    )

    success_rate = (
        (offers / total) * 100
        if total > 0
        else 0
    )

    return (
        total,
        interviews,
        offers,
        rejected,
        interview_rate,
        success_rate
    )