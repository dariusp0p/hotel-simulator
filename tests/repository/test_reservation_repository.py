import pytest
import sqlite3
from datetime import date
from unittest.mock import patch

from src.domain.reservation import Reservation
from src.db import reservation_model as db
from src.repository.reservation_repository import ReservationRepository
from src.utilities.exceptions import (
    ReservationAlreadyExistsError,
    ReservationNotFoundError,
    DatabaseUnavailableError
)



@pytest.fixture
def repo():
    connection = sqlite3.connect(":memory:")
    db.create_reservation_table(connection)
    repository = ReservationRepository(connection)
    yield repository
    connection.close()


def test_add_and_get_reservation(repo):
    reservation = Reservation(
        reservation_id="abc123",
        room_id="101",
        guest_name="Alice",
        number_of_guests=2,
        check_in_date=date(2025, 7, 20),
        check_out_date=date(2025, 7, 25)
    )
    repo.add_reservation(reservation)
    found = repo.get_by_reservation_id("abc123")
    assert found is not None
    assert found.room_number == "101"
    assert found.guest_name == "Alice"
    assert repo.get_reservations_by_room_number("101")[0] is found
    assert repo.get_reservations_by_guest_name("Alice")[0] is found

def test_duplicate_reservation_id_raises(repo):
    reservation = Reservation(
        reservation_id="dup123",
        room_id="102",
        guest_name="Bob",
        number_of_guests=2,
        check_in_date=date(2025, 7, 20),
        check_out_date=date(2025, 7, 25)
    )
    repo.add_reservation(reservation)
    with pytest.raises(ReservationAlreadyExistsError):
        repo.add_reservation(reservation)

def test_update_reservation(repo):
    reservation = Reservation(
        reservation_id="upd123",
        room_id="103",
        guest_name="Charlie",
        number_of_guests=2,
        check_in_date=date(2025, 7, 20),
        check_out_date=date(2025, 7, 25)
    )
    repo.add_reservation(reservation)
    reservation.room_number = "203"
    reservation.guest_name = "CharlieUpdated"
    repo.update_reservation(reservation)

    updated = repo.get_by_reservation_id("upd123")
    assert updated.room_number == "203"
    assert updated.guest_name == "CharlieUpdated"

def test_update_nonexistent_reservation_raises(repo):
    reservation = Reservation(
        db_id=9999,
        reservation_id="doesnotexist",
        room_id="404",
        guest_name="Nobody",
        number_of_guests=1,
        check_in_date=date(2025, 7, 20),
        check_out_date=date(2025, 7, 25)
    )
    with pytest.raises(ReservationNotFoundError):
        repo.update_reservation(reservation)

def test_delete_reservation(repo):
    reservation = Reservation(
        reservation_id="del123",
        room_id="105",
        guest_name="Daisy",
        number_of_guests=2,
        check_in_date=date(2025, 7, 20),
        check_out_date=date(2025, 7, 25)
    )
    repo.add_reservation(reservation)
    repo.delete_reservation("del123")
    assert repo.get_by_reservation_id("del123") is None

def test_delete_nonexistent_reservation_raises(repo):
    with pytest.raises(ReservationNotFoundError):
        repo.delete_reservation("ghost123")

def test_get_by_room_number_and_guest_name_empty(repo):
    assert repo.get_reservations_by_room_number("999") is None
    assert repo.get_reservations_by_guest_name("NoOne") is None

def test_delete_operational_error(repo):
    reservation = Reservation(
        reservation_id="failtest",
        room_id="500",
        guest_name="Ghost",
        number_of_guests=1,
        check_in_date=date(2025, 7, 20),
        check_out_date=date(2025, 7, 25)
    )
    repo.add_reservation(reservation)
    with patch("src.db.reservation_model.delete_reservation") as mock_delete:
        mock_delete.side_effect = sqlite3.OperationalError
        with pytest.raises(DatabaseUnavailableError):
            repo.delete_reservation("failtest")

def test_update_operational_error(repo):
    reservation = Reservation(
        reservation_id="failupdate",
        room_id="501",
        guest_name="Ghost2",
        number_of_guests=1,
        check_in_date=date(2025, 7, 20),
        check_out_date=date(2025, 7, 25)
    )
    repo.add_reservation(reservation)
    with patch("src.db.reservation_model.update_reservation") as mock_update:
        mock_update.side_effect = sqlite3.OperationalError
        with pytest.raises(DatabaseUnavailableError):
            repo.update_reservation(reservation)

def test_load_from_db(repo):
    connection = repo.connection
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO reservations (reservation_id, room_number, guest_name, number_of_guests, check_in_date, check_out_date)
        VALUES ('loadtest', '999', 'Loader', 1, '2025-07-20', '2025-07-25')
    """)
    connection.commit()

    repo.load_from_db()
    found = repo.get_by_reservation_id('loadtest')
    assert found is not None

def test_cache_cleanup_on_delete(repo):
    reservation = Reservation(
        reservation_id="unique1",
        room_id="301",
        guest_name="CleanupGuest",
        number_of_guests=1,
        check_in_date=date(2025, 7, 20),
        check_out_date=date(2025, 7, 25)
    )
    repo.add_reservation(reservation)
    repo.delete_reservation("unique1")
    assert repo.get_reservations_by_room_number("301") is None
    assert repo.get_reservations_by_guest_name("CleanupGuest") is None
