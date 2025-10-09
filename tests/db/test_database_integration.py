from src.db.database_manager import DatabaseManager


def test_database_integration(tmp_path):
    # Create a temporary database file
    db_path = tmp_path / "test.db"

    # Initialize real database
    manager = DatabaseManager(str(db_path))
    manager.initialize_database()

    # Verify database file was created
    assert db_path.exists()

    # Test some operations (insert/query)
    conn = manager.conn

    # Test floor operations
    cursor = conn.cursor()
    cursor.execute("INSERT INTO floors (name, level) VALUES (?, ?)", ("Lobby Floor", 0))
    floor_id = cursor.lastrowid

    cursor.execute("SELECT name FROM floors WHERE level = ?", (0,))
    assert cursor.fetchone()[0] == "Lobby Floor"

    # Test element operations
    cursor.execute("""
                   INSERT INTO elements (element_type, floor_id, x, y, number, capacity, price_per_night)
                   VALUES (?, ?, ?, ?, ?, ?, ?)
                   """, ("room", floor_id, 10, 20, "101", 2, 99.99))
    room_id = cursor.lastrowid

    cursor.execute("SELECT element_type, number FROM elements WHERE floor_id = ?", (floor_id,))
    result = cursor.fetchone()
    assert result[0] == "room"
    assert result[1] == "101"

    # Test reservation operations
    cursor.execute("""
                   INSERT INTO reservations
                   (reservation_id, room_id, guest_name, number_of_guests, check_in_date, check_out_date)
                   VALUES (?, ?, ?, ?, ?, ?)
                   """, ("RES-001", room_id, "John Doe", 2, "2023-05-01", "2023-05-05"))

    cursor.execute("SELECT guest_name FROM reservations WHERE reservation_id = ?", ("RES-001",))
    assert cursor.fetchone()[0] == "John Doe"

    # Verify data integrity across tables
    cursor.execute("""
                   SELECT f.name, e.number, r.guest_name
                   FROM reservations r
                            JOIN elements e ON r.room_id = e.id
                            JOIN floors f ON e.floor_id = f.id
                   WHERE r.reservation_id = ?
                   """, ("RES-001",))

    result = cursor.fetchone()
    assert result[0] == "Lobby Floor"  # floor name
    assert result[1] == "101"  # room number
    assert result[2] == "John Doe"  # guest name
