import getpass
import sqlite3
import sys

from src.backend.api.auth_api import (
    connection,
    hash_password,
    init_auth_db,
    utc_now,
)


def main():
    print("=== Smart CRM – Tạo tài khoản quản lý ===")

    username = input("Tên đăng nhập: ").strip()

    if not username or len(username) > 100:
        print("ERROR: Tên đăng nhập phải có từ 1 đến 100 ký tự.")
        return 1

    password = getpass.getpass("Mật khẩu: ")
    confirmation = getpass.getpass("Nhập lại mật khẩu: ")

    if len(password) < 8:
        print("ERROR: Mật khẩu phải có ít nhất 8 ký tự.")
        return 1

    if password != confirmation:
        print("ERROR: Hai mật khẩu không khớp.")
        return 1

    with connection() as db:
        init_auth_db(db)

        existing = db.execute(
            "SELECT user_id FROM crm_user WHERE username = ?",
            (username,),
        ).fetchone()

        if existing:
            print("ERROR: Tài khoản đã tồn tại.")
            return 1

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

    print("PASS: Đã tạo tài khoản quản lý thành công.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
