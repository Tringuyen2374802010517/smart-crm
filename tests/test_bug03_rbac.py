import sqlite3

from test_reassignment_api import api_env, headers


def test_technician_cannot_assign_ticket(api_env):
    client, tokens, db_path = api_env

    # Tạo phiếu hợp lệ trong database tạm.
    with sqlite3.connect(db_path) as db:
        db.execute(
            """
            INSERT INTO ticket
                (ticket_id, title, incident_group, priority, status, center_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (2, "RBAC assignment test", "MAN_HINH", "CAO", "PENDING", 1),
        )
        db.commit()

    response = client.post(
        "/assignments/",
        json={
            "ticket_id": 2,
            "technician_id": 2,
        },
        headers=headers(tokens["technician_test"]),
    )

    assert response.status_code == 403, (
        f"Expected 403, actual {response.status_code}: "
        f"{response.text}"
    )
