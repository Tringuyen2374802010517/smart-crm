import sqlite3

import pytest

from src.backend import main


class FakeCursor:
    def __init__(self, should_fail=False):
        self.should_fail = should_fail

    def execute(self, query):
        if self.should_fail:
            raise sqlite3.OperationalError("Simulated database error")

    def fetchone(self):
        return (1,)


class FakeConnection:
    def __init__(self, should_fail=False):
        self.closed = False
        self.cursor_instance = FakeCursor(should_fail)

    def cursor(self):
        return self.cursor_instance

    def close(self):
        self.closed = True


def test_db_check_closes_connection_on_success(monkeypatch):
    connection = FakeConnection()

    monkeypatch.setattr(
        main.sqlite3,
        "connect",
        lambda *args, **kwargs: connection
    )

    result = main.db_check()

    assert result == {
        "status": "OK",
        "database": "SQLite",
        "result": 1
    }
    assert connection.closed is True


def test_db_check_closes_connection_on_query_error(monkeypatch):
    connection = FakeConnection(should_fail=True)

    monkeypatch.setattr(
        main.sqlite3,
        "connect",
        lambda *args, **kwargs: connection
    )

    with pytest.raises(sqlite3.OperationalError):
        main.db_check()

    assert connection.closed is True
