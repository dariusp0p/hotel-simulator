from src.exceptions import ApplicationException, InputError
from src.domain.reservation import Reservation
from datetime import datetime
from texttable import Texttable



class UI:

    def __init__(self, service):
        self.__service = service



    def printMenu(self):
        print(f'1. Display Reservations')
        print(f'2. Create Reservation')
        print(f'3. Delete Reservation')
        print(f'4. Interval Reservations')
        print(f'5. Monthly Report')
        print(f'0. Exit')
        print("")



    def displayReservations(self):
        print("All Reservations:")
        for reservation in self.__service.getAll():
            print(reservation)
        print("")

    def createReservation(self):
        try:
            userInput = input("Enter arrival date (dd.mm): ").strip()
            arrivalDate = datetime.strptime(f'{userInput}.2025', '%d.%m.%Y').date()
            userInput = input("Enter departure date (dd.mm): ").strip()
            departureDate = datetime.strptime(f'{userInput}.2025', '%d.%m.%Y').date()
            print(self.__service.getAvailableRooms(arrivalDate, departureDate))
            room = input("Choose room: ")
            name = input("Enter name: ")
            guestNumber = int(input("Enter guest number: "))

            newReservation = Reservation(0, room, name, guestNumber, arrivalDate, departureDate)
            print(newReservation)
            self.__service.create(newReservation)
            print("Reservation created!")
        except Exception as e:
            print(e)

    def deleteReservation(self):
        try:
            userInput = int(input("Reservation number: "))
            self.__service.delete(userInput)
            print("Reservation successfully deleted!")
        except ValueError:
            print("Invalid number!")
        except ApplicationException as e:
            print(e)
        print("")

    def intervalReservations(self):
        userInput = input("Enter interval (dd.mm - dd.mm): ").strip()
        userInput = userInput.split(" - ")
        startDate = datetime.strptime(f'{userInput[0]}.2025', '%d.%m.%Y').date()
        endDate = datetime.strptime(f'{userInput[1]}.2025', '%d.%m.%Y').date()
        reservations = self.__service.getIntervalReservations(startDate, endDate)
        reservations = dict(sorted(reservations.items(), key=lambda x: x[1].arrivalDate))
        monthsFormat = ['','January','February','March','April','May','June','July','August','September','October','November','December']
        months = []
        for reservation in reservations.values():
            if reservation.arrivalDate.month not in months:
                months.append(reservation.arrivalDate.month)

        for month in months:
            table = Texttable()
            table.add_row([monthsFormat[month], "Name", "Guests"])

            table.set_chars(['-', '|', '+', '-'])
            for reservation in reservations.values():
                if reservation.arrivalDate.month == month:
                    table.add_row([f'{reservation.arrivalDate} - {reservation.departureDate}', reservation.name, f'{reservation.guestNumber} persoane'])
                    print(table.draw())
            table.set_chars(['=', '|', '+', '-'])

            print(table.draw())


    def monthlyReport(self):
        month = int(input("Enter month (m): "))
        year = 2025
        first_day = datetime(year, month, 1)
        start_day = first_day.weekday()

        if month == 12:
            next_month = datetime(year + 1, 1, 1)
        else:
            next_month = datetime(year, month + 1, 1)
        num_days = (next_month - first_day).days

        table = Texttable()
        table.add_row(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

        weeks = []
        week = [""] * 7

        day = 1
        for i in range(start_day, 7):
            dayf = f'{day}' if len(str(day)) == 2 else f'0{day}'
            monthf = f'{month}' if len(str(month)) == 2 else f'0{month}'
            startDate = datetime.strptime(f'{dayf}.{monthf}.{year}', '%d.%m.%Y').date()
            endDate = datetime.strptime(f'{dayf}.{monthf}.{year}', '%d.%m.%Y').date()
            week[i] = f'{day} / {len(self.__service.getAvailableRooms(startDate, endDate))}'
            day += 1
        weeks.append(week)

        while day <= num_days:
            week = [""] * 7
            for i in range(7):
                if day <= num_days:
                    dayf = f'{day}' if len(str(day)) == 2 else f'0{day}'
                    monthf = f'{month}' if len(str(month)) == 2 else f'0{month}'
                    startDate = datetime.strptime(f'{dayf}.{monthf}.{year}', '%d.%m.%Y').date()
                    endDate = datetime.strptime(f'{dayf}.{monthf}.{year}', '%d.%m.%Y').date()
                    week[i] = f'{day} / {len(self.__service.getAvailableRooms(startDate, endDate))}'
                    day += 1
            weeks.append(week)

        for week in weeks:
            table.add_row(week)

        print(table.draw())




    def start(self):
        while True:
            self.printMenu()

            try:
                choice = input("Your choice: ")
                print("")

                if choice == "1":
                    self.displayReservations()
                elif choice == "2":
                    self.createReservation()
                elif choice == "3":
                    self.deleteReservation()
                elif choice == "4":
                    self.intervalReservations()
                elif choice == "5":
                    self.monthlyReport()

                elif choice == "0":
                    break


            except ApplicationException as error:
                print(error)
