import sqlite3
from datetime import datetime
from pathlib import Path


# -----------------------------------------
# Database Configuration
# -----------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)

DB_PATH = DATA_DIR / "grievances.db"


# -----------------------------------------
# Database Connection
# -----------------------------------------

def get_connection():
    """Create and return a database connection."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# -----------------------------------------
# Initialize Database
# -----------------------------------------

def initialize_database():
    """Create the grievances table if it does not exist."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS grievances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            citizen_name TEXT NOT NULL,
            contact TEXT,

            title TEXT NOT NULL,
            description TEXT NOT NULL,

            category TEXT DEFAULT 'Other',
            priority TEXT DEFAULT 'Medium',
            severity TEXT DEFAULT 'Medium',

            location TEXT,

            status TEXT DEFAULT 'Pending',

            ai_summary TEXT,
            ai_reason TEXT,

            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


# -----------------------------------------
# Add Grievance
# -----------------------------------------

def add_grievance(
    citizen_name,
    contact,
    title,
    description,
    location,
    category="Other",
    priority="Medium",
    severity="Medium",
    ai_summary="",
    ai_reason=""
):
    """Store a new grievance in the database."""

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO grievances (
            citizen_name,
            contact,
            title,
            description,
            category,
            priority,
            severity,
            location,
            status,
            ai_summary,
            ai_reason,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        citizen_name,
        contact,
        title,
        description,
        category,
        priority,
        severity,
        location,
        "Pending",
        ai_summary,
        ai_reason,
        current_time,
        current_time
    ))

    grievance_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return grievance_id


# -----------------------------------------
# Get All Grievances
# -----------------------------------------

def get_all_grievances():
    """Return all grievances, newest first."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM grievances
        ORDER BY id DESC
    """)

    grievances = cursor.fetchall()

    connection.close()

    return grievances


# -----------------------------------------
# Get Single Grievance
# -----------------------------------------

def get_grievance(grievance_id):
    """Return one grievance using its ID."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM grievances
        WHERE id = ?
    """, (grievance_id,))

    grievance = cursor.fetchone()

    connection.close()

    return grievance


# -----------------------------------------
# Update Status
# -----------------------------------------

def update_status(grievance_id, new_status):
    """Update the current status of a grievance."""

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE grievances
        SET status = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        new_status,
        current_time,
        grievance_id
    ))

    connection.commit()
    connection.close()


# -----------------------------------------
# Update AI Analysis
# -----------------------------------------

def update_ai_analysis(
    grievance_id,
    category,
    priority,
    severity,
    ai_summary,
    ai_reason
):
    """Store AI analysis results for a grievance."""

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE grievances
        SET category = ?,
            priority = ?,
            severity = ?,
            ai_summary = ?,
            ai_reason = ?,
            updated_at = ?
        WHERE id = ?
    """, (
        category,
        priority,
        severity,
        ai_summary,
        ai_reason,
        current_time,
        grievance_id
    ))

    connection.commit()
    connection.close()


# -----------------------------------------
# Statistics
# -----------------------------------------

def get_statistics():
    """Return basic grievance statistics."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM grievances")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM grievances
        WHERE status = 'Pending'
    """)
    pending = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM grievances
        WHERE status = 'In Progress'
    """)
    in_progress = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM grievances
        WHERE status = 'Resolved'
    """)
    resolved = cursor.fetchone()[0]

    connection.close()

    return {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "resolved": resolved
    }


# -----------------------------------------
# Initialize Automatically
# -----------------------------------------

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")
    print(f"Database location: {DB_PATH}")