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

    def get_reservation_by_id(self, reservation_id):
        return self.__reservation_service.get_reservation_by_id(reservation_id)

    def get_reservations_by_guest_name(self, guest_name):
        return self.__reservation_service.get_reservations_by_guest_name(guest_name)

    def get_reservations_by_room_name(self, room_name):
        return self.__reservation_service.get_reservations_by_room_id(room_name)


    def reservation_search(self, search_bar_string=None, from_date=None, to_date=None):
        results = []

        for reservation in self.__reservation_service.get_all_reservations():
            if search_bar_string in reservation.reservation_id or search_bar_string.lower() in reservation.guest_name.lower() or search_bar_string.lower() in reservation.room_number.lower():
                results.append(reservation)

        if from_date:
            filtered_results = [
                res for res in results
                if res.check_out_date >= from_date
            ]
            results = filtered_results

        if to_date:
            filtered_results = [
                res for res in results
                if res.check_in_date <= to_date
            ]
            results = filtered_results

        return results

    def reservation_direct_search(self, search_bar_string):
        results = []

        reservation_by_id = self.__reservation_service.get_reservation_by_id(search_bar_string)
        if reservation_by_id:
            results.append(reservation_by_id)
            return results

        reservations_by_guest_name = self.__reservation_service.get_reservations_by_guest_name(search_bar_string)
        if reservations_by_guest_name:
            results.extend(reservations_by_guest_name)
            return results

        reservations_by_room_name = self.__reservation_service.get_reservations_by_room_id(search_bar_string)
        if reservations_by_room_name:
            results.extend(reservations_by_room_name)
            return results

        return results



    def make_reservation(self, room_number, guest_name, guest_number, arrival_date, departure_date):
        reservation_data = {
            "room_number": room_number,
            "guest_name": guest_name,
            "number_of_guests": guest_number,
            "check_in_date": arrival_date,
            "check_out_date": departure_date,
        }
        self.__reservation_service.make_reservation(reservation_data)

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
        self.__reservation_service.update_reservation(reservation_data)

    def delete_reservation(self, reservation_id):
        self.__reservation_service.delete_reservation(reservation_id)