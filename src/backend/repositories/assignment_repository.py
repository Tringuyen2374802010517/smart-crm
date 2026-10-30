
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
              AND (
                  SELECT COUNT(*)
                  FROM assignment a
                  WHERE a.technician_id = t.technician_id
                    AND a.ended_at IS NULL
              ) < 5
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

    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        ticket = connection.execute(
            "SELECT status FROM ticket WHERE ticket_id = ?",
            (ticket_id,)
        ).fetchone()

        if ticket is None or ticket["status"] != "PENDING":
            raise ValueError("Phiếu không ở trạng thái PENDING")

        active_ticket = connection.execute(
            """
            SELECT 1 FROM assignment
            WHERE ticket_id = ? AND ended_at IS NULL
            """,
            (ticket_id,)
        ).fetchone()

        if active_ticket:
            raise ValueError("Phiếu đã có kỹ thuật viên phụ trách")

        technician = connection.execute(
            """
            SELECT t.center_id, t.availability_status,
                   s.proficiency
            FROM technician t
            JOIN ticket tk ON tk.ticket_id = ?
            LEFT JOIN technician_skill s
              ON s.technician_id = t.technician_id
             AND s.incident_group = tk.incident_group
            WHERE t.technician_id = ?
              AND t.center_id = tk.center_id
            """,
            (ticket_id, technician_id)
        ).fetchone()

        if (
            technician is None
            or technician["availability_status"] != "AVAILABLE"
            or technician["proficiency"] is None
            or technician["proficiency"] < 3
        ):
            raise ValueError("Kỹ thuật viên không đủ điều kiện")

        workload = connection.execute(
            """
            SELECT COUNT(*) FROM assignment
            WHERE technician_id = ? AND ended_at IS NULL
            """,
            (technician_id,)
        ).fetchone()[0]

        if workload >= 5:
            raise ValueError("Kỹ thuật viên đã đạt giới hạn 5 phiếu")

        cursor = connection.execute(
            """
            INSERT INTO assignment
                (ticket_id, technician_id, assigned_at)
            VALUES (?, ?, ?)
            """,
            (ticket_id, technician_id, assigned_at)
        )

        connection.execute(
            """
            UPDATE ticket SET status = 'ASSIGNED'
            WHERE ticket_id = ?
            """,
            (ticket_id,)
        )

        row = connection.execute(
            "SELECT * FROM assignment WHERE assignment_id = ?",
            (cursor.lastrowid,)
        ).fetchone()

        result = dict(row)
        connection.commit()
        return result

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def complete_ticket(ticket_id):
    completed_at = datetime.now(timezone.utc).isoformat()
    connection = get_connection()

    try:
        connection.execute("BEGIN IMMEDIATE")

        ticket = connection.execute(
            "SELECT status FROM ticket WHERE ticket_id = ?",
            (ticket_id,)
        ).fetchone()

        if ticket is None:
            raise ValueError("Không tìm thấy phiếu")

        if ticket["status"] != "ASSIGNED":
            raise ValueError("Chỉ có thể hoàn thành phiếu ASSIGNED")

        cursor = connection.execute(
            """
            UPDATE assignment SET ended_at = ?
            WHERE ticket_id = ? AND ended_at IS NULL
            """,
            (completed_at, ticket_id)
        )

        if cursor.rowcount != 1:
            raise ValueError("Không tìm thấy phân công đang hoạt động")

        connection.execute(
            """
            UPDATE ticket SET status = 'COMPLETED'
            WHERE ticket_id = ?
            """,
            (ticket_id,)
        )

        connection.commit()
        return {"ticket_id": ticket_id, "status": "COMPLETED"}

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
