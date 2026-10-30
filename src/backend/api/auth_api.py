import hashlib
import hmac
import secrets
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/auth", tags=["Authentication"])

DB_PATH = Path(__file__).resolve().parents[3] / "smartcrm.db"
ITERATIONS = 600_000
SESSION_HOURS = 8


def utc_now():
    return datetime.now(timezone.utc)


def connection():
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db


def init_auth_db(db):
    db.executescript("""
        CREATE TABLE IF NOT EXISTS crm_user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'MANAGER',
            created_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS crm_session (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token_hash TEXT NOT NULL UNIQUE,
            expires_at TEXT NOT NULL,
            revoked_at TEXT,
            FOREIGN KEY (user_id) REFERENCES crm_user(user_id)
        );

        CREATE INDEX IF NOT EXISTS idx_crm_session_token
        ON crm_session(token_hash);
    """)


def hash_password(password):
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        ITERATIONS
    )
    return f"pbkdf2_sha256${ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password, stored):
    try:
        algorithm, count, salt_hex, digest_hex = stored.split("$")
        if algorithm != "pbkdf2_sha256":
            return False

        calculated = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(count)
        )
        return hmac.compare_digest(
            calculated,
            bytes.fromhex(digest_hex)
        )
    except (ValueError, TypeError):
        return False


def token_hash(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def get_user_by_token(token):
    with connection() as db:
        init_auth_db(db)
        row = db.execute(
            """
            SELECT u.user_id, u.username, u.role
            FROM crm_session s
            JOIN crm_user u ON u.user_id = s.user_id
            WHERE s.token_hash = ?
              AND s.revoked_at IS NULL
              AND s.expires_at > ?
            """,
            (token_hash(token), utc_now().isoformat())
        ).fetchone()

        return dict(row) if row else None


def require_user(authorization):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Vui lòng đăng nhập"
        )

    token = authorization[7:].strip()
    user = get_user_by_token(token)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Phiên đăng nhập không hợp lệ hoặc đã hết hạn"
        )

    return user, token


class LoginInput(BaseModel):
    username: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1)


@router.post("/login")
def login(data: LoginInput):
    with connection() as db:
        init_auth_db(db)

        user = db.execute(
            "SELECT * FROM crm_user WHERE username = ?",
            (data.username.strip(),)
        ).fetchone()

        if user is None or not verify_password(
            data.password,
            user["password_hash"]
        ):
            raise HTTPException(
                status_code=401,
                detail="Tên đăng nhập hoặc mật khẩu không đúng"
            )

        token = secrets.token_urlsafe(32)
        expires_at = (
            utc_now() + timedelta(hours=SESSION_HOURS)
        ).isoformat()

        db.execute(
            """
            INSERT INTO crm_session
                (user_id, token_hash, expires_at)
            VALUES (?, ?, ?)
            """,
            (user["user_id"], token_hash(token), expires_at)
        )
        db.commit()

        return {
            "access_token": token,
            "token_type": "bearer",
            "expires_at": expires_at,
            "user": {
                "user_id": user["user_id"],
                "username": user["username"],
                "role": user["role"]
            }
        }


@router.get("/me")
def me(authorization: str | None = Header(default=None)):
    user, _ = require_user(authorization)
    return user


@router.post("/logout")
def logout(authorization: str | None = Header(default=None)):
    _, token = require_user(authorization)

    with connection() as db:
        db.execute(
            """
            UPDATE crm_session
            SET revoked_at = ?
            WHERE token_hash = ?
              AND revoked_at IS NULL
            """,
            (utc_now().isoformat(), token_hash(token))
        )
        db.commit()

    return {"message": "Đăng xuất thành công"}
