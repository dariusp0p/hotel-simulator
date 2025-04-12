from src.domain.reservation import Reservation
from src.repository.reservation_repository_memory import ReservationRepositoryMemory
from src.exceptions import RepositoryError

from datetime import datetime



class ReservationRepositoryText(ReservationRepositoryMemory):
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

            arrival_date = datetime.strptime(f'{current_line[4].strip()}', '%Y-%m-%d').date()
            departure_date = datetime.strptime(f'{current_line[5].strip()}', '%Y-%m-%d').date()

            number = current_line[0].strip()
            reservation = Reservation(current_line[1], current_line[2], int(current_line[3]), arrival_date, departure_date)
            super().add(number, reservation)


    def save_file(self):
        file = open(self.__filename, "wt")
        reservations = super().get_all()
        for number, reservation in reservations.items():
            current_line = f'{number}:{reservation.room_number}:{reservation.guest_name}:{reservation.guest_number}:{reservation.arrival_date.strftime("%Y-%m-%d")}:{reservation.departure_date.strftime("%Y-%m-%d")}\n'
            file.write(current_line)
        file.close()


    def add(self, number: str, reservation: Reservation):
        super().add(number, reservation)
        self.save_file()

    def update(self, number: str, reservation: Reservation):
        super().update(number, reservation)
        self.save_file()

    def remove(self, number: str):
        reservation = super().remove(number)
        self.save_file()
        return reservation
