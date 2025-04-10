from src.repository.repository import Repository
from src.exceptions import RepositoryError
from src.domain.reservation import Reservation
from datetime import datetime



class TextFileRepository(Repository):
    def __init__(self, filename = "../data/reservations.txt"):
        super().__init__()
        self.__filename = filename
        self.loadFile()

    def loadFile(self):
        try:
            fin = open(self.__filename, "rt")
            lines = fin.readlines()
            fin.close()
        except:
            raise RepositoryError("Something went wrong!")

        for line in lines:
            currentLine = line.split(",")
            date = currentLine[4].strip()
            arrivalDate = datetime.strptime(f'{date}.2025', '%d.%m.%Y').date()
            date = currentLine[5].strip()
            departureDate = datetime.strptime(f'{date}.2025', '%d.%m.%Y').date()
            newReservation = Reservation(int(currentLine[0]), currentLine[1], currentLine[2], int(currentLine[3]), arrivalDate, departureDate)
            super().create(newReservation)

    def saveFile(self):
        fout = open(self.__filename, "wt")
        reservations = super().readAll()
        for reservation in reservations:
            reservationString = f'{reservation.number},{reservation.room},{reservation.name},{str(reservation.guestNumber)},{reservation.arrivalDate.strftime("%d.%m")},{reservation.departureDate.strftime("%d.%m")}\n'
            fout.write(reservationString)
        fout.close()

    def create(self, reservation):
        super().create(reservation)
        self.saveFile()

    def delete(self, identifier):
        reservation = super().delete(identifier)
        self.saveFile()
        return reservation
