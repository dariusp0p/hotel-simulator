import sqlite3


def test_database_initialization(db_manager, monkeypatch):
    # Mock the create_hotel_simulator_model function
    mock_create_called = False

    def mock_create(conn):
        nonlocal mock_create_called
        mock_create_called = True

    monkeypatch.setattr("src.db.database_manager.create_hotel_simulator_model", mock_create)

    # Call initialize
    db_manager.initialize_database()

    # Assert creation function was called
    assert mock_create_called

def test_conn_property(db_manager):
    # Test that the conn property returns a valid connection
    conn = db_manager.conn
    assert isinstance(conn, sqlite3.Connection)

    # Verify connection works
    cursor = conn.cursor()
    cursor.execute("SELECT 1")
    assert cursor.fetchone()[0] == 1
