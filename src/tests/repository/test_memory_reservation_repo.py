from src.repository.reservation_repository_memory import ReservationRepositoryMemory
from src.domain.reservation import Reservation
from src.exceptions import RepositoryError

import pytest
from datetime import date



@pytest.fixture
def repository():
    return ReservationRepositoryMemory()

def test_add_reservation(repository):
    reservation = Reservation(
        room_number="101",
        guest_name="John Doe",
        guest_number=2,
        arrival_date="2023-10-01",
        departure_date="2023-10-05"
    )
    repository.add("1", reservation)
    assert len(repository.get_all()) == 1
    assert repository.get_by_id("1") == reservation

def test_get_reservation_by_id(repository):
    reservation = Reservation(
        room_number="102",
        guest_name="Jane Smith",
        guest_number=1,
        arrival_date="2023-10-10",
        departure_date="2023-10-15"
    )
    repository.add("2", reservation)
    retrieved = repository.get_by_id("2")
    assert retrieved == reservation

def test_remove_reservation(repository):
    reservation = Reservation(
        room_number="103",
        guest_name="Alice Brown",
        guest_number=3,
        arrival_date="2023-11-01",
        departure_date="2023-11-10"
    )
    repository.add("3", reservation)  # Use "3" as the number key
    repository.remove("3")  # Remove by the same number key
    assert len(repository.get_all()) == 0
    with pytest.raises(RepositoryError):
        repository.get_by_id("3")  # Ensure it raises an error when accessing a removed reservation

def test_update_reservation(repository):
    reservation = Reservation(
        room_number="104",
        guest_name="Bob White",
        guest_number=2,
        arrival_date="2023-12-01",
        departure_date="2023-12-10"
    )
    repository.add("4", reservation)  # Use "4" as the number key
    updated_reservation = Reservation(
        room_number="105",
        guest_name="Bob White",
        guest_number=2,
        arrival_date="2023-12-01",
        departure_date="2023-12-15"
    )
    repository.update("4", updated_reservation)  # Update by the same number key
    assert repository.get_by_id("4").room_number == "105"
    assert repository.get_by_id("4").departure_date == "2023-12-15"

def test_get_number(repository):
    reservation = Reservation(
        room_number="104",
        guest_name="Charlie Brown",
        guest_number=2,
        arrival_date=date(2023, 12, 1),
        departure_date=date(2023, 12, 10)
    )
    repository.add("5", reservation)  # Add the reservation with number "5"
    number = repository.get_number("104", date(2023, 12, 1), date(2023, 12, 10))
    assert number == "5"  # Verify the correct number is returned