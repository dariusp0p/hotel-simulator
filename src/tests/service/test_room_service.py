from src.service.room_service import ReservationService
from src.repository.reservation_repository import ReservationRepositoryMemory
from src.utilities.exceptions import ValidationError

import pytest



@pytest.fixture
def room_repository():
    # Use the actual repository implementation
    return ReservationRepositoryMemory()


@pytest.fixture
def room_service(room_repository):
    return ReservationService(room_repository)


def test_create_room(room_service, room_repository):
    room_data = {
        "number": "101",
        "capacity": 2,
    }
    room_service.create_room(room_data)
    assert len(room_repository.get_all()) == 1


def test_create_room_validation_error(room_service):
    room_data = {
        "number": "101",
        "capacity": "invalid",  # Invalid capacity
    }
    with pytest.raises(ValidationError):
        room_service.create_room(room_data)


def test_update_room(room_service, room_repository):
    old_room_data = {
        "number": "101",
        "capacity": 2,
    }
    new_room_data = {
        "number": "101",
        "capacity": 4,
    }
    room_service.create_room(old_room_data)
    room_service.update_room(old_room_data, new_room_data)
    updated_room = room_repository.get_by_id("101")
    assert updated_room.capacity == 4


def test_delete_room(room_service, room_repository):
    room_data = {
        "number": "101",
        "capacity": 2,
    }
    room_service.create_room(room_data)
    room_service.delete_room(room_data)
    assert len(room_repository.get_all()) == 0


def test_get_all_rooms(room_service, room_repository):
    room1 = {"number": "101", "capacity": 2}
    room2 = {"number": "102", "capacity": 3}
    room_service.create_room(room1)
    room_service.create_room(room2)
    all_rooms = room_service.get_all_rooms()
    assert len(all_rooms) == 2