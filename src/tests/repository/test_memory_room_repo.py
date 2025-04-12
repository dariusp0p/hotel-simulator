from src.repository.room_repository_memory import RoomRepositoryMemory
from src.domain.room import Room
from src.exceptions import RepositoryError

import pytest



@pytest.fixture
def memory_repository():
    return RoomRepositoryMemory()

def test_add_room(memory_repository):
    room = Room("101", 2)
    memory_repository.add("1", room)
    assert memory_repository.get_by_id("1") == room

def test_get_room_by_id(memory_repository):
    room = Room("102", 4)
    memory_repository.add("2", room)
    retrieved = memory_repository.get_by_id("2")
    assert retrieved == room

def test_update_room(memory_repository):
    room = Room("103", 3)
    memory_repository.add("3", room)
    updated_room = Room("103", 5)
    memory_repository.update("3", updated_room)
    assert memory_repository.get_by_id("3").capacity == 5

def test_remove_room(memory_repository):
    room = Room("104", 2)
    memory_repository.add("4", room)
    memory_repository.remove("4")
    with pytest.raises(RepositoryError):
        memory_repository.get_by_id("4")