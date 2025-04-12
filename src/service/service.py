from src.domain.validators import ReservationValidator
from src.repository.reservation_repository_textfile import TextFileRepository



class Service:
    def __init__(self, reservationRepository):
        self.__repository = reservationRepository
        self.__rooms = {'01': 1, '02': 2, '03': 2, '04': 4, '05': 4}

    def create(self, reservation):
        validator = ReservationValidator()
        validator.validate(reservation)
        reservation.number = self.__repository.getAvailableNumber()
        print(reservation)
        if reservation.guestNumber > self.__rooms[reservation.room]:
            raise ValueError('Room to small!')

        self.__repository.create(reservation)

    def delete(self, number):
        self.__repository.delete(number)

    def getAll(self):
        return self.__repository.readAll()

    def getIntervals(self, room):
        intervals = []
        for reservation in self.getAll():
            if reservation.room == room:
                intervals.append([reservation.arrivalDate, reservation.departureDate])
        return intervals


    def getAvailableRooms(self, arrivalDate, departureDate):
        availableRooms = {}
        for room, capacity in self.__rooms.items():
            intervals = self.getIntervals(room)
            overlap = any(s <= departureDate and e >= arrivalDate for s, e in intervals)
            if not overlap:
                availableRooms[room] = capacity
        return availableRooms

    def getIntervalReservations(self, startDate, endDate):
        reservations = {}
        for reservation in self.getAll():
            overlap = reservation.arrivalDate <= endDate and reservation.departureDate >= startDate
            if overlap:
                reservations[reservation.number] = reservation
        return reservations
