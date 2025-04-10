class Reservation:
    def __init__(self, number, room, name, guestNumber, arrivalDate, departureDate):
        self.__number = number
        self.__room = room
        self.__name = name
        self.__guestNumber = guestNumber
        self.__arrivalDate = arrivalDate
        self.__departureDate = departureDate

    @property
    def number(self):
        return self.__number

    @number.setter
    def number(self, value):
        self.__number = value

    @property
    def room(self):
        return self.__room

    @property
    def name(self):
        return self.__name

    @property
    def guestNumber(self):
        return self.__guestNumber

    @property
    def arrivalDate(self):
        return self.__arrivalDate

    @property
    def departureDate(self):
        return self.__departureDate

    def __str__(self):
        return f'{self.__number}, {self.__room}, {self.__name}, {self.__guestNumber}, {self.__arrivalDate.strftime("%d.%m")}, {self.__departureDate.strftime("%d.%m")}'