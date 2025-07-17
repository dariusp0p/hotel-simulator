class Room:
    def __init__(self, number, capacity):
        self.__number = number
        self.__capacity = capacity


    @property
    def number(self):
        return self.__number

    @property
    def capacity(self):
        return self.__capacity


    def __str__(self):
        return f'Number: {self.__number} | Capacity: {self.__capacity}'


    def validate(self) -> list:
        errors = []
        if not isinstance(self.__number, str):
            errors.append("Invalid room number!")
        if not isinstance(self.__capacity, int):
            errors.append("Invalid capacity!")
        if len(errors) > 0:
            return errors
