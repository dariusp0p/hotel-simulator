from datetime import datetime


class Controller:
    def __init__(self, reservation_service, hotel_service):
        self.__reservation_service = reservation_service
        self.__hotel_service = hotel_service


    @property
    def hotel_service(self):
        return self.__hotel_service



    # Getters

    # Reservation
    def get_all_reservations(self):
        return self.__reservation_service.get_all_reservations()

    def get_reservation_by_id(self, reservation_id):
        return self.__reservation_service.get_by_reservation_id(reservation_id)

    def get_reservations_by_guest_name(self, guest_name):
        return self.__reservation_service.get_reservations_by_guest_name(guest_name)

    def reservation_search(self, search_bar_string=None, from_date=None, to_date=None):
        return self.__reservation_service.search(search_bar_string, from_date, to_date)

    def reservation_direct_search(self, search_bar_string):
        return self.__reservation_service.direct_search(search_bar_string)


    # Hotel
    def get_available_rooms(self, arrival_date, departure_date, number_of_guests):
        rooms = self.__hotel_service.get_rooms_by_capacity(number_of_guests) # TO BE MADE IN Theta(1)

        available_rooms = []

        for room in rooms:
            room_id = room[1] # TO BE REVISED
            reservations = self.__reservation_service.get_reservations_by_room_number(room_id) # Theta(1)

            arrival = datetime.strptime(arrival_date, '%Y-%m-%d').date()
            departure = datetime.strptime(departure_date, '%Y-%m-%d').date()

            is_available = all(
                not (arrival <= res.check_out_date and departure >= res.check_in_date)
                for res in reservations
            )

            if is_available:
                available_rooms.append(room)

        return available_rooms


    def get_sidebar_floors(self):
        return self.__hotel_service.get_all_floors_sorted_by_level()



    # CRUD

    # Reservation
    def make_reservation(self, room_number, guest_name, guest_number, arrival_date, departure_date):
        reservation_data = {
            "room_number": room_number,
            "guest_name": guest_name,
            "number_of_guests": guest_number,
            "check_in_date": arrival_date,
            "check_out_date": departure_date,
        }

        try:
            self.__reservation_service.make_reservation(reservation_data)
        except Exception as e:
            raise e

    def update_reservation(self, reservation_id, room_number, guest_name, guest_number, arrival_date, departure_date):
        # if not self.hotel_service.is_room_available(room_number, arrival_date, departure_date):
        #     raise Exception("Room not available")

        reservation_data = {
            "reservation_id": reservation_id,
            "room_number": room_number,
            "guest_name": guest_name,
            "number_of_guests": guest_number,
            "check_in_date": arrival_date,
            "check_out_date": departure_date,
        }

        try:
            self.__reservation_service.update_reservation(reservation_data)
        except Exception as e:
            raise e

    def delete_reservation(self, reservation_id):
        try:
            self.__reservation_service.delete_reservation(reservation_id)
        except Exception as e:
            raise e
