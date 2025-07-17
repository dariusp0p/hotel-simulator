from src.utilities.exceptions import ValidationError
from src.domain.room import Room



class RoomService:
    def __init__(self, room_repository):
        self.__repository = room_repository


    def create_room(self, room_data: dict) -> None:
        room = Room(room_data['number'], room_data['capacity'])

        errors = room.validate()
        if errors:
            raise ValidationError('Validation error!', errors)

        try:
            self.__repository.add(room.number, room)
        except Exception as e:
            raise e


    def update_room(self, old_room_data: dict, new_room_data: dict) -> Room:
        number = old_room_data['number']
        new_room = Room(new_room_data['number'], new_room_data['capacity'])

        errors = new_room.validate()
        if errors:
            raise ValidationError('Validation error!', errors)

        try:
            return self.__repository.update(number, new_room)
        except Exception as e:
            raise e


    def delete_room(self, room_data: dict) -> Room:
        number = room_data['number']

        try:
            return self.__repository.remove(number)
        except Exception as e:
            raise e


    def get_all_rooms(self):
        return self.__repository.get_all()
