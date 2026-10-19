
import sqlite3
from pathlib import Path
from datetime import datetime, timezone


DB_PATH = Path(__file__).resolve().parents[3] / "smartcrm.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def get_ticket(ticket_id):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM ticket WHERE ticket_id = ?",
            (ticket_id,)
        ).fetchone()
        return dict(row) if row else None


def get_technician(technician_id):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM technician WHERE technician_id = ?",
            (technician_id,)
        ).fetchone()
        return dict(row) if row else None


def get_eligible_technicians(center_id, incident_group):
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                t.technician_id,
                t.name,
                t.center_id,
                t.area,
                t.availability_status,
                s.incident_group,
                s.proficiency,
                (
                    SELECT COUNT(*)
                    FROM assignment a
                    WHERE a.technician_id = t.technician_id
                      AND a.ended_at IS NULL
                ) AS current_workload
            FROM technician t
            JOIN technician_skill s
                ON s.technician_id = t.technician_id
            WHERE t.center_id = ?
              AND t.availability_status = 'AVAILABLE'
              AND s.incident_group = ?
              AND s.proficiency >= 3
            ORDER BY current_workload ASC, t.technician_id ASC
            """,
            (center_id, incident_group)
        ).fetchall()
        return [dict(row) for row in rows]


def get_active_assignment(ticket_id):
    with get_connection() as connection:
        row = connection.execute(
            """
            SELECT *
            FROM assignment
            WHERE ticket_id = ?
              AND ended_at IS NULL
            """,
            (ticket_id,)
        ).fetchone()
        return dict(row) if row else None


def create_assignment(ticket_id, technician_id):
    assigned_at = datetime.now(timezone.utc).isoformat()

    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO assignment
                (ticket_id, technician_id, assigned_at)
            VALUES (?, ?, ?)
            """,
            (ticket_id, technician_id, assigned_at)
        )
        connection.commit()
        assignment_id = cursor.lastrowid

        row = connection.execute(
            "SELECT * FROM assignment WHERE assignment_id = ?",
            (assignment_id,)
        ).fetchone()
        return dict(row)
