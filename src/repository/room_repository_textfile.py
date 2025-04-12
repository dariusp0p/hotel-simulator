from src.domain.room import Room
from src.repository.room_repository_memory import RoomRepositoryMemory
from src.exceptions import RepositoryError



class RoomRepositoryText(RoomRepositoryMemory):
    def __init__(self, filename):
        super().__init__()
        self.__filename = filename
        self.load_file()


    def load_file(self):
        try:
            file = open(self.__filename, "rt")
            lines = file.readlines()
            file.close()
        except FileNotFoundError:
            # raise RepositoryError("File not found!")
            with open(self.__filename, "wt") as file:
                lines = []
        except PermissionError:
            raise RepositoryError("Permission denied!")
        except Exception:
            raise RepositoryError("Something went wrong!")

        for line in lines:
            current_line = line.split(":")

            number = current_line[0].strip()
            room = Room(current_line[1], current_line[2])
            super().add(number, room)


    def save_file(self):
        file = open(self.__filename, "wt")
        rooms = super().get_all()
        for number, room in rooms.items():
            current_line = f'{number}:{room.number}:{room.capacity}\n'
            file.write(current_line)
        file.close()


    def add(self, number: str, room: Room):
        super().add(number, room)
        self.save_file()

    def update(self, number: str, room: Room):
        super().update(number, room)
        self.save_file()

    def remove(self, number: str):
        reservation = super().remove(number)
        self.save_file()
        return reservation
