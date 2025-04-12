from src.repository.room_repository_json import RoomRepositoryJSON
from src.domain.room import Room

import pytest
import json



@pytest.fixture
def temp_json_file(tmp_path):
    file_path = tmp_path / "rooms.json"
    return str(file_path)

@pytest.fixture
def json_repository(temp_json_file):
    return RoomRepositoryJSON(temp_json_file)

def test_add_room_json(json_repository, temp_json_file):
    room = Room("301", 2)
    json_repository.add("1", room)
    with open(temp_json_file, "r") as file:
        data = json.load(file)
    assert "1" in data
    assert data["1"]["number"] == "301"

def test_get_room_by_id_json(json_repository):
    room = Room("302", 4)
    json_repository.add("2", room)
    retrieved = json_repository.get_by_id("2")
    assert retrieved == room

def test_update_room_json(json_repository, temp_json_file):
    room = Room("303", 3)
    json_repository.add("3", room)
    updated_room = Room("303", 5)
    json_repository.update("3", updated_room)
    with open(temp_json_file, "r") as file:
        data = json.load(file)
    assert data["3"]["capacity"] == 5

def test_remove_room_json(json_repository, temp_json_file):
    room = Room("304", 2)
    json_repository.add("4", room)
    json_repository.remove("4")
    with open(temp_json_file, "r") as file:
        data = json.load(file)
    assert "4" not in data