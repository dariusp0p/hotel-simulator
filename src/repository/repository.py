from src.exceptions import RepositoryError



class Repository:
    def __init__(self):
        self._data = {}

    def create(self, reservation):
        if reservation.number in self._data.keys():
            raise RepositoryError("Reservation with this number already exists!")
        self._data[reservation.number] = reservation

    def readAll(self):
        return self._data.values()

    def readById(self, number):
        if number not in self._data.keys():
            raise RepositoryError("Reservation with this number does not exist!")
        return self._data[number]

    def delete(self, number):
        if number not in self._data.keys():
            raise RepositoryError("Reservation with this number does not exist!")
        return self._data.pop(number)

    def getAvailableNumber(self):
        for i in range(1000, 10000):
            if i not in self._data.keys():
                return i
