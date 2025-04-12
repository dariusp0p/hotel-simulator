from src.repository.reservation_repository_textfile import ReservationRepositoryText
from src.domain.reservation import Reservation

import pytest
from datetime import date



@pytest.fixture
def temp_file(tmp_path):
    file_path = tmp_path / "reservations.txt"
    return str(file_path)

@pytest.fixture
def repository(temp_file):
    return ReservationRepositoryText(temp_file)

def test_add_reservation(repository, temp_file):
    reservation = Reservation(
        room_number="101",
        guest_name="John Doe",
        guest_number=2,
        arrival_date=date(2023, 10, 1),
        departure_date=date(2023, 10, 5)
    )
    repository.add("1", reservation)
    with open(temp_file, "r") as file:
        content = file.read()
    assert "John Doe" in content  # Verify the reservation is written to the file

def test_get_reservation_by_id(repository):
    reservation = Reservation(
        room_number="102",
        guest_name="Jane Smith",
        guest_number=1,
        arrival_date=date(2023, 10, 10),
        departure_date=date(2023, 10, 15)
    )
    repository.add("2", reservation)
    retrieved = repository.get_by_id("2")
    assert retrieved == reservation

def test_remove_reservation(repository, temp_file):
    reservation = Reservation(
        room_number="103",
        guest_name="Alice Brown",
        guest_number=3,
        arrival_date=date(2023, 11, 1),
        departure_date=date(2023, 11, 10)
    )
    repository.add("3", reservation)
    repository.remove("3")
    with open(temp_file, "r") as file:
        content = file.read()
    assert "Alice Brown" not in content  # Verify the reservation is removed from the file

def test_update_reservation(repository, temp_file):
    reservation = Reservation(
        room_number="104",
        guest_name="Bob White",
        guest_number=2,
        arrival_date=date(2023, 12, 1),
        departure_date=date(2023, 12, 10)
    )
    repository.add("4", reservation)
    updated_reservation = Reservation(
        room_number="105",
        guest_name="Bob White",
        guest_number=2,
        arrival_date=date(2023, 12, 1),
        departure_date=date(2023, 12, 15)
    )
    repository.update("4", updated_reservation)
    with open(temp_file, "r") as file:
        content = file.read()
    assert "105" in content  # Verify the updated reservation is in the file
    assert "104" not in content  # Verify the old reservation is removed