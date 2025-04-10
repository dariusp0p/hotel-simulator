from datetime import datetime, timedelta
from faker import Faker
from random import randint



def readRooms(fileName):
    try:
        fin = open(fileName, "rt")
        lines = fin.readlines()
        fin.close()

        rooms = {}
        for line in lines:
            line = line.split(",")
            rooms[line[0]] = int(line[1])
        return rooms
    except FileNotFoundError:
        print("Error!")



f = Faker("ro_RO")



def generateNumbers(n):
    numbers = []
    while len(numbers) < n:
        number = (randint(1000, 9999))
        if number not in numbers:
            numbers.append(number)
    return numbers

def generateNames(n):
    names = []
    while len(names) < n:
        name = (f.name())
        if name not in names:
            names.append(name)
    return names

def generateGuests(n, capacity):
    numbers = []
    while len(numbers) < n:
        number = randint(1, capacity)
        numbers.append(number)
    return numbers

def generateIntervals(n, year=2025):
    intervals = []
    while len(intervals) < n:
        startDay = randint(1, 365)
        startDate = datetime(year, 1, 1) + timedelta(days=startDay - 1)
        length = randint(1, 7)
        endDate = startDate + timedelta(days=length)
        overlap = any(s <= endDate and e >= startDate for s, e in intervals)
        if not overlap:
            intervals.append((startDate, endDate))
    formattedIntervals = [f"{s.strftime('%d.%m')},{e.strftime('%d.%m')}" for s, e in intervals]
    intervals.sort()
    return formattedIntervals

def generateReservations(n, room, capacity):
    reservations = []
    names = generateNames(n)
    guests = generateGuests(n, capacity)
    intervals = generateIntervals(n)
    for i in range(1, n):
        reservations.append([0, room, names[i], guests[i], intervals[i]])
    return reservations





if __name__ == "__main__":

    rooms = readRooms("../data/rooms.txt")
    reservations = []
    for room, capacity in rooms.items():
        roomRes = generateReservations(41, room, capacity)
        reservations.extend(roomRes)
    numbers = generateNumbers(200)
    for i in range(len(reservations)):
        reservations[i][0] = numbers[i]
    print(len(reservations))
    print(reservations)

    try:
        fout = open("../data/reservations.txt", "w")
        for reservation in reservations:
            dates = reservation[4].split(",")
            resLine = f'{reservation[0]},{reservation[1]},{reservation[2]},{reservation[3]},{dates[0]},{dates[1]}\n'
            # print(resLine)
            fout.write(resLine)
        fout.close()
    except FileNotFoundError:
        print("Error!")