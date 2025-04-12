from src.repository.room_repository_textfile import RoomRepositoryText
from src.domain.room import Room

import pytest



@pytest.fixture
def temp_text_file(tmp_path):
    file_path = tmp_path / "rooms.txt"
    return str(file_path)

@pytest.fixture
def text_repository(temp_text_file):
    return RoomRepositoryText(temp_text_file)

def test_add_room_text(text_repository, temp_text_file):
    room = Room("201", 3)
    text_repository.add("1", room)
    with open(temp_text_file, "r") as file:
        content = file.read()
    assert "201" in content

def test_get_room_by_id_text(text_repository):
    room = Room("202", 4)
    text_repository.add("2", room)
    retrieved = text_repository.get_by_id("2")
    assert retrieved == room

def test_update_room_text(text_repository, temp_text_file):
    room = Room("203", 2)
    text_repository.add("3", room)
    updated_room = Room("203", 5)
    text_repository.update("3", updated_room)
    with open(temp_text_file, "r") as file:
        content = file.read()
    assert "5" in content

def test_remove_room_text(text_repository, temp_text_file):
    room = Room("204", 3)
    text_repository.add("4", room)
    text_repository.remove("4")
    with open(temp_text_file, "r") as file:
        content = file.read()
    assert "204" not in content