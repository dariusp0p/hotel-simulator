import pytest
import sqlite3
from src.db.database_manager import DatabaseManager


@pytest.fixture
def in_memory_db():
    """Provides an in-memory SQLite database connection"""
    conn = sqlite3.connect(":memory:")
    yield conn
    conn.close()

@pytest.fixture
def db_manager(monkeypatch):
    """Creates a DatabaseManager with in-memory database"""

    def mock_get_sqlite_connection(_):
        return sqlite3.connect(":memory:")

    monkeypatch.setattr("src.db.database_manager.get_sqlite_connection", mock_get_sqlite_connection)
    manager = DatabaseManager("test.db")
    return manager
