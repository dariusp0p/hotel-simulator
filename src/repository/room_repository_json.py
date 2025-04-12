from src.domain.room import Room
from src.repository.room_repository_memory import RoomRepositoryMemory
from src.exceptions import RepositoryError

import json



class RoomRepositoryJSON(RoomRepositoryMemory):
    def __init__(self, filename):
        super().__init__()
        self.__filename = filename
        self.load_file()

    def load_file(self):
        try:
            with open(self.__filename, "rt") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open(self.__filename, "wt") as file:
                json.dump({}, file)
            return
        except PermissionError:
            raise RepositoryError("Permission denied!")
        except Exception:
            raise RepositoryError("Something went wrong!")

        for number, room_data in data.items():
            room = Room(
                number=room_data["number"],
                capacity=room_data["capacity"]
            )
            super().add(number, room)

    def save_file(self):
        data = {}
        for number, room in self.get_all().items():
            data[number] = {
                "number": room.number,
                "capacity": room.capacity
            }

        with open(self.__filename, "wt") as file:
            json.dump(data, file, indent=4)

    def add(self, number: str, room: Room):
        super().add(number, room)
        self.save_file()

    def update(self, number: str, room: Room):
        super().update(number, room)
        self.save_file()

    def remove(self, number: str):
        room = super().remove(number)
        self.save_file()
        return room