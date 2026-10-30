from src.backend.repositories import ticket_repository as database


def list_technicians():
    with database.get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM technician ORDER BY technician_id"
        ).fetchall()
        return [dict(row) for row in rows]


def get_technician(technician_id):
    with database.get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM technician WHERE technician_id = ?",
            (technician_id,)
        ).fetchone()
        return dict(row) if row else None


def create_technician(name, center_id, area, availability_status):
    with database.get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO technician
                (name, center_id, area, availability_status)
            VALUES (?, ?, ?, ?)
            """,
            (name, center_id, area, availability_status)
        )
        conn.commit()
        technician_id = cursor.lastrowid

    return get_technician(technician_id)


def update_technician(technician_id, name, center_id, area, availability_status):
    with database.get_connection() as conn:
        conn.execute(
            """
            UPDATE technician
            SET name = ?, center_id = ?, area = ?, availability_status = ?
            WHERE technician_id = ?
            """,
            (name, center_id, area, availability_status, technician_id)
        )
        conn.commit()

    return get_technician(technician_id)


def has_assignments_or_appointments(technician_id):
    with database.get_connection() as conn:
        count = conn.execute(
            """
            SELECT
                (SELECT COUNT(*) FROM assignment WHERE technician_id = ?)
                +
                (SELECT COUNT(*) FROM appointment WHERE technician_id = ?)
            """,
            (technician_id, technician_id)
        ).fetchone()[0]
        return count > 0


def has_active_assignments(technician_id):
    with database.get_connection() as conn:
        count = conn.execute(
            """
            SELECT COUNT(*)
            FROM assignment
            WHERE technician_id = ? AND ended_at IS NULL
            """,
            (technician_id,)
        ).fetchone()[0]
        return count > 0


def delete_technician(technician_id):
    with database.get_connection() as conn:
        conn.execute(
            "DELETE FROM technician_skill WHERE technician_id = ?",
            (technician_id,)
        )
        cursor = conn.execute(
            "DELETE FROM technician WHERE technician_id = ?",
            (technician_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
