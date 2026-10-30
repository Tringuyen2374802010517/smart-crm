import sqlite3

import pytest

from src.backend.repositories import assignment_repository as repo


@pytest.fixture
def workflow_db(tmp_path, monkeypatch):
    db_path = tmp_path / "workflow.db"
    monkeypatch.setattr(repo, "DB_PATH", db_path)

    with sqlite3.connect(db_path) as conn:
        conn.executescript("""
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

            INSERT INTO technician
            VALUES (1, 'Nguyen Van An', 1, 'HCM', 'AVAILABLE');

            INSERT INTO technician_skill
            VALUES (1, 1, 'MAN_HINH', 4);
        """)

        for ticket_id in range(1, 7):
            conn.execute(
                """
                INSERT INTO ticket
                VALUES (?, 'Test ticket', 'MAN_HINH',
                        'CAO', 'PENDING', 1)
                """,
                (ticket_id,)
            )

        conn.commit()

    return db_path


def test_assignment_changes_status(workflow_db):
    result = repo.create_assignment(1, 1)

    assert result["ticket_id"] == 1

    ticket = repo.get_ticket(1)
    assert ticket["status"] == "ASSIGNED"


def test_workload_limit_five(workflow_db):
    for ticket_id in range(1, 6):
        repo.create_assignment(ticket_id, 1)

    eligible = repo.get_eligible_technicians(1, "MAN_HINH")
    assert eligible == []

    with pytest.raises(ValueError, match="giới hạn 5"):
        repo.create_assignment(6, 1)


def test_complete_ticket_releases_workload(workflow_db):
    for ticket_id in range(1, 6):
        repo.create_assignment(ticket_id, 1)

    result = repo.complete_ticket(1)

    assert result["status"] == "COMPLETED"
    assert repo.get_ticket(1)["status"] == "COMPLETED"
    assert repo.get_active_assignment(1) is None

    eligible = repo.get_eligible_technicians(1, "MAN_HINH")
    assert len(eligible) == 1
    assert eligible[0]["current_workload"] == 4


def test_failed_assignment_rolls_back(workflow_db):
    repo.create_assignment(1, 1)

    with pytest.raises(ValueError):
        repo.create_assignment(1, 1)

    assert repo.get_ticket(1)["status"] == "ASSIGNED"
