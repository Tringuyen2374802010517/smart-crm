import sqlite3

import pytest
from fastapi.testclient import TestClient

from src.backend.main import app
from src.backend.api import auth_api
from src.backend.repositories import assignment_repository as repo


@pytest.fixture
def api_env(tmp_path, monkeypatch):
    db_path = tmp_path / "reassignment_api.db"
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

    repo.create_assignment(1, 1)

    auth_path = tmp_path / "reassignment_auth.db"
    monkeypatch.setattr(auth_api, "DB_PATH", auth_path)
    monkeypatch.setattr(auth_api, "ITERATIONS", 1000)

    with auth_api.connection() as db:
        auth_api.init_auth_db(db)

        for username, role in [
            ("manager_test", "MANAGER"),
            ("technician_test", "TECHNICIAN"),
        ]:
            db.execute(
                """
                INSERT INTO crm_user
                    (username, password_hash, role, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    username,
                    auth_api.hash_password("TestPassword123"),
                    role,
                    auth_api.utc_now().isoformat(),
                ),
            )

        db.commit()

    client = TestClient(app)
    tokens = {}

    for username in ["manager_test", "technician_test"]:
        response = client.post(
            "/auth/login",
            json={
                "username": username,
                "password": "TestPassword123",
            },
        )
        assert response.status_code == 200, response.text
        tokens[username] = response.json()["access_token"]

    return client, tokens, db_path


def endpoint():
    return "/assignments/ticket/1/reassign"


def payload(reason="Technician A unavailable"):
    return {
        "technician_id": 2,
        "reason": reason,
    }


def headers(token):
    return {"Authorization": f"Bearer {token}"}


def test_manager_can_reassign(api_env):
    client, tokens, db_path = api_env

    response = client.put(
        endpoint(),
        json=payload(),
        headers=headers(tokens["manager_test"]),
    )

    assert response.status_code == 200, response.text
    assert response.json()["technician_id"] == 2

    with sqlite3.connect(db_path) as db:
        rows = db.execute(
            """
            SELECT technician_id, ended_at, change_reason
            FROM assignment
            WHERE ticket_id = 1
            ORDER BY assignment_id
            """
        ).fetchall()

    assert len(rows) == 2
    assert rows[0][0] == 1
    assert rows[0][1] is not None
    assert rows[0][2] == payload()["reason"]
    assert rows[1][0] == 2
    assert rows[1][1] is None
    assert repo.get_ticket(1)["status"] == "ASSIGNED"


def test_technician_role_is_forbidden(api_env):
    client, tokens, _ = api_env

    response = client.put(
        endpoint(),
        json=payload(),
        headers=headers(tokens["technician_test"]),
    )

    assert response.status_code == 403
    assert repo.get_active_assignment(1)["technician_id"] == 1


def test_unauthenticated_request_is_rejected(api_env):
    client, _, _ = api_env

    response = client.put(endpoint(), json=payload())

    assert response.status_code == 401
    assert repo.get_active_assignment(1)["technician_id"] == 1


def test_empty_reason_is_rejected(api_env):
    client, tokens, _ = api_env

    response = client.put(
        endpoint(),
        json=payload(""),
        headers=headers(tokens["manager_test"]),
    )

    assert response.status_code == 422
    assert repo.get_active_assignment(1)["technician_id"] == 1


def test_unavailable_technician_preserves_assignment(api_env):
    client, tokens, db_path = api_env

    with sqlite3.connect(db_path) as db:
        db.execute(
            """
            UPDATE technician
            SET availability_status = 'BUSY'
            WHERE technician_id = 2
            """
        )

    response = client.put(
        endpoint(),
        json=payload(),
        headers=headers(tokens["manager_test"]),
    )

    assert response.status_code == 400
    assert repo.get_active_assignment(1)["technician_id"] == 1

    with sqlite3.connect(db_path) as db:
        count = db.execute(
            "SELECT COUNT(*) FROM assignment WHERE ticket_id = 1"
        ).fetchone()[0]

    assert count == 1


# BUG-02: Reassignment candidates API tests

def candidates_endpoint(ticket_id=1):
    return f"/assignments/ticket/{ticket_id}/reassignment-candidates"


def test_manager_can_get_reassignment_candidates(api_env):
    client, tokens, _ = api_env

    response = client.get(
        candidates_endpoint(),
        headers=headers(tokens["manager_test"]),
    )

    assert response.status_code == 200, response.text
    candidates = response.json()
    assert isinstance(candidates, list)

    ids = [item["technician_id"] for item in candidates]
    assert 2 in ids
    assert 1 not in ids


def test_technician_cannot_get_reassignment_candidates(api_env):
    client, tokens, _ = api_env

    response = client.get(
        candidates_endpoint(),
        headers=headers(tokens["technician_test"]),
    )

    assert response.status_code == 403


def test_unauthenticated_cannot_get_reassignment_candidates(api_env):
    client, _, _ = api_env

    response = client.get(candidates_endpoint())

    assert response.status_code == 401


def test_reassignment_candidates_reject_unknown_ticket(api_env):
    client, tokens, _ = api_env

    response = client.get(
        candidates_endpoint(9999),
        headers=headers(tokens["manager_test"]),
    )

    assert response.status_code == 404


def test_reassignment_candidates_reject_pending_ticket(api_env):
    client, tokens, db_path = api_env

    with sqlite3.connect(db_path) as db:
        db.execute(
            "UPDATE ticket SET status = 'PENDING' WHERE ticket_id = 1"
        )

    response = client.get(
        candidates_endpoint(),
        headers=headers(tokens["manager_test"]),
    )

    assert response.status_code == 400


# BUG-02: Assignment history API tests

def history_endpoint(ticket_id=1):
    return f"/assignments/ticket/{ticket_id}/history"


def test_manager_can_view_assignment_history(api_env):
    client, tokens, _ = api_env

    response = client.get(
        history_endpoint(),
        headers=headers(tokens["manager_test"]),
    )

    assert response.status_code == 200, response.text
    history = response.json()
    assert len(history) == 1
    assert history[0]["technician_id"] == 1
    assert history[0]["technician_name"] == "Technician A"


def test_technician_cannot_view_assignment_history(api_env):
    client, tokens, _ = api_env

    response = client.get(
        history_endpoint(),
        headers=headers(tokens["technician_test"]),
    )

    assert response.status_code == 403


def test_unauthenticated_cannot_view_assignment_history(api_env):
    client, _, _ = api_env

    response = client.get(history_endpoint())

    assert response.status_code == 401


def test_assignment_history_unknown_ticket(api_env):
    client, tokens, _ = api_env

    response = client.get(
        history_endpoint(9999),
        headers=headers(tokens["manager_test"]),
    )

    assert response.status_code == 404


def test_assignment_history_after_reassignment(api_env):
    client, tokens, _ = api_env
    auth = headers(tokens["manager_test"])
    reason = "Technician A unavailable"

    changed = client.put(
        endpoint(),
        json=payload(reason),
        headers=auth,
    )
    assert changed.status_code == 200, changed.text

    response = client.get(history_endpoint(), headers=auth)
    assert response.status_code == 200, response.text

    history = response.json()
    assert len(history) == 2

    assert history[0]["technician_id"] == 1
    assert history[0]["ended_at"] is not None
    assert history[0]["change_reason"] == reason

    assert history[1]["technician_id"] == 2
    assert history[1]["ended_at"] is None

    assert sum(item["ended_at"] is None for item in history) == 1
