import copy
from datetime import datetime, date


class Action:
    """Abstract base class for actions that can be undone and redone."""
    def redo(self):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError


# Floor actions
class AddFloorAction(Action):
    """Action to add a floor."""
    def __init__(self, hotel_service, request):
        self.hotel_service = hotel_service
        self.floor_id = None
        self.name = request.name
        self.level = request.level

    def redo(self):
        self.floor_id = self.hotel_service.add_floor(self.name, self.level)

    def undo(self):
        self.hotel_service.remove_floor(self.floor_id)

class RenameFloorAction(Action):
    """Action to rename a floor."""
    def __init__(self, hotel_service, request):
        self.hotel_service = hotel_service
        self.floor_id = request.floor_id
        self.new_name = request.new_name
        floor = self.hotel_service.get_floor(self.floor_id)
        self.old_name = floor.name

    def redo(self):
        self.hotel_service.rename_floor(self.old_name, self.new_name)

    def undo(self):
        self.hotel_service.rename_floor(self.new_name, self.old_name)

class UpdateFloorLevelAction(Action):
    """Action to update a floor's level."""
    def __init__(self, hotel_service, request):
        self.hotel_service = hotel_service
        self.floor_id = request.floor_id
        self.new_level = request.new_level
        floor = self.hotel_service.get_floor(self.floor_id)
        self.old_level = floor.level

    def redo(self):
        self.hotel_service.update_floor_level(self.floor_id, self.new_level)

    def undo(self):
        self.hotel_service.update_floor_level(self.floor_id, self.old_level)

class RemoveFloorAction(Action):
    """Action to remove a floor."""
    def __init__(self, hotel_service, reservation_service, request):
        self.hotel_service = hotel_service
        self.reservation_service = reservation_service
        self.floor_id = request.floor_id
        self.floor = None
        self.rooms = []
        self.reservations = []

    def redo(self):
        self.floor = copy.deepcopy(self.hotel_service.get_floor(self.floor_id))
        self.rooms = copy.deepcopy(self.hotel_service.get_elements_by_floor_id(self.floor_id))
        self.reservations = []
        for room in self.rooms:
            if getattr(room, "type", None) == "room":
                res = copy.deepcopy(self.reservation_service.get_reservations_by_room_id(room.db_id))
                self.reservations.extend(res)
                for r in res:
                    self.reservation_service.delete_reservation(r.reservation_id)
        for room in self.rooms:
            self.hotel_service.remove_element(room.db_id, room.type, self.floor_id)
        self.hotel_service.remove_floor(self.floor_id)

    def undo(self):
        self.floor_id = self.hotel_service.add_floor(self.floor.name, self.floor.level)
        old_to_new_room_ids = {}
        for room in self.rooms:
            old_id = room.db_id
            room.floor_id = self.floor_id
            new_id = self.hotel_service.add_element(
                room.type, room.floor_id, room.position,
                getattr(room, "number", None),
                getattr(room, "capacity", None),
                getattr(room, "price_per_night", None)
            )
            old_to_new_room_ids[old_id] = new_id
        for res in self.reservations:
            new_room_id = old_to_new_room_ids.get(res.room_id)
            self.reservation_service.make_reservation(
                res.reservation_id, new_room_id,
                res.guest_name, res.number_of_guests,
                _format_iso_date(res.check_in_date), _format_iso_date(res.check_out_date)
            )

# Floor element actions
class AddElementAction(Action):
    """Action to add a floor element."""
    def __init__(self, hotel_service, request):
        self.hotel_service = hotel_service
        self.element_id = None
        self.type = request.type
        self.floor_id = request.floor_id
        self.position = request.position
        self.number = getattr(request, "number", None)
        self.capacity = getattr(request, "capacity", None)
        self.price_per_night = getattr(request, "price_per_night", None)

    def redo(self):
        self.element_id = self.hotel_service.add_element(
            self.type, self.floor_id, self.position,
            self.number, self.capacity, self.price_per_night
        )

    def undo(self):
        element = self.hotel_service.get_room_by_id(self.element_id) if self.type == "room" else None
        if element is None:
            elements = self.hotel_service.get_elements_by_floor_id(self.floor_id)
            element = next((e for e in elements if e.db_id == self.element_id), None)
        self.hotel_service.remove_element(self.element_id, element.type, self.floor_id)

class EditRoomAction(Action):
    """Action to edit a room."""
    def __init__(self, hotel_service, request):
        self.hotel_service = hotel_service
        self.element_id = request.element_id
        self.new_number = request.number
        self.new_capacity = request.capacity
        self.new_price = request.price_per_night
        room = self.hotel_service.get_room_by_id(self.element_id)
        self.old_number = room.number
        self.old_capacity = room.capacity
        self.old_price = room.price_per_night

    def redo(self):
        self.hotel_service.edit_room(self.element_id, self.new_number, self.new_capacity, self.new_price)

    def undo(self):
        self.hotel_service.edit_room(self.element_id, self.old_number, self.old_capacity, self.old_price)

