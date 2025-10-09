import pytest
import sqlite3
from datetime import date

from src.model.repository.reservation_repository import ReservationRepository
from src.model.domain import Reservation
from src.utilities.exceptions import ReservationAlreadyExistsError, ReservationNotFoundError


@pytest.fixture
def in_memory_db():
    conn = sqlite3.connect(":memory:")
    # Ensure the schema and tables are created
    from src.db.database_operations import create_hotel_simulator_model
    create_hotel_simulator_model(conn)
    yield conn
    conn.close()

@pytest.fixture
def repo(in_memory_db):
    return ReservationRepository(in_memory_db)

def make_reservation(res_id="res1", room_id=101, guest="Alice", guests=2):
    return Reservation(
        db_id=None,
        reservation_id=res_id,
        room_id=room_id,
        guest_name=guest,
        number_of_guests=guests,
        check_in_date=date(2024, 7, 1),
        check_out_date=date(2024, 7, 5),
    )

def test_add_and_get_reservation(repo):
    res = make_reservation()
    repo.add_reservation(res)
    assert repo.get_by_reservation_id("res1") is not None
    assert repo.get_reservations_by_room_id(101)[0].reservation_id == "res1"
    assert repo.get_reservations_by_guest_name("Alice")[0].reservation_id == "res1"

def test_add_duplicate_reservation_raises(repo):
    res = make_reservation()
    repo.add_reservation(res)
    with pytest.raises(ReservationAlreadyExistsError):
        repo.add_reservation(make_reservation())

def test_delete_reservation(repo):
    res = make_reservation()
    repo.add_reservation(res)
    repo.delete_reservation("res1")
    assert repo.get_by_reservation_id("res1") is None
    assert repo.get_reservations_by_room_id(101) == []
    assert repo.get_reservations_by_guest_name("Alice") == []

def test_delete_nonexistent_reservation_raises(repo):
    with pytest.raises(ReservationNotFoundError):
        repo.delete_reservation("does_not_exist")

def test_cache_consistency(repo):
    res1 = make_reservation("res1", 101, "Alice")
    res2 = make_reservation("res2", 101, "Bob")
    repo.add_reservation(res1)
    repo.add_reservation(res2)
    repo.delete_reservation("res1")
    assert repo.get_reservations_by_room_id(101)[0].guest_name == "Bob"
    repo.delete_reservation("res2")
    assert repo.get_reservations_by_room_id(101) == []

def test_get_all_reservations(repo):
    res1 = make_reservation("res1", 101, "Alice")
    res2 = make_reservation("res2", 102, "Bob")
    repo.add_reservation(res1)
    repo.add_reservation(res2)
    all_res = repo.get_all_reservations()
    assert len(all_res) == 2
    ids = {r.reservation_id for r in all_res}
    assert ids == {"res1", "res2"}
