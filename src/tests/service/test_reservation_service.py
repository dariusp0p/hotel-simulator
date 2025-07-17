from src.service.reservation_service import ReservationService
from src.repository.reservation_repository import ReservationRepositoryMemory
from src.utilities.exceptions import ValidationError

import pytest



@pytest.fixture
def reservation_repository():
    # Use the actual repository implementation
    return ReservationRepositoryMemory()


@pytest.fixture
def reservation_service(reservation_repository):
    return ReservationService(reservation_repository)


def test_make_reservation(reservation_service, reservation_repository):
    reservation_data = {
        "room_number": "101",
        "guest_name": "John Doe",
        "guest_number": 2,
        "arrival_date": "15.10.2023",
        "departure_date": "20.10.2023",
    }
    reservation_service.make_reservation(reservation_data)
    assert len(reservation_repository.get_all()) == 1


def test_make_reservation_validation_error(reservation_service):
    reservation_data = {
        "room_number": "101",
        "guest_name": "John Doe",
        "guest_number": "invalid",  # Invalid guest number
        "arrival_date": "15.10.2023",
        "departure_date": "20.10.2023",
    }
    with pytest.raises(ValidationError):
        reservation_service.make_reservation(reservation_data)


def test_delete_reservation(reservation_service, reservation_repository):
    reservation_data = {
        "room_number": "101",
        "guest_name": "John Doe",
        "guest_number": 2,
        "arrival_date": "15.10.2023",
        "departure_date": "20.10.2023",
    }
    reservation_service.make_reservation(reservation_data)
    reservation_service.delete_reservation(reservation_data)
    assert len(reservation_repository.get_all()) == 0