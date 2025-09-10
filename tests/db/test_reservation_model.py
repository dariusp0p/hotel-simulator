import pytest
import sqlite3

from src.db import reservation_model as db  # adjust path to yours


@pytest.fixture
def connection():
    conn = sqlite3.connect(":memory:")
    db.create_reservation_table(conn)
    yield conn
    conn.close()


def test_add_and_get_reservation(connection):
    db.insert_reservation(
        connection,
        reservation_id="test-123",
        room_number="101",
        guest_name="John Doe",
        number_of_guests=2,
        check_in_date="2025-07-20",
        check_out_date="2025-07-22"
    )
    result = db.select_reservation_by_reservation_id(connection, "test-123")

    assert result is not None
    assert result[2] == "101"
    assert result[3] == "John Doe"
    assert result[4] == 2
    assert result[5] == "2025-07-20"
    assert result[6] == "2025-07-22"

def test_add_reservation_duplicate_id(connection):
    db.insert_reservation(
        connection,
        reservation_id="unique-id",
        room_number="101",
        guest_name="Jane Doe",
        number_of_guests=2,
        check_in_date="2025-07-20",
        check_out_date="2025-07-22"
    )
    with pytest.raises(sqlite3.IntegrityError):
        db.insert_reservation(
            connection,
            reservation_id="unique-id",  # Same ID again
            room_number="102",
            guest_name="Different Guest",
            number_of_guests=3,
            check_in_date="2025-07-23",
            check_out_date="2025-07-25"
        )