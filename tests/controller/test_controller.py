import pytest
from unittest.mock import MagicMock
from datetime import date

from src.controller.controller import Controller
from src.controller.dto import RoomDTO, ReservationDTO, FloorDTO, FloorElementDTO

@pytest.fixture
def controller():
    hotel_service = MagicMock()
    reservation_service = MagicMock()
    return Controller(reservation_service, hotel_service)

def make_room(db_id=1, number="101", capacity=2, price_per_night=100, type="room", floor_id=1, position=(0,0)):
    room = MagicMock()
    room.db_id = db_id
    room.number = number
    room.capacity = capacity
    room.price_per_night = price_per_night
    room.type = type
    room.floor_id = floor_id
    room.position = position
    return room

def make_reservation(reservation_id="R1", room_id=1, guest_name="Alice", number_of_guests=2,
                     check_in_date=date(2024,6,1), check_out_date=date(2024,6,5)):
    res = MagicMock()
    res.reservation_id = reservation_id
    res.room_id = room_id
    res.guest_name = guest_name
    res.number_of_guests = number_of_guests
    res.check_in_date = check_in_date
    res.check_out_date = check_out_date
    return res

def test_reservation_search_by_id(controller):
    controller._Controller__reservation_service.get_all_reservations.return_value = [
        make_reservation(reservation_id="R1")
    ]
    controller._Controller__hotel_service.get_rooms_by_partial_number.return_value = []
    results = controller.reservation_search("R1")
    assert len(results) == 1
    assert results[0].reservation_id == "R1"

def test_reservation_search_by_guest_name(controller):
    controller._Controller__reservation_service.get_all_reservations.return_value = [
        make_reservation(guest_name="Bob")
    ]
    controller._Controller__hotel_service.get_rooms_by_partial_number.return_value = []
    results = controller.reservation_search("bob")
    assert len(results) == 1
    assert results[0].guest_name == "Bob"

def test_reservation_search_by_partial_room_number(controller):
    room = make_room(db_id=2, number="201")
    controller._Controller__hotel_service.get_rooms_by_partial_number.return_value = [room]
    controller._Controller__reservation_service.get_all_reservations.return_value = [
        make_reservation(room_id=2)
    ]
    results = controller.reservation_search("20")
    assert len(results) == 1
    assert results[0].room_id == 2

def test_reservation_search_with_date_filter(controller):
    controller._Controller__hotel_service.get_rooms_by_partial_number.return_value = []
    controller._Controller__reservation_service.get_all_reservations.return_value = [
        make_reservation(check_in_date=date(2024,6,10), check_out_date=date(2024,6,15))
    ]
    results = controller.reservation_search("R1", from_date=date(2024,6,12))
    assert len(results) == 1
    results = controller.reservation_search("R1", from_date=date(2024,6,16))
    assert len(results) == 0

def test_reservation_direct_search_by_id(controller):
    controller._Controller__reservation_service.get_by_reservation_id.return_value = make_reservation(reservation_id="R2")
    results = controller.reservation_direct_search("R2")
    assert len(results) == 1
    assert results[0].reservation_id == "R2"

def test_reservation_direct_search_by_guest_name(controller):
    controller._Controller__reservation_service.get_by_reservation_id.return_value = None
    controller._Controller__reservation_service.get_all_reservations.return_value = [
        make_reservation(guest_name="Charlie")
    ]
    results = controller.reservation_direct_search("charlie")
    assert len(results) == 1
    assert results[0].guest_name == "Charlie"

def test_reservation_direct_search_by_room_number(controller):
    controller._Controller__reservation_service.get_by_reservation_id.return_value = None
    controller._Controller__reservation_service.get_all_reservations.return_value = [
        make_reservation(room_id=3)
    ]
    room = make_room(db_id=3, number="301")
    controller._Controller__hotel_service.get_room_by_number.return_value = room
    results = controller.reservation_direct_search("301")
    assert len(results) == 1
    assert results[0].room_id == 3

def test_get_total_reservations_income(controller):
    room = make_room(price_per_night=150)
    controller.get_room_by_id = MagicMock(return_value=room)
    reservation = make_reservation(room_id=1, check_in_date=date(2024,6,1), check_out_date=date(2024,6,4))
    controller.get_all_reservations = MagicMock(return_value=[reservation])
    assert controller.get_total_reservations_income() == 3 * 150

def test_get_room_number_of_reservations(controller):
    controller._Controller__reservation_service.get_reservations_by_room_id.return_value = [
        make_reservation(), make_reservation()
    ]
    assert controller.get_room_number_of_reservations(1) == 2

def test_get_available_rooms(controller):
    room = make_room(db_id=4, capacity=2)
    controller._Controller__hotel_service.get_rooms_by_capacity.return_value = [room]
    controller._Controller__reservation_service.get_reservations_by_room_id.return_value = []
    results = controller.get_available_rooms("2024-06-01", "2024-06-05", 2)
    assert len(results) == 1
    assert results[0].db_id == 4

def test_get_total_rooms_count(controller):
    floor = MagicMock()
    floor.db_id = 1
    controller.get_all_floors = MagicMock(return_value=[floor])
    controller.get_floor_grid = MagicMock(return_value={
        (0,0): make_room(type="room"),
        (0,1): None,
        (1,0): make_room(type="room"),
    })
    assert controller.get_total_rooms_count() == 2

def test_undo_redo_clear_stacks(controller):
    controller._Controller__action_manager.undo = MagicMock()
    controller._Controller__action_manager.redo = MagicMock()
    controller._Controller__action_manager.can_undo = MagicMock(return_value=True)
    controller._Controller__action_manager.can_redo = MagicMock(return_value=True)
    controller._Controller__action_manager.clear_stacks = MagicMock()
    controller.undo()
    controller.redo()
    assert controller.can_undo()
    assert controller.can_redo()
    controller.clear_stacks()
    controller._Controller__action_manager.undo.assert_called_once()
    controller._Controller__action_manager.redo.assert_called_once()
    controller._Controller__action_manager.clear_stacks.assert_called_once()

def test_dto_conversion_methods(controller):
    room = make_room()
    floor_element = MagicMock()
    floor_element.db_id = 10
    floor_element.type = "element"
    floor_element.floor_id = 1
    floor_element.position = (0,0)
    floor = MagicMock()
    floor.db_id = 1
    floor.name = "First"
    floor.level = 1
    floor.elements = {1: room, 2: floor_element}
    reservation = make_reservation()
    controller._Controller__hotel_service.get_room_by_id.return_value = room
    floor_dto = controller._to_floor_dto(floor)
    assert isinstance(floor_dto, FloorDTO)
    assert isinstance(floor_dto.elements[1], RoomDTO)
    assert isinstance(floor_dto.elements[2], FloorElementDTO)
    assert isinstance(controller._to_room_dto(room), RoomDTO)
    assert isinstance(controller._to_floor_element_dto(floor_element), FloorElementDTO)
    assert isinstance(controller._to_reservation_dto(reservation), ReservationDTO)