class MoveElementAction(Action):
    """Action to move a floor element."""
    def __init__(self, hotel_service, request):
        self.hotel_service = hotel_service
        self.element_id = request.element_id
        self.floor_id = request.floor_id
        self.new_position = request.position
        try:
            element = self.hotel_service.get_room_by_id(self.element_id)
        except:
            elements = self.hotel_service.get_elements_by_floor_id(self.floor_id)
            element = next((e for e in elements if e.db_id == self.element_id), None)
        self.old_position = element.position

    def redo(self):
        self.hotel_service.move_element(self.element_id, self.new_position)

    def undo(self):
        self.hotel_service.move_element(self.element_id, self.old_position)

class RemoveElementAction(Action):
    """Action to remove a floor element."""
    def __init__(self, hotel_service, reservation_service, request):
        self.hotel_service = hotel_service
        self.reservation_service = reservation_service
        self.element_id = request.element_id
        self.type = request.type
        self.floor_id = request.floor_id
        self.position = request.position

        if self.type == "room":
            room = self.hotel_service.get_room_by_id(self.element_id)
            self.number = room.number
            self.capacity = room.capacity
            self.price_per_night = room.price_per_night
            self.reservations = [copy.deepcopy(r) for r in self.reservation_service.get_reservations_by_room_id(self.element_id)]

    def redo(self):
        if self.type == "room":
            for res in self.reservations:
                self.reservation_service.delete_reservation(res.reservation_id)
        self.hotel_service.remove_element(self.element_id, self.type, self.floor_id)

    def undo(self):
        self.element_id = self.hotel_service.add_element(
            self.type, self.floor_id, self.position,
            getattr(self, "number", None),
            getattr(self, "capacity", None),
            getattr(self, "price_per_night", None)
        )
        if self.type == "room":
            for res in self.reservations:
                res.room_id = self.element_id
                self.reservation_service.make_reservation(
                    res.reservation_id, res.room_id,
                    res.guest_name, res.number_of_guests,
                    _format_iso_date(res.check_in_date),
                    _format_iso_date(res.check_out_date)
                )

# Reservation actions
class MakeReservationAction(Action):
    """Action to make a reservation."""
    def __init__(self, reservation_service, request):
        self.reservation_service = reservation_service
        self.reservation_id = None
        self.room_id = request.room_id
        self.guest_name = request.guest_name
        self.number_of_guests = request.number_of_guests
        self.check_in_date = request.check_in_date
        self.check_out_date = request.check_out_date

    def redo(self):
        self.reservation_id = self.reservation_service.make_reservation(
            room_id=self.room_id, guest_name=self.guest_name, number_of_guests=self.number_of_guests,
            check_in_date=self.check_in_date, check_out_date=self.check_out_date
        )

    def undo(self):
        self.reservation_service.delete_reservation(self.reservation_id)

class EditReservationAction(Action):
    """Action to edit a reservation."""
    def __init__(self, reservation_service, request):
        self.reservation_service = reservation_service
        self.reservation_id = request.reservation_id
        self.room_id = request.room_id
        self.guest_name = request.guest_name
        self.number_of_guests = request.number_of_guests
        self.check_in_date = request.check_in_date
        self.check_out_date = request.check_out_date
        old_reservation = self.reservation_service.get_by_reservation_id(self.reservation_id)
        self.old_room_id = old_reservation.room_id
        self.old_guest_name = old_reservation.guest_name
        self.old_number_of_guests = old_reservation.number_of_guests
        self.old_check_in_date = _format_iso_date(old_reservation.check_in_date)
        self.old_check_out_date = _format_iso_date(old_reservation.check_out_date)

    def redo(self):
        self.reservation_service.update_reservation(
            self.reservation_id,
            self.room_id, self.guest_name, self.number_of_guests,
            self.check_in_date, self.check_out_date
        )

    def undo(self):
        self.reservation_service.update_reservation(
            self.reservation_id,
            self.old_room_id, self.old_guest_name, self.old_number_of_guests,
            self.old_check_in_date, self.old_check_out_date
        )

class DeleteReservationAction(Action):
    """Action to delete a reservation."""
    def __init__(self, reservation_service, request):
        self.reservation_service = reservation_service
        self.reservation_id = request.reservation_id
        reservation = self.reservation_service.get_by_reservation_id(self.reservation_id)
        self.room_id = reservation.room_id
        self.guest_name = reservation.guest_name
        self.number_of_guests = reservation.number_of_guests
        self.check_in_date = _format_iso_date(reservation.check_in_date)
        self.check_out_date = _format_iso_date(reservation.check_out_date)

    def redo(self):
        self.reservation_service.delete_reservation(self.reservation_id)

    def undo(self):
        self.reservation_service.make_reservation(
            reservation_id=self.reservation_id,
            room_id=self.room_id, guest_name=self.guest_name, number_of_guests=self.number_of_guests,
            check_in_date=self.check_in_date, check_out_date=self.check_out_date
        )

# Utility functions
def _parse_iso_date(s : str) -> date:
    """Parse a date string in ISO format (YYYY-MM-DD) to a date object."""
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError as e:
        raise ValueError(f"Invalid date format, expected YYYY-MM-DD: {s}") from e

def _format_iso_date(d : date) -> str:
    """Format a date object to a string in ISO format (YYYY-MM-DD)."""
    return d.isoformat()