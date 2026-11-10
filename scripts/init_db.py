import os
import sqlite3
from pathlib import Path

from src.backend.api.auth_api import hash_password, utc_now

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "smartcrm.db"


def main():
    username = os.getenv("DEMO_ADMIN_USERNAME", "").strip()
    password = os.getenv("DEMO_ADMIN_PASSWORD", "")

    if not username or len(username) > 100:
        raise ValueError("DEMO_ADMIN_USERNAME must contain 1-100 characters")

    if len(password) < 8:
        raise ValueError("DEMO_ADMIN_PASSWORD must contain at least 8 characters")

    with sqlite3.connect(DB_PATH) as db:
        db.execute("PRAGMA foreign_keys = ON")

        schema = (ROOT / "docs/schema.sql").read_text(encoding="utf-8")
        seed = (ROOT / "docs/seed.sql").read_text(encoding="utf-8")

        db.executescript(schema)
        db.executescript(seed)

        existing = db.execute(
            "SELECT user_id FROM crm_user WHERE username = ?",
            (username,),
        ).fetchone()

        if existing is None:
            db.execute(
                """
                INSERT INTO crm_user
                    (username, password_hash, role, created_at)
                VALUES (?, ?, ?, ?)
                """,
                (
                    username,
                    hash_password(password),
                    "MANAGER",
                    utc_now().isoformat(),
                ),
            )
            db.commit()
            print("PASS: Demo manager account initialized.")
        else:
            print("PASS: Demo manager account already exists.")

        print("PASS: SQLite schema and sample data initialized.")


if __name__ == "__main__":
    main()
