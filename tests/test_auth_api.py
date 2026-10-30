import pytest
from fastapi import HTTPException

from src.backend.api import auth_api as api


@pytest.fixture
def auth_db(tmp_path, monkeypatch):
    db_path = tmp_path / "auth.db"
    monkeypatch.setattr(api, "DB_PATH", db_path)
    monkeypatch.setattr(api, "ITERATIONS", 1000)

    with api.connection() as db:
        api.init_auth_db(db)
        db.execute(
            """
            INSERT INTO crm_user
                (username, password_hash, role, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (
                "manager",
                api.hash_password("TestPassword123"),
                "MANAGER",
                api.utc_now().isoformat(),
            ),
        )
        db.commit()

    return db_path


def credentials(password="TestPassword123"):
    return api.LoginInput(username="manager", password=password)


def test_login_success(auth_db):
    result = api.login(credentials())

    assert result["access_token"]
    assert result["token_type"] == "bearer"
    assert result["user"]["username"] == "manager"


def test_login_wrong_password(auth_db):
    with pytest.raises(HTTPException) as error:
        api.login(credentials("WrongPassword"))

    assert error.value.status_code == 401


def test_me_valid_token(auth_db):
    token = api.login(credentials())["access_token"]

    result = api.me(authorization=f"Bearer {token}")

    assert result["username"] == "manager"
    assert result["role"] == "MANAGER"


def test_me_missing_token(auth_db):
    with pytest.raises(HTTPException) as error:
        api.me(authorization=None)

    assert error.value.status_code == 401


def test_me_invalid_token(auth_db):
    with pytest.raises(HTTPException) as error:
        api.me(authorization="Bearer invalid-token")

    assert error.value.status_code == 401


def test_logout_revokes_token(auth_db):
    token = api.login(credentials())["access_token"]
    authorization = f"Bearer {token}"

    result = api.logout(authorization=authorization)
    assert result["message"] == "Đăng xuất thành công"

    with pytest.raises(HTTPException) as error:
        api.me(authorization=authorization)

    assert error.value.status_code == 401
