import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.backend.main import app
from src.backend.repositories import (
    ticket_repository,
    assignment_repository,
)


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_path = tmp_path / "ticket_test.db"

    with sqlite3.connect(db_path) as conn:
        conn.executescript(
            Path("docs/schema.sql").read_text(encoding="utf-8")
        )
        conn.executescript(
            Path("docs/seed.sql").read_text(encoding="utf-8")
        )

    monkeypatch.setattr(ticket_repository, "DB_PATH", db_path)
    monkeypatch.setattr(assignment_repository, "DB_PATH", db_path)

    return TestClient(app)


def valid_payload():
    return {
        "title": "Test ticket",
        "incident_group": "MAN_HINH",
        "priority": "CAO",
        "center_id": 1,
    }


def test_create_ticket(client):
    response = client.post("/tickets", json=valid_payload())

    assert response.status_code == 201
    assert response.json()["title"] == "Test ticket"
    assert response.json()["status"] == "PENDING"


def test_list_and_get_ticket(client):
    response = client.get("/tickets")

    assert response.status_code == 200
    assert len(response.json()) == 3

    response = client.get("/tickets/1")

    assert response.status_code == 200
    assert response.json()["ticket_id"] == 1


def test_update_ticket(client):
    payload = valid_payload()
    payload["title"] = "Updated ticket"

    response = client.put("/tickets/1", json=payload)

    assert response.status_code == 200
    assert response.json()["title"] == "Updated ticket"


def test_delete_ticket(client):
    response = client.delete("/tickets/1")

    assert response.status_code == 200
    assert client.get("/tickets/1").status_code == 404


def test_invalid_ticket_title(client):
    payload = valid_payload()
    payload["title"] = ""

    response = client.post("/tickets", json=payload)

    assert response.status_code == 400


def test_invalid_ticket_priority(client):
    payload = valid_payload()
    payload["priority"] = "INVALID"

    response = client.post("/tickets", json=payload)

    assert response.status_code == 400


def test_ticket_not_found(client):
    response = client.get("/tickets/999999")

    assert response.status_code == 404


def test_cannot_delete_assigned_ticket(client):
    assignment = client.post(
        "/assignments/",
        json={"ticket_id": 1, "technician_id": 1},
    )

    assert assignment.status_code == 201, assignment.text

    response = client.delete("/tickets/1")

    assert response.status_code == 400
    assert client.get("/tickets/1").status_code == 200
