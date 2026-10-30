import sqlite3

import pytest

from src.backend.repositories import assignment_repository as repo


@pytest.fixture
def priority_db(tmp_path, monkeypatch):
    db_path = tmp_path / "priority.db"
    monkeypatch.setattr(repo, "DB_PATH", db_path)

    with sqlite3.connect(db_path) as conn:
        conn.executescript("""
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
        """)

        for level in range(1, 6):
            conn.execute(
                "INSERT INTO technician VALUES (?, ?, 1, 'HCM', 'AVAILABLE')",
                (level, f"Technician {level}")
            )
            conn.execute(
                "INSERT INTO technician_skill VALUES (?, ?, 'MAN_HINH', ?)",
                (level, level, level)
            )

        conn.commit()

    return db_path


@pytest.mark.parametrize(
    "priority,expected_ids",
    [
        ("THAP", [2, 3, 4, 5]),
        ("TRUNG_BINH", [3, 4, 5]),
        ("CAO", [4, 5]),
    ],
)
def test_priority_filters_technicians(priority_db, priority, expected_ids):
    result = repo.get_eligible_technicians(1, "MAN_HINH", priority)
    actual_ids = [item["technician_id"] for item in result]

    assert actual_ids == expected_ids
