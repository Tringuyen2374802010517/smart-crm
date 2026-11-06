import sqlite3

import pytest

from src.backend.repositories import assignment_repository as repo
from src.backend.services import assignment_service as service


@pytest.fixture
def reassignment_db(tmp_path, monkeypatch):
    db_path = tmp_path / "reassignment.db"
    monkeypatch.setattr(repo, "DB_PATH", db_path)

    with sqlite3.connect(db_path) as db:
        db.executescript("""
            CREATE TABLE ticket (
                ticket_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                incident_group TEXT NOT NULL,
                priority TEXT NOT NULL,
                status TEXT NOT NULL,
                center_id INTEGER NOT NULL
            );

            CREATE TABLE technician (
                technician_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                center_id INTEGER NOT NULL,
                area TEXT,
                availability_status TEXT NOT NULL
            );

            CREATE TABLE technician_skill (
                technician_skill_id INTEGER PRIMARY KEY,
                technician_id INTEGER NOT NULL,
                incident_group TEXT NOT NULL,
                proficiency INTEGER NOT NULL
            );

            CREATE TABLE assignment (
                assignment_id INTEGER PRIMARY KEY,
                ticket_id INTEGER NOT NULL,
                technician_id INTEGER NOT NULL,
                assigned_at TEXT NOT NULL,
                ended_at TEXT,
                change_reason TEXT
            );

            INSERT INTO ticket VALUES
                (1, 'Test reassignment', 'MAN_HINH',
                 'CAO', 'PENDING', 1);

            INSERT INTO technician VALUES
                (1, 'Technician A', 1, 'HCM', 'AVAILABLE'),
                (2, 'Technician B', 1, 'HCM', 'AVAILABLE');

            INSERT INTO technician_skill VALUES
                (1, 1, 'MAN_HINH', 4),
                (2, 2, 'MAN_HINH', 4);
        """)

    return db_path


def test_reassignment_records_reason_and_preserves_one_active(
    reassignment_db,
):
    repo.create_assignment(1, 1)

    reason = "Technician A unavailable"

    service.reassign_technician(1, 2, reason)

    with sqlite3.connect(reassignment_db) as db:
        db.row_factory = sqlite3.Row

        rows = db.execute(
            """
            SELECT technician_id, ended_at, change_reason
            FROM assignment
            WHERE ticket_id = 1
            ORDER BY assignment_id
            """
        ).fetchall()

        active = [r for r in rows if r["ended_at"] is None]

        assert len(rows) == 2
        assert len(active) == 1
        assert active[0]["technician_id"] == 2

        assert rows[0]["technician_id"] == 1
        assert rows[0]["ended_at"] is not None
        assert rows[0]["change_reason"] == reason

    assert repo.get_ticket(1)["status"] == "ASSIGNED"


from src.backend.services.exceptions import BusinessError


@pytest.mark.parametrize("reason", ["", "   ", "x" * 256])
def test_reassignment_rejects_invalid_reason(reassignment_db, reason):
    repo.create_assignment(1, 1)

    with pytest.raises(BusinessError):
        service.reassign_technician(1, 2, reason)

    assert repo.get_active_assignment(1)["technician_id"] == 1


def test_reassignment_rejects_same_technician(reassignment_db):
    repo.create_assignment(1, 1)

    with pytest.raises(BusinessError):
        service.reassign_technician(1, 1, "Change requested")

    assert repo.get_active_assignment(1)["technician_id"] == 1


def test_reassignment_rejects_unavailable_technician(reassignment_db):
    repo.create_assignment(1, 1)

    with sqlite3.connect(reassignment_db) as db:
        db.execute(
            "UPDATE technician SET availability_status = 'BUSY' "
            "WHERE technician_id = 2"
        )

    with pytest.raises(BusinessError):
        service.reassign_technician(1, 2, "Technician A unavailable")

    assert repo.get_active_assignment(1)["technician_id"] == 1


def test_reassignment_rejects_workload_limit(reassignment_db):
    repo.create_assignment(1, 1)

    with sqlite3.connect(reassignment_db) as db:
        for ticket_id in range(2, 7):
            db.execute(
                """
                INSERT INTO ticket
                VALUES (?, 'Extra ticket', 'MAN_HINH',
                        'CAO', 'PENDING', 1)
                """,
                (ticket_id,),
            )

    for ticket_id in range(2, 7):
        repo.create_assignment(ticket_id, 2)

    with pytest.raises(BusinessError):
        service.reassign_technician(1, 2, "Change requested")

    assert repo.get_active_assignment(1)["technician_id"] == 1


def test_reassignment_failure_preserves_original_record(reassignment_db):
    repo.create_assignment(1, 1)

    with pytest.raises(BusinessError):
        service.reassign_technician(1, 1, "Invalid reassignment")

    with sqlite3.connect(reassignment_db) as db:
        rows = db.execute(
            """
            SELECT technician_id, ended_at
            FROM assignment
            WHERE ticket_id = 1
            """
        ).fetchall()

    assert len(rows) == 1
    assert rows[0][0] == 1
    assert rows[0][1] is None
    assert repo.get_ticket(1)["status"] == "ASSIGNED"
