from src.domain.reservation import Reservation
from src.repository.reservation_repository_memory import ReservationRepositoryMemory
from src.exceptions import RepositoryError

import json
from datetime import datetime



class ReservationRepositoryJSON(ReservationRepositoryMemory):
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
            raise RepositoryError("Something went wrong while reading the file!")

        for number, details in data.items():
            arrival_date = datetime.strptime(details['arrival_date'], '%Y-%m-%d').date()
            departure_date = datetime.strptime(details['departure_date'], '%Y-%m-%d').date()

            reservation = Reservation(
                room_number=details['room_number'],
                guest_name=details['guest_name'],
                guest_number=details['guest_number'],
                arrival_date=arrival_date,
                departure_date=departure_date
            )
            super().add(number, reservation)

    def save_file(self):
        data = {}
        for number, reservation in self.get_all().items():
            data[number] = {
                'room_number': reservation.room_number,
                'guest_name': reservation.guest_name,
                'guest_number': reservation.guest_number,
                'arrival_date': reservation.arrival_date.strftime('%Y-%m-%d'),
                'departure_date': reservation.departure_date.strftime('%Y-%m-%d'),
            }

        with open(self.__filename, "wt") as file:
            json.dump(data, file, indent=4)

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