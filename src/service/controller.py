from datetime import datetime


class Controller:
    def __init__(self, reservation_service, hotel_service):
        self.__reservation_service = reservation_service
        self.__hotel_service = hotel_service

    @property
    def hotel_service(self):
        return self.__hotel_service


    def get_available_rooms(self, arrival_date, departure_date, number_of_guests):
        rooms = self.__hotel_service.get_rooms_by_capacity(number_of_guests)
        available_rooms = []

        for room in rooms:
            room_id = room[1]
            reservations = self.__reservation_service.get_reservations_by_room_id(room_id)

            arrival = datetime.strptime(arrival_date, '%Y-%m-%d').date()
            departure = datetime.strptime(departure_date, '%Y-%m-%d').date()

            is_available = all(
                not (arrival <= res.check_out_date and departure >= res.check_in_date)
                for res in reservations
            )

            if is_available:
                available_rooms.append(room)

        return available_rooms

    def get_all_reservations(self):
        return self.__reservation_service.get_all_reservations()

    def get_reservations_by_date_interval(self, from_date, to_date):
        return self.__reservation_service.get_reservations_by_date_interval(from_date, to_date)





    def make_reservation(self, room_number, guest_name, guest_number, arrival_date, departure_date):
        reservation_data = {
            "room_number": room_number,
            "guest_name": guest_name,
            "number_of_guests": guest_number,
            "check_in_date": arrival_date,
            "check_out_date": departure_date,
        }
        self.__reservation_service.make_reservation(reservation_data)

    def delete_reservation(self, reservation_id):
        self.__reservation_service.delete_reservation(reservation_id)