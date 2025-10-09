from src.model.domain import Room


def test_initialization_defaults():
    r = Room()
    assert r.db_id is None
    assert r.type is None
    assert r.floor_id is None
    assert r.position is None
    assert r.number is None
    assert r.capacity is None
    assert r.price_per_night is None

def test_initialization_with_values():
    r = Room(db_id=1, type="room", floor_id=2, position=(3, 4), number="101", capacity=2, price_per_night=99.99)
    assert r.db_id == 1
    assert r.type == "room"
    assert r.floor_id == 2
    assert r.position == (3, 4)
    assert r.number == "101"
    assert r.capacity == 2
    assert r.price_per_night == 99.99

def test_property_setters():
    r = Room()
    r.db_id = 10
    r.floor_id = 1
    r.position = (0, 0)
    r.number = "201"
    r.capacity = 4
    r.price_per_night = 150.0
    assert r.db_id == 10
    assert r.floor_id == 1
    assert r.position == (0, 0)
    assert r.number == "201"
    assert r.capacity == 4
    assert r.price_per_night == 150.0

def test_str_representation():
    r = Room(db_id=1, type="room", floor_id=2, position=(3, 4), number="101", capacity=2, price_per_night=99.99)
    s = str(r)
    assert "DB ID: 1" in s
    assert "Type: room" in s
    assert "Floor ID 2" in s
    assert "Position: (3, 4)" in s
    assert "Number: 101" in s
    assert "Capacity: 2" in s
    assert "Price per night: $99.99" in s

def test_validate_all_valid():
    r = Room(db_id=1, type="room", floor_id=2, position=(3, 4), number="101", capacity=2, price_per_night=99.99)
    assert r.validate() == []

def test_validate_missing_number():
    r = Room(db_id=1, type="room", floor_id=2, position=(3, 4), number=None, capacity=2, price_per_night=99.99)
    errors = r.validate()
    assert "Room number is required!" in errors

def test_validate_number_not_string():
    r = Room(db_id=1, type="room", floor_id=2, position=(3, 4), number=101, capacity=2, price_per_night=99.99)
    errors = r.validate()
    assert "Room number must be a string!" in errors

def test_validate_missing_capacity():
    r = Room(db_id=1, type="room", floor_id=2, position=(3, 4), number="101", capacity=None, price_per_night=99.99)
    errors = r.validate()
    assert "Capacity is required!" in errors

def test_validate_capacity_not_int():
    r = Room(db_id=1, type="room", floor_id=2, position=(3, 4), number="101", capacity="two", price_per_night=99.99)
    errors = r.validate()
    assert "Invalid capacity!" in errors

def test_validate_missing_price_per_night():
    r = Room(db_id=1, type="room", floor_id=2, position=(3, 4), number="101", capacity=2, price_per_night=None)
    errors = r.validate()
    assert "Price per night is required!" in errors

def test_validate_price_per_night_not_float():
    r = Room(db_id=1, type="room", floor_id=2, position=(3, 4), number="101", capacity=2, price_per_night="99.99")
    errors = r.validate()
    assert "Invalid price per night!" in errors
