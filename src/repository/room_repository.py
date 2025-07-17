from src.utilities.exceptions import RepositoryError
from src.domain.room import Room



class RoomRepositoryMemory():
    def __init__(self):
        self.__data = {}


    def add(self, number: str, room: Room) -> None:
        if number in self.__data.keys():
            raise RepositoryError("Room with this number already exists!")
        self.__data[number] = room


    def get_all(self) -> dict:
        return self.__data.copy()


    def get_by_id(self, number: str) -> Room:
        if number not in self.__data.keys():
            raise RepositoryError("Room with this number does not exist!")
        return self.__data[number]


    def update(self, number: str, room) -> Room:
        if number not in self.__data.keys():
            raise RepositoryError("Room with this number does not exist!")
        old_room = self.__data[number]
        self.__data[number] = room
        return old_room


    def remove(self, number: str) -> Room:
        if number not in self.__data.keys():
            raise RepositoryError("Room with this number does not exist!")
        return self.__data.pop(number)
