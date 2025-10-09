import pytest
import sqlite3

from src.model.repository.hotel_repository import HotelRepository
from src.model.domain import Floor
from src.model.domain.floor_element import FloorElement
from src.model.domain import Room
from src.utilities.exceptions import FloorAlreadyExistsError, FloorNotFoundError, ElementNotFoundError


@pytest.fixture
def in_memory_db():
    conn = sqlite3.connect(":memory:")
    from src.db.database_operations import create_hotel_simulator_model
    create_hotel_simulator_model(conn)
    yield conn
    conn.close()

@pytest.fixture
def repo(in_memory_db):
    return HotelRepository(in_memory_db)

def test_add_and_get_floor(repo):
    floor = Floor(db_id=None, name="First", level=1)
    floor_id = repo.add_floor(floor)
    assert repo.get_floor_by_id(floor_id).name == "First"
    assert repo.get_floor_id("First") == floor_id
    assert floor_id in [f.db_id for f in repo.get_all_floors()]

def test_add_duplicate_floor_raises(repo):
    floor = Floor(db_id=None, name="First", level=1)
    repo.add_floor(floor)
    with pytest.raises(FloorAlreadyExistsError):
        repo.add_floor(Floor(db_id=None, name="First", level=2))

def test_remove_floor(repo):
    floor = Floor(db_id=None, name="First", level=1)
    floor_id = repo.add_floor(floor)
    repo.remove_floor(floor_id)
    with pytest.raises(FloorNotFoundError):
        repo.get_floor_by_id(floor_id)

def test_add_and_get_room(repo):
    floor = Floor(db_id=None, name="First", level=1)
    floor_id = repo.add_floor(floor)
    room = Room(
        db_id=None, type="room", floor_id=floor_id, position=(0, 0),
        number="101", capacity=2, price_per_night=100.0
    )
    room_id = repo.add_element(room)
    assert repo.get_room_by_id(room_id).number == "101"
    assert repo.get_room_by_number("101").db_id == room_id
    assert room in repo.get_rooms_by_capacity(2)

def test_add_and_remove_element(repo):
    floor = Floor(db_id=None, name="First", level=1)
    floor_id = repo.add_floor(floor)
    element = FloorElement(db_id=None, type="hallway", floor_id=floor_id, position=(1, 1))
    element_id = repo.add_element(element)
    repo.remove_element(element_id, "hallway", floor_id)
    with pytest.raises(ElementNotFoundError):
        repo.get_room_by_id(element_id)

def test_move_and_rename_floor(repo):
    floor = Floor(db_id=None, name="First", level=1)
    floor_id = repo.add_floor(floor)
    repo.move_floor(floor_id, 2)
    assert repo.get_floor_by_id(floor_id).level == 2
    repo.rename_floor("First", "Ground")
    assert repo.get_floor_id("Ground") == floor_id
    with pytest.raises(FloorNotFoundError):
        repo.get_floor_id("First")
