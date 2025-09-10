from datetime import date, timedelta

from src.domain.reservation import Reservation



def test_valid_reservation_passes():
    reservation = Reservation(
        room_id="101",
        guest_name="John Doe",
        number_of_guests=2,
        check_in_date=date.today(),
        check_out_date=date.today() + timedelta(days=2)
    )
    assert reservation.validate() is None


def test_invalid_room_number_type():
    reservation = Reservation(
        room_id=101,  # int, not str
        guest_name="John Doe",
        number_of_guests=2,
        check_in_date=date.today(),
        check_out_date=date.today() + timedelta(days=2)
    )
    errors = reservation.validate()
    assert "Invalid room!" in errors


def test_invalid_guest_number_type():
    reservation = Reservation(
        room_id="101",
        guest_name="John Doe",
        number_of_guests="two",  # str, not int
        check_in_date=date.today(),
        check_out_date=date.today() + timedelta(days=2)
    )
    errors = reservation.validate()
    assert "Invalid guest number!" in errors


def test_invalid_dates_type():
    reservation = Reservation(
        room_id="101",
        guest_name="John Doe",
        number_of_guests=2,
        check_in_date="2025-07-18",  # str, not date
        check_out_date="2025-07-20"  # str, not date
    )
    errors = reservation.validate()
    assert "Invalid dates!" in errors


def test_checkin_after_checkout():
    reservation = Reservation(
        room_id="101",
        guest_name="John Doe",
        number_of_guests=2,
        check_in_date=date.today() + timedelta(days=2),
        check_out_date=date.today()
    )
    errors = reservation.validate()
    assert "Invalid dates!" in errors


def test_multiple_errors():
    reservation = Reservation(
        room_id=101,  # int
        guest_name="John Doe",
        number_of_guests="two",  # str
        check_in_date="not a date",
        check_out_date="not a date"
    )
    errors = reservation.validate()
    assert "Invalid room!" in errors
    assert "Invalid guest number!" in errors
    assert "Invalid dates!" in errors