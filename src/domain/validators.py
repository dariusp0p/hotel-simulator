from datetime import date
from src.exceptions import ValidationError


class ReservationValidator:
    def validate(self, reservation):
        errors = []

        if reservation.number is not isinstance(reservation.number, int):
            errors.append("Invalid number!")
        if reservation.room is not isinstance(reservation.room, str) or reservation.room not in ['01', '02', '03', '04', '05']:
            errors.append("Invalid room!")
        if reservation.guestNumber is not isinstance(reservation.guestNumber, int):
            errors.append("Invalid guest number!")
        if reservation.arrivalDate is not isinstance(reservation.arrivalDate, date) or reservation.departureDate is not isinstance(reservation.departureDate, date):
            errors.append("Invalid dates!")
        if reservation.arrivalDate > reservation.departureDate:
            errors.append("Invalid dates!")
        if len(errors) > 0:
            raise ValidationError(errors)