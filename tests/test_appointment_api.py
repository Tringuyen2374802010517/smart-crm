import sqlite3
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import HTTPException

from src.backend.api import appointment_api as api


@pytest.fixture
def appointment_db(tmp_path, monkeypatch):
    db_path = tmp_path / "appointments.db"
    monkeypatch.setattr(api, "DB_PATH", db_path)

    with sqlite3.connect(db_path) as db:
        db.executescript("""
            CREATE TABLE ticket (
                ticket_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                status TEXT NOT NULL
            );

            CREATE TABLE technician (
                technician_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );

            CREATE TABLE assignment (
                assignment_id INTEGER PRIMARY KEY,
                ticket_id INTEGER NOT NULL,
                technician_id INTEGER NOT NULL,
                ended_at TEXT
            );

            CREATE TABLE appointment (
                appointment_id INTEGER PRIMARY KEY,
                ticket_id INTEGER NOT NULL,
                technician_id INTEGER NOT NULL,
                appointment_type TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (ticket_id) REFERENCES ticket(ticket_id),
                FOREIGN KEY (technician_id) REFERENCES technician(technician_id),
                CHECK (end_time > start_time)
            );

            INSERT INTO ticket VALUES (1, 'Ticket 1', 'ASSIGNED');
            INSERT INTO ticket VALUES (2, 'Ticket 2', 'ASSIGNED');
            INSERT INTO ticket VALUES (3, 'Ticket 3', 'PENDING');

            INSERT INTO technician VALUES (1, 'Technician 1');

            INSERT INTO assignment VALUES (1, 1, 1, NULL);
            INSERT INTO assignment VALUES (2, 2, 1, NULL);
        """)

    return db_path


def future_time(hours=48):
    return datetime.now(timezone.utc).replace(
        minute=0, second=0, microsecond=0
    ) + timedelta(hours=hours)


def make_input(ticket_id=1, hours=48, appointment_type="DELIVERY"):
    return api.AppointmentInput(
        ticket_id=ticket_id,
        appointment_type=appointment_type,
        start_time=future_time(hours),
    )


def test_create_appointment_success(appointment_db):
    result = api.create_appointment(make_input())
    assert result["status"] == "SCHEDULED"
    assert result["technician_id"] == 1


def test_conflicting_appointment_rejected(appointment_db):
    api.create_appointment(make_input(ticket_id=1))

    with pytest.raises(HTTPException) as error:
        api.create_appointment(make_input(ticket_id=2))

    assert error.value.status_code == 409


def test_adjacent_appointments_allowed(appointment_db):
    first = api.create_appointment(make_input(ticket_id=1, hours=48))
    second = api.create_appointment(make_input(ticket_id=2, hours=49))

    assert first["appointment_id"] != second["appointment_id"]


def test_past_appointment_rejected(appointment_db):
    with pytest.raises(HTTPException) as error:
        api.create_appointment(make_input(hours=-2))

    assert error.value.status_code == 400


def test_unassigned_ticket_rejected(appointment_db):
    with pytest.raises(HTTPException) as error:
        api.create_appointment(make_input(ticket_id=3))

    assert error.value.status_code == 400


def test_invalid_appointment_type_rejected(appointment_db):
    with pytest.raises(HTTPException) as error:
        api.create_appointment(make_input(appointment_type="INVALID"))

    assert error.value.status_code == 400
