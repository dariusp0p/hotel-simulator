from src.model.domain.floor import Floor
from src.model.domain.floor_element import FloorElement
from src.model.domain.room import Room
from src.utilities.exceptions import ElementNotFoundError


def test_initialization_defaults():
    f = Floor()
    assert f.db_id is None
    assert f.name is None
    assert f.level is None
    assert f.elements == {}

def test_initialization_with_values():
    f = Floor(db_id=1, name="First", level=1)
    assert f.db_id == 1
    assert f.name == "First"
    assert f.level == 1

def test_property_setters():
    f = Floor()
    f.db_id = 10
    f.name = "Second"
    f.level = 2
    assert f.db_id == 10
    assert f.name == "Second"
    assert f.level == 2

def test_str_representation():
    f = Floor(db_id=1, name="Main", level=0)
    s = str(f)
    assert "DB ID: 1" in s
    assert "Name: Main" in s
    assert "Level: 0" in s
    assert "Element IDs: []" in s

def test_validate_all_valid():
    f = Floor(db_id=1, name="Main", level=0)
    assert f.validate() == []

def test_validate_missing_name():
    f = Floor(db_id=1, name=None, level=0)
    errors = f.validate()
    assert "Name is required!" in errors

def test_validate_name_not_string():
    f = Floor(db_id=1, name=123, level=0)
    errors = f.validate()
    assert "Name must be a string!" in errors

def test_validate_missing_level():
    f = Floor(db_id=1, name="Main", level=None)
    errors = f.validate()
    assert "Level is required!" in errors

def test_validate_level_not_int():
    f = Floor(db_id=1, name="Main", level="zero")
    errors = f.validate()
    assert "Level must be an integer!" in errors

def test_add_and_delete_element():
    f = Floor(db_id=1, name="Main", level=0)
    e = FloorElement(db_id=100, type="room", floor_id=1, position=(1, 2))
    f.add_element(e)
    assert 100 in f.elements
    f.delete_element(100)
    assert 100 not in f.elements

def test_add_element_updates_grid():
    f = Floor(db_id=1, name="Main", level=0)
    e = FloorElement(db_id=101, type="room", floor_id=1, position=(2, 3))
    f.add_element(e)
    grid = f.grid
    assert (2, 3) in grid
    assert grid[(2, 3)] == e

def test_move_element():
    f = Floor(db_id=1, name="Main", level=0)
    e = FloorElement(db_id=102, type="room", floor_id=1, position=(1, 1))
    f.add_element(e)
    f.grid  # build grid cache
    f.move_element(102, (2, 2))
    assert e.position == (2, 2)
    assert (2, 2) in f.grid
    assert (1, 1) not in f.grid

def test_move_element_not_found():
    f = Floor()
    try:
        f.move_element(999, (0, 0))
        assert False
    except ElementNotFoundError:
        assert True

def test_delete_element_not_found():
    f = Floor()
    try:
        f.delete_element(999)
        assert False
    except ElementNotFoundError:
        assert True

def test_edit_room():
    f = Floor(db_id=1, name="Main", level=0)
    r = Room(db_id=200, type="room", floor_id=1, position=(0, 0), number="101", capacity=2, price_per_night=50.0)
    f.add_element(r)
    f.edit_room(200, "102", 3, 75.0)
    assert r.number == "102"
    assert r.capacity == 3
    assert r.price_per_night == 75.0

def test_edit_room_not_found():
    f = Floor()
    try:
        f.edit_room(999, "102", 3, 75.0)
        assert False
    except ElementNotFoundError:
        assert True

def test_get_element_neighbors():
    f = Floor(db_id=1, name="Main", level=0)
    e1 = FloorElement(db_id=1, type="room", floor_id=1, position=(0, 0))
    e2 = FloorElement(db_id=2, type="room", floor_id=1, position=(1, 0))
    e3 = FloorElement(db_id=3, type="room", floor_id=1, position=(0, 1))
    f.add_element(e1)
    f.add_element(e2)
    f.add_element(e3)
    neighbors = f.get_element_neighbors(1)
    assert (1, 0) in neighbors
    assert (0, 1) in neighbors
