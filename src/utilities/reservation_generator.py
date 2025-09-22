import random
from datetime import timedelta
from PyQt6.QtCore import QDate
from src.service.dto import ReservationDTO, MakeReservationRequest


class ReservationGenerator:
    def __init__(self, controller):
        self.controller = controller
        self.first_names = ["James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
                            "William", "Elizabeth", "David", "Susan", "Richard", "Jessica", "Joseph", "Sarah"]
        self.last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson",
                           "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin"]

    def generate_reservations(self, from_date, to_date, occupancy_percentage):
        """Generate reservations based on date range and occupancy percentage"""
        # Convert QDate to Python date objects
        start_date = from_date.toPyDate()
        end_date = to_date.toPyDate()

        # Get all rooms in the hotel
        all_rooms = self._get_all_rooms()
        if not all_rooms:
            return 0

        # Calculate target number of rooms to fill each day
        target_room_count = max(1, int(len(all_rooms) * (occupancy_percentage / 100.0)))

        # Track how many reservations we create
        reservations_created = 0

        # Create reservations for each day in range
        current_date = start_date
        while current_date <= end_date:
            # For each date, create reservations up to the target occupancy
            date_string = current_date.strftime("%Y-%m-%d")

            # Find available rooms for this date
            available_rooms = self._get_available_rooms_for_date(date_string, all_rooms)

            # Calculate how many new reservations we need
            rooms_to_book = min(target_room_count, len(available_rooms))

            # Create reservations
            for i in range(rooms_to_book):
                if not available_rooms:
                    break

                # Pick a random room
                room = random.choice(available_rooms)
                available_rooms.remove(room)

                # Determine length of stay (1-7 days)
                stay_length = random.randint(1, 7)
                checkout_date = current_date + timedelta(days=stay_length)

                # Generate random guest info
                guest_name = f"{random.choice(self.first_names)} {random.choice(self.last_names)}"
                num_guests = random.randint(1, room.capacity)

                # Create the reservation request
                req = MakeReservationRequest(
                    room_id=room.db_id,
                    guest_name=guest_name,
                    number_of_guests=num_guests,
                    check_in_date=current_date.strftime("%Y-%m-%d"),
                    check_out_date=checkout_date.strftime("%Y-%m-%d")
                )

                # Make the reservation
                try:
                    self.controller.make_reservation(req)
                    reservations_created += 1
                except Exception as e:
                    print(f"Failed to create reservation: {e}")

            # Move to next day
            current_date += timedelta(days=1)

        return reservations_created

    def _get_all_rooms(self):
        """Get all rooms from all floors"""
        rooms = []
        floors = self.controller.get_all_floors()

        for floor in floors:
            floor_grid = self.controller.get_floor_grid(floor.db_id)
            for element in floor_grid.values():
                if element and element.type == "room":
                    rooms.append(element)

        return rooms

    def _get_available_rooms_for_date(self, date_string, all_rooms):
        """Find which rooms are available on a specific date"""
        available_rooms, unavailable_rooms = self.controller.get_rooms_availability_for_date(date_string)
        return [room for room in all_rooms if room.db_id in available_rooms]