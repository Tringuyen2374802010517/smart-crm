import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[3] / "smartcrm.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def get_all_tickets():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT * FROM ticket ORDER BY ticket_id"
        ).fetchall()
        return [dict(row) for row in rows]


def get_ticket_by_id(ticket_id):
    with get_connection() as connection:
        row = connection.execute(
            "SELECT * FROM ticket WHERE ticket_id = ?",
            (ticket_id,)
        ).fetchone()
        return dict(row) if row else None


def create_ticket(title, incident_group, priority, center_id):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO ticket
                (title, incident_group, priority, status, center_id)
            VALUES (?, ?, ?, 'PENDING', ?)
            """,
            (title, incident_group, priority, center_id)
        )
        connection.commit()
        return get_ticket_by_id(cursor.lastrowid)


def update_ticket(ticket_id, title, incident_group, priority, center_id):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            UPDATE ticket
            SET title = ?, incident_group = ?,
                priority = ?, center_id = ?
            WHERE ticket_id = ?
            """,
            (title, incident_group, priority, center_id, ticket_id)
        )
        connection.commit()
        return get_ticket_by_id(ticket_id) if cursor.rowcount else None


def delete_ticket(ticket_id):
    with get_connection() as connection:
        cursor = connection.execute(
            "DELETE FROM ticket WHERE ticket_id = ?",
            (ticket_id,)
        )
        connection.commit()
        return cursor.rowcount > 0
