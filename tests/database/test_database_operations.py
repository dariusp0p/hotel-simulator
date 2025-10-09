import pytest
from src.model.database.database_operations import *
from src.utilities.exceptions import DatabaseError


def test_create_hotel_simulator_model(in_memory_db):
    # Create the database schema
    create_hotel_simulator_model(in_memory_db)

    # Verify tables were created
    cursor = in_memory_db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]

    # Assert expected tables exist based on actual schema
    expected_tables = ['floors', 'elements', 'reservations']
    for table in expected_tables:
        assert table in tables

# Floor operations tests
def test_floor_operations(in_memory_db):
    # Setup database
    create_hotel_simulator_model(in_memory_db)

    # Test insert_floor
    floor_id = insert_floor(in_memory_db, "First Floor", 1)
    assert floor_id is not None

    # Test select_all_floors
    floors = select_all_floors(in_memory_db)
    assert len(floors) == 1
    assert floors[0][1] == "First Floor"  # name
    assert floors[0][2] == 1  # level

    # Test update_floor_name
    update_floor_name(in_memory_db, floor_id, "Ground Floor")
    floors = select_all_floors(in_memory_db)
    assert floors[0][1] == "Ground Floor"

    # Test update_floor_level
    update_floor_level(in_memory_db, floor_id, 0)
    floors = select_all_floors(in_memory_db)
    assert floors[0][2] == 0

    # Test delete_floor
    delete_floor(in_memory_db, floor_id)
    floors = select_all_floors(in_memory_db)
    assert len(floors) == 0

# Element operations tests
def test_element_operations(in_memory_db):
    # Setup database
    create_hotel_simulator_model(in_memory_db)
    floor_id = insert_floor(in_memory_db, "Test Floor", 1)

    # Test insert_element
    element_id = insert_element(in_memory_db, "room", floor_id, 10, 20, "101", 2, 99.99)
    assert element_id is not None

    # Test select_elements_by_floor_id
    elements = select_elements_by_floor_id(in_memory_db, floor_id)
    assert len(elements) == 1
    assert elements[0][1] == "room"  # element_type
    assert elements[0][3] == 10  # x
    assert elements[0][4] == 20  # y

    # Test update_element_position
    update_element_position(in_memory_db, element_id, 15, 25)
    elements = select_elements_by_floor_id(in_memory_db, floor_id)
    assert elements[0][3] == 15  # new x
    assert elements[0][4] == 25  # new y

    # Test update_element
    update_element(in_memory_db, element_id, "102", 3, 129.99)
    elements = select_elements_by_floor_id(in_memory_db, floor_id)
    assert elements[0][5] == "102"  # number
    assert elements[0][6] == 3  # capacity
    assert elements[0][7] == 129.99  # price_per_night

    # Test delete_element
    delete_element(in_memory_db, element_id)
    elements = select_elements_by_floor_id(in_memory_db, floor_id)
    assert len(elements) == 0

# Reservation operations tests
def test_reservation_operations(in_memory_db):
    # Setup database
    create_hotel_simulator_model(in_memory_db)
    floor_id = insert_floor(in_memory_db, "Test Floor", 1)
    room_id = insert_element(in_memory_db, "room", floor_id, 10, 20, "101", 2, 99.99)

    # Test insert_reservation
    reservation_id = "RES-001"
    insert_reservation(in_memory_db, reservation_id, room_id, "John Doe", 2, "2023-05-01", "2023-05-05")

    # Test select_all_reservations
    reservations = select_all_reservations(in_memory_db)
    assert len(reservations) == 1
    assert reservations[0][1] == "RES-001"  # reservation_id

    # Test select_reservation_by_reservation_id
    reservation = select_reservation_by_reservation_id(in_memory_db, reservation_id)
    assert reservation is not None
    assert reservation[2] == room_id  # room_id
    assert reservation[3] == "John Doe"  # guest_name

    # Test update_reservation
    db_id = reservation[0]
    update_reservation(in_memory_db, db_id, "RES-001", room_id, "Jane Doe", 3, "2023-06-01", "2023-06-05")
    updated_res = select_reservation_by_reservation_id(in_memory_db, reservation_id)
    assert updated_res[3] == "Jane Doe"  # guest_name
    assert updated_res[4] == 3  # number_of_guests

    # Test delete_reservation
    delete_reservation(in_memory_db, db_id)
    reservations = select_all_reservations(in_memory_db)
    assert len(reservations) == 0

def test_error_handling(in_memory_db):
    # Setup database
    create_hotel_simulator_model(in_memory_db)

    # Test duplicate constraint error
    floor_id = insert_floor(in_memory_db, "Unique Floor", 1)
    with pytest.raises(DatabaseError):
        insert_floor(in_memory_db, "Unique Floor", 2)  # Duplicate name
