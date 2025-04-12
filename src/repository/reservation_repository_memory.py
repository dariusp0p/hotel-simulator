from src.exceptions import RepositoryError
from src.domain.reservation import Reservation
from src.repository.base_repository import BaseRepository

from datetime import date



class ReservationRepositoryMemory(BaseRepository):
    def __init__(self):
        self.__data = {}


    def add(self, number: str, reservation: Reservation) -> None:
        if number in self.__data.keys():
            raise RepositoryError("Reservation with this number already exists!")
        self.__data[number] = reservation


    def get_all(self) -> dict:
        return self.__data.copy()


    def get_by_id(self, number: str) -> Reservation:
        if number not in self.__data.keys():
            raise RepositoryError("Reservation with this number does not exist!")
        return self.__data[number]


    def get_number(self, room_number: str, arrival_date: date, departure_date: date) -> int:
        for key, value in self.__data.items():
            if value.room_number == room_number and value.arrival_date == arrival_date and value.departure_date == departure_date:
                return key
        raise RepositoryError("Reservation not found!")


    def update(self, number: str, reservation: Reservation) -> None:
        if number not in self.__data.keys():
            raise RepositoryError("Reservation with this number does not exist!")
        self.__data[number] = reservation


    def remove(self, number: str) -> Reservation:
        if number not in self.__data.keys():
            raise RepositoryError("Reservation with this number does not exist!")
        return self.__data.pop(number)


    def is_number_available(self, number: str) -> bool:
        if number not in self.__data.keys():
            return True
        return False
