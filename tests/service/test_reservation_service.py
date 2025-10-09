import pytest
from unittest.mock import MagicMock
from src.model.service.reservation_service import ReservationService
from src.model.domain import Reservation
from src.utilities.exceptions import ValidationError


@pytest.fixture
def mock_repository():
    return MagicMock()

@pytest.fixture
def service(mock_repository):
    return ReservationService(mock_repository)

def test_get_all_reservations(service, mock_repository):
    mock_repository.get_all_reservations.return_value = [
        Reservation(
            reservation_id="R001", room_id=1, guest_name="John Doe", number_of_guests=2,
            check_in_date=None, check_out_date=None
        )
    ]
    result = service.get_all_reservations()
    assert len(result) == 1
    assert result[0].guest_name == "John Doe"

def test_get_by_reservation_id(service, mock_repository):
    mock_repository.get_by_reservation_id.return_value = Reservation(
        reservation_id="R002", room_id=2, guest_name="Jane Doe", number_of_guests=1,
        check_in_date=None, check_out_date=None
    )
    result = service.get_by_reservation_id("R002")
    assert result.reservation_id == "R002"

def test_get_reservations_by_room_id(service, mock_repository):
    mock_repository.get_reservations_by_room_id.return_value = [
        Reservation(
            reservation_id="R003", room_id=3, guest_name="Alice", number_of_guests=2,
            check_in_date=None, check_out_date=None
        )
    ]
    result = service.get_reservations_by_room_id(3)
    assert len(result) == 1
    assert result[0].room_id == 3

def test_make_reservation_valid(service, mock_repository):
    mock_repository.add_reservation.return_value = None
    reservation_id = service.make_reservation(
        room_id=1, guest_name="Bob", number_of_guests=2,
        check_in_date="2024-06-01", check_out_date="2024-06-05"
    )
    assert reservation_id.startswith("R")

def test_make_reservation_invalid(service, mock_repository):
    orig_validate = Reservation.validate
    Reservation.validate = lambda self: ["error"]
    with pytest.raises(ValidationError):
        service.make_reservation(
            room_id=1, guest_name="", number_of_guests=2,
            check_in_date="2024-06-01", check_out_date="2024-06-05"
        )
    Reservation.validate = orig_validate

def test_delete_reservation(service, mock_repository):
    mock_repository.delete_reservation.return_value = "deleted"
    result = service.delete_reservation("R001")
    assert result == "deleted"

def test_parse_iso_date_valid(service):
    date_obj = service._parse_iso_date("2024-06-01")
    assert date_obj.year == 2024
    assert date_obj.month == 6
    assert date_obj.day == 1

def test_parse_iso_date_invalid(service):
    with pytest.raises(ValueError):
        service._parse_iso_date("invalid-date")

def test_search_by_guest_name(service, mock_repository):
    mock_repository.get_all_reservations.return_value = [
        Reservation(
            reservation_id="R004", room_id=4, guest_name="Charlie", number_of_guests=1,
            check_in_date=None, check_out_date=None
        )
    ]
    results = service.search("Charlie")
    assert len(results) == 1
    assert results[0].guest_name == "Charlie"

def test_direct_search_by_id(service, mock_repository):
    mock_repository.get_by_reservation_id.return_value = Reservation(
        reservation_id="R005", room_id=5, guest_name="Dana", number_of_guests=2,
        check_in_date=None, check_out_date=None
    )
    mock_repository.get_reservations_by_guest_name.return_value = []
    results = service.direct_search("R005")
    assert len(results) == 1
    assert results[0].reservation_id == "R005"

def test_direct_search_by_guest_name(service, mock_repository):
    mock_repository.get_by_reservation_id.return_value = None
    mock_repository.get_reservations_by_guest_name.return_value = [
        Reservation(
            reservation_id="R006", room_id=6, guest_name="Eve", number_of_guests=1,
            check_in_date=None, check_out_date=None
        )
    ]
    results = service.direct_search("Eve")
    assert len(results) == 1
    assert results[0].guest_name == "Eve"
