from datetime import date, timedelta
from src.model.domain import Reservation


def test_initialization_defaults():
    r = Reservation()
    assert r.db_id is None
    assert r.reservation_id is None
    assert r.room_id is None
    assert r.guest_name is None
    assert r.number_of_guests is None
    assert r.check_in_date is None
    assert r.check_out_date is None

def test_initialization_with_values():
    d1 = date.today()
    d2 = d1 + timedelta(days=2)
    r = Reservation(db_id=1, reservation_id="R001", room_id=101, guest_name="John Doe",
                    number_of_guests=2, check_in_date=d1, check_out_date=d2)
    assert r.db_id == 1
    assert r.reservation_id == "R001"
    assert r.room_id == 101
    assert r.guest_name == "John Doe"
    assert r.number_of_guests == 2
    assert r.check_in_date == d1
    assert r.check_out_date == d2

def test_property_setters():
    r = Reservation()
    r.db_id = 10
    r.room_id = 201
    r.guest_name = "Jane Doe"
    r.number_of_guests = 3
    d1 = date.today()
    d2 = d1 + timedelta(days=1)
    r.check_in_date = d1
    r.check_out_date = d2
    assert r.db_id == 10
    assert r.room_id == 201
    assert r.guest_name == "Jane Doe"
    assert r.number_of_guests == 3
    assert r.check_in_date == d1
    assert r.check_out_date == d2

def test_str_representation():
    d1 = date(2024, 6, 1)
    d2 = date(2024, 6, 5)
    r = Reservation(db_id=1, reservation_id="R002", room_id=102, guest_name="Alice",
                    number_of_guests=1, check_in_date=d1, check_out_date=d2)
    s = str(r)
    assert "DB ID: 1" in s
    assert "Reservation ID: R002" in s
    assert "Room ID: 102" in s
    assert "Guest name: Alice" in s
    assert "Number of guests: 1" in s
    assert "Check-in date: 2024-06-01" in s
    assert "Check-out date: 2024-06-05" in s

def test_validate_all_valid():
    d1 = date.today()
    d2 = d1 + timedelta(days=1)
    r = Reservation(db_id=1, reservation_id="R003", room_id=103, guest_name="Bob",
                    number_of_guests=2, check_in_date=d1, check_out_date=d2)
    assert r.validate() == []

def test_validate_invalid_db_id():
    d1 = date.today()
    d2 = d1 + timedelta(days=1)
    r = Reservation(db_id="one", reservation_id="R004", room_id=104, guest_name="Eve",
                    number_of_guests=2, check_in_date=d1, check_out_date=d2)
    errors = r.validate()
    assert "DB ID must be an integer or None!" in errors

def test_validate_missing_reservation_id():
    d1 = date.today()
    d2 = d1 + timedelta(days=1)
    r = Reservation(db_id=1, reservation_id=None, room_id=105, guest_name="Sam",
                    number_of_guests=2, check_in_date=d1, check_out_date=d2)
    errors = r.validate()
    assert "Reservation ID is required!" in errors

def test_validate_reservation_id_not_string():
    d1 = date.today()
    d2 = d1 + timedelta(days=1)
    r = Reservation(db_id=1, reservation_id=123, room_id=106, guest_name="Sam",
                    number_of_guests=2, check_in_date=d1, check_out_date=d2)
    errors = r.validate()
    assert "Reservation ID must be a string or None!" in errors

def test_validate_missing_room_id():
    d1 = date.today()
    d2 = d1 + timedelta(days=1)
    r = Reservation(db_id=1, reservation_id="R005", room_id=None, guest_name="Sam",
                    number_of_guests=2, check_in_date=d1, check_out_date=d2)
    errors = r.validate()
    assert "Room ID is required!" in errors

def test_validate_room_id_not_int():
    d1 = date.today()
    d2 = d1 + timedelta(days=1)
    r = Reservation(db_id=1, reservation_id="R006", room_id="106", guest_name="Sam",
                    number_of_guests=2, check_in_date=d1, check_out_date=d2)
    errors = r.validate()
    assert "Room ID must be an integer!" in errors

def test_validate_missing_guest_name():
    d1 = date.today()
    d2 = d1 + timedelta(days=1)
    r = Reservation(db_id=1, reservation_id="R007", room_id=107, guest_name=None,
                    number_of_guests=2, check_in_date=d1, check_out_date=d2)
    errors = r.validate()
    assert "Guest name is required!" in errors

def test_validate_guest_name_not_string():
    d1 = date.today()
    d2 = d1 + timedelta(days=1)
    r = Reservation(db_id=1, reservation_id="R008", room_id=108, guest_name=123,
                    number_of_guests=2, check_in_date=d1, check_out_date=d2)
    errors = r.validate()
    assert "Guest name must be a string!" in errors

def test_validate_missing_number_of_guests():
    d1 = date.today()
    d2 = d1 + timedelta(days=1)
    r = Reservation(db_id=1, reservation_id="R009", room_id=109, guest_name="Sam",
                    number_of_guests=None, check_in_date=d1, check_out_date=d2)
    errors = r.validate()
    assert "Number of guests is required!" in errors

def test_validate_number_of_guests_not_int():
    d1 = date.today()
    d2 = d1 + timedelta(days=1)
    r = Reservation(db_id=1, reservation_id="R010", room_id=110, guest_name="Sam",
                    number_of_guests="two", check_in_date=d1, check_out_date=d2)
    errors = r.validate()
    assert "Number of guests must be an integer!" in errors

def test_validate_number_of_guests_zero_or_negative():
    d1 = date.today()
    d2 = d1 + timedelta(days=1)
    r = Reservation(db_id=1, reservation_id="R011", room_id=111, guest_name="Sam",
                    number_of_guests=0, check_in_date=d1, check_out_date=d2)
    errors = r.validate()
    assert "Number of guests must be greater than zero!" in errors
    r.number_of_guests = -1
    errors = r.validate()
    assert "Number of guests must be greater than zero!" in errors

def test_validate_missing_check_in_date():
    d2 = date.today() + timedelta(days=1)
    r = Reservation(db_id=1, reservation_id="R012", room_id=112, guest_name="Sam",
                    number_of_guests=2, check_in_date=None, check_out_date=d2)
    errors = r.validate()
    assert "Check-in date is required!" in errors

def test_validate_check_in_date_not_date():
    d1 = "2024-06-01"
    d2 = date.today() + timedelta(days=1)
    r = Reservation(db_id=1, reservation_id="R013", room_id=113, guest_name="Sam",
                    number_of_guests=2, check_in_date=d1, check_out_date=d2)
    errors = r.validate()
    assert "Check-in date must be a date!" in errors

def test_validate_missing_check_out_date():
    d1 = date.today()
    r = Reservation(db_id=1, reservation_id="R014", room_id=114, guest_name="Sam",
                    number_of_guests=2, check_in_date=d1, check_out_date=None)
    errors = r.validate()
    assert "Check-out date is required!" in errors

def test_validate_check_out_date_not_date():
    d1 = date.today()
    d2 = "2024-06-02"
    r = Reservation(db_id=1, reservation_id="R015", room_id=115, guest_name="Sam",
                    number_of_guests=2, check_in_date=d1, check_out_date=d2)
    errors = r.validate()
    assert "Check-out date must be a date!" in errors

def test_validate_invalid_date_interval():
    d1 = date.today()
    d2 = d1 - timedelta(days=1)
    r = Reservation(db_id=1, reservation_id="R016", room_id=116, guest_name="Sam",
                    number_of_guests=2, check_in_date=d1, check_out_date=d2)
    errors = r.validate()
    assert "Invalid date interval!" in errors
