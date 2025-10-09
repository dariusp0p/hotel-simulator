from src.model.domain.floor_element import FloorElement


def test_initialization_defaults():
    fe = FloorElement()
    assert fe.db_id is None
    assert fe.type is None
    assert fe.floor_id is None
    assert fe.position is None

def test_initialization_with_values():
    fe = FloorElement(db_id=1, type="room", floor_id=2, position=(3, 4))
    assert fe.db_id == 1
    assert fe.type == "room"
    assert fe.floor_id == 2
    assert fe.position == (3, 4)

def test_property_setters():
    fe = FloorElement()
    fe.db_id = 10
    fe.floor_id = 20
    fe.position = (5, 6)
    assert fe.db_id == 10
    assert fe.floor_id == 20
    assert fe.position == (5, 6)

def test_str_representation():
    fe = FloorElement(db_id=1, type="room", floor_id=2, position=(3, 4))
    s = str(fe)
    assert "DB ID: 1" in s
    assert "Type: room" in s
    assert "Floor ID 2" in s
    assert "Position: (3, 4)" in s

def test_validate_all_valid():
    fe = FloorElement(db_id=1, type="room", floor_id=2, position=(3, 4))
    assert fe.validate() == []

def test_validate_invalid_db_id():
    fe = FloorElement(db_id="one", type="room", floor_id=2, position=(3, 4))
    errors = fe.validate()
    assert "DB ID must be an integer or None!" in errors

def test_validate_missing_type():
    fe = FloorElement(db_id=1, type=None, floor_id=2, position=(3, 4))
    errors = fe.validate()
    assert "Type is required!" in errors

def test_validate_type_not_string():
    fe = FloorElement(db_id=1, type=123, floor_id=2, position=(3, 4))
    errors = fe.validate()
    assert "Type must be a string!" in errors

def test_validate_missing_floor_id():
    fe = FloorElement(db_id=1, type="room", floor_id=None, position=(3, 4))
    errors = fe.validate()
    assert "Floor ID is required!" in errors

def test_validate_floor_id_not_int():
    fe = FloorElement(db_id=1, type="room", floor_id="two", position=(3, 4))
    errors = fe.validate()
    assert "Floor ID must be an integer!" in errors

def test_validate_missing_position():
    fe = FloorElement(db_id=1, type="room", floor_id=2, position=None)
    errors = fe.validate()
    assert "Position is required!" in errors

def test_validate_position_not_tuple():
    fe = FloorElement(db_id=1, type="room", floor_id=2, position=[3, 4])
    errors = fe.validate()
    assert "Position must be a tuple of two integers!" in errors

def test_validate_position_wrong_length():
    fe = FloorElement(db_id=1, type="room", floor_id=2, position=(3,))
    errors = fe.validate()
    assert "Position must be a tuple of two integers!" in errors

def test_validate_position_non_ints():
    fe = FloorElement(db_id=1, type="room", floor_id=2, position=(3, "four"))
    errors = fe.validate()
    assert "Position must be a tuple of two integers!" in errors
