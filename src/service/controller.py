from src.utilities.decorators import require_role
from src.utilities.roles import Roles
from src.service.room_service import RoomService
from src.service.reservation_service import ReservationService
from src.service.action_manager import ActionManager
from src.service.action import Action



class Controller:
    def __init__(self, user_role, room_service, reservation_service):
        self.__user_role = user_role
        self.__room_service = room_service
        self.__reservation_service = reservation_service
        self.__action_manager = ActionManager()


    @require_role(Roles.ADMIN)
    def add_room(self, room_number: str, room_capacity: int) -> None:
        room_data = { 'number': room_number, 'capacity': room_capacity }
        action = Action( action_type="add_room",
                         redo_func=self.__room_service.create_room,
                         undo_func=self.__room_service.delete_room,
                         room_data=room_data )
        try:
            self.__room_service.create_room(room_data)
            self.__action_manager.add_action(action)
        except Exception as e:
            raise e

    @require_role(Roles.ADMIN)
    def update_room(self, old_room_number: str, new_room_number: str, new_room_capacity: int) -> None:
        old_room_data = { 'number': old_room_number }
        new_room_data = { 'number': new_room_number, 'capacity': new_room_capacity }
        try:
            old_room = self.__room_service.update_room(old_room_data, new_room_data)
            old_room_data = { 'number': old_room.number, 'capacity': old_room.capacity }
            action = Action( action_type="update_room",
                             redo_func=self.__room_service.update_room,
                             undo_func=self.__room_service.update_room,
                             new_room_data=new_room_data,
                             old_room_data=old_room_data )
            self.__action_manager.add_action(action)
        except Exception as e:
            raise e

    @require_role(Roles.ADMIN)
    def delete_room(self, room_number: str) -> None:
        room_data = { 'number': room_number }
        try:
            old_room = self.__room_service.delete_room(room_data)
            room_data = { 'number': old_room.number, 'capacity': old_room.capacity }
            action = Action( action_type="delete_room",
                             redo_func=self.__room_service.delete_room,
                             undo_func=self.__room_service.create_room,
                             room_data=room_data )
            self.__action_manager.add_action(action)
        except Exception as e:
            raise e



    @require_role(Roles.ADMIN, Roles.USER, Roles.GUEST)
    def get_all_rooms(self):
        return self.__room_service.get_all_rooms()

    @require_role(Roles.ADMIN, Roles.USER)
    def make_reservation(self, room_number: str, guest_name: str, guest_number: int, arrival_date: str, departure_date: str) -> None:
        reservation_data = { 'room_number': room_number, 'guest_name': guest_name, 'guest_number': guest_number, 'arrival_date': arrival_date, 'departure_date': departure_date }
        action = Action( action_type="make_reservation",
                         redo_func=self.__reservation_service.create_reservation,
                         undo_func=self.__reservation_service.delete_reservation,
                         reservation_data=reservation_data )
        try:
            self.__reservation_service.create_reservation(reservation_data)
            self.__action_manager.add_action(action)
        except Exception as e:
            raise e


    @require_role(Roles.ADMIN)
    def update_reservation(self, old_reservation_number):
        pass

    @require_role(Roles.ADMIN)
    def delete_reservation(self, reservation_number):
        pass

    @require_role(Roles.ADMIN)
    def get_all_reservations(self):
        return self.__reservation_service.get_all_reservations()
