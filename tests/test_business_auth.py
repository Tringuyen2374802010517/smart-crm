import sqlite3
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.backend.main import app
from src.backend.api import auth_api
from src.backend.repositories import ticket_repository, assignment_repository


@pytest.fixture
def auth_client(tmp_path, monkeypatch):
    business_db = tmp_path / "business.db"

    with sqlite3.connect(business_db) as db:
        db.executescript(
            Path("docs/schema.sql").read_text(encoding="utf-8")
        )
        db.executescript(
            Path("docs/seed.sql").read_text(encoding="utf-8")
        )

    monkeypatch.setattr(ticket_repository, "DB_PATH", business_db)
    monkeypatch.setattr(assignment_repository, "DB_PATH", business_db)

    auth_db = tmp_path / "authentication.db"
    monkeypatch.setattr(auth_api, "DB_PATH", auth_db)
    monkeypatch.setattr(auth_api, "ITERATIONS", 1000)

    with auth_api.connection() as db:
        auth_api.init_auth_db(db)
        db.execute(
            """
            INSERT INTO crm_user
                (username, password_hash, role, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                "security_tester",
                auth_api.hash_password("TestPassword123"),
                "MANAGER",
                auth_api.utc_now().isoformat(),
            ),
        )
        db.commit()

    client = TestClient(app)

    login_response = client.post(
        "/auth/login",
        json={
            "username": "security_tester",
            "password": "TestPassword123",
        },
    )

    assert login_response.status_code == 200, login_response.text

    token = login_response.json()["access_token"]
    return client, token


PROTECTED_ENDPOINTS = [
    "/tickets",
    "/technicians",
    "/appointments",
    "/assignments/ticket/1/detail",
]


@pytest.mark.parametrize("endpoint", PROTECTED_ENDPOINTS)
def test_missing_token_returns_401(auth_client, endpoint):
    client, _ = auth_client

    response = client.get(endpoint)

    assert response.status_code == 401


@pytest.mark.parametrize("endpoint", PROTECTED_ENDPOINTS)
def test_invalid_token_returns_401(auth_client, endpoint):
    client, _ = auth_client

    response = client.get(
        endpoint,
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401


@pytest.mark.parametrize(
    "endpoint,payload",
    [
        (
            "/tickets",
            {
                "title": "Unauthorized ticket",
                "incident_group": "MAN_HINH",
                "priority": "CAO",
                "center_id": 1,
            },
        ),
        (
            "/assignments/",
            {"ticket_id": 1, "technician_id": 1},
        ),
    ],
)
def test_unauthorized_write_returns_401(auth_client, endpoint, payload):
    client, _ = auth_client

    response = client.post(endpoint, json=payload)

    assert response.status_code == 401


def test_valid_token_can_access_tickets(auth_client):
    client, token = auth_client

    response = client.get(
        "/tickets",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_revoked_token_returns_401(auth_client):
    client, token = auth_client
    headers = {"Authorization": f"Bearer {token}"}

    logout_response = client.post("/auth/logout", headers=headers)

    assert logout_response.status_code == 200

    response = client.get("/tickets", headers=headers)

    assert response.status_code == 401
